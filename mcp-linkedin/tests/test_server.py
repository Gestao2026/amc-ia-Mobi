"""
Testes do mcp-linkedin: a ferramenta de teste `linkedin_mcp_status`,
a resolucao de configuracao de transporte (stdio vs streamable-http),
e a validacao real do app Streamable HTTP (Etapa 6C).

Nenhum teste aqui abre porta publica nem acessa rede externa.
`resolve_run_config` e uma funcao pura, testada com um dicionario de
ambiente fictício. Os testes de Streamable HTTP usam
`starlette.testclient.TestClient` (ja disponivel via `starlette`,
dependencia transitiva do pacote `mcp` ja instalado — nenhuma
dependencia nova), que fala com o app MCP inteiramente em processo,
via transporte ASGI, sem nunca abrir um socket real de rede.
Nenhuma chamada externa, nenhum OAuth, nenhum acesso ao LinkedIn ou
ao Claude.
"""

import base64
import hashlib
import json
import secrets
import time
import urllib.parse

import pytest
from mcp.server.auth.settings import AuthSettings, ClientRegistrationOptions, RevocationOptions
from mcp.server.mcpserver import MCPServer
from starlette.testclient import TestClient

from mcp_linkedin.auth_claude.provider import ClaudeAuthProvider
from mcp_linkedin.auth_claude.session_store import ClaudeSessionStore
from mcp_linkedin.server import (
    STREAMABLE_HTTP_HOST,
    STREAMABLE_HTTP_PATH,
    InvalidTransportConfigError,
    StdioRunConfig,
    StreamableHttpRunConfig,
    apply_claude_auth_config,
    linkedin_mcp_status,
    mcp,
    resolve_claude_auth_config,
    resolve_run_config,
)

FAKE_LINKEDIN_CLIENT_SECRET = "FAKE_CLIENT_SECRET_NAO_REAL"


def test_linkedin_mcp_status_retorna_campos_esperados(monkeypatch):
    # Sem as variaveis da Camada 2 no ambiente, o status reporta
    # "nao_configurado" e lista o que falta, sem expor valor nenhum.
    # A partir da Etapa 7B estes campos deixaram de ser estaticos: ver
    # test_linkedin.py para o cenario com a Camada 2 ligada.
    monkeypatch.setattr("mcp_linkedin.server._linkedin_runtime", None)

    resultado = linkedin_mcp_status()

    assert resultado["componente"] == "mcp-linkedin"
    assert resultado["linkedin"] == "nao_conectado"
    assert resultado["oauth"] == "nao_configurado"
    assert resultado["status"] == "operacional"


# --- resolucao de transporte ---


def test_transporte_stdio_e_o_padrao_sem_env():
    config = resolve_run_config(env={})

    assert isinstance(config, StdioRunConfig)
    assert config.transport == "stdio"


def test_transporte_stdio_continua_disponivel_explicitamente():
    config = resolve_run_config(env={"MCP_TRANSPORT": "stdio"})

    assert isinstance(config, StdioRunConfig)


def test_transporte_streamable_http_e_reconhecido():
    config = resolve_run_config(env={"MCP_TRANSPORT": "streamable-http", "PORT": "8080"})

    assert isinstance(config, StreamableHttpRunConfig)
    assert config.transport == "streamable-http"


def test_host_de_producao_e_0_0_0_0():
    config = resolve_run_config(env={"MCP_TRANSPORT": "streamable-http", "PORT": "8080"})

    assert config.host == "0.0.0.0"
    assert config.host == STREAMABLE_HTTP_HOST


def test_porta_vem_da_configuracao_nao_e_fixa_no_codigo():
    config_a = resolve_run_config(env={"MCP_TRANSPORT": "streamable-http", "PORT": "8080"})
    config_b = resolve_run_config(env={"MCP_TRANSPORT": "streamable-http", "PORT": "3000"})

    assert config_a.port == 8080
    assert config_b.port == 3000
    assert config_a.port != config_b.port


def test_path_e_barra_mcp():
    config = resolve_run_config(env={"MCP_TRANSPORT": "streamable-http", "PORT": "8080"})

    assert config.streamable_http_path == "/mcp"
    assert config.streamable_http_path == STREAMABLE_HTTP_PATH


# --- configuracao invalida ---


def test_mcp_transport_desconhecido_gera_erro():
    with pytest.raises(InvalidTransportConfigError):
        resolve_run_config(env={"MCP_TRANSPORT": "websocket-inventado"})


def test_streamable_http_sem_port_gera_erro():
    with pytest.raises(InvalidTransportConfigError):
        resolve_run_config(env={"MCP_TRANSPORT": "streamable-http"})


def test_port_nao_numerica_gera_erro():
    with pytest.raises(InvalidTransportConfigError):
        resolve_run_config(env={"MCP_TRANSPORT": "streamable-http", "PORT": "nao-e-numero"})


def test_port_fora_do_intervalo_valido_gera_erro():
    with pytest.raises(InvalidTransportConfigError):
        resolve_run_config(env={"MCP_TRANSPORT": "streamable-http", "PORT": "0"})

    with pytest.raises(InvalidTransportConfigError):
        resolve_run_config(env={"MCP_TRANSPORT": "streamable-http", "PORT": "70000"})


# --- seguranca ---


def test_nenhum_segredo_aparece_na_mensagem_de_erro():
    env_com_segredo_irrelevante = {
        "MCP_TRANSPORT": "streamable-http",
        "PORT": "nao-e-numero",
        "LINKEDIN_CLIENT_SECRET": FAKE_LINKEDIN_CLIENT_SECRET,
    }

    with pytest.raises(InvalidTransportConfigError) as excinfo:
        resolve_run_config(env=env_com_segredo_irrelevante)

    assert FAKE_LINKEDIN_CLIENT_SECRET not in str(excinfo.value)


def test_resolve_run_config_nao_le_variaveis_de_segredo():
    # resolve_run_config so deve olhar MCP_TRANSPORT e PORT; um
    # ambiente com um "segredo" fictício presente nao deve influenciar
    # o resultado nem vazar para a configuracao devolvida.
    env = {
        "MCP_TRANSPORT": "streamable-http",
        "PORT": "8080",
        "LINKEDIN_CLIENT_SECRET": FAKE_LINKEDIN_CLIENT_SECRET,
    }

    config = resolve_run_config(env=env)

    assert FAKE_LINKEDIN_CLIENT_SECRET not in repr(config)


def test_resolve_run_config_nao_faz_chamada_de_rede(monkeypatch):
    import socket

    def bloquear_rede(*args, **kwargs):
        raise AssertionError("resolve_run_config nao deve abrir conexao de rede")

    monkeypatch.setattr(socket.socket, "connect", bloquear_rede)

    resolve_run_config(env={"MCP_TRANSPORT": "streamable-http", "PORT": "8080"})
    resolve_run_config(env={"MCP_TRANSPORT": "stdio"})


# =====================================================================
# Streamable HTTP real, em processo (Etapa 6C)
# =====================================================================
#
# Validam que MCPServer -> streamable-http -> /mcp de fato funciona,
# sem Docker, sem Fly.io, sem porta publica. TestClient fala com o
# app MCP via transporte ASGI em processo (nao abre socket real); o
# base_url usa 127.0.0.1:8080 para satisfazer a protecao anti DNS
# rebinding que o proprio SDK habilita automaticamente para hosts
# locais.

_MCP_TEST_BASE_URL = "http://127.0.0.1:8080"


def _mcp_initialize_payload() -> dict:
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "teste-local", "version": "0.0.0"},
        },
    }


def _parse_sse_data(texto_sse: str) -> dict:
    """Extrai o JSON da linha 'data: ...' de uma resposta SSE do MCP."""
    for linha in texto_sse.splitlines():
        if linha.startswith("data: "):
            return json.loads(linha[len("data: ") :])
    raise AssertionError(f"nenhuma linha 'data:' na resposta SSE: {texto_sse!r}")


def test_streamable_http_app_pode_ser_criado():
    app = mcp.streamable_http_app()

    assert app is not None


def test_endpoint_mcp_existe():
    app = mcp.streamable_http_app()

    caminhos = [getattr(rota, "path", None) for rota in app.routes]

    assert "/mcp" in caminhos


def test_requisicao_ao_mcp_recebe_resposta_http_valida_do_servidor():
    app = mcp.streamable_http_app()

    with TestClient(app, base_url=_MCP_TEST_BASE_URL) as client:
        resposta = client.post(
            "/mcp",
            json=_mcp_initialize_payload(),
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
            },
        )

    assert resposta.status_code == 200
    assert "mcp-session-id" in resposta.headers

    corpo = _parse_sse_data(resposta.text)
    assert corpo["jsonrpc"] == "2.0"
    assert corpo["result"]["serverInfo"]["name"] == "mcp-linkedin"


def test_servidor_nao_depende_do_linkedin():
    # A partir da Etapa 7B, server.py PASSA a importar auth_linkedin
    # (a Camada 2 vive nele). O que continua valendo, e e o que este
    # teste protege, e que nada disso e necessario para o servidor
    # funcionar: sem as variaveis do LinkedIn no ambiente, o runtime
    # resolve para None e o handshake HTTP segue normal. Nenhuma
    # ferramenta de negocio do LinkedIn (linkedin_client) existe ainda.
    import mcp_linkedin.server as modulo_servidor

    assert "linkedin_client" not in modulo_servidor.__dict__
    assert modulo_servidor.resolve_linkedin_runtime(env={}) is None


def test_nenhuma_credencial_e_necessaria_para_o_handshake():
    # Documenta o cenario SEM a Camada 1 configurada: o `mcp` deste
    # modulo nunca tem auth_server_provider/token_verifier atribuidos
    # durante os testes (isso so acontece dentro de main(), nunca
    # chamado aqui), entao o handshake continua livre -- exatamente
    # o que aconteceria em producao se MCP_CLAUDE_CLIENT_ID ou
    # MCP_PUBLIC_BASE_URL nao estivessem definidas. Ver
    # test_mcp_sem_bearer_recebe_401_quando_camada_1_configurada para
    # o cenario oposto, com a Camada 1 (Etapa 7A) ligada.
    app = mcp.streamable_http_app()

    with TestClient(app, base_url=_MCP_TEST_BASE_URL) as client:
        # De proposito, sem nenhum header Authorization/Bearer.
        resposta = client.post(
            "/mcp",
            json=_mcp_initialize_payload(),
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
            },
        )

    assert resposta.status_code == 200


def test_nenhuma_chamada_de_rede_externa_ocorre_no_handshake(monkeypatch):
    import socket

    conectar_original = socket.socket.connect

    def bloquear_rede_externa(self, endereco, *args, **kwargs):
        host = endereco[0] if isinstance(endereco, tuple) else str(endereco)
        if host not in ("127.0.0.1", "::1", "localhost"):
            raise AssertionError(f"conexao externa bloqueada: {endereco!r}")
        return conectar_original(self, endereco, *args, **kwargs)

    monkeypatch.setattr(socket.socket, "connect", bloquear_rede_externa)

    app = mcp.streamable_http_app()
    with TestClient(app, base_url=_MCP_TEST_BASE_URL) as client:
        resposta = client.post(
            "/mcp",
            json=_mcp_initialize_payload(),
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
            },
        )

    assert resposta.status_code == 200


def test_nenhum_arquivo_e_criado_durante_o_handshake(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    app = mcp.streamable_http_app()
    with TestClient(app, base_url=_MCP_TEST_BASE_URL) as client:
        client.post(
            "/mcp",
            json=_mcp_initialize_payload(),
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
            },
        )

    assert list(tmp_path.rglob("*")) == []


# =====================================================================
# OAuth Claude <-> mcp-linkedin, Camada 1 (Etapa 7A)
# =====================================================================
#
# Estes testes constroem um MCPServer PROPRIO, separado do `mcp`
# compartilhado pelos testes acima, com a Camada 1 ja configurada na
# construcao. Isso evita mutar o `mcp` do modulo (essa mutacao so
# acontece dentro de main(), nunca chamada durante os testes) e
# mantem os testes acima (sem Camada 1) e estes (com Camada 1)
# totalmente isolados um do outro.
#
# Nenhum destes testes acessa o LinkedIn ou o Claude.ai de verdade.
# client_id/secret/state sao sempre ficticios (prefixo FAKE_). O PKCE
# usado e criptograficamente real (par verifier/challenge gerado de
# verdade), exercitando a validacao S256 do proprio SDK, nao uma
# simulacao.

FAKE_CLAUDE_CLIENT_ID = "FAKE_CLAUDE_CLIENT_ID_NAO_REAL"
FAKE_CLAUDE_CLIENT_SECRET = "FAKE_CLAUDE_CLIENT_SECRET_NAO_REAL"
FAKE_ISSUER_URL = "https://mcp-test.invalid"
FAKE_CLAUDE_STATE = "FAKE_STATE_NAO_REAL"

# Confirmado por inspecao/teste manual na Etapa 7A: quando o resource
# server nao esta na raiz (resource_server_url = "<issuer>/mcp"), o
# SDK publica os metadados RFC 9728 sob um path com o mesmo sufixo.
PROTECTED_RESOURCE_METADATA_PATH = "/.well-known/oauth-protected-resource/mcp"
AUTHORIZATION_SERVER_METADATA_PATH = "/.well-known/oauth-authorization-server"


def _pkce_pair():
    """Par verifier/challenge PKCE S256 real, nao uma simulacao."""
    verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).decode().rstrip("=")
    return verifier, challenge


def _build_auth_app(clock=None):
    """
    Monta um MCPServer isolado, so para estes testes, com a Camada 1
    ja configurada na construcao (client estatico ficticio, sem DCR,
    sem revogacao).
    """
    store = ClaudeSessionStore(clock=clock) if clock else ClaudeSessionStore()
    provider = ClaudeAuthProvider(
        client_id=FAKE_CLAUDE_CLIENT_ID, client_secret=None, store=store
    )
    auth_settings = AuthSettings(
        issuer_url=FAKE_ISSUER_URL,
        resource_server_url=f"{FAKE_ISSUER_URL}{STREAMABLE_HTTP_PATH}",
        client_registration_options=ClientRegistrationOptions(enabled=False),
        revocation_options=RevocationOptions(enabled=False),
    )
    # auth_server_provider e token_verifier sao mutuamente exclusivos
    # no construtor do MCPServer; passando so o provider, o SDK cria
    # o ProviderTokenVerifier correspondente automaticamente.
    servidor = MCPServer(
        "mcp-linkedin-teste-camada-1",
        auth_server_provider=provider,
        auth=auth_settings,
    )

    @servidor.tool()
    def dummy_tool() -> dict:
        return {"ok": True}

    return servidor.streamable_http_app()


def _authorize_params(challenge: str, state: str = FAKE_CLAUDE_STATE) -> dict:
    return {
        "response_type": "code",
        "client_id": FAKE_CLAUDE_CLIENT_ID,
        "redirect_uri": "https://claude.ai/api/mcp/auth_callback",
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "state": state,
    }


def _extract_code_from_redirect(location: str) -> str:
    query = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(location).query))
    return query["code"]


def test_resolve_claude_auth_config_desabilitado_sem_env():
    assert resolve_claude_auth_config(env={}) is None


def test_resolve_claude_auth_config_desabilitado_so_com_client_id():
    config = resolve_claude_auth_config(env={"MCP_CLAUDE_CLIENT_ID": FAKE_CLAUDE_CLIENT_ID})

    assert config is None


def test_resolve_claude_auth_config_habilitado_com_client_id_e_base_url():
    config = resolve_claude_auth_config(
        env={
            "MCP_CLAUDE_CLIENT_ID": FAKE_CLAUDE_CLIENT_ID,
            "MCP_PUBLIC_BASE_URL": FAKE_ISSUER_URL,
        }
    )

    assert config is not None
    assert str(config.auth_settings.issuer_url).rstrip("/") == FAKE_ISSUER_URL
    assert str(config.auth_settings.resource_server_url) == f"{FAKE_ISSUER_URL}{STREAMABLE_HTTP_PATH}"
    assert config.auth_settings.client_registration_options.enabled is False
    assert config.auth_settings.revocation_options.enabled is False


def test_mcp_sem_bearer_recebe_401_quando_camada_1_configurada():
    app = _build_auth_app()

    with TestClient(app, base_url=_MCP_TEST_BASE_URL) as client:
        resposta = client.post(
            "/mcp",
            json=_mcp_initialize_payload(),
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
            },
        )

    assert resposta.status_code == 401
    assert "WWW-Authenticate" in resposta.headers
    assert "resource_metadata=" in resposta.headers["WWW-Authenticate"]


def test_well_known_protected_resource_existe():
    app = _build_auth_app()

    with TestClient(app, base_url=_MCP_TEST_BASE_URL) as client:
        resposta = client.get(PROTECTED_RESOURCE_METADATA_PATH)

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["resource"] == f"{FAKE_ISSUER_URL}{STREAMABLE_HTTP_PATH}"
    assert corpo["authorization_servers"] == [FAKE_ISSUER_URL]


def test_well_known_authorization_server_existe_e_sem_registration_endpoint():
    app = _build_auth_app()

    with TestClient(app, base_url=_MCP_TEST_BASE_URL) as client:
        resposta = client.get(AUTHORIZATION_SERVER_METADATA_PATH)

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["issuer"] == FAKE_ISSUER_URL
    assert corpo["authorization_endpoint"].endswith("/authorize")
    assert corpo["token_endpoint"].endswith("/token")
    # DCR desligado (decisao da Etapa 7A): sem registration_endpoint.
    assert corpo.get("registration_endpoint") is None


def test_dcr_register_endpoint_nao_existe():
    app = _build_auth_app()

    with TestClient(app, base_url=_MCP_TEST_BASE_URL) as client:
        resposta = client.post("/register", json={})

    assert resposta.status_code == 404


def test_revoke_endpoint_nao_existe():
    app = _build_auth_app()

    with TestClient(app, base_url=_MCP_TEST_BASE_URL) as client:
        resposta = client.post("/revoke", data={"token": "qualquer"})

    assert resposta.status_code == 404


def test_fluxo_completo_authorize_token_e_chamada_autenticada():
    app = _build_auth_app()
    verifier, challenge = _pkce_pair()

    with TestClient(app, base_url=_MCP_TEST_BASE_URL) as client:
        resposta_authorize = client.get(
            "/authorize", params=_authorize_params(challenge), follow_redirects=False
        )
        assert resposta_authorize.status_code == 302
        location = resposta_authorize.headers["location"]
        assert location.startswith("https://claude.ai/api/mcp/auth_callback")

        query = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(location).query))
        assert query["state"] == FAKE_CLAUDE_STATE
        code = query["code"]

        resposta_token = client.post(
            "/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": "https://claude.ai/api/mcp/auth_callback",
                "client_id": FAKE_CLAUDE_CLIENT_ID,
                "code_verifier": verifier,
            },
        )
        assert resposta_token.status_code == 200
        token_body = resposta_token.json()
        assert token_body["token_type"] == "Bearer"
        access_token = token_body["access_token"]
        refresh_token = token_body["refresh_token"]

        resposta_mcp = client.post(
            "/mcp",
            json=_mcp_initialize_payload(),
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )
        assert resposta_mcp.status_code == 200

        resposta_refresh = client.post(
            "/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": FAKE_CLAUDE_CLIENT_ID,
            },
        )
        assert resposta_refresh.status_code == 200
        assert resposta_refresh.json()["access_token"] != access_token


def test_pkce_invalido_e_rejeitado_no_token():
    app = _build_auth_app()
    _, challenge = _pkce_pair()
    verifier_errado = "FAKE_VERIFIER_ERRADO_NAO_CONFERE_COM_O_CHALLENGE"

    with TestClient(app, base_url=_MCP_TEST_BASE_URL) as client:
        resposta_authorize = client.get(
            "/authorize", params=_authorize_params(challenge), follow_redirects=False
        )
        code = _extract_code_from_redirect(resposta_authorize.headers["location"])

        resposta_token = client.post(
            "/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": "https://claude.ai/api/mcp/auth_callback",
                "client_id": FAKE_CLAUDE_CLIENT_ID,
                "code_verifier": verifier_errado,
            },
        )

    assert resposta_token.status_code == 400
    assert resposta_token.json()["error"] == "invalid_grant"


def test_token_invalido_recebe_401_no_mcp():
    app = _build_auth_app()

    with TestClient(app, base_url=_MCP_TEST_BASE_URL) as client:
        resposta = client.post(
            "/mcp",
            json=_mcp_initialize_payload(),
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
                "Authorization": "Bearer FAKE_ACCESS_TOKEN_INVALIDO_NAO_REAL",
            },
        )

    assert resposta.status_code == 401


def test_token_expirado_recebe_401_no_mcp():
    # O TokenHandler do proprio SDK tambem valida AuthorizationCode.expires_at
    # contra o relogio real (confirmado por teste manual na Etapa 7A) -- por
    # isso o FakeClock aqui comeca em time.time() real, nao num valor
    # arbitrario, e so avanca para expirar o ACCESS TOKEN (que so o nosso
    # provider confere), nao o authorization code (ja consumido antes disso).
    class FakeClock:
        def __init__(self, start: float | None = None):
            self._now = start if start is not None else time.time()

        def __call__(self) -> float:
            return self._now

        def advance(self, seconds: float) -> None:
            self._now += seconds

    clock = FakeClock()
    app = _build_auth_app(clock=clock)
    verifier, challenge = _pkce_pair()

    with TestClient(app, base_url=_MCP_TEST_BASE_URL) as client:
        resposta_authorize = client.get(
            "/authorize", params=_authorize_params(challenge), follow_redirects=False
        )
        code = _extract_code_from_redirect(resposta_authorize.headers["location"])

        resposta_token = client.post(
            "/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": "https://claude.ai/api/mcp/auth_callback",
                "client_id": FAKE_CLAUDE_CLIENT_ID,
                "code_verifier": verifier,
            },
        )
        access_token = resposta_token.json()["access_token"]

        clock.advance(3601)  # ACCESS_TOKEN_TTL_SECONDS + 1

        resposta_mcp = client.post(
            "/mcp",
            json=_mcp_initialize_payload(),
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )

    assert resposta_mcp.status_code == 401


def test_nenhum_segredo_aparece_nos_logs_do_fluxo_oauth_completo(capsys):
    app = _build_auth_app()
    verifier, challenge = _pkce_pair()

    with TestClient(app, base_url=_MCP_TEST_BASE_URL) as client:
        resposta_authorize = client.get(
            "/authorize", params=_authorize_params(challenge), follow_redirects=False
        )
        code = _extract_code_from_redirect(resposta_authorize.headers["location"])

        resposta_token = client.post(
            "/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": "https://claude.ai/api/mcp/auth_callback",
                "client_id": FAKE_CLAUDE_CLIENT_ID,
                "code_verifier": verifier,
            },
        )
        token_body = resposta_token.json()

    captured = capsys.readouterr()
    assert code not in captured.out
    assert token_body["access_token"] not in captured.out
    assert token_body["refresh_token"] not in captured.out
    assert code not in captured.err
    assert token_body["access_token"] not in captured.err
    assert token_body["refresh_token"] not in captured.err


def test_nenhuma_chamada_de_rede_no_fluxo_oauth_completo(monkeypatch):
    import socket

    conectar_original = socket.socket.connect

    def bloquear_rede_externa(self, endereco, *args, **kwargs):
        host = endereco[0] if isinstance(endereco, tuple) else str(endereco)
        if host not in ("127.0.0.1", "::1", "localhost"):
            raise AssertionError(f"conexao externa bloqueada: {endereco!r}")
        return conectar_original(self, endereco, *args, **kwargs)

    monkeypatch.setattr(socket.socket, "connect", bloquear_rede_externa)

    app = _build_auth_app()
    verifier, challenge = _pkce_pair()

    with TestClient(app, base_url=_MCP_TEST_BASE_URL) as client:
        resposta_authorize = client.get(
            "/authorize", params=_authorize_params(challenge), follow_redirects=False
        )
        code = _extract_code_from_redirect(resposta_authorize.headers["location"])

        resposta_token = client.post(
            "/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": "https://claude.ai/api/mcp/auth_callback",
                "client_id": FAKE_CLAUDE_CLIENT_ID,
                "code_verifier": verifier,
            },
        )
        access_token = resposta_token.json()["access_token"]

        resposta_mcp = client.post(
            "/mcp",
            json=_mcp_initialize_payload(),
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )

    assert resposta_mcp.status_code == 200


# =====================================================================
# Caminho real de producao: main() sem chamar mcp.run() (Etapa 7A,
# validacao final antes do commit)
# =====================================================================
#
# Os testes acima constroem um MCPServer PROPRIO (`_build_auth_app`),
# separado do `mcp` do modulo -- bom para isolamento, mas nao prova
# que resolve_run_config() + resolve_claude_auth_config() +
# apply_claude_auth_config() encadeados exatamente como em main()
# realmente autenticam o `mcp` de producao. Este teste exercita esse
# caminho, literal e completo, sem nunca chamar mcp.run() (que abriria
# uma porta real): mesma resolucao de variaveis de ambiente (via
# monkeypatch.setenv, lidas de os.environ de verdade, nao um dict
# passado por parametro), mesmo objeto `mcp`, mesma funcao
# apply_claude_auth_config() que main() usa.
#
# Como `mcp` e compartilhado por TODOS os testes deste arquivo, o
# fixture abaixo restaura seu estado de autenticacao original (None)
# depois do teste, para nao vazar configuracao entre testes.


@pytest.fixture
def _mcp_auth_state_restaurado():
    provider_original = mcp._auth_server_provider
    verifier_original = mcp._token_verifier
    auth_original = mcp.settings.auth
    yield
    mcp._auth_server_provider = provider_original
    mcp._token_verifier = verifier_original
    mcp.settings.auth = auth_original


def test_caminho_real_de_producao_resulta_em_app_autenticado(monkeypatch, _mcp_auth_state_restaurado):
    # Bloqueia qualquer conexao que nao seja loopback (loopback e
    # necessario para o event loop do asyncio no Windows, sem relacao
    # com rede externa -- mesma ressalva das demais Etapas).
    import socket

    conectar_original = socket.socket.connect

    def bloquear_rede_externa(self, endereco, *args, **kwargs):
        host = endereco[0] if isinstance(endereco, tuple) else str(endereco)
        if host not in ("127.0.0.1", "::1", "localhost"):
            raise AssertionError(f"conexao externa bloqueada: {endereco!r}")
        return conectar_original(self, endereco, *args, **kwargs)

    monkeypatch.setattr(socket.socket, "connect", bloquear_rede_externa)

    # As mesmas variaveis de ambiente que o Render teria em producao,
    # com valores ficticios. monkeypatch.setenv edita os.environ de
    # verdade (com undo automatico ao final do teste) -- entao
    # resolve_run_config()/resolve_claude_auth_config(), chamadas SEM
    # o parametro env (exatamente como main() chama), leem estes
    # valores de verdade, nao um dict passado por fora.
    monkeypatch.setenv("MCP_TRANSPORT", "streamable-http")
    monkeypatch.setenv("PORT", "10000")
    monkeypatch.setenv("MCP_PUBLIC_BASE_URL", "https://mcp-linkedin-run7.onrender.com")
    monkeypatch.setenv("MCP_CLAUDE_CLIENT_ID", "FAKE_CLAUDE_CLIENT_ID")
    monkeypatch.setenv("MCP_CLAUDE_CLIENT_SECRET", "FAKE_CLAUDE_CLIENT_SECRET")

    # --- exatamente a sequencia de main(), sem chamar mcp.run() ---
    config = resolve_run_config()
    assert isinstance(config, StreamableHttpRunConfig)

    auth_config = resolve_claude_auth_config()
    assert auth_config is not None

    apply_claude_auth_config(mcp, auth_config)

    app = mcp.streamable_http_app()
    # ----------------------------------------------------------------

    client_id = "FAKE_CLAUDE_CLIENT_ID"
    client_secret = "FAKE_CLAUDE_CLIENT_SECRET"
    redirect_uri = "https://claude.ai/api/mcp/auth_callback"
    verifier, challenge = _pkce_pair()

    with TestClient(app, base_url=_MCP_TEST_BASE_URL) as client:
        # 1) /mcp sem Bearer -> 401 com WWW-Authenticate
        resposta_sem_bearer = client.post(
            "/mcp",
            json=_mcp_initialize_payload(),
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
            },
        )
        assert resposta_sem_bearer.status_code == 401
        assert "WWW-Authenticate" in resposta_sem_bearer.headers

        # 2) os dois .well-known
        resposta_as = client.get(AUTHORIZATION_SERVER_METADATA_PATH)
        assert resposta_as.status_code == 200
        assert resposta_as.json()["issuer"] == "https://mcp-linkedin-run7.onrender.com"

        resposta_pr = client.get(PROTECTED_RESOURCE_METADATA_PATH)
        assert resposta_pr.status_code == 200
        assert resposta_pr.json()["resource"] == "https://mcp-linkedin-run7.onrender.com/mcp"

        # 3) DCR e revogacao desligados
        assert client.post("/register", json={}).status_code == 404
        assert client.post("/revoke", data={"token": "qualquer"}).status_code == 404

        # 4) fluxo completo: authorize -> token -> /mcp autenticado -> refresh
        resposta_authorize = client.get(
            "/authorize",
            params={
                "response_type": "code",
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "code_challenge": challenge,
                "code_challenge_method": "S256",
                "state": "FAKE_STATE_CAMINHO_REAL",
            },
            follow_redirects=False,
        )
        assert resposta_authorize.status_code == 302
        code = _extract_code_from_redirect(resposta_authorize.headers["location"])

        resposta_token = client.post(
            "/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": client_id,
                "client_secret": client_secret,
                "code_verifier": verifier,
            },
        )
        assert resposta_token.status_code == 200
        token_body = resposta_token.json()
        access_token = token_body["access_token"]
        refresh_token = token_body["refresh_token"]

        resposta_mcp_autenticado = client.post(
            "/mcp",
            json=_mcp_initialize_payload(),
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
        )
        assert resposta_mcp_autenticado.status_code == 200

        resposta_refresh = client.post(
            "/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": client_id,
                "client_secret": client_secret,
            },
        )
        assert resposta_refresh.status_code == 200
        assert resposta_refresh.json()["access_token"] != access_token

        # 5) PKCE invalido e rejeitado
        resposta_authorize_2 = client.get(
            "/authorize",
            params={
                "response_type": "code",
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "code_challenge": challenge,
                "code_challenge_method": "S256",
                "state": "FAKE_STATE_CAMINHO_REAL_2",
            },
            follow_redirects=False,
        )
        code_2 = _extract_code_from_redirect(resposta_authorize_2.headers["location"])

        resposta_pkce_invalido = client.post(
            "/token",
            data={
                "grant_type": "authorization_code",
                "code": code_2,
                "redirect_uri": redirect_uri,
                "client_id": client_id,
                "client_secret": client_secret,
                "code_verifier": "FAKE_VERIFIER_ERRADO_NAO_CONFERE_COM_O_CHALLENGE",
            },
        )
        assert resposta_pkce_invalido.status_code == 400
        assert resposta_pkce_invalido.json()["error"] == "invalid_grant"

    # nenhum segredo real usado: so os valores FAKE_ definidos acima
    assert "FAKE_CLAUDE_CLIENT_SECRET" == client_secret
