"""
Testes do registro de cliente estatico da Camada 1 (Claude.ai <->
mcp-linkedin). Nenhum acesso ao LinkedIn, nenhuma chamada de rede,
valores ficticios (FAKE_...).
"""

from mcp_linkedin.auth_claude.client_registry import (
    CLAUDE_HOSTED_REDIRECT_URI,
    build_static_claude_client,
)

FAKE_CLIENT_ID = "FAKE_CLAUDE_CLIENT_ID_NAO_REAL"
FAKE_CLIENT_SECRET = "FAKE_CLAUDE_CLIENT_SECRET_NAO_REAL"


def test_redirect_uri_e_exatamente_o_do_claude_hospedado():
    assert CLAUDE_HOSTED_REDIRECT_URI == "https://claude.ai/api/mcp/auth_callback"


def test_cliente_publico_sem_secret():
    cliente = build_static_claude_client(FAKE_CLIENT_ID)

    assert cliente.client_id == FAKE_CLIENT_ID
    assert cliente.client_secret is None
    assert cliente.token_endpoint_auth_method == "none"
    assert str(cliente.redirect_uris[0]) == CLAUDE_HOSTED_REDIRECT_URI


def test_cliente_confidencial_com_secret():
    cliente = build_static_claude_client(FAKE_CLIENT_ID, FAKE_CLIENT_SECRET)

    assert cliente.client_secret == FAKE_CLIENT_SECRET
    assert cliente.token_endpoint_auth_method == "client_secret_post"


def test_apenas_um_redirect_uri_e_aceito():
    cliente = build_static_claude_client(FAKE_CLIENT_ID)

    assert len(cliente.redirect_uris) == 1


def test_grant_types_suportados_incluem_authorization_code_e_refresh_token():
    cliente = build_static_claude_client(FAKE_CLIENT_ID)

    assert "authorization_code" in cliente.grant_types
    assert "refresh_token" in cliente.grant_types


def test_response_types_e_somente_code():
    cliente = build_static_claude_client(FAKE_CLIENT_ID)

    assert cliente.response_types == ["code"]


def test_client_id_diferente_nao_e_confundido_com_o_estatico():
    cliente = build_static_claude_client(FAKE_CLIENT_ID)

    assert cliente.client_id != "outro-client-id-qualquer"
