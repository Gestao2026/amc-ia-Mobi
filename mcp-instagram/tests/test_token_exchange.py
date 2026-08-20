"""
Testes da troca de authorization code por access token do Instagram.

O comportamento crítico coberto aqui é a troca em DUAS etapas: parar na
etapa 1 devolveria um token de uma hora, que na prática não é uma
conexão. Vários testes existem justamente para garantir que a etapa 2
não pode ser silenciosamente pulada.

Nenhum teste aqui acessa rede: o transporte é sempre falso.
"""

from __future__ import annotations

import json

import pytest

from mcp_instagram.auth_instagram.token_exchange import (
    LONG_LIVED_TOKEN_ENDPOINT,
    SHORT_LIVED_TOKEN_ENDPOINT,
    HttpResponse,
    TokenExchangeConfig,
    TokenExchangeError,
    TokenExchangeResult,
    TransportError,
    build_long_lived_token_request,
    build_short_lived_token_request,
    exchange_and_store_token,
    exchange_code_for_token,
)
from mcp_instagram.auth_instagram.token_store import InMemoryCredentialBackend, TokenStore

FAKE_CLIENT_ID = "1234567890"
FAKE_CLIENT_SECRET = "segredo-de-teste-nunca-real"
FAKE_REDIRECT_URI = "https://mcp-instagram.exemplo.test/oauth/instagram/callback"
FAKE_CODE = "authorization-code-de-teste"
FAKE_TOKEN_CURTO = "token-curto-de-teste"
FAKE_TOKEN_LONGO = "token-longo-de-teste"
FAKE_USER_ID = "17841400000000000"

SESSENTA_DIAS = 5184000


def config() -> TokenExchangeConfig:
    return TokenExchangeConfig(
        client_id=FAKE_CLIENT_ID,
        client_secret=FAKE_CLIENT_SECRET,
        redirect_uri=FAKE_REDIRECT_URI,
    )


class FakeTransport:
    """
    Transporte falso que registra as chamadas recebidas e devolve as
    respostas programadas, uma para cada etapa.
    """

    def __init__(self, resposta_curta: HttpResponse, resposta_longa: HttpResponse | None = None):
        self.resposta_curta = resposta_curta
        self.resposta_longa = resposta_longa
        self.chamadas: list[tuple[str, str, dict]] = []

    def post(self, url: str, data: dict) -> HttpResponse:
        self.chamadas.append(("POST", url, data))
        return self.resposta_curta

    def get(self, url: str, params: dict) -> HttpResponse:
        self.chamadas.append(("GET", url, params))
        if self.resposta_longa is None:
            raise AssertionError("A etapa 2 nao deveria ter sido chamada neste cenario.")
        return self.resposta_longa


def resposta_curta_formato_atual() -> HttpResponse:
    """Formato atual da Meta: os campos vêm embrulhados numa lista em `data`."""
    corpo = {"data": [{"access_token": FAKE_TOKEN_CURTO, "user_id": FAKE_USER_ID}]}
    return HttpResponse(status_code=200, text=json.dumps(corpo))


def resposta_curta_formato_legado() -> HttpResponse:
    """Formato legado da Meta: os campos vêm na raiz do objeto."""
    corpo = {"access_token": FAKE_TOKEN_CURTO, "user_id": int(FAKE_USER_ID)}
    return HttpResponse(status_code=200, text=json.dumps(corpo))


def resposta_longa_ok() -> HttpResponse:
    corpo = {
        "access_token": FAKE_TOKEN_LONGO,
        "token_type": "bearer",
        "expires_in": SESSENTA_DIAS,
    }
    return HttpResponse(status_code=200, text=json.dumps(corpo))


def relogio_fixo() -> float:
    return 1_000_000.0


# --- montagem das requisições ---------------------------------------


def test_etapa_1_manda_o_secret_no_corpo_e_nao_na_url():
    pedido = build_short_lived_token_request(config(), FAKE_CODE)

    assert pedido.method == "POST"
    assert pedido.url == SHORT_LIVED_TOKEN_ENDPOINT
    assert "?" not in pedido.url
    assert pedido.params["client_secret"] == FAKE_CLIENT_SECRET
    assert pedido.params["code"] == FAKE_CODE
    assert pedido.params["grant_type"] == "authorization_code"


def test_etapa_2_usa_o_grant_type_de_troca_do_instagram():
    pedido = build_long_lived_token_request(config(), FAKE_TOKEN_CURTO)

    assert pedido.method == "GET"
    assert pedido.url == LONG_LIVED_TOKEN_ENDPOINT
    assert pedido.params["grant_type"] == "ig_exchange_token"
    assert pedido.params["access_token"] == FAKE_TOKEN_CURTO


def test_repr_da_requisicao_mascara_secret_code_e_token():
    curto = repr(build_short_lived_token_request(config(), FAKE_CODE))
    longo = repr(build_long_lived_token_request(config(), FAKE_TOKEN_CURTO))

    assert FAKE_CLIENT_SECRET not in curto
    assert FAKE_CODE not in curto
    assert FAKE_CLIENT_SECRET not in longo
    assert FAKE_TOKEN_CURTO not in longo
    assert "***" in curto and "***" in longo


# --- troca completa --------------------------------------------------


def test_troca_completa_devolve_o_token_de_longa_duracao():
    transport = FakeTransport(resposta_curta_formato_atual(), resposta_longa_ok())

    resultado = exchange_code_for_token(config(), FAKE_CODE, transport, relogio_fixo)

    assert resultado.access_token == FAKE_TOKEN_LONGO
    assert resultado.expires_at == relogio_fixo() + SESSENTA_DIAS
    assert resultado.user_id == FAKE_USER_ID


def test_troca_completa_aceita_o_formato_legado_da_etapa_1():
    transport = FakeTransport(resposta_curta_formato_legado(), resposta_longa_ok())

    resultado = exchange_code_for_token(config(), FAKE_CODE, transport, relogio_fixo)

    assert resultado.access_token == FAKE_TOKEN_LONGO
    assert resultado.user_id == FAKE_USER_ID


def test_as_duas_etapas_sao_executadas_na_ordem_correta():
    transport = FakeTransport(resposta_curta_formato_atual(), resposta_longa_ok())

    exchange_code_for_token(config(), FAKE_CODE, transport, relogio_fixo)

    metodos = [(metodo, url) for metodo, url, _ in transport.chamadas]
    assert metodos == [
        ("POST", SHORT_LIVED_TOKEN_ENDPOINT),
        ("GET", LONG_LIVED_TOKEN_ENDPOINT),
    ]


def test_o_token_curto_nunca_e_devolvido_como_resultado_final():
    transport = FakeTransport(resposta_curta_formato_atual(), resposta_longa_ok())

    resultado = exchange_code_for_token(config(), FAKE_CODE, transport, relogio_fixo)

    assert resultado.access_token != FAKE_TOKEN_CURTO


# --- falhas ----------------------------------------------------------


@pytest.mark.parametrize("status", [400, 401, 403, 500])
def test_status_de_erro_na_etapa_1_interrompe_a_troca(status):
    transport = FakeTransport(HttpResponse(status_code=status, text="{}"))

    with pytest.raises(TokenExchangeError):
        exchange_code_for_token(config(), FAKE_CODE, transport, relogio_fixo)

    # A etapa 2 nao chegou a ser chamada.
    assert len(transport.chamadas) == 1


def test_falha_na_etapa_2_faz_a_troca_inteira_falhar():
    transport = FakeTransport(
        resposta_curta_formato_atual(),
        HttpResponse(status_code=400, text="{}"),
    )

    with pytest.raises(TokenExchangeError):
        exchange_code_for_token(config(), FAKE_CODE, transport, relogio_fixo)


def test_etapa_2_sem_expires_in_e_recusada():
    corpo = json.dumps({"access_token": FAKE_TOKEN_LONGO, "token_type": "bearer"})
    transport = FakeTransport(
        resposta_curta_formato_atual(), HttpResponse(status_code=200, text=corpo)
    )

    with pytest.raises(TokenExchangeError):
        exchange_code_for_token(config(), FAKE_CODE, transport, relogio_fixo)


def test_erro_oauth_no_corpo_e_recusado_mesmo_com_http_200():
    corpo = json.dumps({"error_type": "OAuthException", "error_message": "irrelevante"})
    transport = FakeTransport(HttpResponse(status_code=200, text=corpo))

    with pytest.raises(TokenExchangeError):
        exchange_code_for_token(config(), FAKE_CODE, transport, relogio_fixo)


def test_resposta_que_nao_e_json_e_recusada():
    transport = FakeTransport(HttpResponse(status_code=200, text="<html>erro</html>"))

    with pytest.raises(TokenExchangeError):
        exchange_code_for_token(config(), FAKE_CODE, transport, relogio_fixo)


def test_falha_de_transporte_vira_transport_error():
    class TransporteQuebrado:
        def post(self, url, data):
            raise ConnectionError("rede caiu")

        def get(self, url, params):
            raise AssertionError("nao deveria chegar aqui")

    with pytest.raises(TransportError):
        exchange_code_for_token(config(), FAKE_CODE, TransporteQuebrado(), relogio_fixo)


def test_mensagens_de_erro_nunca_contem_segredo():
    transport = FakeTransport(HttpResponse(status_code=400, text="{}"))

    with pytest.raises(TokenExchangeError) as excinfo:
        exchange_code_for_token(config(), FAKE_CODE, transport, relogio_fixo)

    mensagem = str(excinfo.value)
    assert FAKE_CLIENT_SECRET not in mensagem
    assert FAKE_CODE not in mensagem


# --- gravação --------------------------------------------------------


def test_gravacao_so_acontece_quando_a_troca_da_certo():
    store = TokenStore(backend=InMemoryCredentialBackend(), clock=relogio_fixo)

    def exchanger_que_falha(code):
        raise TokenExchangeError("falhou")

    with pytest.raises(TokenExchangeError):
        exchange_and_store_token(FAKE_CODE, exchanger_que_falha, store)

    assert store.get_access_token() is None


def test_gravacao_guarda_token_validade_e_conta():
    store = TokenStore(backend=InMemoryCredentialBackend(), clock=relogio_fixo)

    def exchanger_ok(code):
        return TokenExchangeResult(
            access_token=FAKE_TOKEN_LONGO,
            expires_at=relogio_fixo() + SESSENTA_DIAS,
            user_id=FAKE_USER_ID,
        )

    exchange_and_store_token(FAKE_CODE, exchanger_ok, store)

    assert store.get_access_token() == FAKE_TOKEN_LONGO
    assert store.has_valid_token() is True
    assert store.get_token_metadata().user_id == FAKE_USER_ID
