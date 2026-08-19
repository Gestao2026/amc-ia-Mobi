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

import json

import pytest
from starlette.testclient import TestClient

from mcp_linkedin.server import (
    STREAMABLE_HTTP_HOST,
    STREAMABLE_HTTP_PATH,
    InvalidTransportConfigError,
    StdioRunConfig,
    StreamableHttpRunConfig,
    linkedin_mcp_status,
    mcp,
    resolve_run_config,
)

FAKE_LINKEDIN_CLIENT_SECRET = "FAKE_CLIENT_SECRET_NAO_REAL"


def test_linkedin_mcp_status_retorna_campos_esperados():
    resultado = linkedin_mcp_status()

    assert resultado["componente"] == "mcp-linkedin"
    assert resultado["ambiente"] == "local"
    assert resultado["linkedin"] == "nao_conectado"
    assert resultado["oauth"] == "nao_implementado"
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
    # server.py nao importa nada de auth_linkedin nem de
    # linkedin_client; o handshake HTTP nao precisa de nenhum modulo
    # relacionado ao LinkedIn.
    import mcp_linkedin.server as modulo_servidor

    assert "linkedin_client" not in modulo_servidor.__dict__
    assert "auth_linkedin" not in modulo_servidor.__dict__


def test_nenhuma_credencial_e_necessaria_para_o_handshake():
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
