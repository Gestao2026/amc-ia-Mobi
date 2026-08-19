"""
Testes do backend da ponte HTTPS (Render -> HostGator -> MySQL local).

NENHUM teste aqui acessa a ponte real, a HostGator, o MySQL ou
qualquer rede:
- o `PonteCredentialBackend` REAL recebe um `httpx2.MockTransport`, que
  intercepta a requisicao dentro do proprio httpx2. O codigo de
  producao roda inteiro (cabecalhos, corpo, tratamento de erro), mas
  nenhum pacote sai da maquina;
- `PonteFalsa` implementa o MESMO contrato que o token.php precisa
  cumprir, com um dicionario no lugar do MySQL. Ela serve como
  especificacao executavel do lado PHP: se o token.php se comportar
  como ela, a ponte funciona;
- as chaves de cifragem sao geradas na hora e nunca saem do teste;
- os demais valores sao ficticios, com o prefixo FAKE_, e o dominio
  usado e `.invalid` (RFC 2606), que nunca resolve na internet real.
"""

import json
import socket

import httpx2
import pytest

from mcp_linkedin.auth_linkedin.crypto import TokenCipher, generate_key_base64
from mcp_linkedin.auth_linkedin.ponte_backend import (
    CABECALHO_SEGREDO,
    PonteCredentialBackend,
)
from mcp_linkedin.auth_linkedin.runtime import build_credential_backend
from mcp_linkedin.auth_linkedin.token_store import (
    TARGET_NAME,
    EncryptedCredentialBackend,
    TokenStore,
    TokenStoreBackendError,
)
from mcp_linkedin.config import (
    TOKEN_STORE_BACKEND_PONTE,
    InvalidLinkedInConfigError,
    resolve_linkedin_config,
)

FAKE_PONTE_URL = "https://ponte.invalid/token.php"
FAKE_PONTE_SECRET = "FAKE_PONTE_SECRET_NAO_REAL"
FAKE_ACCESS_TOKEN = "FAKE_ACCESS_TOKEN_NAO_REAL"
FAKE_CLIENT_ID = "FAKE_LINKEDIN_CLIENT_ID_NAO_REAL"
FAKE_CLIENT_SECRET = "FAKE_LINKEDIN_CLIENT_SECRET_NAO_REAL"
FAKE_BASE_URL = "https://mcp-linkedin.invalid"


def _backend(handler) -> PonteCredentialBackend:
    """O backend REAL, com o transporte interno do httpx2 trocado por um mock."""
    return PonteCredentialBackend(
        url=FAKE_PONTE_URL,
        secret=FAKE_PONTE_SECRET,
        httpx_transport=httpx2.MockTransport(handler),
    )


def _env_ponte(**overrides) -> dict:
    env = {
        "LINKEDIN_CLIENT_ID": FAKE_CLIENT_ID,
        "LINKEDIN_CLIENT_SECRET": FAKE_CLIENT_SECRET,
        "MCP_PUBLIC_BASE_URL": FAKE_BASE_URL,
        "LINKEDIN_TOKEN_STORE_BACKEND": "ponte",
        "MCP_LINKEDIN_PONTE_URL": FAKE_PONTE_URL,
        "MCP_LINKEDIN_PONTE_SECRET": FAKE_PONTE_SECRET,
        "LINKEDIN_TOKEN_ENCRYPTION_KEY": generate_key_base64(),
    }
    env.update({c: v for c, v in overrides.items() if v is not None})
    return env


class PonteFalsa:
    """
    Especificacao executavel do token.php: mesmo contrato de entrada e
    saida, com um dicionario no lugar do MySQL.

    Se o token.php responder como esta classe, a ponte funciona. Todo
    comportamento exercitado aqui e comportamento que o PHP precisa ter.
    """

    def __init__(self, segredo=FAKE_PONTE_SECRET, alvo_esperado=TARGET_NAME):
        self._segredo = segredo
        self._alvo_esperado = alvo_esperado
        self.armazenado: dict[str, str] = {}
        self.requisicoes: list[dict] = []

    def __call__(self, request):
        self.requisicoes.append(
            {
                "url": str(request.url),
                "method": request.method,
                "headers": dict(request.headers),
                "corpo": request.content.decode(),
            }
        )

        # 1. so POST
        if request.method != "POST":
            return httpx2.Response(405, text=json.dumps({"status": "erro"}))

        # 2. segredo, em tempo constante no PHP (hash_equals)
        recebido = request.headers.get(CABECALHO_SEGREDO.lower(), "")
        if not recebido:
            auth = request.headers.get("authorization", "")
            if auth.startswith("Bearer "):
                recebido = auth[7:]
        if recebido != self._segredo:
            return httpx2.Response(401, text=json.dumps({"status": "erro"}))

        entrada = json.loads(request.content)

        # 3. alvo fixo: a ponte nao e armazenamento generico
        if entrada.get("alvo") != self._alvo_esperado:
            return httpx2.Response(400, text=json.dumps({"status": "erro"}))

        acao = entrada.get("acao")

        if acao == "ler":
            valor = self.armazenado.get(entrada["alvo"])
            if not valor:
                return httpx2.Response(200, text=json.dumps({"status": "vazio"}))
            return httpx2.Response(200, text=json.dumps({"status": "ok", "secret": valor}))

        if acao == "gravar":
            segredo = entrada.get("secret")
            if not isinstance(segredo, str) or not segredo:
                return httpx2.Response(400, text=json.dumps({"status": "erro"}))
            self.armazenado[entrada["alvo"]] = segredo
            return httpx2.Response(200, text=json.dumps({"status": "ok"}))

        if acao == "excluir":
            self.armazenado.pop(entrada["alvo"], None)
            return httpx2.Response(200, text=json.dumps({"status": "ok"}))

        return httpx2.Response(400, text=json.dumps({"status": "erro"}))


# =====================================================================
# Contrato da ponte
# =====================================================================


def test_gravacao_envia_acao_alvo_e_segredo():
    ponte = PonteFalsa()

    _backend(ponte).write(TARGET_NAME, "cifrado-ficticio")

    corpo = json.loads(ponte.requisicoes[0]["corpo"])
    assert corpo == {"acao": "gravar", "alvo": TARGET_NAME, "secret": "cifrado-ficticio"}
    assert ponte.requisicoes[0]["method"] == "POST"


def test_leitura_devolve_o_que_foi_gravado():
    ponte = PonteFalsa()
    backend = _backend(ponte)

    backend.write(TARGET_NAME, "cifrado-ficticio")

    assert backend.read(TARGET_NAME) == "cifrado-ficticio"


def test_leitura_sem_nada_gravado_devolve_none():
    assert _backend(PonteFalsa()).read(TARGET_NAME) is None


def test_exclusao_remove_o_valor():
    ponte = PonteFalsa()
    backend = _backend(ponte)
    backend.write(TARGET_NAME, "cifrado-ficticio")

    backend.delete(TARGET_NAME)

    assert backend.read(TARGET_NAME) is None


def test_exclusao_do_que_nao_existe_nao_e_erro():
    _backend(PonteFalsa()).delete(TARGET_NAME)


def test_gravacao_repetida_substitui():
    ponte = PonteFalsa()
    backend = _backend(ponte)

    backend.write(TARGET_NAME, "primeiro")
    backend.write(TARGET_NAME, "segundo")

    assert backend.read(TARGET_NAME) == "segundo"


# =====================================================================
# Autenticacao
# =====================================================================


def test_segredo_vai_em_cabecalho_nunca_na_url_nem_no_corpo():
    ponte = PonteFalsa()

    _backend(ponte).write(TARGET_NAME, "cifrado-ficticio")

    requisicao = ponte.requisicoes[0]
    assert requisicao["headers"][CABECALHO_SEGREDO.lower()] == FAKE_PONTE_SECRET
    assert FAKE_PONTE_SECRET not in requisicao["url"]
    assert FAKE_PONTE_SECRET not in requisicao["corpo"]


def test_segredo_tambem_vai_como_bearer():
    # Redundancia proposital: em hospedagem compartilhada, ora um
    # cabecalho chega, ora o outro.
    ponte = PonteFalsa()

    _backend(ponte).write(TARGET_NAME, "cifrado-ficticio")

    assert ponte.requisicoes[0]["headers"]["authorization"] == f"Bearer {FAKE_PONTE_SECRET}"


def test_ponte_com_segredo_errado_recusa():
    ponte = PonteFalsa(segredo="FAKE_OUTRO_SEGREDO")

    with pytest.raises(TokenStoreBackendError):
        _backend(ponte).read(TARGET_NAME)


def test_alvo_diferente_do_esperado_e_recusado():
    # A ponte nao serve como armazenamento generico.
    ponte = PonteFalsa()

    with pytest.raises(TokenStoreBackendError):
        _backend(ponte).read("outro-alvo-qualquer")


# =====================================================================
# Erros
# =====================================================================


@pytest.mark.parametrize("status", [400, 401, 403, 404, 500, 502])
def test_status_de_erro_vira_erro_de_backend(status):
    def handler(request):
        return httpx2.Response(status, text=json.dumps({"status": "erro"}))

    with pytest.raises(TokenStoreBackendError):
        _backend(handler).read(TARGET_NAME)


def test_redirecionamento_e_recusado():
    hosts = []

    def handler(request):
        hosts.append(request.url.host)
        if request.url.host != "ponte.invalid":
            raise AssertionError(f"host inesperado contatado: {request.url.host}")
        return httpx2.Response(302, headers={"location": "https://atacante.invalid/roubo"}, text="")

    with pytest.raises(TokenStoreBackendError):
        _backend(handler).read(TARGET_NAME)

    # O host do atacante nunca recebe os cabecalhos com o segredo.
    assert hosts == ["ponte.invalid"]


def test_timeout_vira_erro_de_backend():
    def handler(request):
        raise httpx2.TimeoutException("simulado", request=request)

    with pytest.raises(TokenStoreBackendError):
        _backend(handler).read(TARGET_NAME)


def test_falha_de_rede_vira_erro_de_backend():
    def handler(request):
        raise httpx2.ConnectError("simulado", request=request)

    with pytest.raises(TokenStoreBackendError):
        _backend(handler).read(TARGET_NAME)


def test_resposta_nao_json_vira_erro_de_backend():
    def handler(request):
        return httpx2.Response(200, text="<html>pagina de erro da hospedagem</html>")

    with pytest.raises(TokenStoreBackendError):
        _backend(handler).read(TARGET_NAME)


def test_status_inesperado_no_corpo_vira_erro():
    def handler(request):
        return httpx2.Response(200, text=json.dumps({"status": "sei-la"}))

    with pytest.raises(TokenStoreBackendError):
        _backend(handler).read(TARGET_NAME)


def test_erro_nunca_expoe_segredo_nem_conteudo():
    def handler(request):
        raise httpx2.ConnectError("simulado", request=request)

    with pytest.raises(TokenStoreBackendError) as excinfo:
        _backend(handler).write(TARGET_NAME, FAKE_ACCESS_TOKEN)

    assert FAKE_PONTE_SECRET not in str(excinfo.value)
    assert FAKE_ACCESS_TOKEN not in str(excinfo.value)
    # `from None` corta o encadeamento: o Request do httpx2, que carrega
    # os cabecalhos com o segredo, nao viaja no traceback.
    assert excinfo.value.__cause__ is None


def test_corpo_de_erro_da_ponte_nao_vaza_para_a_mensagem():
    def handler(request):
        return httpx2.Response(500, text="stack trace do php com caminho e usuario do banco")

    with pytest.raises(TokenStoreBackendError) as excinfo:
        _backend(handler).read(TARGET_NAME)

    assert "stack trace" not in str(excinfo.value)


def test_repr_nao_expoe_o_segredo():
    assert FAKE_PONTE_SECRET not in repr(_backend(PonteFalsa()))


# =====================================================================
# AES-GCM continua valendo: o PHP so ve texto cifrado
# =====================================================================


def test_ciphertext_e_o_unico_conteudo_que_chega_na_ponte():
    ponte = PonteFalsa()
    cipher = TokenCipher.from_base64_key(generate_key_base64())
    backend = EncryptedCredentialBackend(inner=_backend(ponte), cipher=cipher)

    backend.write(TARGET_NAME, FAKE_ACCESS_TOKEN)

    # Nem no corpo da requisicao, nem no "banco" da ponte.
    assert FAKE_ACCESS_TOKEN not in ponte.requisicoes[0]["corpo"]
    assert FAKE_ACCESS_TOKEN not in ponte.armazenado[TARGET_NAME]


def test_ciclo_completo_cifrado_pela_ponte():
    ponte = PonteFalsa()
    cipher = TokenCipher.from_base64_key(generate_key_base64())
    store = TokenStore(
        backend=EncryptedCredentialBackend(inner=_backend(ponte), cipher=cipher),
        clock=lambda: 1000.0,
    )

    store.save_access_token(FAKE_ACCESS_TOKEN, expires_at=2000.0)

    assert store.get_access_token() == FAKE_ACCESS_TOKEN
    assert store.has_valid_token() is True
    # O expires_at tambem fica dentro do envelope.
    assert "expires_at" not in ponte.armazenado[TARGET_NAME]


def test_a_ponte_nunca_recebe_a_chave_aes():
    ponte = PonteFalsa()
    chave = generate_key_base64()
    backend = EncryptedCredentialBackend(
        inner=_backend(ponte), cipher=TokenCipher.from_base64_key(chave)
    )

    backend.write(TARGET_NAME, FAKE_ACCESS_TOKEN)
    backend.read(TARGET_NAME)

    for requisicao in ponte.requisicoes:
        assert chave not in requisicao["corpo"]
        assert chave not in json.dumps(requisicao["headers"])
        assert chave not in requisicao["url"]


def test_quem_tem_o_banco_da_ponte_nao_consegue_ler_o_token():
    # Simula o comprometimento total da HostGator: o atacante tem tudo
    # o que a ponte guardou, mas nao a chave, que so existe no Render.
    ponte = PonteFalsa()
    backend = EncryptedCredentialBackend(
        inner=_backend(ponte), cipher=TokenCipher.from_base64_key(generate_key_base64())
    )
    backend.write(TARGET_NAME, FAKE_ACCESS_TOKEN)

    conteudo_roubado = ponte.armazenado[TARGET_NAME]
    outra_chave = TokenCipher.from_base64_key(generate_key_base64())

    from mcp_linkedin.auth_linkedin.crypto import TokenDecryptionError

    with pytest.raises(TokenDecryptionError):
        outra_chave.decrypt(conteudo_roubado)


# =====================================================================
# Configuracao
# =====================================================================


def test_configuracao_da_ponte_e_resolvida():
    config = resolve_linkedin_config(env=_env_ponte())

    assert config.token_store_backend == TOKEN_STORE_BACKEND_PONTE
    assert config.ponte_url == FAKE_PONTE_URL


@pytest.mark.parametrize(
    "faltante", ["MCP_LINKEDIN_PONTE_URL", "MCP_LINKEDIN_PONTE_SECRET", "LINKEDIN_TOKEN_ENCRYPTION_KEY"]
)
def test_ponte_sem_variavel_obrigatoria_falha_na_inicializacao(faltante):
    env = _env_ponte()
    del env[faltante]

    with pytest.raises(InvalidLinkedInConfigError) as excinfo:
        resolve_linkedin_config(env=env)

    assert faltante in str(excinfo.value)


@pytest.mark.parametrize(
    "url", ["http://ponte.invalid/token.php", "HTTP://ponte.invalid/token.php", "ftp://ponte.invalid"]
)
def test_url_sem_https_e_recusada(url):
    # O envelope protege o token, mas o segredo da ponte viaja em
    # cabecalho: em HTTP simples iria em claro pela internet.
    with pytest.raises(InvalidLinkedInConfigError) as excinfo:
        resolve_linkedin_config(env=_env_ponte(MCP_LINKEDIN_PONTE_URL=url))

    assert "https" in str(excinfo.value).lower()


def test_https_maiusculo_e_aceito():
    config = resolve_linkedin_config(env=_env_ponte(MCP_LINKEDIN_PONTE_URL="HTTPS://ponte.invalid/t.php"))

    assert config.ponte_url == "HTTPS://ponte.invalid/t.php"


def test_chave_de_cifragem_invalida_falha_na_inicializacao():
    with pytest.raises(InvalidLinkedInConfigError):
        resolve_linkedin_config(env=_env_ponte(LINKEDIN_TOKEN_ENCRYPTION_KEY="chave-curta"))


def test_repr_da_configuracao_mascara_o_segredo_da_ponte():
    config = resolve_linkedin_config(env=_env_ponte())
    texto = repr(config)

    assert FAKE_PONTE_SECRET not in texto
    assert config.token_encryption_key not in texto
    assert FAKE_CLIENT_SECRET not in texto


def test_senha_do_mysql_nao_e_variavel_do_render():
    # Nesta arquitetura o Render nunca fala com o MySQL: a senha do
    # banco existe so no config.php da HostGator.
    from mcp_linkedin.config import REQUIRED_PONTE_ENV_VARS

    assert not any("MYSQL" in nome or "DB_PASS" in nome for nome in REQUIRED_PONTE_ENV_VARS)


# =====================================================================
# Montagem pelo runtime
# =====================================================================


def test_runtime_monta_backend_cifrado_sobre_a_ponte(monkeypatch):
    monkeypatch.setattr(
        socket.socket,
        "connect",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("montar backend nao deve abrir conexao")),
    )

    backend = build_credential_backend(resolve_linkedin_config(env=_env_ponte()))

    assert isinstance(backend, EncryptedCredentialBackend)
    assert isinstance(backend._inner, PonteCredentialBackend)


def test_backend_supabase_continua_disponivel():
    # Regra desta rodada: nao remover o backend do Supabase.
    from mcp_linkedin.auth_linkedin.supabase_backend import SupabaseCredentialBackend
    from mcp_linkedin.config import TOKEN_STORE_BACKEND_SUPABASE, VALID_TOKEN_STORE_BACKENDS

    assert TOKEN_STORE_BACKEND_SUPABASE in VALID_TOKEN_STORE_BACKENDS
    assert SupabaseCredentialBackend is not None


def test_nenhuma_chamada_de_rede_em_todo_o_fluxo(monkeypatch):
    monkeypatch.setattr(
        socket.socket,
        "connect",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("nenhum teste deve abrir conexao")),
    )

    ponte = PonteFalsa()
    backend = EncryptedCredentialBackend(
        inner=_backend(ponte), cipher=TokenCipher.from_base64_key(generate_key_base64())
    )
    backend.write(TARGET_NAME, FAKE_ACCESS_TOKEN)
    backend.read(TARGET_NAME)
    backend.delete(TARGET_NAME)


def test_nenhum_segredo_aparece_em_stdout_stderr(capsys):
    ponte = PonteFalsa()
    backend = EncryptedCredentialBackend(
        inner=_backend(ponte), cipher=TokenCipher.from_base64_key(generate_key_base64())
    )
    backend.write(TARGET_NAME, FAKE_ACCESS_TOKEN)
    backend.read(TARGET_NAME)

    captured = capsys.readouterr()
    for segredo in (FAKE_PONTE_SECRET, FAKE_ACCESS_TOKEN):
        assert segredo not in captured.out
        assert segredo not in captured.err


def test_valores_ficticios_sao_claramente_marcados():
    assert FAKE_PONTE_SECRET.startswith("FAKE_")
    assert FAKE_ACCESS_TOKEN.startswith("FAKE_")
    assert FAKE_PONTE_URL.startswith("https://") and ".invalid" in FAKE_PONTE_URL
