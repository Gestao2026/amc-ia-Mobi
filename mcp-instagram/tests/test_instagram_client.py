"""
Testes do cliente de leitura do Instagram (pacote `instagram_client`).

Nenhum teste aqui acessa a rede. O transporte real (`TransporteGraphHttpx`)
é exercitado de ponta a ponta com `httpx2.MockTransport`, no mesmo padrão
dos testes da Camada 2: os próprios métodos rodam, mas nenhum pacote sai
da máquina.
"""

from __future__ import annotations

import json

import httpx2
import pytest

from mcp_instagram.instagram_client.leitura import (
    BASE_GRAPH,
    JANELA_DIAS_MAXIMA,
    LIMITE_PUBLICACOES_MAXIMO,
    VERSAO_API_PADRAO,
    ClienteLeituraInstagram,
    ErroDaApi,
    SemAutorizacaoError,
    _interpretar,
    _limitar,
)
from mcp_instagram.instagram_client.transporte import (
    ErroDeTransporte,
    RespostaGraph,
    TransporteGraphHttpx,
)

TOKEN_FALSO = "token-de-teste-nao-e-real"


class TransporteEspiao:
    """Transporte falso que grava a chamada recebida e devolve o que foi programado."""

    def __init__(self, resposta: RespostaGraph) -> None:
        self.resposta = resposta
        self.chamadas: list[tuple[str, dict, str]] = []

    def get(self, url: str, params: dict, token: str) -> RespostaGraph:
        self.chamadas.append((url, params, token))
        return self.resposta


def resposta_ok(corpo: dict) -> RespostaGraph:
    return RespostaGraph(status_code=200, text=json.dumps(corpo))


def montar_cliente(resposta: RespostaGraph, token: str | None = TOKEN_FALSO, relogio=None):
    transporte = TransporteEspiao(resposta)
    cliente = ClienteLeituraInstagram(
        transporte=transporte,
        obter_token=lambda: token,
        relogio=relogio or (lambda: 1_700_000_000.0),
    )
    return cliente, transporte


# =====================================================================
# Interpretação da resposta
# =====================================================================


def test_interpretar_devolve_o_corpo_quando_a_resposta_e_valida():
    assert _interpretar(resposta_ok({"id": "123"})) == {"id": "123"}


def test_interpretar_repassa_a_mensagem_de_erro_da_meta():
    corpo = {
        "error": {
            "message": "Metrica indisponivel para este tipo de conta.",
            "type": "OAuthException",
            "code": 100,
        }
    }
    resposta = RespostaGraph(status_code=400, text=json.dumps(corpo))

    with pytest.raises(ErroDaApi) as capturado:
        _interpretar(resposta)

    erro = capturado.value
    assert erro.mensagem == "Metrica indisponivel para este tipo de conta."
    assert erro.tipo == "OAuthException"
    assert erro.codigo == 100
    assert erro.status_http == 400


def test_interpretar_reconhece_erro_mesmo_com_status_200():
    # A Graph API as vezes devolve 200 com corpo de erro.
    corpo = {"error": {"message": "Permissao ausente.", "code": 10}}

    with pytest.raises(ErroDaApi) as capturado:
        _interpretar(RespostaGraph(status_code=200, text=json.dumps(corpo)))

    assert capturado.value.mensagem == "Permissao ausente."


def test_interpretar_falha_com_corpo_que_nao_e_json():
    with pytest.raises(ErroDaApi) as capturado:
        _interpretar(RespostaGraph(status_code=502, text="<html>erro</html>"))

    assert "JSON" in capturado.value.mensagem
    assert capturado.value.status_http == 502


def test_interpretar_falha_com_json_que_nao_e_objeto():
    with pytest.raises(ErroDaApi):
        _interpretar(RespostaGraph(status_code=200, text="[1, 2, 3]"))


def test_interpretar_falha_em_status_de_erro_sem_corpo_de_erro():
    with pytest.raises(ErroDaApi) as capturado:
        _interpretar(RespostaGraph(status_code=500, text="{}"))

    assert capturado.value.status_http == 500


# =====================================================================
# Faixa de valores
# =====================================================================


@pytest.mark.parametrize(
    "entrada,esperado",
    [(0, 1), (1, 1), (7, 7), (50, 50), (999, 50), (-3, 1), ("8", 8), ("abc", 1), (None, 1)],
)
def test_limitar_mantem_o_valor_na_faixa(entrada, esperado):
    assert _limitar(entrada, 1, 50) == esperado


# =====================================================================
# Leituras
# =====================================================================


def test_perfil_monta_a_url_e_os_campos_certos():
    cliente, transporte = montar_cliente(resposta_ok({"username": "mobilizando"}))

    resultado = cliente.perfil()

    url, params, token = transporte.chamadas[0]
    assert url == f"{BASE_GRAPH}/{VERSAO_API_PADRAO}/me"
    assert "followers_count" in params["fields"]
    assert "media_count" in params["fields"]
    assert token == TOKEN_FALSO
    assert resultado == {"username": "mobilizando"}


def test_publicacoes_pede_engajamento_junto_da_listagem():
    cliente, transporte = montar_cliente(resposta_ok({"data": []}))

    cliente.publicacoes(limite=5)

    url, params, _ = transporte.chamadas[0]
    assert url.endswith("/me/media")
    assert params["limit"] == 5
    assert "like_count" in params["fields"]
    assert "comments_count" in params["fields"]
    assert "permalink" in params["fields"]


def test_publicacoes_limita_o_pedido_ao_teto_da_meta():
    cliente, transporte = montar_cliente(resposta_ok({"data": []}))

    cliente.publicacoes(limite=5000)

    _, params, _ = transporte.chamadas[0]
    assert params["limit"] == LIMITE_PUBLICACOES_MAXIMO


def test_metricas_publicacao_usa_o_id_no_caminho():
    cliente, transporte = montar_cliente(resposta_ok({"data": []}))

    cliente.metricas_publicacao("17895695668004550")

    url, params, _ = transporte.chamadas[0]
    assert url.endswith("/17895695668004550/insights")
    assert "reach" in params["metric"]


def test_metricas_conta_calcula_a_janela_pedida():
    agora = 1_700_000_000.0
    cliente, transporte = montar_cliente(resposta_ok({"data": []}), relogio=lambda: agora)

    cliente.metricas_conta(dias=7)

    _, params, _ = transporte.chamadas[0]
    assert params["until"] == int(agora)
    assert params["since"] == int(agora) - 7 * 86400
    assert params["metric_type"] == "total_value"


def test_metricas_conta_reduz_janela_maior_que_o_teto_da_meta():
    agora = 1_700_000_000.0
    cliente, transporte = montar_cliente(resposta_ok({"data": []}), relogio=lambda: agora)

    cliente.metricas_conta(dias=365)

    _, params, _ = transporte.chamadas[0]
    assert params["since"] == int(agora) - JANELA_DIAS_MAXIMA * 86400


def test_leitura_sem_token_falha_antes_de_qualquer_chamada():
    cliente, transporte = montar_cliente(resposta_ok({}), token=None)

    with pytest.raises(SemAutorizacaoError):
        cliente.perfil()

    assert transporte.chamadas == []


def test_token_e_lido_a_cada_chamada_e_nao_guardado():
    # Revogar a autorizacao precisa valer ja na chamada seguinte.
    tokens = [TOKEN_FALSO, None]
    transporte = TransporteEspiao(resposta_ok({}))
    cliente = ClienteLeituraInstagram(
        transporte=transporte,
        obter_token=lambda: tokens.pop(0),
    )

    cliente.perfil()

    with pytest.raises(SemAutorizacaoError):
        cliente.perfil()


# =====================================================================
# Transporte real, sem rede
# =====================================================================


def test_transporte_envia_o_token_no_cabecalho_e_nunca_na_url():
    capturada: dict = {}

    def responder(request: httpx2.Request) -> httpx2.Response:
        capturada["url"] = str(request.url)
        capturada["authorization"] = request.headers.get("Authorization")
        return httpx2.Response(200, json={"id": "123"})

    transporte = TransporteGraphHttpx(httpx_transport=httpx2.MockTransport(responder))

    resposta = transporte.get(
        f"{BASE_GRAPH}/{VERSAO_API_PADRAO}/me", {"fields": "id"}, TOKEN_FALSO
    )

    assert resposta.status_code == 200
    assert capturada["authorization"] == f"Bearer {TOKEN_FALSO}"
    assert TOKEN_FALSO not in capturada["url"]
    assert "access_token" not in capturada["url"]


def test_transporte_converte_timeout_em_erro_sem_vazar_token():
    def responder(request: httpx2.Request) -> httpx2.Response:
        raise httpx2.TimeoutException("timeout", request=request)

    transporte = TransporteGraphHttpx(httpx_transport=httpx2.MockTransport(responder))

    with pytest.raises(ErroDeTransporte) as capturado:
        transporte.get(f"{BASE_GRAPH}/me", {}, TOKEN_FALSO)

    assert TOKEN_FALSO not in str(capturado.value)
    assert capturado.value.__cause__ is None


def test_transporte_converte_falha_de_rede_em_erro_sem_vazar_token():
    def responder(request: httpx2.Request) -> httpx2.Response:
        raise httpx2.ConnectError("sem rede", request=request)

    transporte = TransporteGraphHttpx(httpx_transport=httpx2.MockTransport(responder))

    with pytest.raises(ErroDeTransporte) as capturado:
        transporte.get(f"{BASE_GRAPH}/me", {}, TOKEN_FALSO)

    assert TOKEN_FALSO not in str(capturado.value)


def test_repr_do_transporte_nao_contem_token():
    assert TOKEN_FALSO not in repr(TransporteGraphHttpx())
