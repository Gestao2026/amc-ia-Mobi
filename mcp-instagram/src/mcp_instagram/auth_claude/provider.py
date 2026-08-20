"""
OAuthAuthorizationServerProvider da Camada 1 (Claude.ai <->
mcp-instagram), Etapa 7A.

Consentimento: sem tela HTML nesta v1 (decisao explicita). Depois que
o framework do SDK ja validou client_id, redirect_uri e
response_type (antes mesmo de chamar authorize()), este provider
autoriza e redireciona imediatamente. A seguranca desta v1 vem do
client_id ser um valor pre-registrado, conhecido so por quem
configurou o conector no Claude.ai, somado ao PKCE S256 obrigatorio.

PKCE: o code_challenge S256 e validado pelo TokenHandler do proprio
SDK na troca por token (confirmado por inspecao do codigo-fonte na
Etapa 7A) -- este modulo nunca compara code_verifier com
code_challenge, so armazena fielmente o code_challenge recebido.

DCR (registro dinamico, /register) e revogacao via /revoke ficam
desligados nesta etapa (decisao explicita): register_client() sempre
recusa, e a rota /revoke nem chega a ser criada (ver
resolve_claude_auth_config em server.py).

Refresh token: implementado, com rotacao dos dois tokens a cada uso
(recomendado pelo proprio SDK para clientes publicos).

Nenhuma funcao aqui imprime, loga ou inclui code/token/client_secret
em mensagem de erro.
"""

from __future__ import annotations

from mcp.server.auth.provider import (
    AccessToken,
    AuthorizationCode,
    AuthorizationParams,
    OAuthAuthorizationServerProvider,
    OAuthClientInformationFull,
    OAuthToken,
    RefreshToken,
    construct_redirect_uri,
)

from mcp_instagram.auth_claude.client_registry import build_static_claude_client
from mcp_instagram.auth_claude.session_store import ACCESS_TOKEN_TTL_SECONDS, ClaudeSessionStore


class ClaudeAuthProvider(OAuthAuthorizationServerProvider[AuthorizationCode, RefreshToken, AccessToken]):
    """Provider minimo: um unico cliente estatico, sem DCR, sem tela de consentimento."""

    def __init__(self, client_id: str, client_secret: str | None, store: ClaudeSessionStore) -> None:
        self._client = build_static_claude_client(client_id, client_secret)
        self._store = store

    async def get_client(self, client_id: str) -> OAuthClientInformationFull | None:
        if client_id != self._client.client_id:
            return None
        return self._client

    async def register_client(self, client_info: OAuthClientInformationFull) -> None:
        # DCR desabilitado nesta etapa (decisao explicita da Etapa 7A).
        raise NotImplementedError("Registro dinamico de cliente (DCR) nao esta habilitado nesta etapa.")

    async def authorize(self, client: OAuthClientInformationFull, params: AuthorizationParams) -> str:
        auth_code = self._store.create_authorization_code(
            client_id=client.client_id,
            scopes=params.scopes or [],
            code_challenge=params.code_challenge,
            redirect_uri=params.redirect_uri,
            redirect_uri_provided_explicitly=params.redirect_uri_provided_explicitly,
        )
        return construct_redirect_uri(str(params.redirect_uri), code=auth_code.code, state=params.state)

    async def load_authorization_code(
        self, client: OAuthClientInformationFull, authorization_code: str
    ) -> AuthorizationCode | None:
        auth_code = self._store.get_authorization_code(authorization_code)
        if auth_code is None or auth_code.client_id != client.client_id:
            return None
        return auth_code

    async def exchange_authorization_code(
        self, client: OAuthClientInformationFull, authorization_code: AuthorizationCode
    ) -> OAuthToken:
        # Uso unico: consumido aqui, independente do resultado do que segue.
        self._store.consume_authorization_code(authorization_code.code)

        access_token = self._store.create_access_token(
            client_id=client.client_id, scopes=authorization_code.scopes
        )
        refresh_token = self._store.create_refresh_token(
            client_id=client.client_id, scopes=authorization_code.scopes
        )

        return OAuthToken(
            access_token=access_token.token,
            token_type="Bearer",
            expires_in=ACCESS_TOKEN_TTL_SECONDS,
            scope=" ".join(authorization_code.scopes) if authorization_code.scopes else None,
            refresh_token=refresh_token.token,
        )

    async def load_refresh_token(
        self, client: OAuthClientInformationFull, refresh_token: str
    ) -> RefreshToken | None:
        token = self._store.get_refresh_token(refresh_token)
        if token is None or token.client_id != client.client_id:
            return None
        return token

    async def exchange_refresh_token(
        self,
        client: OAuthClientInformationFull,
        refresh_token: RefreshToken,
        scopes: list[str],
    ) -> OAuthToken:
        # Rotaciona os dois tokens a cada uso (recomendado pelo SDK para clientes publicos).
        self._store.revoke_refresh_token(refresh_token.token)

        escopos_finais = scopes or refresh_token.scopes
        novo_access_token = self._store.create_access_token(client_id=client.client_id, scopes=escopos_finais)
        novo_refresh_token = self._store.create_refresh_token(client_id=client.client_id, scopes=escopos_finais)

        return OAuthToken(
            access_token=novo_access_token.token,
            token_type="Bearer",
            expires_in=ACCESS_TOKEN_TTL_SECONDS,
            scope=" ".join(escopos_finais) if escopos_finais else None,
            refresh_token=novo_refresh_token.token,
        )

    async def load_access_token(self, token: str) -> AccessToken | None:
        return self._store.get_access_token(token)

    async def revoke_token(self, token: AccessToken | RefreshToken) -> None:
        # Rota /revoke desabilitada nesta etapa, mas o metodo continua
        # funcional (poderia ser chamado internamente ou numa etapa futura).
        self._store.revoke_access_token(token.token)
        self._store.revoke_refresh_token(token.token)
