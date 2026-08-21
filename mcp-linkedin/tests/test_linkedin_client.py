"""
Testes do cliente do LinkedIn (pacote `linkedin_client`) e das
ferramentas de negocio do servidor.

Nenhum teste aqui acessa a rede nem publica coisa alguma. O transporte
real e exercitado com `httpx2.MockTransport`, no mesmo padrao dos
testes da Camada 2.

O grupo mais importante e o da CONFIRMACAO: ele guarda a promessa de
que nada vai ao ar sem o autor ter lido o texto e aprovado.
"""

from __future__ import annotations

import json

import httpx2
import pytest

from mcp_linkedin import server as modulo_servidor
from mcp_linkedin.linkedin_client.publicacao import (
    LIMITE_CARACTERES,
    URL_PUBLICACOES,
    ClienteLinkedIn,
    ErroDaApi,
    PermissaoAusenteError,
    SemAutorizacaoError,
    TextoInvalidoError,
    _interpretar,
)
from mcp_linkedin.linkedin_client.transporte import (
    ErroDeTransporte,
    RespostaLinkedIn,
    TransporteLinkedInHttpx,
)

TOKEN_FALSO = "token-de-teste-nao-e-real"
SUB_FALSO = "AbC123xyz"


class TransporteEspiao:
    """Transporte falso que grava as chamadas e devolve o que foi programado."""

    def __init__(self, resposta_get=None, resposta_post=None) -> None:
        self.resposta_get = resposta_get or RespostaLinkedIn(
            status_code=200, text=json.dumps({"sub": SUB_FALSO, "name": "Fulana"})
        )
        self.resposta_post = resposta_post or RespostaLinkedIn(
            status_code=201, text="", id_criado="urn:li:share:7000"
        )
        self.gets: list[tuple] = []
        self.posts: list[tuple] = []

    def get(self, url, params, token):
        self.gets.append((url, params, token))
        return self.resposta_get

    def post(self, url, corpo, token):
        self.posts.append((url, corpo, token))
        return self.resposta_post


def montar(resposta_post=None, token=TOKEN_FALSO):
    transporte = TransporteEspiao(resposta_post=resposta_post)
    return ClienteLinkedIn(transporte=transporte, obter_token=lambda: token), transporte


# =====================================================================
# A trava da confirmacao. O grupo que mais importa.
# =====================================================================


def test_sem_confirmar_nao_publica_e_devolve_a_previa():
    resultado = modulo_servidor.linkedin_publicar(texto="Texto de teste")

    assert resultado["status"] == "previa"
    assert resultado["publicado"] is False
    assert resultado["texto"] == "Texto de teste"


def test_o_padrao_de_confirmado_e_falso():
    # Uma chamada distraida, sem passar confirmado, nunca publica.
    import inspect

    assinatura = inspect.signature(modulo_servidor.linkedin_publicar)
    assert assinatura.parameters["confirmado"].default is False


def test_a_previa_mostra_o_texto_exato_que_seria_publicado():
    # A decisao precisa ser tomada sobre o texto real, nao sobre um resumo.
    texto = "Primeira linha.\n\nSegunda linha, com acento e numero 3."
    resultado = modulo_servidor.linkedin_publicar(texto=texto)

    assert resultado["texto"] == texto
    assert resultado["caracteres"] == len(texto)


def test_previa_de_texto_vazio_avisa_em_vez_de_publicar_em_branco():
    resultado = modulo_servidor.linkedin_publicar(texto="   ")

    assert resultado["status"] == "texto_invalido"
    assert resultado.get("publicado") is not True


# =====================================================================
# Validacao do texto
# =====================================================================


def test_texto_vazio_nao_chega_a_api():
    cliente, transporte = montar()

    with pytest.raises(TextoInvalidoError):
        cliente.publicar("   ")

    assert transporte.posts == []


def test_texto_acima_do_limite_e_recusado_antes_da_rede():
    cliente, transporte = montar()

    with pytest.raises(TextoInvalidoError) as capturado:
        cliente.publicar("a" * (LIMITE_CARACTERES + 10))

    assert "10 caracteres" in str(capturado.value)
    assert transporte.posts == []


def test_texto_no_limite_exato_e_aceito():
    cliente, transporte = montar()

    cliente.publicar("a" * LIMITE_CARACTERES)

    assert len(transporte.posts) == 1


def test_visibilidade_invalida_e_recusada_antes_da_rede():
    cliente, transporte = montar()

    with pytest.raises(TextoInvalidoError):
        cliente.publicar("texto", visibilidade="SOMENTE_EU")

    assert transporte.posts == []


def test_publicar_sem_token_falha_antes_de_qualquer_chamada():
    cliente, transporte = montar(token=None)

    with pytest.raises(SemAutorizacaoError):
        cliente.publicar("texto")

    assert transporte.posts == []
    assert transporte.gets == []


# =====================================================================
# Publicacao
# =====================================================================


def test_publicar_monta_o_corpo_que_o_linkedin_espera():
    cliente, transporte = montar()

    resultado = cliente.publicar("Bom dia.")

    url, corpo, token = transporte.posts[0]
    assert url == URL_PUBLICACOES
    assert token == TOKEN_FALSO
    assert corpo["author"] == f"urn:li:person:{SUB_FALSO}"
    assert corpo["commentary"] == "Bom dia."
    assert corpo["visibility"] == "PUBLIC"
    assert corpo["lifecycleState"] == "PUBLISHED"
    assert resultado["id"] == "urn:li:share:7000"


def test_o_texto_e_publicado_sem_espaco_sobrando_nas_pontas():
    cliente, transporte = montar()

    cliente.publicar("  Bom dia.  ")

    _, corpo, _ = transporte.posts[0]
    assert corpo["commentary"] == "Bom dia."


def test_publicacao_com_201_e_corpo_vazio_e_sucesso():
    # A API responde 201 sem corpo: o id vem no cabecalho. Sem tratar
    # isso, uma publicacao bem-sucedida seria reportada como erro.
    cliente, _ = montar(
        resposta_post=RespostaLinkedIn(status_code=201, text="", id_criado="urn:li:share:1")
    )

    assert cliente.publicar("ok")["id"] == "urn:li:share:1"


def test_403_vira_erro_de_permissao_com_a_solucao_no_texto():
    cliente, _ = montar(
        resposta_post=RespostaLinkedIn(status_code=403, text=json.dumps({"message": "denied"}))
    )

    with pytest.raises(PermissaoAusenteError) as capturado:
        cliente.publicar("texto")

    assert "w_member_social" in str(capturado.value)


def test_erro_da_api_repassa_a_mensagem_do_linkedin():
    cliente, _ = montar(
        resposta_post=RespostaLinkedIn(
            status_code=422, text=json.dumps({"message": "Duplicate post", "code": "DUP"})
        )
    )

    with pytest.raises(ErroDaApi) as capturado:
        cliente.publicar("texto")

    assert capturado.value.mensagem == "Duplicate post"
    assert capturado.value.status_http == 422


# =====================================================================
# Perfil
# =====================================================================


def test_perfil_le_o_endpoint_openid():
    cliente, transporte = montar()

    dados = cliente.perfil()

    url, _, token = transporte.gets[0]
    assert url.endswith("/v2/userinfo")
    assert token == TOKEN_FALSO
    assert dados["sub"] == SUB_FALSO


def test_urn_do_autor_falha_com_mensagem_util_se_o_sub_nao_vier():
    transporte = TransporteEspiao(resposta_get=RespostaLinkedIn(200, json.dumps({})))
    cliente = ClienteLinkedIn(transporte=transporte, obter_token=lambda: TOKEN_FALSO)

    with pytest.raises(ErroDaApi) as capturado:
        cliente.urn_do_autor()

    assert "openid" in str(capturado.value)


# =====================================================================
# Interpretacao da resposta
# =====================================================================


def test_interpretar_aceita_corpo_vazio_apenas_quando_autorizado():
    assert _interpretar(RespostaLinkedIn(201, ""), aceita_corpo_vazio=True) == {}

    with pytest.raises(ErroDaApi):
        _interpretar(RespostaLinkedIn(201, ""))


def test_interpretar_falha_com_corpo_que_nao_e_json():
    with pytest.raises(ErroDaApi) as capturado:
        _interpretar(RespostaLinkedIn(502, "<html>erro</html>"))

    assert capturado.value.status_http == 502


# =====================================================================
# Transporte real, sem rede
# =====================================================================


def test_transporte_envia_token_no_cabecalho_e_a_versao_da_api():
    capturada: dict = {}

    def responder(request: httpx2.Request) -> httpx2.Response:
        capturada["url"] = str(request.url)
        capturada["auth"] = request.headers.get("Authorization")
        capturada["versao"] = request.headers.get("LinkedIn-Version")
        return httpx2.Response(200, json={"sub": SUB_FALSO})

    transporte = TransporteLinkedInHttpx(httpx_transport=httpx2.MockTransport(responder))
    transporte.get("https://api.linkedin.com/v2/userinfo", {}, TOKEN_FALSO)

    assert capturada["auth"] == f"Bearer {TOKEN_FALSO}"
    assert capturada["versao"]
    assert TOKEN_FALSO not in capturada["url"]


def test_transporte_le_o_id_criado_do_cabecalho():
    def responder(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(201, headers={"x-restli-id": "urn:li:share:42"})

    transporte = TransporteLinkedInHttpx(httpx_transport=httpx2.MockTransport(responder))
    resposta = transporte.post(URL_PUBLICACOES, {}, TOKEN_FALSO)

    assert resposta.id_criado == "urn:li:share:42"


def test_transporte_converte_falha_de_rede_sem_vazar_token():
    def responder(request: httpx2.Request) -> httpx2.Response:
        raise httpx2.ConnectError("sem rede", request=request)

    transporte = TransporteLinkedInHttpx(httpx_transport=httpx2.MockTransport(responder))

    with pytest.raises(ErroDeTransporte) as capturado:
        transporte.post(URL_PUBLICACOES, {}, TOKEN_FALSO)

    assert TOKEN_FALSO not in str(capturado.value)
    assert capturado.value.__cause__ is None


def test_repr_do_transporte_nao_contem_token():
    assert TOKEN_FALSO not in repr(TransporteLinkedInHttpx())
