"""
Armazenamento seguro LOCAL do access token do LinkedIn (Camada 2),
usando o Windows Credential Manager via pywin32 (win32cred).

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
