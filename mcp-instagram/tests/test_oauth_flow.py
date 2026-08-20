"""
Testes da montagem da URL de autorização do Instagram (oauth_flow.py).

O ponto crítico coberto aqui é o separador de escopos: o Instagram exige
vírgula, e o padrão OAuth usado no mcp-linkedin usa espaço. Enviar
espaço faz a Meta recusar a autorização inteira, e o erro apareceria só
na tela do captador.

Nenhum teste aqui acessa rede.
"""

from __future__ import annotations

from urllib.parse import parse_qs, urlparse

from mcp_instagram.auth_instagram.oauth_flow import (
    AUTHORIZATION_ENDPOINT,
    InstagramOAuthConfig,
    build_authorization_request,
)
from mcp_instagram.auth_instagram.state_store import StateStore

FAKE_CLIENT_ID = "1234567890"
FAKE_CLIENT_SECRET = "segredo-de-teste-nunca-real"
FAKE_REDIRECT_URI = "https://mcp-instagram.exemplo.test/oauth/instagram/callback"


def config_padrao() -> InstagramOAuthConfig:
    return InstagramOAuthConfig(
        client_id=FAKE_CLIENT_ID,
        redirect_uri=FAKE_REDIRECT_URI,
        scopes=["instagram_business_basic", "instagram_business_manage_insights"],
    )


def query_da_url(url: str) -> dict:
    return parse_qs(urlparse(url).query)


def test_url_aponta_para_o_endpoint_oficial_do_instagram():
    pedido = build_authorization_request(config_padrao(), StateStore())

    assert pedido.url.startswith(AUTHORIZATION_ENDPOINT + "?")
    assert urlparse(pedido.url).netloc == "www.instagram.com"


def test_escopos_sao_separados_por_virgula_e_nao_por_espaco():
    pedido = build_authorization_request(config_padrao(), StateStore())

    scope = query_da_url(pedido.url)["scope"][0]

    assert scope == "instagram_business_basic,instagram_business_manage_insights"
    assert " " not in scope


def test_parametros_obrigatorios_estao_presentes():
    pedido = build_authorization_request(config_padrao(), StateStore())

    query = query_da_url(pedido.url)

    assert query["client_id"] == [FAKE_CLIENT_ID]
    assert query["redirect_uri"] == [FAKE_REDIRECT_URI]
    assert query["response_type"] == ["code"]
    assert query["state"] == [pedido.state]


def test_client_secret_nunca_entra_na_url():
    # O tipo InstagramOAuthConfig sequer possui campo de secret, mas o
    # teste guarda a propriedade contra uma mudanca futura desatenta.
    pedido = build_authorization_request(config_padrao(), StateStore())

    assert FAKE_CLIENT_SECRET not in pedido.url
    assert "client_secret" not in pedido.url


def test_state_e_registrado_no_store_e_e_unico_por_chamada():
    store = StateStore()

    primeiro = build_authorization_request(config_padrao(), store)
    segundo = build_authorization_request(config_padrao(), store)

    assert primeiro.state != segundo.state
    assert len(store) == 2
    assert store.validate_and_consume(primeiro.state) is True
    # Uso unico: a segunda validacao do mesmo state falha.
    assert store.validate_and_consume(primeiro.state) is False
