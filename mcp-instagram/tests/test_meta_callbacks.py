"""
Testes das duas rotas exigidas pela Meta: desautorização e exclusão de
dados.

A propriedade mais importante coberta aqui é a verificação de
assinatura. As duas rotas são públicas por necessidade do protocolo (a
Meta não envia nenhum token nosso), então, sem a conferência do HMAC,
qualquer pessoa que descobrisse a URL apagaria a autorização do captador
com um POST vazio.

Nenhum teste aqui acessa a Meta ou abre socket real: o app é exercitado
em processo, via ASGI, com `starlette.testclient.TestClient`.
"""

from __future__ import annotations

import pytest
from starlette.testclient import TestClient

import mcp_instagram.server as modulo_servidor
from mcp_instagram.auth_instagram.runtime import InstagramOAuthRuntime
from mcp_instagram.auth_instagram.signed_request import (
    InvalidSignedRequestError,
    build_signed_request,
    parse_signed_request,
)
from mcp_instagram.auth_instagram.state_store import StateStore
from mcp_instagram.auth_instagram.token_store import InMemoryCredentialBackend, TokenStore
from mcp_instagram.config import (
    INSTAGRAM_DATA_DELETION_PATH,
    INSTAGRAM_DATA_DELETION_STATUS_PATH,
    INSTAGRAM_DEAUTHORIZE_PATH,
    resolve_instagram_config,
)

FAKE_CLIENT_ID = "FAKE_INSTAGRAM_CLIENT_ID_NAO_REAL"
FAKE_CLIENT_SECRET = "FAKE_INSTAGRAM_CLIENT_SECRET_NAO_REAL"
FAKE_BASE_URL = "https://mcp-instagram.invalid"
FAKE_USER_ID = "17841400000000000"

_TEST_BASE_URL = "http://127.0.0.1:8080"

PAYLOAD_VALIDO = {"algorithm": "HMAC-SHA256", "user_id": FAKE_USER_ID, "issued_at": 1700000000}


def _env() -> dict:
    return {
        "INSTAGRAM_CLIENT_ID": FAKE_CLIENT_ID,
        "INSTAGRAM_CLIENT_SECRET": FAKE_CLIENT_SECRET,
        "MCP_PUBLIC_BASE_URL": FAKE_BASE_URL,
        "INSTAGRAM_TOKEN_STORE_BACKEND": "memory",
    }


class TransporteProibido:
    def post(self, url, data):
        raise AssertionError("nenhuma chamada de rede deveria acontecer aqui")

    def get(self, url, params):
        raise AssertionError("nenhuma chamada de rede deveria acontecer aqui")


@pytest.fixture
def runtime_com_token():
    """Runtime com uma autorização gravada, para dar o que apagar."""
    runtime = InstagramOAuthRuntime(
        config=resolve_instagram_config(_env()),
        state_store=StateStore(),
        token_store=TokenStore(backend=InMemoryCredentialBackend()),
        transport=TransporteProibido(),
    )
    runtime.token_store.save_access_token("token-de-teste", 9_999_999_999.0, FAKE_USER_ID)
    modulo_servidor._instagram_runtime = runtime

    yield runtime

    modulo_servidor._instagram_runtime = modulo_servidor._RUNTIME_NAO_RESOLVIDO
    _EXCLUSOES = modulo_servidor._EXCLUSOES_ATENDIDAS
    _EXCLUSOES.clear()


def _cliente():
    return TestClient(modulo_servidor.mcp.streamable_http_app(), base_url=_TEST_BASE_URL)


def _assinado(payload=None, secret=FAKE_CLIENT_SECRET) -> dict:
    return {"signed_request": build_signed_request(payload or PAYLOAD_VALIDO, secret)}


# =====================================================================
# Verificação da assinatura
# =====================================================================


def test_assinatura_valida_e_aceita():
    payload = parse_signed_request(
        build_signed_request(PAYLOAD_VALIDO, FAKE_CLIENT_SECRET), FAKE_CLIENT_SECRET
    )

    assert payload["user_id"] == FAKE_USER_ID


def test_assinatura_de_outro_segredo_e_recusada():
    assinado = build_signed_request(PAYLOAD_VALIDO, "outro-segredo")

    with pytest.raises(InvalidSignedRequestError):
        parse_signed_request(assinado, FAKE_CLIENT_SECRET)


def test_payload_adulterado_e_recusado():
    assinado = build_signed_request(PAYLOAD_VALIDO, FAKE_CLIENT_SECRET)
    assinatura, payload = assinado.split(".")
    adulterado = f"{assinatura}.{payload[:-4]}AAAA"

    with pytest.raises(InvalidSignedRequestError):
        parse_signed_request(adulterado, FAKE_CLIENT_SECRET)


@pytest.mark.parametrize("valor", [None, "", "sem-ponto", "a.b.c", "!!!.???"])
def test_formatos_invalidos_sao_recusados(valor):
    with pytest.raises(InvalidSignedRequestError):
        parse_signed_request(valor, FAKE_CLIENT_SECRET)


def test_algoritmo_diferente_e_recusado():
    assinado = build_signed_request({"algorithm": "NONE", "user_id": "1"}, FAKE_CLIENT_SECRET)

    with pytest.raises(InvalidSignedRequestError):
        parse_signed_request(assinado, FAKE_CLIENT_SECRET)


def test_mensagens_de_erro_nunca_contem_o_segredo():
    assinado = build_signed_request(PAYLOAD_VALIDO, "outro-segredo")

    with pytest.raises(InvalidSignedRequestError) as excinfo:
        parse_signed_request(assinado, FAKE_CLIENT_SECRET)

    assert FAKE_CLIENT_SECRET not in str(excinfo.value)


# =====================================================================
# Rota de desautorização
# =====================================================================


def test_desautorizacao_apaga_a_autorizacao(runtime_com_token):
    with _cliente() as client:
        resposta = client.post(INSTAGRAM_DEAUTHORIZE_PATH, data=_assinado())

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "desautorizado"
    assert runtime_com_token.token_store.get_access_token() is None


def test_desautorizacao_sem_assinatura_nao_apaga_nada(runtime_com_token):
    with _cliente() as client:
        resposta = client.post(INSTAGRAM_DEAUTHORIZE_PATH, data={})

    assert resposta.status_code == 400
    assert runtime_com_token.token_store.get_access_token() == "token-de-teste"


def test_desautorizacao_com_assinatura_forjada_nao_apaga_nada(runtime_com_token):
    with _cliente() as client:
        resposta = client.post(
            INSTAGRAM_DEAUTHORIZE_PATH, data=_assinado(secret="segredo-do-atacante")
        )

    assert resposta.status_code == 400
    assert runtime_com_token.token_store.get_access_token() == "token-de-teste"


# =====================================================================
# Rota de exclusão de dados
# =====================================================================


def test_exclusao_apaga_e_devolve_o_formato_exigido_pela_meta(runtime_com_token):
    with _cliente() as client:
        resposta = client.post(INSTAGRAM_DATA_DELETION_PATH, data=_assinado())

    assert resposta.status_code == 200
    corpo = resposta.json()

    # Nomes de campo definidos pela Meta.
    assert "url" in corpo
    assert "confirmation_code" in corpo
    assert corpo["url"].startswith(FAKE_BASE_URL)
    assert runtime_com_token.token_store.get_access_token() is None


def test_exclusao_com_assinatura_forjada_nao_apaga_nada(runtime_com_token):
    with _cliente() as client:
        resposta = client.post(
            INSTAGRAM_DATA_DELETION_PATH, data=_assinado(secret="segredo-do-atacante")
        )

    assert resposta.status_code == 400
    assert runtime_com_token.token_store.get_access_token() == "token-de-teste"


def test_status_da_exclusao_confirma_o_codigo_emitido(runtime_com_token):
    with _cliente() as client:
        codigo = client.post(INSTAGRAM_DATA_DELETION_PATH, data=_assinado()).json()[
            "confirmation_code"
        ]

        resposta = client.get(INSTAGRAM_DATA_DELETION_STATUS_PATH, params={"codigo": codigo})

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "concluido"


def test_status_de_codigo_inexistente_responde_404(runtime_com_token):
    with _cliente() as client:
        resposta = client.get(
            INSTAGRAM_DATA_DELETION_STATUS_PATH, params={"codigo": "codigo-que-nao-existe"}
        )

    assert resposta.status_code == 404
    assert resposta.json()["status"] == "desconhecido"


def test_nenhuma_resposta_expoe_o_token_ou_o_segredo(runtime_com_token):
    with _cliente() as client:
        desautorizacao = client.post(INSTAGRAM_DEAUTHORIZE_PATH, data=_assinado())
        exclusao = client.post(INSTAGRAM_DATA_DELETION_PATH, data=_assinado())

    for resposta in (desautorizacao, exclusao):
        assert "token-de-teste" not in resposta.text
        assert FAKE_CLIENT_SECRET not in resposta.text
