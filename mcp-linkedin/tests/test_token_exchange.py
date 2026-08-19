"""
Testes da troca de authorization code por access token (Camada 2,
mcp-linkedin -> LinkedIn), e da integracao com o TokenStore
(exchange_and_store_token).

Todos os testes usam um transporte HTTP falso (FakeHttpTransport),
injetado em exchange_code_for_token, e um TokenStore com backend de
credencial falso em memoria (FakeCredentialBackend), nunca o Windows
Credential Manager real. Nenhum teste chama a rede real, o LinkedIn,
ou abre navegador. Todos os valores de credencial, code e token sao
ficticios, marcados com o prefixo FAKE_.
"""

import json

import pytest

from mcp_linkedin.auth_linkedin.token_exchange import (
    TOKEN_ENDPOINT,
    HttpResponse,
    TokenExchangeConfig,
    TokenExchangeError,
    TokenExchangeResult,
    TransportError,
    build_token_request,
    exchange_and_store_token,
    exchange_code_for_token,
)
from mcp_linkedin.auth_linkedin.token_store import TokenStore

FAKE_CLIENT_ID = "FAKE_CLIENT_ID_NAO_REAL"
FAKE_CLIENT_SECRET = "FAKE_CLIENT_SECRET_NAO_REAL"
FAKE_REDIRECT_URI = "https://mcp-linkedin.invalid/oauth/linkedin/callback"
FAKE_AUTHORIZATION_CODE = "FAKE_AUTHORIZATION_CODE_NAO_REAL"
FAKE_ACCESS_TOKEN = "FAKE_ACCESS_TOKEN_NAO_REAL"


def _config() -> TokenExchangeConfig:
    return TokenExchangeConfig(
        client_id=FAKE_CLIENT_ID,
        client_secret=FAKE_CLIENT_SECRET,
        redirect_uri=FAKE_REDIRECT_URI,
    )


class FakeHttpTransport:
    """Transporte falso. Nunca acessa rede; devolve ou levanta o que for configurado no teste."""

    def __init__(self, response=None, exception=None):
        self._response = response
        self._exception = exception
        self.last_url = None
        self.last_data = None

    def post(self, url, data):
        self.last_url = url
        self.last_data = data
        if self._exception is not None:
            raise self._exception
        return self._response


class FakeClock:
    def __init__(self, start: float = 1000.0):
        self._now = start

    def __call__(self) -> float:
        return self._now


def _resposta_valida(access_token=FAKE_ACCESS_TOKEN, expires_in=3600):
    body = json.dumps({"access_token": access_token, "expires_in": expires_in})
    return HttpResponse(status_code=200, text=body)


# --- construcao da requisicao (sem transporte, sem execucao) ---


def test_grant_type_correto():
    request = build_token_request(_config(), FAKE_AUTHORIZATION_CODE)
    assert request.form_data["grant_type"] == "authorization_code"


def test_authorization_code_correto():
    request = build_token_request(_config(), FAKE_AUTHORIZATION_CODE)
    assert request.form_data["code"] == FAKE_AUTHORIZATION_CODE


def test_redirect_uri_correto():
    request = build_token_request(_config(), FAKE_AUTHORIZATION_CODE)
    assert request.form_data["redirect_uri"] == FAKE_REDIRECT_URI


def test_client_id_correto():
    request = build_token_request(_config(), FAKE_AUTHORIZATION_CODE)
    assert request.form_data["client_id"] == FAKE_CLIENT_ID


def test_client_secret_enviado_somente_no_body():
    request = build_token_request(_config(), FAKE_AUTHORIZATION_CODE)
    assert request.form_data["client_secret"] == FAKE_CLIENT_SECRET
    assert request.url == TOKEN_ENDPOINT


def test_client_secret_nao_aparece_na_url():
    request = build_token_request(_config(), FAKE_AUTHORIZATION_CODE)
    assert FAKE_CLIENT_SECRET not in request.url
    assert "client_secret" not in request.url


# --- resposta valida ---


def test_resposta_valida_gera_access_token_e_expires_at():
    transport = FakeHttpTransport(response=_resposta_valida())
    resultado = exchange_code_for_token(_config(), FAKE_AUTHORIZATION_CODE, transport, clock=FakeClock())

    assert resultado.access_token == FAKE_ACCESS_TOKEN


def test_expires_in_e_calculado_corretamente():
    transport = FakeHttpTransport(response=_resposta_valida(expires_in=3600))
    clock = FakeClock(start=1000.0)

    resultado = exchange_code_for_token(_config(), FAKE_AUTHORIZATION_CODE, transport, clock=clock)

    assert resultado.expires_at == 1000.0 + 3600


# --- erros de conteudo da resposta ---


def test_access_token_ausente_gera_erro():
    body = json.dumps({"expires_in": 3600})
    transport = FakeHttpTransport(response=HttpResponse(status_code=200, text=body))

    with pytest.raises(TokenExchangeError):
        exchange_code_for_token(_config(), FAKE_AUTHORIZATION_CODE, transport, clock=FakeClock())


def test_expires_in_ausente_gera_erro():
    body = json.dumps({"access_token": FAKE_ACCESS_TOKEN})
    transport = FakeHttpTransport(response=HttpResponse(status_code=200, text=body))

    with pytest.raises(TokenExchangeError):
        exchange_code_for_token(_config(), FAKE_AUTHORIZATION_CODE, transport, clock=FakeClock())


def test_expires_in_invalido_gera_erro():
    body = json.dumps({"access_token": FAKE_ACCESS_TOKEN, "expires_in": "nao-e-numero"})
    transport = FakeHttpTransport(response=HttpResponse(status_code=200, text=body))

    with pytest.raises(TokenExchangeError):
        exchange_code_for_token(_config(), FAKE_AUTHORIZATION_CODE, transport, clock=FakeClock())


def test_resposta_json_invalida_gera_erro():
    transport = FakeHttpTransport(response=HttpResponse(status_code=200, text="isto nao e json"))

    with pytest.raises(TokenExchangeError):
        exchange_code_for_token(_config(), FAKE_AUTHORIZATION_CODE, transport, clock=FakeClock())


def test_erro_oauth_retornado_pelo_linkedin_gera_erro():
    body = json.dumps({"error": "invalid_grant", "error_description": "authorization code invalido ou expirado"})
    transport = FakeHttpTransport(response=HttpResponse(status_code=200, text=body))

    with pytest.raises(TokenExchangeError):
        exchange_code_for_token(_config(), FAKE_AUTHORIZATION_CODE, transport, clock=FakeClock())


# --- erros HTTP ---


def test_http_400_gera_erro():
    transport = FakeHttpTransport(response=HttpResponse(status_code=400, text="{}"))

    with pytest.raises(TokenExchangeError):
        exchange_code_for_token(_config(), FAKE_AUTHORIZATION_CODE, transport, clock=FakeClock())


def test_http_401_gera_erro():
    transport = FakeHttpTransport(response=HttpResponse(status_code=401, text="{}"))

    with pytest.raises(TokenExchangeError):
        exchange_code_for_token(_config(), FAKE_AUTHORIZATION_CODE, transport, clock=FakeClock())


def test_http_403_gera_erro():
    transport = FakeHttpTransport(response=HttpResponse(status_code=403, text="{}"))

    with pytest.raises(TokenExchangeError):
        exchange_code_for_token(_config(), FAKE_AUTHORIZATION_CODE, transport, clock=FakeClock())


# --- erros de transporte ---


def test_timeout_gera_erro():
    transport = FakeHttpTransport(exception=TimeoutError("simulado"))

    with pytest.raises(TransportError):
        exchange_code_for_token(_config(), FAKE_AUTHORIZATION_CODE, transport, clock=FakeClock())


def test_erro_de_transporte_generico_gera_erro():
    transport = FakeHttpTransport(exception=ConnectionError("simulado"))

    with pytest.raises(TransportError):
        exchange_code_for_token(_config(), FAKE_AUTHORIZATION_CODE, transport, clock=FakeClock())


# --- ausencia de segredo em erro/log/repr ---


def test_segredo_nao_aparece_na_mensagem_de_erro():
    transport = FakeHttpTransport(response=HttpResponse(status_code=401, text="{}"))

    with pytest.raises(TokenExchangeError) as excinfo:
        exchange_code_for_token(_config(), FAKE_AUTHORIZATION_CODE, transport, clock=FakeClock())

    assert FAKE_CLIENT_SECRET not in str(excinfo.value)
    assert FAKE_AUTHORIZATION_CODE not in str(excinfo.value)


def test_client_secret_e_code_nao_aparecem_no_repr_da_requisicao():
    request = build_token_request(_config(), FAKE_AUTHORIZATION_CODE)

    texto = repr(request)

    assert FAKE_CLIENT_SECRET not in texto
    assert FAKE_AUTHORIZATION_CODE not in texto


def test_access_token_nao_aparece_em_logs(capsys):
    transport = FakeHttpTransport(response=_resposta_valida())

    exchange_code_for_token(_config(), FAKE_AUTHORIZATION_CODE, transport, clock=FakeClock())

    captured = capsys.readouterr()
    assert FAKE_ACCESS_TOKEN not in captured.out
    assert FAKE_ACCESS_TOKEN not in captured.err


def test_nenhum_teste_realiza_chamada_de_rede(monkeypatch):
    import socket

    def bloquear_rede(*args, **kwargs):
        raise AssertionError("token_exchange nao deve abrir conexao de rede nos testes")

    monkeypatch.setattr(socket.socket, "connect", bloquear_rede)

    transport = FakeHttpTransport(response=_resposta_valida())
    exchange_code_for_token(_config(), FAKE_AUTHORIZATION_CODE, transport, clock=FakeClock())


# =====================================================================
# Integracao: exchange_and_store_token (Token Exchange -> TokenStore)
# =====================================================================
#
# Estes testes nunca tocam o Windows Credential Manager real: o
# TokenStore aqui sempre recebe um FakeCredentialBackend em memoria.
# O "Fake Token Exchange" e um callable simples que simula
# exchange_code_for_token ja aplicado (config/transport/clock fixados
# em producao), devolvendo um TokenExchangeResult ou levantando uma
# excecao, conforme o cenario do teste.


class FakeCredentialBackend:
    """Backend em memoria para o TokenStore nestes testes. Nunca grava no Credential Manager real."""

    def __init__(self):
        self._store = {}

    def write(self, target_name, secret):
        self._store[target_name] = secret

    def read(self, target_name):
        return self._store.get(target_name)

    def delete(self, target_name):
        self._store.pop(target_name, None)


def _token_store(clock=None):
    backend = FakeCredentialBackend()
    store = TokenStore(backend=backend, clock=clock or FakeClock())
    return store, backend


def _fake_token_exchanger_sucesso(access_token=FAKE_ACCESS_TOKEN, expires_at=2000.0):
    def _fn(authorization_code):
        return TokenExchangeResult(access_token=access_token, expires_at=expires_at)

    return _fn


def _fake_token_exchanger_falha():
    def _fn(authorization_code):
        raise TokenExchangeError("falha simulada na troca de token")

    return _fn


def test_token_exchange_bem_sucedido_salva_token():
    store, _ = _token_store()
    exchanger = _fake_token_exchanger_sucesso()

    exchange_and_store_token(FAKE_AUTHORIZATION_CODE, exchanger, store)

    assert store.get_access_token() == FAKE_ACCESS_TOKEN


def test_expires_at_e_preservado():
    store, _ = _token_store()
    exchanger = _fake_token_exchanger_sucesso(expires_at=12345.0)

    exchange_and_store_token(FAKE_AUTHORIZATION_CODE, exchanger, store)

    metadata = store.get_token_metadata()
    assert metadata.expires_at == 12345.0


def test_token_inexistente_gera_erro():
    store, _ = _token_store()
    exchanger = _fake_token_exchanger_sucesso(access_token="")

    with pytest.raises(ValueError):
        exchange_and_store_token(FAKE_AUTHORIZATION_CODE, exchanger, store)

    assert store.get_access_token() is None


def test_expires_at_invalido_gera_erro():
    store, _ = _token_store()
    exchanger = _fake_token_exchanger_sucesso(expires_at=-1.0)

    with pytest.raises(ValueError):
        exchange_and_store_token(FAKE_AUTHORIZATION_CODE, exchanger, store)

    assert store.get_access_token() is None


def test_falha_no_token_exchange_nao_grava_token():
    store, _ = _token_store()
    exchanger = _fake_token_exchanger_falha()

    with pytest.raises(TokenExchangeError):
        exchange_and_store_token(FAKE_AUTHORIZATION_CODE, exchanger, store)

    assert store.get_access_token() is None


def test_erro_no_token_store_e_propagado_com_seguranca():
    class BackendComErro:
        def write(self, target_name, secret):
            raise RuntimeError("falha simulada de Credential Manager")

        def read(self, target_name):
            return None

        def delete(self, target_name):
            pass

    store = TokenStore(backend=BackendComErro(), clock=FakeClock())
    exchanger = _fake_token_exchanger_sucesso()

    with pytest.raises(RuntimeError) as excinfo:
        exchange_and_store_token(FAKE_AUTHORIZATION_CODE, exchanger, store)

    assert FAKE_ACCESS_TOKEN not in str(excinfo.value)
    assert FAKE_CLIENT_SECRET not in str(excinfo.value)


def test_access_token_nao_aparece_nos_logs_da_integracao(capsys):
    store, _ = _token_store()
    exchanger = _fake_token_exchanger_sucesso()

    exchange_and_store_token(FAKE_AUTHORIZATION_CODE, exchanger, store)

    captured = capsys.readouterr()
    assert FAKE_ACCESS_TOKEN not in captured.out
    assert FAKE_ACCESS_TOKEN not in captured.err


def test_client_secret_nao_aparece_nos_logs_da_integracao(capsys):
    store, _ = _token_store()
    exchanger = _fake_token_exchanger_sucesso()

    exchange_and_store_token(FAKE_AUTHORIZATION_CODE, exchanger, store)

    captured = capsys.readouterr()
    assert FAKE_CLIENT_SECRET not in captured.out
    assert FAKE_CLIENT_SECRET not in captured.err


def test_authorization_code_nao_aparece_nos_logs_da_integracao(capsys):
    store, _ = _token_store()
    exchanger = _fake_token_exchanger_sucesso()

    exchange_and_store_token(FAKE_AUTHORIZATION_CODE, exchanger, store)

    captured = capsys.readouterr()
    assert FAKE_AUTHORIZATION_CODE not in captured.out
    assert FAKE_AUTHORIZATION_CODE not in captured.err


def test_nenhum_arquivo_e_criado_durante_a_integracao(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    store, _ = _token_store()
    exchanger = _fake_token_exchanger_sucesso()

    exchange_and_store_token(FAKE_AUTHORIZATION_CODE, exchanger, store)

    assert list(tmp_path.rglob("*")) == []


def test_nenhuma_chamada_de_rede_na_integracao(monkeypatch):
    import socket

    def bloquear_rede(*args, **kwargs):
        raise AssertionError("exchange_and_store_token nao deve abrir conexao de rede")

    monkeypatch.setattr(socket.socket, "connect", bloquear_rede)

    store, _ = _token_store()
    exchanger = _fake_token_exchanger_sucesso()

    exchange_and_store_token(FAKE_AUTHORIZATION_CODE, exchanger, store)


def test_token_salvo_pode_ser_recuperado_pelo_fake_credential_backend():
    store, backend = _token_store()
    exchanger = _fake_token_exchanger_sucesso()

    exchange_and_store_token(FAKE_AUTHORIZATION_CODE, exchanger, store)

    assert backend.read(store._target_name) is not None
    assert store.get_access_token() == FAKE_ACCESS_TOKEN


def test_token_expirado_nao_e_considerado_valido():
    clock = FakeClock(start=5000.0)
    store, _ = _token_store(clock=clock)
    exchanger = _fake_token_exchanger_sucesso(expires_at=1000.0)  # ja no passado

    exchange_and_store_token(FAKE_AUTHORIZATION_CODE, exchanger, store)

    assert store.has_valid_token() is False
