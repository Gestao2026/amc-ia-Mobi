"""
Testes da construcao da URL de autorizacao OAuth do LinkedIn.

Nenhum destes testes acessa rede, abre navegador, ou usa Client
Secret, authorization code ou token algum. Todos os valores de
client_id e redirect_uri usados aqui sao ficticios, marcados de forma
explicita para nao serem confundidos com configuracao real: o
client_id traz o prefixo "FAKE_" e o redirect_uri usa o dominio
reservado ".invalid" (RFC 2606), que nunca resolve na internet real.
"""

from urllib.parse import parse_qs, urlparse

from mcp_linkedin.auth_linkedin.oauth_flow import (
    AUTHORIZATION_ENDPOINT,
    LinkedInOAuthConfig,
    build_authorization_request,
)
from mcp_linkedin.auth_linkedin.state_store import StateStore

# Scopes da primeira versao planejada (ver plano tecnico da Etapa 3),
# usados aqui apenas para exercitar a codificacao da URL. Nenhuma
# implementacao real decide, a partir daqui, quais scopes sao
# efetivamente solicitados.
SCOPES_PLANO = [
    "openid",
    "profile",
    "email",
    "r_basicprofile",
    "r_organization_social",
    "r_organization_admin",
    "w_organization_social",
    "w_member_social",
]

FAKE_CLIENT_ID = "FAKE_CLIENT_ID_NAO_REAL abc&def"
FAKE_REDIRECT_URI = "https://mcp-linkedin.invalid/oauth/linkedin/callback"


def _config(scopes=None) -> LinkedInOAuthConfig:
    return LinkedInOAuthConfig(
        client_id=FAKE_CLIENT_ID,
        redirect_uri=FAKE_REDIRECT_URI,
        scopes=scopes if scopes is not None else SCOPES_PLANO,
    )


def test_url_contem_endpoint_correto():
    result = build_authorization_request(_config(), StateStore())

    assert result.url.startswith(AUTHORIZATION_ENDPOINT + "?")


def test_response_type_e_code():
    result = build_authorization_request(_config(), StateStore())
    query = parse_qs(urlparse(result.url).query)

    assert query["response_type"] == ["code"]


def test_client_id_e_corretamente_codificado():
    result = build_authorization_request(_config(), StateStore())
    query = parse_qs(urlparse(result.url).query)

    # O client_id ficticio contem espaco e "&", que precisam ser
    # percent-encoded na URL bruta, mas devem voltar intactos ao
    # decodificar a query string.
    assert "FAKE_CLIENT_ID_NAO_REAL abc&def" not in result.url
    assert query["client_id"] == [FAKE_CLIENT_ID]


def test_redirect_uri_e_corretamente_codificado():
    result = build_authorization_request(_config(), StateStore())
    query = parse_qs(urlparse(result.url).query)

    # A URL crua nao deve conter o redirect_uri em texto puro (ele
    # tem "://" e "/", que sao percent-encoded como valor de query).
    assert "redirect_uri=https://" not in result.url
    assert query["redirect_uri"] == [FAKE_REDIRECT_URI]


def test_scope_e_corretamente_codificado():
    result = build_authorization_request(_config(), StateStore())
    query = parse_qs(urlparse(result.url).query)

    assert query["scope"] == [" ".join(SCOPES_PLANO)]
    assert "scope=openid%20profile%20email" in result.url


def test_state_e_criado_pelo_state_store():
    store = StateStore()
    assert len(store) == 0

    result = build_authorization_request(_config(), store)

    assert result.state
    assert len(store) == 1


def test_state_e_diferente_em_duas_autorizacoes_sucessivas():
    store = StateStore()

    primeira = build_authorization_request(_config(), store)
    segunda = build_authorization_request(_config(), store)

    assert primeira.state != segunda.state


def test_state_criado_pode_ser_validado_pelo_state_store():
    store = StateStore()
    result = build_authorization_request(_config(), store)

    assert store.validate_and_consume(result.state) is True


def test_client_secret_nunca_aparece_na_url():
    result = build_authorization_request(_config(), StateStore())

    assert "secret" not in result.url.lower()
    assert not hasattr(LinkedInOAuthConfig, "client_secret")


def test_nenhum_acesso_de_rede_ocorre(monkeypatch):
    import socket

    def bloquear_rede(*args, **kwargs):
        raise AssertionError("oauth_flow nao deve abrir conexao de rede")

    monkeypatch.setattr(socket.socket, "connect", bloquear_rede)

    build_authorization_request(_config(), StateStore())


def test_valores_ficticios_nao_sao_confundidos_com_configuracao_real():
    config = _config()

    assert "FAKE" in config.client_id
    assert config.redirect_uri.endswith(".invalid/oauth/linkedin/callback")


def test_lista_de_scopes_pode_ser_configurada():
    scopes_minimos = ["openid", "email", "r_basicprofile", "r_organization_admin"]

    result = build_authorization_request(_config(scopes=scopes_minimos), StateStore())
    query = parse_qs(urlparse(result.url).query)

    assert query["scope"] == [" ".join(scopes_minimos)]
