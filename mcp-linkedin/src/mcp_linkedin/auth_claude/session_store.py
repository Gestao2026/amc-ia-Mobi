"""
Armazenamento em memoria da Camada 1 (Claude.ai <-> mcp-linkedin):
authorization codes, access tokens e refresh tokens. Etapa 7A.

Mesmo principio ja usado na Camada 2 (StateStore, TokenStore): TTL,
uso unico para o authorization code, nada em disco, nada em log.

Persistencia: opcional, por injecao de um CredentialBackend (o mesmo
Protocol da Camada 2, ja usado pelo TokenStore). Sem backend, o
comportamento e o da v1: memoria do processo, exclusivamente, e
reiniciar (ex. o servico "dormir" no plano Free) derruba todas as
sessoes, exigindo nova autorizacao do Claude.

Com backend, access token e refresh token sobrevivem ao reinicio, e o
conector para de pedir "Reconectar" a cada hibernacao. O authorization
code continua so em memoria de proposito: ele vive 5 minutos, no meio
de um aperto de mao que nao atravessa reinicio, e persisti-lo so
acrescentaria escrita remota sem ganho.

A chave de armazenamento e o SHA-256 do token, nunca o token em si: o
backend remoto guarda hash na chave e conteudo cifrado no valor, entao
um dump do banco nao entrega credencial nenhuma.

Persistir nunca pode derrubar autenticacao. Falha do backend (rede
fora, ponte com erro) e engolida e o store segue em memoria: o pior
caso vira o comportamento da v1, que e pedir para reconectar, nunca um
erro na cara do captador.
"""

from __future__ import annotations

import hashlib
import json
import secrets
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable

from mcp.server.auth.provider import AccessToken, AuthorizationCode, RefreshToken

if TYPE_CHECKING:
    # So para tipagem: importar em tempo de execucao criaria uma
    # dependencia da Camada 1 para a Camada 2 sem necessidade nenhuma.
    # Qualquer objeto com write/read/delete serve.
    from mcp_linkedin.auth_linkedin.token_store import CredentialBackend

AUTHORIZATION_CODE_TTL_SECONDS = 300  # 5 minutos
ACCESS_TOKEN_TTL_SECONDS = 3600  # 1 hora
REFRESH_TOKEN_TTL_SECONDS = 60 * 60 * 24 * 30  # 30 dias

# Prefixos das chaves no armazenamento persistente. Especificos deste
# componente, para nao colidir com o alvo do token da rede social
# (Camada 2), que divide o mesmo backend.
PREFIXO_ALVO_ACCESS = "mcp-linkedin:claude-access"
PREFIXO_ALVO_REFRESH = "mcp-linkedin:claude-refresh"


def generate_token() -> str:
    """Valor criptograficamente aleatorio, mesmo padrao usado em toda a Camada 2."""
    return secrets.token_urlsafe(32)


@dataclass
class ClaudeSessionStore:
    """
    Guarda authorization codes, access tokens e refresh tokens.

    Sem `backend`, tudo vive so em memoria. Com `backend`, access e
    refresh token tambem vao para o armazenamento persistente, e a
    memoria passa a ser cache: so a primeira leitura depois de um
    reinicio paga a ida ate la.
    """

    clock: Callable[[], float] = time.time
    backend: "CredentialBackend | None" = None
    _codes: dict = field(default_factory=dict, init=False, repr=False)
    _access_tokens: dict = field(default_factory=dict, init=False, repr=False)
    _refresh_tokens: dict = field(default_factory=dict, init=False, repr=False)

    # --- authorization code ---

    def create_authorization_code(
        self,
        *,
        client_id: str,
        scopes: list[str],
        code_challenge: str,
        redirect_uri,
        redirect_uri_provided_explicitly: bool,
    ) -> AuthorizationCode:
        auth_code = AuthorizationCode(
            code=generate_token(),
            scopes=scopes,
            expires_at=self.clock() + AUTHORIZATION_CODE_TTL_SECONDS,
            client_id=client_id,
            code_challenge=code_challenge,
            redirect_uri=redirect_uri,
            redirect_uri_provided_explicitly=redirect_uri_provided_explicitly,
        )
        self._codes[auth_code.code] = auth_code
        return auth_code

    def get_authorization_code(self, code: str) -> AuthorizationCode | None:
        auth_code = self._codes.get(code)
        if auth_code is None:
            return None
        if auth_code.expires_at < self.clock():
            del self._codes[code]
            return None
        return auth_code

    def consume_authorization_code(self, code: str) -> None:
        """Uso unico: remove o code, independente do resultado da troca por token."""
        self._codes.pop(code, None)

    # --- access token ---

    def create_access_token(self, *, client_id: str, scopes: list[str]) -> AccessToken:
        access_token = AccessToken(
            token=generate_token(),
            client_id=client_id,
            scopes=scopes,
            expires_at=int(self.clock() + ACCESS_TOKEN_TTL_SECONDS),
        )
        self._access_tokens[access_token.token] = access_token
        self._gravar(PREFIXO_ALVO_ACCESS, access_token)
        return access_token

    def get_access_token(self, token: str) -> AccessToken | None:
        access_token = self._access_tokens.get(token)
        if access_token is None:
            access_token = self._recuperar_access_token(token)
        if access_token is None:
            return None
        if access_token.expires_at is not None and access_token.expires_at < self.clock():
            self.revoke_access_token(token)
            return None
        return access_token

    def revoke_access_token(self, token: str) -> None:
        self._access_tokens.pop(token, None)
        self._esquecer(PREFIXO_ALVO_ACCESS, token)

    def _recuperar_access_token(self, token: str) -> AccessToken | None:
        """Le do armazenamento persistente e recoloca em memoria."""
        dados = self._ler(PREFIXO_ALVO_ACCESS, token)
        if dados is None:
            return None
        access_token = AccessToken(
            token=token,
            client_id=dados.get("client_id", ""),
            scopes=list(dados.get("scopes") or []),
            expires_at=dados.get("expires_at"),
        )
        self._access_tokens[token] = access_token
        return access_token

    # --- refresh token ---

    def create_refresh_token(self, *, client_id: str, scopes: list[str]) -> RefreshToken:
        refresh_token = RefreshToken(
            token=generate_token(),
            client_id=client_id,
            scopes=scopes,
            expires_at=int(self.clock() + REFRESH_TOKEN_TTL_SECONDS),
        )
        self._refresh_tokens[refresh_token.token] = refresh_token
        self._gravar(PREFIXO_ALVO_REFRESH, refresh_token)
        return refresh_token

    def get_refresh_token(self, token: str) -> RefreshToken | None:
        refresh_token = self._refresh_tokens.get(token)
        if refresh_token is None:
            refresh_token = self._recuperar_refresh_token(token)
        if refresh_token is None:
            return None
        if refresh_token.expires_at is not None and refresh_token.expires_at < self.clock():
            self.revoke_refresh_token(token)
            return None
        return refresh_token

    def revoke_refresh_token(self, token: str) -> None:
        self._refresh_tokens.pop(token, None)
        self._esquecer(PREFIXO_ALVO_REFRESH, token)

    def _recuperar_refresh_token(self, token: str) -> RefreshToken | None:
        """Le do armazenamento persistente e recoloca em memoria."""
        dados = self._ler(PREFIXO_ALVO_REFRESH, token)
        if dados is None:
            return None
        refresh_token = RefreshToken(
            token=token,
            client_id=dados.get("client_id", ""),
            scopes=list(dados.get("scopes") or []),
            expires_at=dados.get("expires_at"),
        )
        self._refresh_tokens[token] = refresh_token
        return refresh_token

    # --- persistencia opcional ---

    @staticmethod
    def _alvo(prefixo: str, token: str) -> str:
        """
        Chave de armazenamento: o SHA-256 do token, nunca o token.

        O backend remoto guarda a chave em claro, entao usar o proprio
        token ali anularia a cifragem do valor: quem lesse o banco
        colheria credencial pronta. O hash mantem a busca direta (quem
        apresenta o token calcula a mesma chave) sem guardar o segredo.
        """
        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        return f"{prefixo}:{digest}"

    def _gravar(self, prefixo: str, token) -> None:
        if self.backend is None:
            return
        conteudo = json.dumps(
            {
                "client_id": token.client_id,
                "scopes": list(token.scopes),
                "expires_at": token.expires_at,
            }
        )
        try:
            self.backend.write(self._alvo(prefixo, token.token), conteudo)
        except Exception:
            # Persistir e melhoria, nao requisito. Se o backend estiver
            # fora, a sessao segue valida em memoria e o pior caso e o
            # comportamento da v1: pedir para reconectar depois de um
            # reinicio. Derrubar a autorizacao aqui seria pior que isso.
            pass

    def _ler(self, prefixo: str, token: str) -> dict | None:
        if self.backend is None:
            return None
        try:
            conteudo = self.backend.read(self._alvo(prefixo, token))
        except Exception:
            return None
        if not conteudo:
            return None
        try:
            dados = json.loads(conteudo)
        except ValueError:
            # Conteudo corrompido ou cifrado com outra chave equivale a
            # nao haver sessao gravada, que e recuperavel reconectando.
            return None
        return dados if isinstance(dados, dict) else None

    def _esquecer(self, prefixo: str, token: str) -> None:
        if self.backend is None:
            return
        try:
            self.backend.delete(self._alvo(prefixo, token))
        except Exception:
            pass
