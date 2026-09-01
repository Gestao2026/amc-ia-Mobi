"""
Teste ponta a ponta da sessao da Camada 1 sobre a ponte (Etapa 8).

Os outros testes exercitam as pecas em separado. Este liga a cadeia
inteira do jeito que roda em producao:

    ClaudeSessionStore -> EncryptedCredentialBackend -> PonteCredentialBackend -> PonteFalsa

PonteFalsa e a especificacao executavel do PHP publicado na HostGator.
Se o PHP responder como ela, a sessao sobrevive ao reinicio. Se recusar
o namespace 'claude-', este teste falha, que e exatamente o aviso que
se quer ter ANTES de publicar.

Nenhum pacote sai da maquina: o transporte e um MockTransport em
processo.
"""

import httpx2

from mcp_linkedin.auth_claude.session_store import ClaudeSessionStore
from mcp_linkedin.auth_linkedin.crypto import TokenCipher, generate_key_base64
from mcp_linkedin.auth_linkedin.ponte_backend import PonteCredentialBackend
from mcp_linkedin.auth_linkedin.token_store import EncryptedCredentialBackend

from .test_ponte import FAKE_PONTE_SECRET, FAKE_PONTE_URL, PonteFalsa

FAKE_CLIENT_ID = "FAKE_CLAUDE_CLIENT_ID_NAO_REAL"


def _backend(ponte: PonteFalsa) -> EncryptedCredentialBackend:
    """A mesma composicao que build_credential_backend monta em producao."""
    return EncryptedCredentialBackend(
        inner=PonteCredentialBackend(
            url=FAKE_PONTE_URL,
            secret=FAKE_PONTE_SECRET,
            httpx_transport=httpx2.MockTransport(ponte),
        ),
        cipher=TokenCipher.from_base64_key(generate_key_base64()),
    )


def test_a_sessao_atravessa_o_reinicio_pela_ponte():
    ponte = PonteFalsa()
    backend = _backend(ponte)

    store = ClaudeSessionStore(backend=backend)
    access = store.create_access_token(client_id=FAKE_CLIENT_ID, scopes=["FAKE_ESCOPO"])
    refresh = store.create_refresh_token(client_id=FAKE_CLIENT_ID, scopes=["FAKE_ESCOPO"])

    # O processo dorme e acorda: store novo, mesma ponte.
    apos_reinicio = ClaudeSessionStore(backend=_backend_com_mesma_chave(backend, ponte))

    recuperado = apos_reinicio.get_access_token(access.token)
    assert recuperado is not None
    assert recuperado.client_id == FAKE_CLIENT_ID

    recuperado_refresh = apos_reinicio.get_refresh_token(refresh.token)
    assert recuperado_refresh is not None
    assert recuperado_refresh.scopes == ["FAKE_ESCOPO"]


def _backend_com_mesma_chave(anterior, ponte):
    """
    Reinicio de verdade mantem a chave de cifragem (ela vem do ambiente
    do Render, nao e sorteada a cada boot). Reaproveitar a cifra do
    backend anterior reproduz isso.
    """
    return EncryptedCredentialBackend(
        inner=PonteCredentialBackend(
            url=FAKE_PONTE_URL,
            secret=FAKE_PONTE_SECRET,
            httpx_transport=httpx2.MockTransport(ponte),
        ),
        cipher=anterior._cipher,
    )


def test_a_ponte_recebe_o_hash_e_nunca_o_token():
    ponte = PonteFalsa()
    store = ClaudeSessionStore(backend=_backend(ponte))

    token = store.create_access_token(client_id=FAKE_CLIENT_ID, scopes=[])

    for requisicao in ponte.requisicoes:
        assert token.token not in requisicao["corpo"]
    for chave, valor in ponte.armazenado.items():
        assert token.token not in chave
        assert token.token not in valor


def test_o_token_da_conta_e_a_sessao_convivem_sem_se_sobrescrever():
    """
    A regressao que motivou a trava: a versao anterior do PHP gravava
    tudo no alvo do token da conta, entao a sessao apagaria a
    autorizacao do LinkedIn.
    """
    ponte = PonteFalsa()
    backend = _backend(ponte)

    backend.write(ponte._alvo_esperado, "FAKE_TOKEN_DA_CONTA")
    guardado = ponte.armazenado[ponte._alvo_esperado]

    store = ClaudeSessionStore(backend=backend)
    store.create_access_token(client_id=FAKE_CLIENT_ID, scopes=[])
    store.create_refresh_token(client_id=FAKE_CLIENT_ID, scopes=[])

    assert ponte.armazenado[ponte._alvo_esperado] == guardado, "o token da conta ficou intacto"
    assert len(ponte.armazenado) == 3, "token da conta + access + refresh, em linhas separadas"


def test_revogar_a_sessao_nao_toca_no_token_da_conta():
    ponte = PonteFalsa()
    backend = _backend(ponte)

    backend.write(ponte._alvo_esperado, "FAKE_TOKEN_DA_CONTA")
    guardado = ponte.armazenado[ponte._alvo_esperado]

    store = ClaudeSessionStore(backend=backend)
    token = store.create_access_token(client_id=FAKE_CLIENT_ID, scopes=[])

    store.revoke_access_token(token.token)

    assert ponte.armazenado == {ponte._alvo_esperado: guardado}
