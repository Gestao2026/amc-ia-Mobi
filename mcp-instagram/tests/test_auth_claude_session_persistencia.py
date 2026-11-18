"""
Testes da persistencia opcional da sessao da Camada 1 (Etapa 8).

Cobrem a promessa da mudanca: com um backend injetado, access token e
refresh token sobrevivem ao reinicio do processo, e o conector para de
pedir "Reconectar" a cada hibernacao do Render.

Cobrem tambem as tres garantias que a acompanham: o token nunca vai
para o armazenamento (so o hash dele), falha do backend nao derruba a
autenticacao, e o authorization code continua fora dali de proposito.

Nenhuma chamada de rede, nenhum acesso ao Instagram ou ao Claude, so
valores ficticios (FAKE_...).
"""

import hashlib
import json

from mcp_instagram.auth_claude.session_store import (
    ACCESS_TOKEN_TTL_SECONDS,
    PREFIXO_ALVO_ACCESS,
    PREFIXO_ALVO_REFRESH,
    REFRESH_TOKEN_TTL_SECONDS,
    ClaudeSessionStore,
)

FAKE_CLIENT_ID = "FAKE_CLAUDE_CLIENT_ID_NAO_REAL"
FAKE_CODE_CHALLENGE = "FAKE_CODE_CHALLENGE_NAO_REAL"
FAKE_REDIRECT_URI = "https://claude.ai/api/mcp/auth_callback"
FAKE_TOKEN_INEXISTENTE = "FAKE_TOKEN_QUE_NUNCA_FOI_CRIADO"


class FakeClock:
    def __init__(self, start: float = 1000.0):
        self._now = start

    def __call__(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        self._now += seconds


class BackendFalso:
    """
    Backend em memoria que vive fora do store, ao contrario dos dicts
    internos. E o que permite simular reinicio: monta-se um store novo
    apontando para o mesmo backend, exatamente como o processo faz ao
    acordar e reencontrar a ponte.
    """

    def __init__(self):
        self.dados: dict[str, str] = {}
        self.leituras = 0

    def write(self, target_name: str, secret: str) -> None:
        self.dados[target_name] = secret

    def read(self, target_name: str) -> str | None:
        self.leituras += 1
        return self.dados.get(target_name)

    def delete(self, target_name: str) -> None:
        self.dados.pop(target_name, None)


class BackendQueFalha:
    """Backend indisponivel, como a ponte fora do ar ou a rede caida."""

    def write(self, target_name: str, secret: str) -> None:
        raise RuntimeError("FAKE: ponte indisponivel")

    def read(self, target_name: str) -> str | None:
        raise RuntimeError("FAKE: ponte indisponivel")

    def delete(self, target_name: str) -> None:
        raise RuntimeError("FAKE: ponte indisponivel")


def _criar_authorization_code(store):
    return store.create_authorization_code(
        client_id=FAKE_CLIENT_ID,
        scopes=[],
        code_challenge=FAKE_CODE_CHALLENGE,
        redirect_uri=FAKE_REDIRECT_URI,
        redirect_uri_provided_explicitly=True,
    )


# --- sem backend: comportamento da v1, intacto ---


def test_sem_backend_a_sessao_morre_no_reinicio():
    clock = FakeClock()
    store = ClaudeSessionStore(clock=clock)

    token = store.create_access_token(client_id=FAKE_CLIENT_ID, scopes=[])
    apos_reinicio = ClaudeSessionStore(clock=clock)

    assert apos_reinicio.get_access_token(token.token) is None


# --- com backend: a sessao atravessa o reinicio ---


def test_access_token_sobrevive_ao_reinicio():
    backend = BackendFalso()
    clock = FakeClock()

    store = ClaudeSessionStore(clock=clock, backend=backend)
    token = store.create_access_token(client_id=FAKE_CLIENT_ID, scopes=["FAKE_ESCOPO"])

    apos_reinicio = ClaudeSessionStore(clock=clock, backend=backend)
    recuperado = apos_reinicio.get_access_token(token.token)

    assert recuperado is not None
    assert recuperado.token == token.token
    assert recuperado.client_id == FAKE_CLIENT_ID
    assert recuperado.scopes == ["FAKE_ESCOPO"]
    assert recuperado.expires_at == token.expires_at


def test_refresh_token_sobrevive_ao_reinicio():
    backend = BackendFalso()
    clock = FakeClock()

    store = ClaudeSessionStore(clock=clock, backend=backend)
    token = store.create_refresh_token(client_id=FAKE_CLIENT_ID, scopes=["FAKE_ESCOPO"])

    apos_reinicio = ClaudeSessionStore(clock=clock, backend=backend)
    recuperado = apos_reinicio.get_refresh_token(token.token)

    assert recuperado is not None
    assert recuperado.token == token.token
    assert recuperado.client_id == FAKE_CLIENT_ID
    assert recuperado.scopes == ["FAKE_ESCOPO"]
    assert recuperado.expires_at == token.expires_at


def test_recuperar_do_armazenamento_acontece_uma_vez_so():
    """Depois da primeira leitura o token fica em memoria, e a ponte nao e chamada de novo."""
    backend = BackendFalso()
    clock = FakeClock()

    store = ClaudeSessionStore(clock=clock, backend=backend)
    token = store.create_access_token(client_id=FAKE_CLIENT_ID, scopes=[])

    apos_reinicio = ClaudeSessionStore(clock=clock, backend=backend)
    backend.leituras = 0
    apos_reinicio.get_access_token(token.token)
    apos_reinicio.get_access_token(token.token)
    apos_reinicio.get_access_token(token.token)

    assert backend.leituras == 1


# --- seguranca: o token nao vai para o armazenamento ---


def test_o_token_nunca_e_gravado_no_armazenamento():
    backend = BackendFalso()
    store = ClaudeSessionStore(clock=FakeClock(), backend=backend)

    token = store.create_access_token(client_id=FAKE_CLIENT_ID, scopes=[])

    # Nem como chave, nem dentro do valor gravado.
    assert token.token not in json.dumps(backend.dados)


def test_a_chave_de_armazenamento_e_o_hash_do_token():
    backend = BackendFalso()
    store = ClaudeSessionStore(clock=FakeClock(), backend=backend)

    token = store.create_refresh_token(client_id=FAKE_CLIENT_ID, scopes=[])

    digest = hashlib.sha256(token.token.encode("utf-8")).hexdigest()
    assert f"{PREFIXO_ALVO_REFRESH}:{digest}" in backend.dados


def test_access_e_refresh_nao_colidem_no_armazenamento():
    """Prefixos distintos: o mesmo valor de token nos dois papeis nao se sobrescreve."""
    assert PREFIXO_ALVO_ACCESS != PREFIXO_ALVO_REFRESH


# --- revogacao e validade ---


def test_revogar_apaga_do_armazenamento():
    backend = BackendFalso()
    store = ClaudeSessionStore(clock=FakeClock(), backend=backend)

    token = store.create_access_token(client_id=FAKE_CLIENT_ID, scopes=[])
    store.revoke_access_token(token.token)

    assert backend.dados == {}


def test_revogar_refresh_apaga_do_armazenamento():
    backend = BackendFalso()
    store = ClaudeSessionStore(clock=FakeClock(), backend=backend)

    token = store.create_refresh_token(client_id=FAKE_CLIENT_ID, scopes=[])
    store.revoke_refresh_token(token.token)

    assert backend.dados == {}


def test_access_token_vencido_nao_volta_do_armazenamento():
    backend = BackendFalso()
    clock = FakeClock()

    store = ClaudeSessionStore(clock=clock, backend=backend)
    token = store.create_access_token(client_id=FAKE_CLIENT_ID, scopes=[])
    clock.advance(ACCESS_TOKEN_TTL_SECONDS + 1)

    apos_reinicio = ClaudeSessionStore(clock=clock, backend=backend)

    assert apos_reinicio.get_access_token(token.token) is None
    assert backend.dados == {}, "o vencido tambem sai do armazenamento"


def test_refresh_token_vencido_nao_volta_do_armazenamento():
    backend = BackendFalso()
    clock = FakeClock()

    store = ClaudeSessionStore(clock=clock, backend=backend)
    token = store.create_refresh_token(client_id=FAKE_CLIENT_ID, scopes=[])
    clock.advance(REFRESH_TOKEN_TTL_SECONDS + 1)

    apos_reinicio = ClaudeSessionStore(clock=clock, backend=backend)

    assert apos_reinicio.get_refresh_token(token.token) is None
    assert backend.dados == {}


# --- o authorization code fica de fora, de proposito ---


def test_authorization_code_nao_e_persistido():
    backend = BackendFalso()
    store = ClaudeSessionStore(clock=FakeClock(), backend=backend)

    _criar_authorization_code(store)

    assert backend.dados == {}


# --- falha do backend nunca derruba a autenticacao ---


def test_falha_ao_gravar_nao_impede_a_criacao_do_token():
    store = ClaudeSessionStore(clock=FakeClock(), backend=BackendQueFalha())

    token = store.create_access_token(client_id=FAKE_CLIENT_ID, scopes=[])

    # A sessao segue valida em memoria: o pior caso e voltar a pedir
    # Reconectar depois de um reinicio, nunca um erro agora.
    assert store.get_access_token(token.token) is not None


def test_falha_ao_gravar_refresh_nao_impede_a_criacao():
    store = ClaudeSessionStore(clock=FakeClock(), backend=BackendQueFalha())

    token = store.create_refresh_token(client_id=FAKE_CLIENT_ID, scopes=[])

    assert store.get_refresh_token(token.token) is not None


def test_falha_ao_ler_equivale_a_sessao_ausente():
    store = ClaudeSessionStore(clock=FakeClock(), backend=BackendQueFalha())

    assert store.get_access_token(FAKE_TOKEN_INEXISTENTE) is None
    assert store.get_refresh_token(FAKE_TOKEN_INEXISTENTE) is None


def test_falha_ao_apagar_nao_derruba_a_revogacao():
    store = ClaudeSessionStore(clock=FakeClock(), backend=BackendQueFalha())
    token = store.create_access_token(client_id=FAKE_CLIENT_ID, scopes=[])

    store.revoke_access_token(token.token)

    assert store.get_access_token(token.token) is None


def test_conteudo_corrompido_equivale_a_sessao_ausente():
    """Chave de cifragem trocada ou dado corrompido leva a reconectar, nao a estourar."""
    backend = BackendFalso()
    clock = FakeClock()

    store = ClaudeSessionStore(clock=clock, backend=backend)
    token = store.create_access_token(client_id=FAKE_CLIENT_ID, scopes=[])
    chave = next(iter(backend.dados))
    backend.dados[chave] = "FAKE_CONTEUDO_QUE_NAO_E_JSON"

    apos_reinicio = ClaudeSessionStore(clock=clock, backend=backend)

    assert apos_reinicio.get_access_token(token.token) is None


def test_conteudo_json_que_nao_e_objeto_equivale_a_sessao_ausente():
    backend = BackendFalso()
    clock = FakeClock()

    store = ClaudeSessionStore(clock=clock, backend=backend)
    token = store.create_access_token(client_id=FAKE_CLIENT_ID, scopes=[])
    chave = next(iter(backend.dados))
    backend.dados[chave] = json.dumps(["FAKE_LISTA"])

    apos_reinicio = ClaudeSessionStore(clock=clock, backend=backend)

    assert apos_reinicio.get_access_token(token.token) is None
