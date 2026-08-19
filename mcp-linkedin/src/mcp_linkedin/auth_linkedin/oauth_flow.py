"""
Construcao da URL de autorizacao OAuth do LinkedIn (Camada 2,
mcp-linkedin -> LinkedIn), Authorization Code Flow (3-legged member
authorization).

Escopo deste modulo: somente montar a URL de autorizacao e gerar o
state correspondente via StateStore. Nenhuma chamada HTTP, nenhuma
abertura de navegador, nenhuma troca de authorization code por token,
nenhum callback e nenhum Client Secret pertencem a este modulo. O
Client Secret so entra na troca code -> token (etapa futura, ainda
nao implementada) e nunca deve aparecer numa URL, inclusive na de
autorizacao.

O separador de scopes usado aqui (espaco, codificado como %20) segue
a convencao padrao de OAuth 2.0. Isso deve ser reconferido contra a
documentacao oficial do LinkedIn no momento em que este fluxo for
usado de fato, ja que este modulo nunca acessa o LinkedIn para
validar isso.
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote, urlencode

from mcp_linkedin.auth_linkedin.state_store import StateStore

AUTHORIZATION_ENDPOINT = "https://www.linkedin.com/oauth/v2/authorization"


@dataclass(frozen=True)
class LinkedInOAuthConfig:
    """
    Configuracao necessaria para montar a URL de autorizacao.

    Deliberadamente nao possui campo de Client Secret: essa credencial
    nunca deve viajar numa URL de autorizacao, e este tipo nem
    permite passa-la por engano.
    """

    client_id: str
    redirect_uri: str
    scopes: list[str]


@dataclass(frozen=True)
class AuthorizationRequest:
    """URL de autorizacao pronta e o state que foi gerado para ela."""

    url: str
    state: str


def build_authorization_request(
    config: LinkedInOAuthConfig,
    state_store: StateStore,
) -> AuthorizationRequest:
    """
    Gera um state via StateStore e monta a URL de autorizacao do
    LinkedIn. Nao executa nenhuma chamada de rede, nao abre navegador,
    nao troca nada por token.
    """
    state = state_store.generate()

    params = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "state": state,
        "scope": " ".join(config.scopes),
    }

    query_string = urlencode(params, quote_via=quote)
    url = f"{AUTHORIZATION_ENDPOINT}?{query_string}"

    return AuthorizationRequest(url=url, state=state)
