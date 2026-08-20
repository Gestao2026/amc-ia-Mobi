"""
Construção da URL de autorização OAuth do Instagram (Camada 2,
mcp-instagram para Instagram), no fluxo Authorization Code do
"Instagram API com login do Instagram" (Business Login).

Escopo deste módulo: somente montar a URL de autorização e gerar o
state correspondente via StateStore. Nenhuma chamada HTTP, nenhuma
abertura de navegador, nenhuma troca de authorization code por token,
nenhum callback e nenhum Client Secret pertencem a este módulo. O
Client Secret só entra na troca code para token (token_exchange.py) e
nunca deve aparecer numa URL, inclusive na de autorização.

DIFERENÇA IMPORTANTE EM RELAÇÃO AO LINKEDIN: o Instagram separa os
escopos por VÍRGULA, não por espaço. Enviar separado por espaço faz a
Meta recusar a autorização inteira. É por isso que este módulo não é um
espelho do oauth_flow.py do mcp-linkedin.

A conta precisa ser Comercial (Business) ou Criador de conteúdo. Contas
pessoais não são atendidas pela API da Meta, e a autorização falha na
própria tela do Instagram, não aqui.
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote, urlencode

from mcp_instagram.auth_instagram.state_store import StateStore

AUTHORIZATION_ENDPOINT = "https://www.instagram.com/oauth/authorize"

# Separador exigido pela Meta na lista de escopos. Constante nomeada, e
# não uma vírgula solta no meio do código, porque é justamente o detalhe
# que difere do padrão OAuth usado no mcp-linkedin.
SCOPE_SEPARATOR = ","


@dataclass(frozen=True)
class InstagramOAuthConfig:
    """
    Configuração necessária para montar a URL de autorização.

    Deliberadamente não possui campo de Client Secret: essa credencial
    nunca deve viajar numa URL de autorização, e este tipo nem permite
    passá-la por engano.
    """

    client_id: str
    redirect_uri: str
    scopes: list[str]


@dataclass(frozen=True)
class AuthorizationRequest:
    """URL de autorização pronta e o state que foi gerado para ela."""

    url: str
    state: str


def build_authorization_request(
    config: InstagramOAuthConfig,
    state_store: StateStore,
) -> AuthorizationRequest:
    """
    Gera um state via StateStore e monta a URL de autorização do
    Instagram. Não executa nenhuma chamada de rede, não abre navegador,
    não troca nada por token.
    """
    state = state_store.generate()

    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "scope": SCOPE_SEPARATOR.join(config.scopes),
        "state": state,
    }

    query_string = urlencode(params, quote_via=quote)
    url = f"{AUTHORIZATION_ENDPOINT}?{query_string}"

    return AuthorizationRequest(url=url, state=state)
