"""
Testes do armazenamento em memoria da Camada 1 (authorization codes,
access tokens, refresh tokens). Nenhuma chamada de rede, nenhum
acesso ao Instagram ou ao Claude, so valores ficticios (FAKE_...).
"""

from mcp_instagram.auth_claude.session_store import (
    ACCESS_TOKEN_TTL_SECONDS,
    AUTHORIZATION_CODE_TTL_SECONDS,
    REFRESH_TOKEN_TTL_SECONDS,
    ClaudeSessionStore,
)

FAKE_CLIENT_ID = "FAKE_CLAUDE_CLIENT_ID_NAO_REAL"
FAKE_CODE_CHALLENGE = "FAKE_CODE_CHALLENGE_NAO_REAL"
FAKE_REDIRECT_URI = "https://claude.ai/api/mcp/auth_callback"


class FakeClock:
    def __init__(self, start: float = 1000.0):
        self._now = start

    def __call__(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        self._now += seconds


def _store(clock=None) -> ClaudeSessionStore:
    return ClaudeSessionStore(clock=clock or FakeClock())


def _criar_authorization_code(store):
    return store.create_authorization_code(
        client_id=FAKE_CLIENT_ID,
        scopes=[],
        code_challenge=FAKE_CODE_CHALLENGE,
        redirect_uri=FAKE_REDIRECT_URI,
        redirect_uri_provided_explicitly=True,
    )


# --- authorization code ---


def test_authorization_code_criado_pode_ser_recuperado():
    store = _store()
    auth_code = _criar_authorization_code(store)

    recuperado = store.get_authorization_code(auth_code.code)

    assert recuperado is not None
    assert recuperado.client_id == FAKE_CLIENT_ID
    assert recuperado.code_challenge == FAKE_CODE_CHALLENGE


def test_authorization_code_inexistente_retorna_none():
    store = _store()

    assert store.get_authorization_code("codigo-nunca-emitido") is None


def test_authorization_code_expirado_retorna_none():
    clock = FakeClock(start=1000.0)
    store = _store(clock=clock)
    auth_code = _criar_authorization_code(store)

    clock.advance(AUTHORIZATION_CODE_TTL_SECONDS + 1)

    assert store.get_authorization_code(auth_code.code) is None


def test_authorization_code_consumido_nao_pode_ser_reutilizado():
    store = _store()
    auth_code = _criar_authorization_code(store)

    store.consume_authorization_code(auth_code.code)

    assert store.get_authorization_code(auth_code.code) is None


# --- access token ---


def test_access_token_criado_pode_ser_recuperado():
    store = _store()
    token = store.create_access_token(client_id=FAKE_CLIENT_ID, scopes=[])

    recuperado = store.get_access_token(token.token)

    assert recuperado is not None
    assert recuperado.client_id == FAKE_CLIENT_ID


def test_access_token_inexistente_retorna_none():
    store = _store()

    assert store.get_access_token("token-nunca-emitido") is None


def test_access_token_expirado_retorna_none():
    clock = FakeClock(start=1000.0)
    store = _store(clock=clock)
    token = store.create_access_token(client_id=FAKE_CLIENT_ID, scopes=[])

    clock.advance(ACCESS_TOKEN_TTL_SECONDS + 1)

    assert store.get_access_token(token.token) is None


def test_access_token_revogado_nao_e_mais_valido():
    store = _store()
    token = store.create_access_token(client_id=FAKE_CLIENT_ID, scopes=[])

    store.revoke_access_token(token.token)

    assert store.get_access_token(token.token) is None


# --- refresh token ---


def test_refresh_token_criado_pode_ser_recuperado():
    store = _store()
    token = store.create_refresh_token(client_id=FAKE_CLIENT_ID, scopes=[])

    assert store.get_refresh_token(token.token) is not None


def test_refresh_token_expirado_retorna_none():
    clock = FakeClock(start=1000.0)
    store = _store(clock=clock)
    token = store.create_refresh_token(client_id=FAKE_CLIENT_ID, scopes=[])

    clock.advance(REFRESH_TOKEN_TTL_SECONDS + 1)

    assert store.get_refresh_token(token.token) is None


def test_refresh_token_revogado_nao_e_mais_valido():
    store = _store()
    token = store.create_refresh_token(client_id=FAKE_CLIENT_ID, scopes=[])

    store.revoke_refresh_token(token.token)

    assert store.get_refresh_token(token.token) is None


# --- seguranca ---


def test_nenhum_valor_e_impresso(capsys):
    store = _store()
    auth_code = _criar_authorization_code(store)
    access = store.create_access_token(client_id=FAKE_CLIENT_ID, scopes=[])
    refresh = store.create_refresh_token(client_id=FAKE_CLIENT_ID, scopes=[])

    captured = capsys.readouterr()
    assert auth_code.code not in captured.out
    assert access.token not in captured.out
    assert refresh.token not in captured.out
    assert auth_code.code not in captured.err
    assert access.token not in captured.err
    assert refresh.token not in captured.err


def test_nenhuma_chamada_de_rede(monkeypatch):
    import socket

    def bloquear(*args, **kwargs):
        raise AssertionError("session_store nao deve abrir conexao de rede")

    monkeypatch.setattr(socket.socket, "connect", bloquear)

    store = _store()
    auth_code = _criar_authorization_code(store)
    store.consume_authorization_code(auth_code.code)
    store.create_access_token(client_id=FAKE_CLIENT_ID, scopes=[])
    store.create_refresh_token(client_id=FAKE_CLIENT_ID, scopes=[])
