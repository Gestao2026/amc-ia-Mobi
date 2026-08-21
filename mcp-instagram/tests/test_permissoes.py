"""
Testes das garantias de escopo e de transparência do servidor.

Estes testes existem por um motivo específico: a conexão foi autorizada
como SOMENTE LEITURA (perfil e métricas). Se um dia alguém acrescentar um
escopo de publicação, comentário, mensagem ou anúncio sem decisão
explícita, é aqui que isso precisa aparecer.

Nenhum teste aqui acessa rede ou o Instagram.
"""

from __future__ import annotations

import pytest

import mcp_instagram.server as modulo_servidor
from mcp_instagram.auth_instagram.state_store import StateStore
from mcp_instagram.auth_instagram.token_store import InMemoryCredentialBackend, TokenStore
from mcp_instagram.config import resolve_instagram_config
from mcp_instagram.server import (
    PERMISSOES,
    descrever_permissoes,
    instagram_desconectar,
    instagram_mcp_status,
    instagram_oauth_iniciar,
    instagram_oauth_status,
)

FAKE_CLIENT_ID = "FAKE_INSTAGRAM_CLIENT_ID_NAO_REAL"
FAKE_CLIENT_SECRET = "FAKE_INSTAGRAM_CLIENT_SECRET_NAO_REAL"
FAKE_BASE_URL = "https://mcp-instagram.invalid"


def _env(**overrides) -> dict:
    env = {
        "INSTAGRAM_CLIENT_ID": FAKE_CLIENT_ID,
        "INSTAGRAM_CLIENT_SECRET": FAKE_CLIENT_SECRET,
        "MCP_PUBLIC_BASE_URL": FAKE_BASE_URL,
    }
    env.update(overrides)
    return env


class TransporteProibido:
    """Qualquer chamada de rede neste teste é um defeito."""

    def post(self, url, data):
        raise AssertionError("nenhuma chamada de rede deveria acontecer aqui")

    def get(self, url, params):
        raise AssertionError("nenhuma chamada de rede deveria acontecer aqui")


@pytest.fixture
def runtime_injetado():
    from mcp_instagram.auth_instagram.runtime import InstagramOAuthRuntime

    def _injetar(env=None):
        runtime = InstagramOAuthRuntime(
            config=resolve_instagram_config(env or _env()),
            state_store=StateStore(),
            token_store=TokenStore(backend=InMemoryCredentialBackend()),
            transport=TransporteProibido(),
        )
        modulo_servidor._instagram_runtime = runtime
        return runtime

    yield _injetar

    modulo_servidor._instagram_runtime = modulo_servidor._RUNTIME_NAO_RESOLVIDO


# --- catálogo de permissões -----------------------------------------


def test_permissoes_de_leitura_nao_permitem_escrita_nem_mensagem():
    for escopo in ("instagram_business_basic", "instagram_business_manage_insights"):
        detalhe = PERMISSOES[escopo]
        assert detalhe["publicar"] is False
        assert detalhe["editar"] is False
        assert detalhe["excluir"] is False
        assert detalhe["mensagens"] is False
        assert detalhe["anuncios"] is False


def test_escopo_desconhecido_e_declarado_e_nunca_omitido():
    descricoes = descrever_permissoes(["escopo_que_nao_existe"])

    assert len(descricoes) == 1
    assert descricoes[0]["escopo"] == "escopo_que_nao_existe"
    assert "não catalogada" in descricoes[0]["nome"]


# --- ferramentas -----------------------------------------------------


def test_iniciar_declara_as_permissoes_e_como_revogar(runtime_injetado):
    runtime_injetado()

    resultado = instagram_oauth_iniciar()

    assert resultado["status"] == "aguardando_autorizacao"
    assert resultado["somente_leitura"] is True
    assert [p["escopo"] for p in resultado["permissoes"]] == [
        "instagram_business_basic",
        "instagram_business_manage_insights",
    ]
    assert "revogar" in resultado["como_revogar"].lower()


def test_iniciar_nunca_devolve_o_client_secret(runtime_injetado):
    runtime_injetado()

    resultado = instagram_oauth_iniciar()

    assert FAKE_CLIENT_SECRET not in str(resultado)


def test_status_declara_que_nenhuma_acao_e_possivel(runtime_injetado):
    runtime_injetado()

    resultado = instagram_mcp_status()

    assert resultado["somente_leitura"] is True
    assert resultado["escopos_de_escrita"] == []
    assert "não publica" in resultado["acoes_possiveis"]


def test_status_denuncia_escopo_de_escrita_configurado(runtime_injetado):
    runtime_injetado(
        _env(INSTAGRAM_SCOPES="instagram_business_basic,instagram_business_content_publish")
    )

    resultado = instagram_mcp_status()

    assert resultado["somente_leitura"] is False
    assert resultado["escopos_de_escrita"] == ["instagram_business_content_publish"]


def test_desconectar_apaga_a_autorizacao_guardada(runtime_injetado):
    runtime = runtime_injetado()
    runtime.token_store.save_access_token("token-de-teste", 9_999_999_999.0, "17841400000000000")
    assert instagram_oauth_status()["status"] == "conectado"

    resultado = instagram_desconectar()

    assert resultado["status"] == "desconectado"
    assert runtime.token_store.get_access_token() is None
    assert instagram_oauth_status()["status"] == "nao_conectado"


def test_status_conectado_mostra_a_conta_e_nunca_o_token(runtime_injetado):
    runtime = runtime_injetado()
    runtime.token_store.save_access_token("token-de-teste", 9_999_999_999.0, "17841400000000000")

    resultado = instagram_oauth_status()

    assert resultado["conta_conectada"] == "17841400000000000"
    assert "token-de-teste" not in str(resultado)


@pytest.mark.anyio
async def test_nenhuma_ferramenta_de_escrita_existe():
    """
    Guarda a promessa feita ao captador: este servidor LÊ perfil,
    publicações e métricas, mas não publica, não edita, não exclui, não
    comenta, não responde mensagens e não administra anúncios. Se alguém
    acrescentar uma ferramenta de escrita, este teste falha e obriga uma
    decisão consciente.

    A lista é fechada de propósito. Uma verificação por palavra proibida
    no nome deixaria passar qualquer ferramenta batizada de forma
    criativa; exigir que o conjunto seja exatamente este obriga quem
    acrescentar algo a vir aqui e declarar o que está fazendo.

    A verificação é feita no registro de ferramentas do próprio servidor
    MCP, e não nos nomes do módulo: as rotas HTTP exigidas pela Meta
    (desautorização e exclusão de dados) também moram neste módulo, mas
    não são ferramentas e não podem ser chamadas pelo modelo.
    """
    ferramentas_de_conexao = {
        "instagram_mcp_status",
        "instagram_oauth_iniciar",
        "instagram_oauth_status",
        "instagram_desconectar",
    }
    # Todas somente leitura. Nenhuma altera a conta do Instagram.
    ferramentas_de_leitura = {
        "instagram_perfil",
        "instagram_publicacoes",
        "instagram_metricas_publicacao",
        "instagram_metricas_conta",
    }

    registradas = {ferramenta.name for ferramenta in await modulo_servidor.mcp.list_tools()}

    assert registradas == ferramentas_de_conexao | ferramentas_de_leitura


def test_o_cliente_de_leitura_nao_expoe_metodo_de_escrita():
    """
    A trava estrutural: o transporte usado pelas ferramentas de negócio
    só tem `get`. Sem `post`, `put`, `patch` ou `delete`, nenhuma
    ferramenta de escrita pode ser construída sobre ele por engano, nem
    mesmo por quem não leu a documentação.
    """
    from mcp_instagram.instagram_client.transporte import TransporteGraphHttpx

    metodos_publicos = {
        nome for nome in dir(TransporteGraphHttpx) if not nome.startswith("_")
    }

    assert metodos_publicos == {"get"}


@pytest.fixture
def anyio_backend():
    return "asyncio"
