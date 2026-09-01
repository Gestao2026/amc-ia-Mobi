"""
Testes da ligacao entre a Camada 1 e o armazenamento persistente da
sessao (Etapa 8).

Os testes de session_store provam que o store SABE persistir. Estes
provam duas coisas do mundo real, que decidem se a mudanca ajuda ou
atrapalha:

1. Que o store RECEBE o backend na inicializacao quando pode receber.
   Sem isto, a funcionalidade estaria completa e desligada.

2. Que ele NAO recebe pela ponte enquanto o PHP publicado trabalhar com
   alvo fixo. Persistir ali sobrescreveria o token da rede social e
   derrubaria a conta. O padrao precisa ser o seguro.

Nenhuma chamada de rede: build_credential_backend so instancia, e a
primeira ida ao armazenamento aconteceria apenas numa leitura ou
gravacao.
"""

import pytest

from mcp_instagram.auth_instagram.crypto import generate_key_base64
from mcp_instagram.server import (
    VARIAVEL_PONTE_SESSAO,
    build_claude_session_backend,
    ponte_aceita_sessao,
    resolve_claude_auth_config,
)

FAKE_CLAUDE_CLIENT_ID = "FAKE_CLAUDE_CLIENT_ID_NAO_REAL"
FAKE_CLIENT_ID = "FAKE_INSTAGRAM_CLIENT_ID_NAO_REAL"
FAKE_CLIENT_SECRET = "FAKE_INSTAGRAM_CLIENT_SECRET_NAO_REAL"
FAKE_BASE_URL = "https://fake-instagram.invalid"
FAKE_PONTE_URL = "https://ponte.invalid/t.php"
FAKE_PONTE_SECRET = "FAKE_PONTE_SECRET_NAO_REAL"
FAKE_SUPABASE_URL = "https://fake-supabase.invalid"
FAKE_SUPABASE_KEY = "FAKE_SUPABASE_KEY_NAO_REAL"


def _env(**overrides) -> dict:
    """Ambiente equivalente ao de producao: Camada 1 ligada, Camada 2 na ponte."""
    env = {
        "MCP_CLAUDE_CLIENT_ID": FAKE_CLAUDE_CLIENT_ID,
        "MCP_PUBLIC_BASE_URL": FAKE_BASE_URL,
        "INSTAGRAM_CLIENT_ID": FAKE_CLIENT_ID,
        "INSTAGRAM_CLIENT_SECRET": FAKE_CLIENT_SECRET,
        "INSTAGRAM_TOKEN_STORE_BACKEND": "ponte",
        "MCP_INSTAGRAM_PONTE_URL": FAKE_PONTE_URL,
        "MCP_INSTAGRAM_PONTE_SECRET": FAKE_PONTE_SECRET,
        "INSTAGRAM_TOKEN_ENCRYPTION_KEY": generate_key_base64(),
    }
    for chave, valor in overrides.items():
        if valor is None:
            env.pop(chave, None)
        else:
            env[chave] = valor
    return env


def _env_supabase(**overrides) -> dict:
    env = _env(**overrides)
    env["INSTAGRAM_TOKEN_STORE_BACKEND"] = "supabase"
    env["MCP_INSTAGRAM_SUPABASE_URL"] = FAKE_SUPABASE_URL
    env["MCP_INSTAGRAM_SUPABASE_KEY"] = FAKE_SUPABASE_KEY
    return env


# --- a trava da ponte ---


def test_ponte_sem_confirmacao_nao_recebe_a_sessao():
    """
    O padrao seguro. O PHP publicado grava sempre no alvo fixo, entao
    persistir a sessao ali destruiria o token da rede social.
    """
    assert build_claude_session_backend(_env()) is None


def test_ponte_confirmada_recebe_a_sessao():
    env = _env(**{VARIAVEL_PONTE_SESSAO: "1"})

    assert build_claude_session_backend(env) is not None


@pytest.mark.parametrize("valor", ["1", "true", "TRUE", "sim", " Sim "])
def test_valores_que_confirmam_a_ponte(valor):
    assert ponte_aceita_sessao({VARIAVEL_PONTE_SESSAO: valor}) is True


@pytest.mark.parametrize("valor", ["", "0", "false", "nao", "talvez"])
def test_valores_que_nao_confirmam_a_ponte(valor):
    assert ponte_aceita_sessao({VARIAVEL_PONTE_SESSAO: valor}) is False


def test_sem_a_variavel_a_ponte_nao_e_confirmada():
    assert ponte_aceita_sessao({}) is False


# --- o Supabase nao precisa de trava ---


def test_supabase_recebe_a_sessao_sem_confirmacao():
    """Uma linha por target_name: o namespace da sessao cabe sem mudar nada."""
    assert build_claude_session_backend(_env_supabase()) is not None


# --- o caminho real de inicializacao ---


def test_o_provider_recebe_o_store_persistente_quando_liberado():
    config = resolve_claude_auth_config(env=_env(**{VARIAVEL_PONTE_SESSAO: "1"}))

    assert config is not None
    assert config.provider._store.backend is not None


def test_por_padrao_o_provider_sobe_sem_persistencia():
    config = resolve_claude_auth_config(env=_env())

    assert config is not None, "a Camada 1 precisa subir de qualquer forma"
    assert config.provider._store.backend is None


# --- nada disto pode impedir a Camada 1 de subir ---


def test_sem_a_camada_2_a_sessao_segue_so_em_memoria():
    env = _env(**{"INSTAGRAM_CLIENT_ID": None})

    assert build_claude_session_backend(env) is None

    config = resolve_claude_auth_config(env=env)
    assert config is not None
    assert config.provider._store.backend is None


@pytest.mark.parametrize("backend", ["memory", "windows"])
def test_backend_que_nao_sobrevive_ao_reinicio_e_recusado(backend):
    """
    'memory' e 'windows' morrem com o conteiner (ou nem existem no
    Linux do Render): aceita-los daria falsa sensacao de persistencia.
    """
    env = _env(**{"INSTAGRAM_TOKEN_STORE_BACKEND": backend, VARIAVEL_PONTE_SESSAO: "1"})

    assert build_claude_session_backend(env) is None


def test_configuracao_invalida_nao_derruba_a_camada_1():
    """
    Chave de cifragem malformada faz resolve_instagram_config levantar.
    A Camada 1 precisa subir assim mesmo, sem persistencia.
    """
    env = _env(
        **{"INSTAGRAM_TOKEN_ENCRYPTION_KEY": "FAKE_CHAVE_CURTA", VARIAVEL_PONTE_SESSAO: "1"}
    )

    assert build_claude_session_backend(env) is None

    config = resolve_claude_auth_config(env=env)
    assert config is not None
    assert config.provider._store.backend is None
