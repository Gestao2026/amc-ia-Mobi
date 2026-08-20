"""
Testes da Camada 2 ligada de ponta a ponta (Etapa 7B):

    config -> ferramenta MCP -> URL de autorizacao -> callback HTTP
    -> troca de code por token -> TokenStore

Cobrem `config.py`, `auth_instagram/http_transport.py`,
`auth_instagram/runtime.py` e a integracao no `server.py` (rota de
callback e as tres ferramentas MCP).

NENHUM teste aqui acessa o Instagram real, abre navegador ou usa
credencial real:
- todos os valores de client_id, client_secret, authorization code,
  state e token sao ficticios, com o prefixo FAKE_;
- o redirect_uri usa o dominio reservado ".invalid" (RFC 2606), que
  nunca resolve na internet real;
- o transporte HTTP e sempre falso (FakeHttpTransport), exceto nos
  testes especificos do HttpxTransport, que usam um MockTransport do
  proprio httpx2 (resposta sintetica, em processo, sem socket);
- o TokenStore sempre recebe o InMemoryCredentialBackend, nunca o
  Windows Credential Manager real;
- os testes da rota usam starlette.testclient.TestClient, que fala com
  o app via ASGI em processo, sem abrir socket real;
- varios testes bloqueiam ativamente qualquer conexao que nao seja
  loopback.
"""

import json
import socket

import httpx2
import pytest
from starlette.testclient import TestClient

import mcp_instagram.server as modulo_servidor
from mcp_instagram.auth_instagram.http_transport import DEFAULT_TIMEOUT_SECONDS, HttpxTransport
from mcp_instagram.auth_instagram.oauth_callback import CallbackOutcome, CallbackParams
from mcp_instagram.auth_instagram.runtime import (
    InstagramOAuthRuntime,
    build_credential_backend,
    build_runtime,
)
from mcp_instagram.auth_instagram.state_store import StateStore
from mcp_instagram.auth_instagram.token_exchange import (
    LONG_LIVED_TOKEN_ENDPOINT,
    SHORT_LIVED_TOKEN_ENDPOINT,
    HttpResponse,
    TokenExchangeError,
    TransportError,
)
from mcp_instagram.auth_instagram.token_store import InMemoryCredentialBackend, TokenStore
from mcp_instagram.config import (
    DEFAULT_INSTAGRAM_SCOPES,
    INSTAGRAM_CALLBACK_PATH,
    TOKEN_STORE_BACKEND_MEMORY,
    TOKEN_STORE_BACKEND_WINDOWS,
    InvalidInstagramConfigError,
    InstagramConfig,
    default_token_store_backend,
    missing_instagram_env_vars,
    resolve_instagram_config,
)
from mcp_instagram.server import (
    instagram_mcp_status,
    instagram_oauth_iniciar,
    instagram_oauth_status,
    resolve_instagram_runtime,
)

FAKE_CLIENT_ID = "FAKE_INSTAGRAM_CLIENT_ID_NAO_REAL"
FAKE_CLIENT_SECRET = "FAKE_INSTAGRAM_CLIENT_SECRET_NAO_REAL"
FAKE_BASE_URL = "https://mcp-instagram.invalid"
FAKE_REDIRECT_URI = f"{FAKE_BASE_URL}{INSTAGRAM_CALLBACK_PATH}"
FAKE_ACCESS_TOKEN = "FAKE_ACCESS_TOKEN_NAO_REAL"
FAKE_AUTHORIZATION_CODE = "FAKE_AUTHORIZATION_CODE_NAO_REAL"

_TEST_BASE_URL = "http://127.0.0.1:8080"


def _env(**overrides) -> dict:
    env = {
        "INSTAGRAM_CLIENT_ID": FAKE_CLIENT_ID,
        "INSTAGRAM_CLIENT_SECRET": FAKE_CLIENT_SECRET,
        "MCP_PUBLIC_BASE_URL": FAKE_BASE_URL,
    }
    env.update({chave: valor for chave, valor in overrides.items() if valor is not None})
    return env


class FakeClock:
    def __init__(self, start: float = 1000.0):
        self._now = start

    def __call__(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        self._now += seconds


FAKE_SHORT_LIVED_TOKEN = "FAKE_SHORT_LIVED_TOKEN_NAO_REAL"
FAKE_USER_ID = "17841400000000000"


class FakeHttpTransport:
    """
    Transporte falso. Nunca acessa rede; devolve ou levanta o que o teste
    configurar.

    Precisa cobrir as DUAS etapas da troca do Instagram: `post` responde a
    etapa 1 (token de curta duracao) e `get` responde a etapa 2 (token de
    longa duracao). Quando o teste passa apenas `response`, ela e usada na
    etapa 2, que e a que produz o token final gravado.
    """

    def __init__(self, response=None, exception=None, response_curta=None, exception_get=None):
        self._response = response
        self._exception = exception
        self._response_curta = response_curta or _resposta_token_curto_valida()
        self._exception_get = exception_get
        self.chamadas = []
        self.chamadas_get = []

    def post(self, url, data):
        self.chamadas.append((url, data))
        if self._exception is not None:
            raise self._exception
        return self._response_curta

    def get(self, url, params):
        self.chamadas_get.append((url, params))
        if self._exception_get is not None:
            raise self._exception_get
        return self._response


def _resposta_token_curto_valida(
    access_token=FAKE_SHORT_LIVED_TOKEN, user_id=FAKE_USER_ID
) -> HttpResponse:
    """Resposta da etapa 1: token de curta duracao e id da conta, sem expires_in."""
    return HttpResponse(
        status_code=200,
        text=json.dumps({"data": [{"access_token": access_token, "user_id": user_id}]}),
    )


def _resposta_token_valida(access_token=FAKE_ACCESS_TOKEN, expires_in=3600) -> HttpResponse:
    """Resposta da etapa 2: token de longa duracao, com expires_in."""
    return HttpResponse(
        status_code=200,
        text=json.dumps(
            {"access_token": access_token, "token_type": "bearer", "expires_in": expires_in}
        ),
    )


def _runtime(transport=None, clock=None, config=None) -> InstagramOAuthRuntime:
    """Runtime completo com peças reais, exceto o transporte HTTP (sempre falso)."""
    clock = clock or FakeClock()
    return InstagramOAuthRuntime(
        config=config or resolve_instagram_config(_env()),
        state_store=StateStore(clock=FakeClock()),
        token_store=TokenStore(backend=InMemoryCredentialBackend(), clock=clock),
        transport=transport or FakeHttpTransport(response=_resposta_token_valida()),
        clock=clock,
    )


@pytest.fixture
def runtime_injetado(request):
    """
    Injeta um runtime nas ferramentas/rota do server.py e restaura o
    sentinela de "ainda nao resolvido" ao final, para nao vazar estado
    entre testes.
    """
    runtimes = []

    def _injetar(runtime):
        modulo_servidor._instagram_runtime = runtime
        runtimes.append(runtime)
        return runtime

    yield _injetar

    modulo_servidor._instagram_runtime = modulo_servidor._RUNTIME_NAO_RESOLVIDO


def _bloquear_rede_externa(monkeypatch):
    """Deixa passar só loopback (necessário para o event loop no Windows)."""
    conectar_original = socket.socket.connect

    def bloquear(self, endereco, *args, **kwargs):
        host = endereco[0] if isinstance(endereco, tuple) else str(endereco)
        if host not in ("127.0.0.1", "::1", "localhost"):
            raise AssertionError(f"conexao externa bloqueada: {endereco!r}")
        return conectar_original(self, endereco, *args, **kwargs)

    monkeypatch.setattr(socket.socket, "connect", bloquear)


# =====================================================================
# config.py
# =====================================================================


def test_camada_2_desligada_sem_nenhuma_variavel():
    assert resolve_instagram_config(env={}) is None


@pytest.mark.parametrize("faltante", ["INSTAGRAM_CLIENT_ID", "INSTAGRAM_CLIENT_SECRET", "MCP_PUBLIC_BASE_URL"])
def test_camada_2_desligada_com_configuracao_parcial(faltante):
    env = _env()
    del env[faltante]

    assert resolve_instagram_config(env=env) is None


def test_variaveis_ausentes_lista_apenas_nomes():
    ausentes = missing_instagram_env_vars(env={"INSTAGRAM_CLIENT_ID": FAKE_CLIENT_ID})

    assert ausentes == ["INSTAGRAM_CLIENT_SECRET", "MCP_PUBLIC_BASE_URL"]
    assert FAKE_CLIENT_ID not in ausentes


def test_variaveis_ausentes_vazia_quando_tudo_configurado():
    assert missing_instagram_env_vars(env=_env()) == []


def test_variavel_vazia_conta_como_ausente():
    env = _env()
    env["INSTAGRAM_CLIENT_ID"] = ""

    assert "INSTAGRAM_CLIENT_ID" in missing_instagram_env_vars(env=env)
    assert resolve_instagram_config(env=env) is None


def test_configuracao_completa_e_resolvida():
    config = resolve_instagram_config(env=_env())

    assert config is not None
    assert config.client_id == FAKE_CLIENT_ID
    assert config.client_secret == FAKE_CLIENT_SECRET


def test_redirect_uri_e_derivado_da_base_publica():
    config = resolve_instagram_config(env=_env())

    assert config.redirect_uri == FAKE_REDIRECT_URI
    assert config.redirect_uri.endswith("/oauth/instagram/callback")


def test_barra_final_na_base_publica_nao_duplica_no_redirect_uri():
    config = resolve_instagram_config(env=_env(MCP_PUBLIC_BASE_URL=f"{FAKE_BASE_URL}/"))

    assert config.redirect_uri == FAKE_REDIRECT_URI
    assert "//oauth" not in config.redirect_uri


def test_escopos_padrao_quando_variavel_ausente():
    config = resolve_instagram_config(env=_env())

    assert config.scopes == DEFAULT_INSTAGRAM_SCOPES


def test_escopos_podem_ser_configurados():
    config = resolve_instagram_config(env=_env(INSTAGRAM_SCOPES="openid email w_member_social"))

    assert config.scopes == ("openid", "email", "w_member_social")


def test_escopos_vazios_geram_erro():
    with pytest.raises(InvalidInstagramConfigError):
        resolve_instagram_config(env=_env(INSTAGRAM_SCOPES="   "))


def test_backend_padrao_por_plataforma():
    assert default_token_store_backend("win32") == TOKEN_STORE_BACKEND_WINDOWS
    assert default_token_store_backend("linux") == TOKEN_STORE_BACKEND_MEMORY


def test_backend_pode_ser_forcado():
    config = resolve_instagram_config(env=_env(INSTAGRAM_TOKEN_STORE_BACKEND="memory"))

    assert config.token_store_backend == TOKEN_STORE_BACKEND_MEMORY


def test_backend_invalido_gera_erro():
    with pytest.raises(InvalidInstagramConfigError):
        resolve_instagram_config(env=_env(INSTAGRAM_TOKEN_STORE_BACKEND="banco-inventado"))


def test_organization_urn_ainda_nao_e_lido():
    # Documenta a decisao desta etapa: o URN da Pagina so entra nas
    # ferramentas de negocio (etapa futura), nao no OAuth.
    config = resolve_instagram_config(env=_env(INSTAGRAM_ORGANIZATION_URN="urn:li:organization:FAKE"))

    assert not hasattr(config, "organization_urn")


def test_client_secret_nao_aparece_no_repr_da_configuracao():
    config = resolve_instagram_config(env=_env())

    assert FAKE_CLIENT_SECRET not in repr(config)
    assert "***" in repr(config)


def test_config_nao_faz_chamada_de_rede(monkeypatch):
    monkeypatch.setattr(
        socket.socket,
        "connect",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("config nao deve abrir conexao")),
    )

    resolve_instagram_config(env=_env())


def test_backend_de_credencial_e_escolhido_pela_configuracao():
    config = resolve_instagram_config(env=_env(INSTAGRAM_TOKEN_STORE_BACKEND="memory"))

    assert isinstance(build_credential_backend(config), InMemoryCredentialBackend)


# =====================================================================
# InMemoryCredentialBackend
# =====================================================================


def test_backend_em_memoria_guarda_e_devolve():
    backend = InMemoryCredentialBackend()
    backend.write("alvo", "segredo-ficticio")

    assert backend.read("alvo") == "segredo-ficticio"


def test_backend_em_memoria_apaga():
    backend = InMemoryCredentialBackend()
    backend.write("alvo", "segredo-ficticio")
    backend.delete("alvo")

    assert backend.read("alvo") is None


def test_backend_em_memoria_nao_persiste_entre_instancias():
    primeiro = InMemoryCredentialBackend()
    primeiro.write("alvo", "segredo-ficticio")

    assert InMemoryCredentialBackend().read("alvo") is None


def test_backend_em_memoria_nao_expoe_conteudo_no_repr():
    backend = InMemoryCredentialBackend()
    backend.write("alvo", FAKE_ACCESS_TOKEN)

    assert FAKE_ACCESS_TOKEN not in repr(backend)


def test_backend_em_memoria_nao_escreve_em_disco(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    backend = InMemoryCredentialBackend()

    backend.write("alvo", FAKE_ACCESS_TOKEN)

    assert list(tmp_path.rglob("*")) == []


# =====================================================================
# HttpxTransport (transporte real, exercitado sem socket)
# =====================================================================
#
# httpx2.MockTransport intercepta a requisicao dentro do proprio httpx2
# e devolve uma resposta sintetica: o codigo real do HttpxTransport
# roda inteiro (montagem da requisicao, tratamento de excecao,
# conversao para HttpResponse), mas nenhum pacote sai da maquina.


def _HttpxTransportComMock(handler) -> HttpxTransport:
    """
    O HttpxTransport REAL, com o transporte interno do httpx2
    substituido por um mock. O `post` exercitado e o de producao, sem
    nenhuma reimplementacao no teste.
    """
    return HttpxTransport(httpx_transport=httpx2.MockTransport(handler))


def test_httpx_transport_devolve_status_e_texto():
    def handler(request):
        return httpx2.Response(200, text='{"access_token": "x", "expires_in": 3600}')

    resposta = _HttpxTransportComMock(handler).post(SHORT_LIVED_TOKEN_ENDPOINT, {"grant_type": "authorization_code"})

    assert resposta.status_code == 200
    assert "access_token" in resposta.text


def test_httpx_transport_envia_dados_no_corpo_nao_na_url():
    capturadas = {}

    def handler(request):
        capturadas["url"] = str(request.url)
        capturadas["corpo"] = request.content.decode()
        return httpx2.Response(200, text="{}")

    _HttpxTransportComMock(handler).post(
        SHORT_LIVED_TOKEN_ENDPOINT, {"code": FAKE_AUTHORIZATION_CODE, "client_secret": FAKE_CLIENT_SECRET}
    )

    assert FAKE_CLIENT_SECRET not in capturadas["url"]
    assert FAKE_AUTHORIZATION_CODE not in capturadas["url"]
    assert FAKE_CLIENT_SECRET in capturadas["corpo"]


def test_httpx_transport_converte_timeout_em_transport_error():
    def handler(request):
        raise httpx2.TimeoutException("simulado", request=request)

    with pytest.raises(TransportError):
        _HttpxTransportComMock(handler).post(SHORT_LIVED_TOKEN_ENDPOINT, {})


def test_httpx_transport_converte_erro_de_rede_em_transport_error():
    def handler(request):
        raise httpx2.ConnectError("simulado", request=request)

    with pytest.raises(TransportError):
        _HttpxTransportComMock(handler).post(SHORT_LIVED_TOKEN_ENDPOINT, {})


def test_httpx_transport_nao_expoe_segredo_no_erro():
    def handler(request):
        raise httpx2.ConnectError("simulado", request=request)

    with pytest.raises(TransportError) as excinfo:
        _HttpxTransportComMock(handler).post(
            SHORT_LIVED_TOKEN_ENDPOINT, {"client_secret": FAKE_CLIENT_SECRET, "code": FAKE_AUTHORIZATION_CODE}
        )

    assert FAKE_CLIENT_SECRET not in str(excinfo.value)
    assert FAKE_AUTHORIZATION_CODE not in str(excinfo.value)
    # `from None` corta o encadeamento, entao o objeto Request do
    # httpx2 (que referencia o corpo com o segredo) nao viaja junto.
    assert excinfo.value.__cause__ is None


def test_httpx_transport_nao_segue_redirecionamento():
    def handler(request):
        if request.url.host == "api.instagram.com":
            return httpx2.Response(302, headers={"location": "https://atacante.invalid/roubo"})
        raise AssertionError("o transporte nao deveria seguir o redirecionamento")

    resposta = _HttpxTransportComMock(handler).post(SHORT_LIVED_TOKEN_ENDPOINT, {"client_secret": FAKE_CLIENT_SECRET})

    assert resposta.status_code == 302


def test_httpx_transport_tem_timeout_configurado():
    assert HttpxTransport()._timeout_seconds == DEFAULT_TIMEOUT_SECONDS
    assert HttpxTransport(timeout_seconds=3.0)._timeout_seconds == 3.0


def test_httpx_transport_nao_expoe_segredo_no_repr():
    assert FAKE_CLIENT_SECRET not in repr(HttpxTransport())


# =====================================================================
# Runtime: fluxo completo em memoria
# =====================================================================


def test_url_de_autorizacao_usa_a_configuracao():
    from urllib.parse import parse_qs, urlparse

    autorizacao = _runtime().start_authorization()
    query = parse_qs(urlparse(autorizacao.url).query)

    assert query["client_id"] == [FAKE_CLIENT_ID]
    assert query["redirect_uri"] == [FAKE_REDIRECT_URI]
    assert query["scope"] == [",".join(DEFAULT_INSTAGRAM_SCOPES)]
    assert query["response_type"] == ["code"]


def test_client_secret_nunca_entra_na_url_de_autorizacao():
    autorizacao = _runtime().start_authorization()

    assert FAKE_CLIENT_SECRET not in autorizacao.url


def test_fluxo_completo_grava_o_token():
    runtime = _runtime()
    autorizacao = runtime.start_authorization()

    resultado = runtime.handle_callback(CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=autorizacao.state))

    assert resultado.outcome is CallbackOutcome.TOKEN_EXCHANGE_STARTED
    assert runtime.token_store.get_access_token() == FAKE_ACCESS_TOKEN
    assert runtime.has_valid_token() is True


def test_fluxo_completo_envia_as_credenciais_certas_ao_endpoint_de_token():
    transport = FakeHttpTransport(response=_resposta_token_valida())
    runtime = _runtime(transport=transport)
    autorizacao = runtime.start_authorization()

    runtime.handle_callback(CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=autorizacao.state))

    url, data = transport.chamadas[0]
    assert url == SHORT_LIVED_TOKEN_ENDPOINT
    assert data["grant_type"] == "authorization_code"
    assert data["code"] == FAKE_AUTHORIZATION_CODE
    assert data["client_id"] == FAKE_CLIENT_ID
    assert data["client_secret"] == FAKE_CLIENT_SECRET
    # O redirect_uri da troca precisa ser identico ao da autorizacao,
    # senao o Instagram recusa: mesma fonte (InstagramConfig).
    assert data["redirect_uri"] == FAKE_REDIRECT_URI


def test_expires_at_e_calculado_a_partir_do_relogio_do_runtime():
    clock = FakeClock(start=1000.0)
    runtime = _runtime(clock=clock)
    autorizacao = runtime.start_authorization()

    runtime.handle_callback(CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=autorizacao.state))

    assert runtime.token_store.get_token_metadata().expires_at == 1000.0 + 3600


def test_state_de_outra_autorizacao_nao_serve():
    runtime = _runtime()
    runtime.start_authorization()

    resultado = runtime.handle_callback(
        CallbackParams(code=FAKE_AUTHORIZATION_CODE, state="FAKE_STATE_NUNCA_EMITIDO")
    )

    assert resultado.outcome is CallbackOutcome.REJECTED_STATE_INVALID
    assert runtime.token_store.get_access_token() is None


def test_replay_do_mesmo_callback_e_rejeitado():
    runtime = _runtime()
    autorizacao = runtime.start_authorization()

    primeiro = runtime.handle_callback(
        CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=autorizacao.state)
    )
    segundo = runtime.handle_callback(
        CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=autorizacao.state)
    )

    assert primeiro.outcome is CallbackOutcome.TOKEN_EXCHANGE_STARTED
    assert segundo.outcome is CallbackOutcome.REJECTED_STATE_INVALID


def test_usuario_que_nega_consentimento_nao_grava_token():
    runtime = _runtime()
    autorizacao = runtime.start_authorization()

    resultado = runtime.handle_callback(
        CallbackParams(state=autorizacao.state, error="user_cancelled_login")
    )

    assert resultado.outcome is CallbackOutcome.REJECTED_OAUTH_ERROR
    assert runtime.token_store.get_access_token() is None


def test_falha_do_instagram_na_troca_nao_grava_token():
    transport = FakeHttpTransport(response=HttpResponse(status_code=401, text="{}"))
    runtime = _runtime(transport=transport)
    autorizacao = runtime.start_authorization()

    with pytest.raises(TokenExchangeError):
        runtime.handle_callback(CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=autorizacao.state))

    assert runtime.token_store.get_access_token() is None


def test_falha_de_rede_na_troca_nao_grava_token():
    transport = FakeHttpTransport(exception=TransportError("simulado"))
    runtime = _runtime(transport=transport)
    autorizacao = runtime.start_authorization()

    with pytest.raises(TransportError):
        runtime.handle_callback(CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=autorizacao.state))

    assert runtime.token_store.get_access_token() is None


def test_token_expirado_deixa_de_ser_valido():
    clock = FakeClock(start=1000.0)
    runtime = _runtime(clock=clock)
    autorizacao = runtime.start_authorization()
    runtime.handle_callback(CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=autorizacao.state))

    assert runtime.has_valid_token() is True
    clock.advance(3601)
    assert runtime.has_valid_token() is False


def test_nenhum_segredo_aparece_nos_logs_do_fluxo(capsys):
    runtime = _runtime()
    autorizacao = runtime.start_authorization()
    runtime.handle_callback(CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=autorizacao.state))

    captured = capsys.readouterr()
    for segredo in (FAKE_CLIENT_SECRET, FAKE_ACCESS_TOKEN, FAKE_AUTHORIZATION_CODE, autorizacao.state):
        assert segredo not in captured.out
        assert segredo not in captured.err


def test_nenhum_arquivo_e_criado_no_fluxo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runtime = _runtime()
    autorizacao = runtime.start_authorization()

    runtime.handle_callback(CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=autorizacao.state))

    assert list(tmp_path.rglob("*")) == []


def test_build_runtime_nao_acessa_rede_nem_credential_manager(monkeypatch):
    _bloquear_rede_externa(monkeypatch)
    config = resolve_instagram_config(env=_env(INSTAGRAM_TOKEN_STORE_BACKEND="memory"))

    runtime = build_runtime(config)

    assert isinstance(runtime.token_store._backend, InMemoryCredentialBackend)
    assert isinstance(runtime.transport, HttpxTransport)


# =====================================================================
# Ferramentas MCP
# =====================================================================


def test_ferramenta_iniciar_sem_configuracao_orienta_o_operador(runtime_injetado):
    runtime_injetado(None)

    resultado = instagram_oauth_iniciar()

    assert resultado["status"] == "nao_configurado"
    assert "url_autorizacao" not in resultado


def test_ferramenta_iniciar_devolve_a_url(runtime_injetado):
    runtime_injetado(_runtime())

    resultado = instagram_oauth_iniciar()

    assert resultado["status"] == "aguardando_autorizacao"
    assert resultado["url_autorizacao"].startswith("https://www.instagram.com/oauth/authorize?")
    assert resultado["escopos_solicitados"] == list(DEFAULT_INSTAGRAM_SCOPES)


def test_ferramenta_iniciar_nunca_devolve_o_state_isolado(runtime_injetado):
    runtime_injetado(_runtime())

    resultado = instagram_oauth_iniciar()

    assert "state" not in resultado
    assert FAKE_CLIENT_SECRET not in json.dumps(resultado)


def test_ferramenta_status_sem_configuracao(runtime_injetado):
    runtime_injetado(None)

    assert instagram_oauth_status()["status"] == "nao_configurado"


def test_ferramenta_status_antes_e_depois_de_autorizar(runtime_injetado):
    runtime = runtime_injetado(_runtime())

    assert instagram_oauth_status()["status"] == "nao_conectado"

    autorizacao = runtime.start_authorization()
    runtime.handle_callback(CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=autorizacao.state))

    assert instagram_oauth_status()["status"] == "conectado"


def test_ferramenta_status_nunca_devolve_o_token(runtime_injetado):
    runtime = runtime_injetado(_runtime())
    autorizacao = runtime.start_authorization()
    runtime.handle_callback(CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=autorizacao.state))

    assert FAKE_ACCESS_TOKEN not in json.dumps(instagram_oauth_status())


def test_ferramenta_mcp_status_reflete_a_conexao(runtime_injetado):
    runtime = runtime_injetado(_runtime())

    assert instagram_mcp_status()["oauth"] == "configurado"
    assert instagram_mcp_status()["instagram"] == "nao_conectado"

    autorizacao = runtime.start_authorization()
    runtime.handle_callback(CallbackParams(code=FAKE_AUTHORIZATION_CODE, state=autorizacao.state))

    assert instagram_mcp_status()["instagram"] == "conectado"


def test_ferramentas_estao_registradas_no_servidor():
    nomes = {ferramenta.name for ferramenta in modulo_servidor.mcp._tool_manager.list_tools()}

    assert {"instagram_mcp_status", "instagram_oauth_iniciar", "instagram_oauth_status"} <= nomes


def test_nenhuma_ferramenta_de_negocio_do_instagram_existe_ainda():
    # Etapa 7B estabelece só o OAuth: leitura e publicação ficam para
    # a etapa seguinte.
    nomes = {ferramenta.name for ferramenta in modulo_servidor.mcp._tool_manager.list_tools()}

    assert not any("publicar" in nome or "post" in nome for nome in nomes)


# =====================================================================
# Rota HTTP de callback
# =====================================================================


def test_rota_de_callback_existe():
    app = modulo_servidor.mcp.streamable_http_app()

    caminhos = [getattr(rota, "path", None) for rota in app.routes]

    assert INSTAGRAM_CALLBACK_PATH in caminhos


def test_callback_conclui_a_autorizacao(runtime_injetado):
    runtime = runtime_injetado(_runtime())
    autorizacao = runtime.start_authorization()
    app = modulo_servidor.mcp.streamable_http_app()

    with TestClient(app, base_url=_TEST_BASE_URL) as client:
        resposta = client.get(
            INSTAGRAM_CALLBACK_PATH,
            params={"code": FAKE_AUTHORIZATION_CODE, "state": autorizacao.state},
        )

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "conectado"
    assert runtime.has_valid_token() is True


def test_callback_nao_exige_autorizacao_da_camada_1(runtime_injetado):
    # O Instagram nao envia o Bearer da Camada 1; a rota precisa ser
    # publica, e o `state` de uso unico e o que a protege.
    runtime = runtime_injetado(_runtime())
    autorizacao = runtime.start_authorization()
    app = modulo_servidor.mcp.streamable_http_app()

    with TestClient(app, base_url=_TEST_BASE_URL) as client:
        # De proposito, sem nenhum header Authorization.
        resposta = client.get(
            INSTAGRAM_CALLBACK_PATH,
            params={"code": FAKE_AUTHORIZATION_CODE, "state": autorizacao.state},
        )

    assert resposta.status_code == 200


def test_callback_com_state_forjado_e_rejeitado(runtime_injetado):
    runtime = runtime_injetado(_runtime())
    app = modulo_servidor.mcp.streamable_http_app()

    with TestClient(app, base_url=_TEST_BASE_URL) as client:
        resposta = client.get(
            INSTAGRAM_CALLBACK_PATH,
            params={"code": FAKE_AUTHORIZATION_CODE, "state": "FAKE_STATE_FORJADO"},
        )

    assert resposta.status_code == 400
    assert resposta.json()["motivo"] == CallbackOutcome.REJECTED_STATE_INVALID.value
    assert runtime.token_store.get_access_token() is None


def test_callback_sem_state_e_rejeitado(runtime_injetado):
    runtime_injetado(_runtime())
    app = modulo_servidor.mcp.streamable_http_app()

    with TestClient(app, base_url=_TEST_BASE_URL) as client:
        resposta = client.get(INSTAGRAM_CALLBACK_PATH, params={"code": FAKE_AUTHORIZATION_CODE})

    assert resposta.status_code == 400
    assert resposta.json()["motivo"] == CallbackOutcome.REJECTED_STATE_MISSING.value


def test_callback_com_erro_do_instagram_e_reportado(runtime_injetado):
    runtime = runtime_injetado(_runtime())
    autorizacao = runtime.start_authorization()
    app = modulo_servidor.mcp.streamable_http_app()

    with TestClient(app, base_url=_TEST_BASE_URL) as client:
        resposta = client.get(
            INSTAGRAM_CALLBACK_PATH,
            params={
                "state": autorizacao.state,
                "error": "user_cancelled_login",
                "error_description": "o usuario cancelou",
            },
        )

    assert resposta.status_code == 400
    assert resposta.json()["erro_instagram"] == "user_cancelled_login"
    assert runtime.token_store.get_access_token() is None


def test_callback_com_falha_na_troca_responde_502(runtime_injetado):
    runtime = runtime_injetado(
        _runtime(transport=FakeHttpTransport(response=HttpResponse(status_code=401, text="{}")))
    )
    autorizacao = runtime.start_authorization()
    app = modulo_servidor.mcp.streamable_http_app()

    with TestClient(app, base_url=_TEST_BASE_URL) as client:
        resposta = client.get(
            INSTAGRAM_CALLBACK_PATH,
            params={"code": FAKE_AUTHORIZATION_CODE, "state": autorizacao.state},
        )

    assert resposta.status_code == 502
    assert resposta.json()["status"] == "erro_na_troca_de_token"
    assert runtime.token_store.get_access_token() is None


def test_callback_com_falha_de_armazenamento_responde_502(runtime_injetado):
    # Antes desta rodada, uma falha do armazenamento remoto (ponte ou
    # Supabase fora do ar) escapava do try da rota e virava um 500 com
    # traceback. Agora e tratada como as demais falhas de troca.
    from mcp_instagram.auth_instagram.token_store import TokenStoreBackendError

    class TokenStoreQueFalha:
        def save_access_token(self, access_token, expires_at, user_id=None):
            raise TokenStoreBackendError("armazenamento remoto indisponivel")

        def has_valid_token(self):
            return False

    runtime = _runtime()
    runtime = runtime_injetado(
        InstagramOAuthRuntime(
            config=runtime.config,
            state_store=runtime.state_store,
            token_store=TokenStoreQueFalha(),
            transport=runtime.transport,
            clock=runtime.clock,
        )
    )
    autorizacao = runtime.start_authorization()
    app = modulo_servidor.mcp.streamable_http_app()

    with TestClient(app, base_url=_TEST_BASE_URL) as client:
        resposta = client.get(
            INSTAGRAM_CALLBACK_PATH,
            params={"code": FAKE_AUTHORIZATION_CODE, "state": autorizacao.state},
        )

    assert resposta.status_code == 502
    assert resposta.json()["status"] == "erro_na_troca_de_token"
    assert "armazenamento remoto indisponivel" not in resposta.text


def test_callback_sem_configuracao_responde_503(runtime_injetado):
    runtime_injetado(None)
    app = modulo_servidor.mcp.streamable_http_app()

    with TestClient(app, base_url=_TEST_BASE_URL) as client:
        resposta = client.get(INSTAGRAM_CALLBACK_PATH, params={"code": "x", "state": "y"})

    assert resposta.status_code == 503


def test_callback_nunca_ecoa_code_state_nem_token(runtime_injetado):
    runtime = runtime_injetado(_runtime())
    autorizacao = runtime.start_authorization()
    app = modulo_servidor.mcp.streamable_http_app()

    with TestClient(app, base_url=_TEST_BASE_URL) as client:
        resposta_ok = client.get(
            INSTAGRAM_CALLBACK_PATH,
            params={"code": FAKE_AUTHORIZATION_CODE, "state": autorizacao.state},
        )
        resposta_rejeitada = client.get(
            INSTAGRAM_CALLBACK_PATH,
            params={"code": FAKE_AUTHORIZATION_CODE, "state": "FAKE_STATE_FORJADO"},
        )

    for resposta in (resposta_ok, resposta_rejeitada):
        for segredo in (FAKE_AUTHORIZATION_CODE, autorizacao.state, FAKE_ACCESS_TOKEN, FAKE_CLIENT_SECRET):
            assert segredo not in resposta.text


def test_callback_responde_json_e_nao_html(runtime_injetado):
    runtime = runtime_injetado(_runtime())
    autorizacao = runtime.start_authorization()
    app = modulo_servidor.mcp.streamable_http_app()

    with TestClient(app, base_url=_TEST_BASE_URL) as client:
        resposta = client.get(
            INSTAGRAM_CALLBACK_PATH,
            params={"code": FAKE_AUTHORIZATION_CODE, "state": autorizacao.state},
        )

    assert resposta.headers["content-type"].startswith("application/json")
    assert "<html" not in resposta.text.lower()


def test_fluxo_de_ponta_a_ponta_pela_ferramenta_e_pela_rota(runtime_injetado, monkeypatch):
    """
    O caminho real, do jeito que o captador vai usar: a ferramenta MCP
    devolve a URL, o Instagram (aqui, o TestClient) chama o callback com
    o state daquela URL, e o token acaba gravado. Nenhuma conexao sai
    da maquina.
    """
    from urllib.parse import parse_qs, urlparse

    _bloquear_rede_externa(monkeypatch)
    runtime = runtime_injetado(_runtime())

    inicio = instagram_oauth_iniciar()
    assert inicio["status"] == "aguardando_autorizacao"
    state = parse_qs(urlparse(inicio["url_autorizacao"]).query)["state"][0]

    assert instagram_oauth_status()["status"] == "nao_conectado"

    app = modulo_servidor.mcp.streamable_http_app()
    with TestClient(app, base_url=_TEST_BASE_URL) as client:
        resposta = client.get(
            INSTAGRAM_CALLBACK_PATH, params={"code": FAKE_AUTHORIZATION_CODE, "state": state}
        )

    assert resposta.status_code == 200
    assert instagram_oauth_status()["status"] == "conectado"
    assert instagram_mcp_status()["instagram"] == "conectado"
    assert runtime.token_store.get_access_token() == FAKE_ACCESS_TOKEN


# =====================================================================
# Integracao com o resto do servidor
# =====================================================================


def test_servidor_sobe_sem_a_camada_2_configurada():
    assert resolve_instagram_runtime(env={}) is None


def test_camada_2_desligada_nao_quebra_o_handshake_mcp(runtime_injetado):
    runtime_injetado(None)
    app = modulo_servidor.mcp.streamable_http_app()

    with TestClient(app, base_url=_TEST_BASE_URL) as client:
        resposta = client.post(
            "/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "teste-local", "version": "0.0.0"},
                },
            },
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
            },
        )

    assert resposta.status_code == 200


def test_valores_ficticios_sao_claramente_marcados():
    assert FAKE_CLIENT_ID.startswith("FAKE_")
    assert FAKE_CLIENT_SECRET.startswith("FAKE_")
    assert FAKE_ACCESS_TOKEN.startswith("FAKE_")
    assert FAKE_AUTHORIZATION_CODE.startswith("FAKE_")
    assert FAKE_BASE_URL.endswith(".invalid")
