"""
Testes do TokenStore (armazenamento seguro local do access token do
Instagram).

Todos os testes usam um backend falso em memoria (FakeCredentialBackend)
injetado no TokenStore. Nenhum teste toca o Windows Credential Manager
real da maquina (Win32CredentialBackend nunca e instanciado aqui),
nenhum grava em arquivo, nenhum acessa rede, nenhum usa access token,
Client ID ou Client Secret reais do Instagram.
"""

import pytest

from mcp_instagram.auth_instagram.token_store import TARGET_NAME, TokenStore

FAKE_ACCESS_TOKEN = "FAKE_ACCESS_TOKEN_NAO_REAL_abc123"


class FakeCredentialBackend:
    """Backend em memoria para teste. Nunca grava no Credential Manager real."""

    def __init__(self):
        self.calls = []
        self._store = {}

    def write(self, target_name, secret):
        self.calls.append(("write", target_name))
        self._store[target_name] = secret

    def read(self, target_name):
        self.calls.append(("read", target_name))
        return self._store.get(target_name)

    def delete(self, target_name):
        self.calls.append(("delete", target_name))
        self._store.pop(target_name, None)


class BackendComErro:
    """Backend que sempre falha, para testar propagacao de erro do Credential Manager."""

    def write(self, target_name, secret):
        raise RuntimeError("falha simulada de Credential Manager")

    def read(self, target_name):
        raise RuntimeError("falha simulada de Credential Manager")

    def delete(self, target_name):
        raise RuntimeError("falha simulada de Credential Manager")


class FakeClock:
    """Relogio controlavel manualmente, para testes deterministicos."""

    def __init__(self, start: float = 0.0):
        self._now = start

    def __call__(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        self._now += seconds


def _store(clock=None):
    backend = FakeCredentialBackend()
    store = TokenStore(backend=backend, clock=clock or FakeClock())
    return store, backend


def test_salvar_e_recuperar_token_ficticio():
    store, _ = _store()
    store.save_access_token(FAKE_ACCESS_TOKEN, expires_at=1000.0)

    assert store.get_access_token() == FAKE_ACCESS_TOKEN


def test_metadados_sao_recuperados_corretamente():
    store, _ = _store()
    store.save_access_token(FAKE_ACCESS_TOKEN, expires_at=1234.0)

    metadata = store.get_token_metadata()

    assert metadata is not None
    assert metadata.expires_at == 1234.0


def test_token_valido_quando_dentro_da_validade():
    clock = FakeClock(start=1000.0)
    store, _ = _store(clock=clock)
    store.save_access_token(FAKE_ACCESS_TOKEN, expires_at=2000.0)

    assert store.has_valid_token() is True


def test_token_invalido_quando_expirado():
    clock = FakeClock(start=2000.0)
    store, _ = _store(clock=clock)
    store.save_access_token(FAKE_ACCESS_TOKEN, expires_at=1000.0)

    assert store.has_valid_token() is False


def test_token_no_limite_exato_de_expiracao_e_invalido():
    clock = FakeClock(start=1000.0)
    store, _ = _store(clock=clock)
    store.save_access_token(FAKE_ACCESS_TOKEN, expires_at=1000.0)

    # expires_at <= agora deve ser tratado como invalido.
    assert store.has_valid_token() is False


def test_token_inexistente_e_invalido():
    store, _ = _store()

    assert store.has_valid_token() is False
    assert store.get_access_token() is None
    assert store.get_token_metadata() is None


def test_excluir_token():
    store, _ = _store()
    store.save_access_token(FAKE_ACCESS_TOKEN, expires_at=1000.0)

    store.delete_access_token()

    assert store.get_access_token() is None
    assert store.has_valid_token() is False


def test_token_expirado_permanece_apos_has_valid_token_mas_nao_e_valido():
    # Esta etapa nao exclui automaticamente token expirado; documenta
    # esse comportamento em teste, conforme decisao registrada.
    clock = FakeClock(start=2000.0)
    store, backend = _store(clock=clock)
    store.save_access_token(FAKE_ACCESS_TOKEN, expires_at=1000.0)

    assert store.has_valid_token() is False
    assert store.get_access_token() == FAKE_ACCESS_TOKEN


def test_token_nao_e_escrito_em_arquivo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    store, _ = _store()

    store.save_access_token(FAKE_ACCESS_TOKEN, expires_at=1000.0)

    arquivos = list(tmp_path.rglob("*"))
    assert arquivos == []


def test_nenhuma_chamada_de_rede_ocorre(monkeypatch):
    import socket

    def bloquear_rede(*args, **kwargs):
        raise AssertionError("token_store nao deve abrir conexao de rede")

    monkeypatch.setattr(socket.socket, "connect", bloquear_rede)

    store, _ = _store()
    store.save_access_token(FAKE_ACCESS_TOKEN, expires_at=1000.0)
    store.get_access_token()
    store.has_valid_token()
    store.delete_access_token()


def test_comportamento_quando_backend_retorna_erro():
    store = TokenStore(backend=BackendComErro(), clock=FakeClock())

    with pytest.raises(RuntimeError):
        store.save_access_token(FAKE_ACCESS_TOKEN, expires_at=1000.0)


def test_nenhuma_funcao_imprime_o_token(capsys):
    store, _ = _store()
    store.save_access_token(FAKE_ACCESS_TOKEN, expires_at=99999.0)

    store.get_access_token()
    store.get_token_metadata()
    store.has_valid_token()
    store.delete_access_token()

    captured = capsys.readouterr()
    assert FAKE_ACCESS_TOKEN not in captured.out
    assert FAKE_ACCESS_TOKEN not in captured.err


def test_nenhuma_funcao_inclui_o_token_em_excecao():
    store = TokenStore(backend=BackendComErro(), clock=FakeClock())

    with pytest.raises(RuntimeError) as excinfo:
        store.save_access_token(FAKE_ACCESS_TOKEN, expires_at=1000.0)

    assert FAKE_ACCESS_TOKEN not in str(excinfo.value)


def test_target_name_padrao_e_especifico_do_componente():
    assert TARGET_NAME == "mcp-instagram:instagram-access-token"


def test_nenhum_client_secret_e_armazenado_junto_com_o_token():
    store, backend = _store()
    store.save_access_token(FAKE_ACCESS_TOKEN, expires_at=1000.0)

    segredo_gravado = backend._store[TARGET_NAME]
    assert "client_secret" not in segredo_gravado.lower()
