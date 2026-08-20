"""
Testes do OAuthAuthorizationServerProvider da Camada 1 (Claude.ai <->
mcp-instagram). Todos os metodos sao chamados diretamente como
corrotinas Python -- sem servidor HTTP, sem rede, sem Instagram.
Valores ficticios (FAKE_...) em todo lugar.
"""

import asyncio

import pytest
from mcp.server.auth.provider import AuthorizationParams

from mcp_instagram.auth_claude.provider import ClaudeAuthProvider
from mcp_instagram.auth_claude.session_store import ACCESS_TOKEN_TTL_SECONDS, ClaudeSessionStore

FAKE_CLIENT_ID = "FAKE_CLAUDE_CLIENT_ID_NAO_REAL"
FAKE_CLIENT_SECRET = "FAKE_CLAUDE_CLIENT_SECRET_NAO_REAL"
FAKE_CODE_CHALLENGE = "FAKE_CODE_CHALLENGE_NAO_REAL"
FAKE_REDIRECT_URI = "https://claude.ai/api/mcp/auth_callback"
FAKE_STATE = "FAKE_STATE_NAO_REAL"


class FakeClock:
    def __init__(self, start: float = 1000.0):
        self._now = start

    def __call__(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        self._now += seconds


def _provider(clock=None, client_secret=None):
    store = ClaudeSessionStore(clock=clock or FakeClock())
    provider = ClaudeAuthProvider(client_id=FAKE_CLIENT_ID, client_secret=client_secret, store=store)
    return provider, store


def _params():
    return AuthorizationParams(
        state=FAKE_STATE,
        scopes=None,
        code_challenge=FAKE_CODE_CHALLENGE,
        redirect_uri=FAKE_REDIRECT_URI,
        redirect_uri_provided_explicitly=True,
    )


def _run(coro):
    return asyncio.run(coro)


def _emitir_authorization_code(provider, cliente):
    url = _run(provider.authorize(cliente, _params()))
    return url.split("code=")[1].split("&")[0]


# --- get_client / register_client ---


def test_get_client_reconhece_o_cliente_estatico():
    provider, _ = _provider()

    cliente = _run(provider.get_client(FAKE_CLIENT_ID))

    assert cliente is not None
    assert cliente.client_id == FAKE_CLIENT_ID


def test_get_client_rejeita_client_id_desconhecido():
    provider, _ = _provider()

    assert _run(provider.get_client("outro-client-id-qualquer")) is None


def test_register_client_nao_esta_habilitado():
    provider, _ = _provider()

    with pytest.raises(NotImplementedError):
        _run(provider.register_client(None))


# --- authorize / load_authorization_code ---


def test_authorize_redireciona_para_o_redirect_uri_com_code_e_state():
    provider, _ = _provider()
    cliente = _run(provider.get_client(FAKE_CLIENT_ID))

    url = _run(provider.authorize(cliente, _params()))

    assert url.startswith(FAKE_REDIRECT_URI)
    assert "code=" in url
    assert f"state={FAKE_STATE}" in url


def test_load_authorization_code_recupera_o_code_emitido():
    provider, _ = _provider()
    cliente = _run(provider.get_client(FAKE_CLIENT_ID))
    code = _emitir_authorization_code(provider, cliente)

    auth_code = _run(provider.load_authorization_code(cliente, code))

    assert auth_code is not None
    assert auth_code.code_challenge == FAKE_CODE_CHALLENGE


def test_load_authorization_code_inexistente_retorna_none():
    provider, _ = _provider()
    cliente = _run(provider.get_client(FAKE_CLIENT_ID))

    assert _run(provider.load_authorization_code(cliente, "codigo-nunca-emitido")) is None


# --- exchange_authorization_code ---


def test_exchange_authorization_code_emite_access_e_refresh_token():
    provider, _ = _provider()
    cliente = _run(provider.get_client(FAKE_CLIENT_ID))
    code = _emitir_authorization_code(provider, cliente)
    auth_code = _run(provider.load_authorization_code(cliente, code))

    oauth_token = _run(provider.exchange_authorization_code(cliente, auth_code))

    assert oauth_token.access_token
    assert oauth_token.refresh_token
    assert oauth_token.token_type == "Bearer"
    assert oauth_token.expires_in == ACCESS_TOKEN_TTL_SECONDS


def test_authorization_code_e_uso_unico_apos_exchange():
    provider, _ = _provider()
    cliente = _run(provider.get_client(FAKE_CLIENT_ID))
    code = _emitir_authorization_code(provider, cliente)
    auth_code = _run(provider.load_authorization_code(cliente, code))

    _run(provider.exchange_authorization_code(cliente, auth_code))

    assert _run(provider.load_authorization_code(cliente, code)) is None


# --- load_access_token ---


def test_load_access_token_valida_token_emitido():
    provider, _ = _provider()
    cliente = _run(provider.get_client(FAKE_CLIENT_ID))
    code = _emitir_authorization_code(provider, cliente)
    auth_code = _run(provider.load_authorization_code(cliente, code))
    oauth_token = _run(provider.exchange_authorization_code(cliente, auth_code))

    access_token = _run(provider.load_access_token(oauth_token.access_token))

    assert access_token is not None
    assert access_token.client_id == FAKE_CLIENT_ID


def test_load_access_token_rejeita_token_desconhecido():
    provider, _ = _provider()

    assert _run(provider.load_access_token("token-nunca-emitido")) is None


def test_load_access_token_rejeita_token_expirado():
    clock = FakeClock(start=1000.0)
    provider, _ = _provider(clock=clock)
    cliente = _run(provider.get_client(FAKE_CLIENT_ID))
    code = _emitir_authorization_code(provider, cliente)
    auth_code = _run(provider.load_authorization_code(cliente, code))
    oauth_token = _run(provider.exchange_authorization_code(cliente, auth_code))

    clock.advance(ACCESS_TOKEN_TTL_SECONDS + 1)

    assert _run(provider.load_access_token(oauth_token.access_token)) is None


# --- refresh token ---


def test_exchange_refresh_token_rotaciona_ambos_os_tokens():
    provider, _ = _provider()
    cliente = _run(provider.get_client(FAKE_CLIENT_ID))
    code = _emitir_authorization_code(provider, cliente)
    auth_code = _run(provider.load_authorization_code(cliente, code))
    primeiro_token = _run(provider.exchange_authorization_code(cliente, auth_code))

    refresh_token_obj = _run(provider.load_refresh_token(cliente, primeiro_token.refresh_token))
    novo_token = _run(provider.exchange_refresh_token(cliente, refresh_token_obj, []))

    assert novo_token.access_token != primeiro_token.access_token
    assert novo_token.refresh_token != primeiro_token.refresh_token
    # uso unico / rotacao: o refresh token antigo nao funciona mais
    assert _run(provider.load_refresh_token(cliente, primeiro_token.refresh_token)) is None


def test_load_refresh_token_rejeita_token_desconhecido():
    provider, _ = _provider()
    cliente = _run(provider.get_client(FAKE_CLIENT_ID))

    assert _run(provider.load_refresh_token(cliente, "refresh-nunca-emitido")) is None


# --- revoke_token ---


def test_revoke_token_invalida_o_access_token():
    provider, _ = _provider()
    cliente = _run(provider.get_client(FAKE_CLIENT_ID))
    code = _emitir_authorization_code(provider, cliente)
    auth_code = _run(provider.load_authorization_code(cliente, code))
    oauth_token = _run(provider.exchange_authorization_code(cliente, auth_code))
    access_token_obj = _run(provider.load_access_token(oauth_token.access_token))

    _run(provider.revoke_token(access_token_obj))

    assert _run(provider.load_access_token(oauth_token.access_token)) is None


# --- cliente confidencial ---


def test_cliente_confidencial_recebe_token_endpoint_auth_method_correto():
    provider, _ = _provider(client_secret=FAKE_CLIENT_SECRET)

    cliente = _run(provider.get_client(FAKE_CLIENT_ID))

    assert cliente.token_endpoint_auth_method == "client_secret_post"
    assert cliente.client_secret == FAKE_CLIENT_SECRET


# --- seguranca ---


def test_nenhum_segredo_ou_token_e_impresso(capsys):
    provider, _ = _provider(client_secret=FAKE_CLIENT_SECRET)
    cliente = _run(provider.get_client(FAKE_CLIENT_ID))
    code = _emitir_authorization_code(provider, cliente)
    auth_code = _run(provider.load_authorization_code(cliente, code))
    oauth_token = _run(provider.exchange_authorization_code(cliente, auth_code))

    captured = capsys.readouterr()
    assert FAKE_CLIENT_SECRET not in captured.out
    assert code not in captured.out
    assert oauth_token.access_token not in captured.out
    assert oauth_token.refresh_token not in captured.out
    assert FAKE_CLIENT_SECRET not in captured.err
    assert code not in captured.err


def test_nenhuma_chamada_de_rede(monkeypatch):
    # Bloqueia so conexoes externas; loopback e liberado porque o
    # proprio asyncio.run() do Windows usa socket.socketpair() (via
    # connect() em 127.0.0.1) como mecanismo interno do event loop,
    # sem nenhuma relacao com rede externa (mesma situacao ja tratada
    # na Etapa 6C).
    import socket

    conectar_original = socket.socket.connect

    def bloquear_rede_externa(self, endereco, *args, **kwargs):
        host = endereco[0] if isinstance(endereco, tuple) else str(endereco)
        if host not in ("127.0.0.1", "::1", "localhost"):
            raise AssertionError(f"conexao externa bloqueada: {endereco!r}")
        return conectar_original(self, endereco, *args, **kwargs)

    monkeypatch.setattr(socket.socket, "connect", bloquear_rede_externa)

    provider, _ = _provider()
    cliente = _run(provider.get_client(FAKE_CLIENT_ID))
    code = _emitir_authorization_code(provider, cliente)
    auth_code = _run(provider.load_authorization_code(cliente, code))
    oauth_token = _run(provider.exchange_authorization_code(cliente, auth_code))
    refresh_token_obj = _run(provider.load_refresh_token(cliente, oauth_token.refresh_token))
    _run(provider.exchange_refresh_token(cliente, refresh_token_obj, []))
