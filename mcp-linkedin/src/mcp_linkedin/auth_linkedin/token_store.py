"""
Armazenamento seguro do access token do LinkedIn (Camada 2).

Tres backends, escolhidos por configuracao (ver config.py):

- `Win32CredentialBackend`: desenvolvimento local no Windows. A
  protecao vem do proprio sistema (Credential Manager / DPAPI). NAO
  funciona em Linux: o pywin32 nem chega a ser instalado la, entao
  toda operacao levanta ModuleNotFoundError.
- `SupabaseCredentialBackend` + `EncryptedCredentialBackend`:
  producao. O token e cifrado no processo (AES-256-GCM, chave vinda
  do ambiente) ANTES de sair para o banco, o que devolve remotamente
  a propriedade que o DPAPI da localmente.
- `InMemoryCredentialBackend`: testes e uso efemero. Nao persiste.

Este modulo nunca acessa o LinkedIn, nunca executa OAuth, nunca gera
ou usa Client Secret. Ele so guarda, le, valida e remove o access
token e o expires_at que uma etapa futura (troca de authorization
code por token, ainda nao implementada) vier a produzir.

O access token nunca e gravado em arquivo, em .env, em banco de
dados, nem cifrado manualmente com Fernet: a protecao vem do proprio
Windows Credential Manager (DPAPI), atraves de win32cred.CredWrite /
CredRead / CredDelete. Nenhuma funcao aqui imprime, loga ou inclui o
token em mensagem de excecao.

O Client Secret nunca e armazenado junto com o access token: este
modulo nao possui nenhum campo para ele.

O backend de armazenamento e injetavel (`CredentialBackend`), para
permitir testes automatizados com um backend falso em memoria, sem
jamais tocar o Credential Manager real da maquina. `Win32CredentialBackend`
e o backend real, para uso local fora da suite de testes.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Callable, Protocol

from mcp_linkedin.auth_linkedin.crypto import TokenCipher, TokenDecryptionError

# TargetName fixo e especifico deste componente, para nao colidir com
# nenhuma outra credencial ja gravada no Windows por outro programa.
TARGET_NAME = "mcp-linkedin:linkedin-access-token"

# Codigo de erro do Windows para "elemento nao encontrado", retornado
# por CredRead/CredDelete quando a credencial nao existe.
_ERROR_NOT_FOUND = 1168


@dataclass(frozen=True)
class TokenMetadata:
    """Metadados minimos de controle de validade do access token."""

    expires_at: float  # epoch seconds


class TokenStoreBackendError(Exception):
    """
    Falha ao falar com um armazenamento remoto de credencial. Nunca
    contem segredo.

    Vive aqui, e nao no modulo de um backend especifico, porque mais de
    um backend remoto a levanta (Supabase e ponte HTTPS) e quem trata o
    erro (a rota de callback) precisa de um unico tipo para capturar.
    """


class CredentialBackend(Protocol):
    """Interface minima que qualquer backend de credencial precisa cumprir."""

    def write(self, target_name: str, secret: str) -> None: ...

    def read(self, target_name: str) -> str | None: ...

    def delete(self, target_name: str) -> None: ...


class Win32CredentialBackend:
    """
    Backend real, baseado no Windows Credential Manager via pywin32.

    So deve ser usado fora da suite de testes automatizada. O import
    de win32cred fica dentro de cada metodo (nao no topo do modulo)
    para manter este arquivo importavel mesmo num ambiente sem
    pywin32, e para deixar explicito que so uma instancia deste
    backend, nunca o FakeCredentialBackend dos testes, de fato toca
    o Windows.
    """

    def write(self, target_name: str, secret: str) -> None:
        import win32cred

        credential = {
            "Type": win32cred.CRED_TYPE_GENERIC,
            "TargetName": target_name,
            "CredentialBlob": secret,
            "Persist": win32cred.CRED_PERSIST_LOCAL_MACHINE,
        }
        win32cred.CredWrite(credential, 0)

    def read(self, target_name: str) -> str | None:
        import pywintypes
        import win32cred

        try:
            credential = win32cred.CredRead(target_name, win32cred.CRED_TYPE_GENERIC)
        except pywintypes.error as erro:
            if erro.winerror == _ERROR_NOT_FOUND:
                return None
            raise

        blob = credential["CredentialBlob"]
        if isinstance(blob, bytes):
            return blob.decode("utf-16-le")
        return blob

    def delete(self, target_name: str) -> None:
        import pywintypes
        import win32cred

        try:
            win32cred.CredDelete(target_name, win32cred.CRED_TYPE_GENERIC)
        except pywintypes.error as erro:
            if erro.winerror == _ERROR_NOT_FOUND:
                return
            raise


class InMemoryCredentialBackend:
    """
    Backend em memoria do processo, para ambientes sem Windows
    Credential Manager (o container de producao no Render roda Linux,
    onde pywin32 nem existe).

    Nao persiste: reiniciar o processo derruba o token e exige uma nova
    autorizacao no LinkedIn. E a mesma decisao ja tomada para as
    sessoes da Camada 1 (ClaudeSessionStore, Etapa 7A) -- suficiente
    para validar o fluxo, e explicitamente uma pendencia conhecida ate
    a etapa que definir o armazenamento persistente de producao.

    Nao grava em disco, o que e proposital: um token em arquivo dentro
    do container seria menos seguro que em memoria, sem ganho real de
    durabilidade (o sistema de arquivos do Render tambem e efemero).
    """

    def __init__(self) -> None:
        self._store: dict[str, str] = {}

    def write(self, target_name: str, secret: str) -> None:
        self._store[target_name] = secret

    def read(self, target_name: str) -> str | None:
        return self._store.get(target_name)

    def delete(self, target_name: str) -> None:
        self._store.pop(target_name, None)

    def __repr__(self) -> str:
        # Nunca expor o conteudo gravado (o proprio access token).
        return f"InMemoryCredentialBackend(credenciais_gravadas={len(self._store)})"


class EncryptedCredentialBackend:
    """
    Envelopa outro CredentialBackend, cifrando o segredo antes de
    grava-lo e decifrando na leitura.

    Existe para o armazenamento remoto (Supabase): no Windows local a
    protecao ja vem do proprio sistema (DPAPI), e cifrar de novo so
    acrescentaria uma chave para gerenciar sem ganho de seguranca.

    Falha de decifragem devolve None, nao excecao: o efeito pratico e
    "nao ha token valido", que leva o captador a reautorizar. E o
    desfecho recuperavel correto quando a chave foi trocada ou o dado
    corrompeu, e evita derrubar a ferramenta de status por causa disso.
    """

    def __init__(self, inner: CredentialBackend, cipher: TokenCipher) -> None:
        self._inner = inner
        self._cipher = cipher

    def write(self, target_name: str, secret: str) -> None:
        self._inner.write(target_name, self._cipher.encrypt(secret))

    def read(self, target_name: str) -> str | None:
        armazenado = self._inner.read(target_name)
        if armazenado is None:
            return None
        try:
            return self._cipher.decrypt(armazenado)
        except TokenDecryptionError:
            return None

    def delete(self, target_name: str) -> None:
        self._inner.delete(target_name)

    def __repr__(self) -> str:
        return f"EncryptedCredentialBackend(inner={self._inner!r})"


class TokenStore:
    """
    Abstracao de leitura/escrita/validade do access token local.

    `get_access_token()` e `get_token_metadata()` devolvem o que
    estiver gravado, mesmo que expirado; esta classe nao exclui um
    token vencido automaticamente. Quem for usar o token deve sempre
    checar `has_valid_token()` antes.
    """

    def __init__(
        self,
        backend: CredentialBackend | None = None,
        target_name: str = TARGET_NAME,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self._backend = backend if backend is not None else Win32CredentialBackend()
        self._target_name = target_name
        self._clock = clock

    def save_access_token(self, access_token: str, expires_at: float) -> None:
        """Grava o access token e o expires_at (epoch seconds) como um unico segredo serializado."""
        payload = json.dumps({"access_token": access_token, "expires_at": expires_at})
        self._backend.write(self._target_name, payload)

    def get_access_token(self) -> str | None:
        """Devolve o access token gravado, ou None se nao houver nenhum. Nao verifica validade."""
        payload = self._read_payload()
        if payload is None:
            return None
        return payload["access_token"]

    def get_token_metadata(self) -> TokenMetadata | None:
        """Devolve os metadados (expires_at) do token gravado, ou None se nao houver nenhum."""
        payload = self._read_payload()
        if payload is None:
            return None
        return TokenMetadata(expires_at=payload["expires_at"])

    def has_valid_token(self) -> bool:
        """
        True se existir um token gravado e seu expires_at ainda nao
        tiver sido alcancado. Nunca devolve o valor do token.
        """
        metadata = self.get_token_metadata()
        if metadata is None:
            return False
        return metadata.expires_at > self._clock()

    def delete_access_token(self) -> None:
        """Remove o token gravado, se houver."""
        self._backend.delete(self._target_name)

    def _read_payload(self) -> dict | None:
        raw = self._backend.read(self._target_name)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return None
