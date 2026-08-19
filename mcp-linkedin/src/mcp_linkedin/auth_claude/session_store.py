"""
Armazenamento em memoria da Camada 1 (Claude.ai <-> mcp-linkedin):
authorization codes, access tokens e refresh tokens. Etapa 7A.

Mesmo principio ja usado na Camada 2 (StateStore, TokenStore): TTL,
uso unico para o authorization code, nada em disco, nada em log.

Escopo desta v1: memoria do processo, exclusivamente (decisao
explicita da Etapa 7A, so para validar o fluxo no Render). Reiniciar
o processo (ex. o servico "dormir" no plano Free) derruba todas as
sessoes, exigindo nova autorizacao do Claude. E uma limitacao
conhecida desta v1, nao um bug.
"""

from __future__ import annotations

import secrets
import time
from dataclasses import dataclass, field
from typing import Callable

from mcp.server.auth.provider import AccessToken, AuthorizationCode, RefreshToken

AUTHORIZATION_CODE_TTL_SECONDS = 300  # 5 minutos
ACCESS_TOKEN_TTL_SECONDS = 3600  # 1 hora
REFRESH_TOKEN_TTL_SECONDS = 60 * 60 * 24 * 30  # 30 dias


def generate_token() -> str:
    """Valor criptograficamente aleatorio, mesmo padrao usado em toda a Camada 2."""
    return secrets.token_urlsafe(32)


@dataclass
class ClaudeSessionStore:
    """Guarda authorization codes, access tokens e refresh tokens, somente em memoria."""

    clock: Callable[[], float] = time.time
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
        return access_token

    def get_access_token(self, token: str) -> AccessToken | None:
        access_token = self._access_tokens.get(token)
        if access_token is None:
            return None
        if access_token.expires_at is not None and access_token.expires_at < self.clock():
            del self._access_tokens[token]
            return None
        return access_token

    def revoke_access_token(self, token: str) -> None:
        self._access_tokens.pop(token, None)

    # --- refresh token ---

    def create_refresh_token(self, *, client_id: str, scopes: list[str]) -> RefreshToken:
        refresh_token = RefreshToken(
            token=generate_token(),
            client_id=client_id,
            scopes=scopes,
            expires_at=int(self.clock() + REFRESH_TOKEN_TTL_SECONDS),
        )
        self._refresh_tokens[refresh_token.token] = refresh_token
        return refresh_token

    def get_refresh_token(self, token: str) -> RefreshToken | None:
        refresh_token = self._refresh_tokens.get(token)
        if refresh_token is None:
            return None
        if refresh_token.expires_at is not None and refresh_token.expires_at < self.clock():
            del self._refresh_tokens[token]
            return None
        return refresh_token

    def revoke_refresh_token(self, token: str) -> None:
        self._refresh_tokens.pop(token, None)
