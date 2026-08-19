"""
Registro do cliente OAuth estatico da Camada 1 (Claude.ai <->
mcp-linkedin), Etapa 7A.

Sem DCR (RFC 7591) nesta etapa: existe exatamente um cliente
reconhecido, pre-registrado via variavel de ambiente
(MCP_CLAUDE_CLIENT_ID / MCP_CLAUDE_CLIENT_SECRET), nunca hardcoded.

O redirect_uri aceito e fixo e publico, documentado pela Anthropic
para as superficies hospedadas do Claude (claude.ai, Desktop, mobile,
Cowork). Nao e um segredo, por isso pode ser uma constante.
"""

from __future__ import annotations

from mcp.server.auth.provider import OAuthClientInformationFull

CLAUDE_HOSTED_REDIRECT_URI = "https://claude.ai/api/mcp/auth_callback"


def build_static_claude_client(
    client_id: str, client_secret: str | None = None
) -> OAuthClientInformationFull:
    """
    Monta o unico OAuthClientInformationFull reconhecido por este
    servidor: o Claude.ai, identificado pelo client_id configurado.

    Se client_secret for fornecido, o cliente e tratado como
    confidencial (token_endpoint_auth_method="client_secret_post").
    Caso contrario, como publico ("none") -- o PKCE S256, ja validado
    pelo proprio SDK, e a protecao suficiente para um cliente
    publico, conforme OAuth 2.1.
    """
    return OAuthClientInformationFull(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uris=[CLAUDE_HOSTED_REDIRECT_URI],
        grant_types=["authorization_code", "refresh_token"],
        response_types=["code"],
        token_endpoint_auth_method="client_secret_post" if client_secret else "none",
    )
