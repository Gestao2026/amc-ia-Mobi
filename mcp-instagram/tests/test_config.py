"""
Testes da configuração específica do Instagram (config.py).

Cobre o que difere do mcp-linkedin: escopos padrão travados em leitura,
exigência de HTTPS na base pública, aceitação de vírgula ou espaço como
separador de escopos, e a distinção entre escopo de leitura e escopo de
escrita.

Nenhum teste aqui acessa rede ou o Instagram.
"""

from __future__ import annotations

import pytest

from mcp_instagram.config import (
    DEFAULT_INSTAGRAM_SCOPES,
    INSTAGRAM_CALLBACK_PATH,
    InvalidInstagramConfigError,
    missing_instagram_env_vars,
    resolve_instagram_config,
)

FAKE_CLIENT_ID = "1234567890"
FAKE_CLIENT_SECRET = "segredo-de-teste-nunca-real"
FAKE_BASE_URL = "https://mcp-instagram.exemplo.test"


def env_minimo(**extra) -> dict:
    base = {
        "INSTAGRAM_CLIENT_ID": FAKE_CLIENT_ID,
        "INSTAGRAM_CLIENT_SECRET": FAKE_CLIENT_SECRET,
        "MCP_PUBLIC_BASE_URL": FAKE_BASE_URL,
        "INSTAGRAM_TOKEN_STORE_BACKEND": "memory",
    }
    base.update(extra)
    return base


# --- escopos padrão -------------------------------------------------


def test_escopos_padrao_sao_somente_leitura():
    config = resolve_instagram_config(env=env_minimo())

    assert config.scopes == DEFAULT_INSTAGRAM_SCOPES
    assert config.somente_leitura is True
    assert config.escopos_de_escrita == ()


def test_escopos_padrao_nao_incluem_publicacao_comentario_mensagem_ou_anuncio():
    proibidos = {
        "instagram_business_content_publish",
        "instagram_business_manage_comments",
        "instagram_business_manage_messages",
        "ads_management",
        "ads_read",
    }

    assert proibidos.isdisjoint(set(DEFAULT_INSTAGRAM_SCOPES))


def test_escopo_de_escrita_configurado_e_denunciado():
    config = resolve_instagram_config(
        env=env_minimo(
            INSTAGRAM_SCOPES="instagram_business_basic,instagram_business_content_publish"
        )
    )

    assert config.somente_leitura is False
    assert config.escopos_de_escrita == ("instagram_business_content_publish",)


# --- separador de escopos -------------------------------------------


def test_escopos_aceitam_virgula():
    config = resolve_instagram_config(
        env=env_minimo(INSTAGRAM_SCOPES="instagram_business_basic,instagram_business_manage_insights")
    )

    assert config.scopes == (
        "instagram_business_basic",
        "instagram_business_manage_insights",
    )


def test_escopos_aceitam_espaco():
    config = resolve_instagram_config(
        env=env_minimo(INSTAGRAM_SCOPES="instagram_business_basic instagram_business_manage_insights")
    )

    assert config.scopes == (
        "instagram_business_basic",
        "instagram_business_manage_insights",
    )


def test_escopos_vazios_sao_recusados():
    with pytest.raises(InvalidInstagramConfigError):
        resolve_instagram_config(env=env_minimo(INSTAGRAM_SCOPES="   "))


# --- HTTPS obrigatório ----------------------------------------------


def test_base_publica_sem_https_e_recusada():
    with pytest.raises(InvalidInstagramConfigError) as excinfo:
        resolve_instagram_config(env=env_minimo(MCP_PUBLIC_BASE_URL="http://exemplo.test"))

    assert "https" in str(excinfo.value).lower()


def test_redirect_uri_e_derivado_da_base_publica():
    config = resolve_instagram_config(env=env_minimo(MCP_PUBLIC_BASE_URL=FAKE_BASE_URL + "/"))

    assert config.redirect_uri == f"{FAKE_BASE_URL}{INSTAGRAM_CALLBACK_PATH}"


# --- camada desligada e variáveis ausentes --------------------------


def test_camada_desligada_quando_falta_variavel():
    assert resolve_instagram_config(env={}) is None


def test_variaveis_ausentes_devolve_nomes_nunca_valores():
    ausentes = missing_instagram_env_vars(env={"INSTAGRAM_CLIENT_ID": FAKE_CLIENT_ID})

    assert "INSTAGRAM_CLIENT_SECRET" in ausentes
    assert "MCP_PUBLIC_BASE_URL" in ausentes
    assert FAKE_CLIENT_ID not in ausentes


# --- mascaramento ---------------------------------------------------


def test_repr_nunca_expoe_o_client_secret():
    config = resolve_instagram_config(env=env_minimo())

    texto = repr(config)

    assert FAKE_CLIENT_SECRET not in texto
    assert "client_secret='***'" in texto
