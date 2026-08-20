"""
Testes do processamento logico do callback OAuth do Instagram.

Nenhum destes testes inicia servidor HTTP, acessa rede ou usa Client
ID/Client Secret/authorization code/access token reais. Usa o
StateStore real (em memoria, ja testado na Etapa 3A) com um relogio
falso, e um token_exchanger fictico injetado, nunca o token_exchange
real do Instagram.
"""

import pytest

from mcp_instagram.auth_instagram.oauth_callback import (
    CallbackOutcome,
    CallbackParams,
    CallbackResult,
    process_callback,
)
from mcp_instagram.auth_instagram.state_store import StateStore

FAKE_AUTHORIZATION_CODE = "FAKE_AUTHORIZATION_CODE_NAO_REAL"
FAKE_STATE_INVALIDO = "FAKE_STATE_NAO_REAL_NUNCA_EMITIDO"
FAKE_CLIENT_SECRET = "FAKE_CLIENT_SECRET_NAO_REAL"
FAKE_ACCESS_TOKEN = "FAKE_ACCESS_TOKEN_NAO_REAL"


class FakeClock:
    def __init__(self, start: float = 0.0):
        self._now = start

    def __call__(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        self._now += seconds


def _token_exchanger_nao_deve_ser_chamado():
    def _fn(authorization_code):
        raise AssertionError("token_exchanger nao deveria ser chamado neste cenario")

    return _fn


# --- caminho feliz ---


def test_callback_valido_encaminha_para_token_exchange():
    store = StateStore(clock=FakeClock())
    state = store.generate()
    params = CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=state)

    resultado = process_callback(params, store, lambda code: "resultado-ficticio")

    assert resultado.outcome == CallbackOutcome.TOKEN_EXCHANGE_STARTED
    assert resultado.token_exchange_result == "resultado-ficticio"


def test_code_valido_e_encaminhado_ao_token_exchange():
    store = StateStore(clock=FakeClock())
    state = store.generate()
    chamadas = []

    def fake_token_exchanger(authorization_code):
        chamadas.append(authorization_code)
        return "ok"

    params = CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=state)
    process_callback(params, store, fake_token_exchanger)

    assert chamadas == [FAKE_AUTHORIZATION_CODE]


# --- state ---


def test_state_ausente_e_rejeitado():
    store = StateStore(clock=FakeClock())
    params = CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=None)

    resultado = process_callback(params, store, _token_exchanger_nao_deve_ser_chamado())

    assert resultado.outcome == CallbackOutcome.REJECTED_STATE_MISSING


def test_state_invalido_e_rejeitado():
    store = StateStore(clock=FakeClock())
    params = CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=FAKE_STATE_INVALIDO)

    resultado = process_callback(params, store, _token_exchanger_nao_deve_ser_chamado())

    assert resultado.outcome == CallbackOutcome.REJECTED_STATE_INVALID


def test_state_expirado_e_rejeitado():
    clock = FakeClock()
    store = StateStore(ttl_seconds=600, clock=clock)
    state = store.generate()
    clock.advance(601)

    params = CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=state)
    resultado = process_callback(params, store, _token_exchanger_nao_deve_ser_chamado())

    assert resultado.outcome == CallbackOutcome.REJECTED_STATE_INVALID


def test_state_reutilizado_e_rejeitado():
    store = StateStore(clock=FakeClock())
    state = store.generate()

    primeiro = process_callback(
        CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=state), store, lambda code: "ok"
    )
    segundo = process_callback(
        CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=state),
        store,
        _token_exchanger_nao_deve_ser_chamado(),
    )

    assert primeiro.outcome == CallbackOutcome.TOKEN_EXCHANGE_STARTED
    assert segundo.outcome == CallbackOutcome.REJECTED_STATE_INVALID


def test_state_e_consumido_antes_do_encaminhamento():
    store = StateStore(clock=FakeClock())
    state = store.generate()

    def token_exchanger_que_falha(authorization_code):
        raise RuntimeError("falha simulada no token exchange")

    params = CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=state)

    with pytest.raises(RuntimeError):
        process_callback(params, store, token_exchanger_que_falha)

    # Mesmo com falha no exchange, o state ja foi consumido (uso
    # unico): tentar valida-lo de novo falha.
    assert store.validate_and_consume(state) is False


def test_callback_repetido_e_rejeitado():
    store = StateStore(clock=FakeClock())
    state = store.generate()

    process_callback(CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=state), store, lambda code: "ok")

    # Repetir o mesmo callback (possivel replay), mesmo com um code
    # diferente, deve falhar porque o state ja foi consumido.
    resultado_repetido = process_callback(
        CallbackParams(code="FAKE_AUTHORIZATION_CODE_OUTRO", state=state),
        store,
        _token_exchanger_nao_deve_ser_chamado(),
    )

    assert resultado_repetido.outcome == CallbackOutcome.REJECTED_STATE_INVALID


# --- code ---


def test_code_ausente_e_rejeitado():
    store = StateStore(clock=FakeClock())
    state = store.generate()
    params = CallbackParams(code=None, state=state)

    resultado = process_callback(params, store, _token_exchanger_nao_deve_ser_chamado())

    assert resultado.outcome == CallbackOutcome.REJECTED_CODE_MISSING


# --- erro OAuth retornado pelo provedor ---


def test_erro_oauth_retornado_e_rejeitado():
    store = StateStore(clock=FakeClock())
    state = store.generate()
    params = CallbackParams(state=state, error="access_denied")

    resultado = process_callback(params, store, _token_exchanger_nao_deve_ser_chamado())

    assert resultado.outcome == CallbackOutcome.REJECTED_OAUTH_ERROR
    assert resultado.oauth_error == "access_denied"


def test_erro_oauth_com_descricao_e_rejeitado():
    store = StateStore(clock=FakeClock())
    state = store.generate()
    params = CallbackParams(
        state=state,
        error="access_denied",
        error_description="o usuario negou o consentimento",
    )

    resultado = process_callback(params, store, _token_exchanger_nao_deve_ser_chamado())

    assert resultado.outcome == CallbackOutcome.REJECTED_OAUTH_ERROR
    assert resultado.oauth_error == "access_denied"
    assert resultado.oauth_error_description == "o usuario negou o consentimento"


# --- seguranca: ausencia de segredo em erro/log/repr ---


def test_nenhum_segredo_aparece_em_erros():
    store = StateStore(clock=FakeClock())
    state = store.generate()

    resultado = process_callback(
        CallbackParams(code=None, state=state), store, _token_exchanger_nao_deve_ser_chamado()
    )

    assert FAKE_CLIENT_SECRET not in resultado.detail
    assert FAKE_ACCESS_TOKEN not in resultado.detail
    assert state not in resultado.detail


def test_callback_params_repr_nao_expoe_code_nem_state():
    params = CallbackParams(code=FAKE_AUTHORIZATION_CODE, state="alguma-coisa-secreta")

    texto = repr(params)

    assert FAKE_AUTHORIZATION_CODE not in texto
    assert "alguma-coisa-secreta" not in texto


def test_nenhum_code_aparece_em_stdout_stderr(capsys):
    store = StateStore(clock=FakeClock())
    state = store.generate()
    params = CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=state)

    process_callback(params, store, lambda code: "ok")

    captured = capsys.readouterr()
    assert FAKE_AUTHORIZATION_CODE not in captured.out
    assert FAKE_AUTHORIZATION_CODE not in captured.err


def test_nenhuma_chamada_de_rede(monkeypatch):
    import socket

    def bloquear_rede(*args, **kwargs):
        raise AssertionError("oauth_callback nao deve abrir conexao de rede")

    monkeypatch.setattr(socket.socket, "connect", bloquear_rede)

    store = StateStore(clock=FakeClock())
    state = store.generate()
    params = CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=state)

    process_callback(params, store, lambda code: "ok")


def test_valores_ficticios_usados_sao_claramente_marcados():
    assert FAKE_AUTHORIZATION_CODE.startswith("FAKE_")
    assert FAKE_STATE_INVALIDO.startswith("FAKE_")
    assert FAKE_CLIENT_SECRET.startswith("FAKE_")
    assert FAKE_ACCESS_TOKEN.startswith("FAKE_")
