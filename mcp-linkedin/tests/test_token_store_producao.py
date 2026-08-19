"""
Testes do backend de producao do TokenStore: cifragem em envelope
(crypto.py), armazenamento no Supabase (supabase_backend.py), a
composicao dos dois (EncryptedCredentialBackend) e a configuracao que
os liga.

NENHUM teste aqui acessa o Supabase real, o LinkedIn ou qualquer rede:
- o SupabaseCredentialBackend recebe um `httpx2.MockTransport`, que
  intercepta a requisicao dentro do proprio httpx2 e devolve uma
  resposta sintetica. O codigo de producao roda inteiro (montagem de
  cabecalhos, URL, tratamento de erro), mas nenhum pacote sai da
  maquina;
- as chaves de cifragem sao geradas na hora, para o teste, e nunca
  saem dele;
- os demais valores sao ficticios, com o prefixo FAKE_;
- varios testes bloqueiam ativamente qualquer conexao de socket.
"""

import base64
import json
import socket

import httpx2
import pytest

from mcp_linkedin.auth_linkedin.crypto import (
    KEY_SIZE_BYTES,
    NONCE_SIZE_BYTES,
    InvalidEncryptionKeyError,
    TokenCipher,
    TokenDecryptionError,
    generate_key_base64,
)
from mcp_linkedin.auth_linkedin.runtime import build_credential_backend
from mcp_linkedin.auth_linkedin.supabase_backend import (
    COLUNA_ALVO,
    COLUNA_SEGREDO,
    DEFAULT_TABLE,
    SupabaseCredentialBackend,
    TokenStoreBackendError,
)
from mcp_linkedin.auth_linkedin.token_store import (
    TARGET_NAME,
    EncryptedCredentialBackend,
    InMemoryCredentialBackend,
    TokenStore,
)
from mcp_linkedin.config import (
    TOKEN_STORE_BACKEND_SUPABASE,
    InvalidLinkedInConfigError,
    resolve_linkedin_config,
)

FAKE_ACCESS_TOKEN = "FAKE_ACCESS_TOKEN_NAO_REAL"
FAKE_SUPABASE_KEY = "FAKE_SUPABASE_SERVICE_KEY_NAO_REAL"
FAKE_SUPABASE_URL = "https://projeto-ficticio.invalid"
FAKE_CLIENT_ID = "FAKE_LINKEDIN_CLIENT_ID_NAO_REAL"
FAKE_CLIENT_SECRET = "FAKE_LINKEDIN_CLIENT_SECRET_NAO_REAL"
FAKE_BASE_URL = "https://mcp-linkedin.invalid"


def _chave() -> str:
    return generate_key_base64()


def _cipher() -> TokenCipher:
    return TokenCipher.from_base64_key(_chave())


def _env_supabase(**overrides) -> dict:
    env = {
        "LINKEDIN_CLIENT_ID": FAKE_CLIENT_ID,
        "LINKEDIN_CLIENT_SECRET": FAKE_CLIENT_SECRET,
        "MCP_PUBLIC_BASE_URL": FAKE_BASE_URL,
        "LINKEDIN_TOKEN_STORE_BACKEND": "supabase",
        "MCP_LINKEDIN_SUPABASE_URL": FAKE_SUPABASE_URL,
        "MCP_LINKEDIN_SUPABASE_KEY": FAKE_SUPABASE_KEY,
        "LINKEDIN_TOKEN_ENCRYPTION_KEY": _chave(),
    }
    env.update({c: v for c, v in overrides.items() if v is not None})
    return env


def _backend_supabase(handler, table=DEFAULT_TABLE) -> SupabaseCredentialBackend:
    """O backend REAL, com o transporte interno do httpx2 trocado por um mock."""
    return SupabaseCredentialBackend(
        base_url=FAKE_SUPABASE_URL,
        api_key=FAKE_SUPABASE_KEY,
        table=table,
        httpx_transport=httpx2.MockTransport(handler),
    )


# =====================================================================
# crypto.py: cifragem em envelope
# =====================================================================


def test_ciclo_completo_cifrar_e_decifrar():
    cipher = _cipher()

    assert cipher.decrypt(cipher.encrypt(FAKE_ACCESS_TOKEN)) == FAKE_ACCESS_TOKEN


def test_texto_cifrado_nao_contem_o_texto_claro():
    cifrado = _cipher().encrypt(FAKE_ACCESS_TOKEN)

    assert FAKE_ACCESS_TOKEN not in cifrado
    assert FAKE_ACCESS_TOKEN.encode() not in base64.b64decode(cifrado)


def test_duas_cifragens_do_mesmo_texto_sao_diferentes():
    # Nonce novo a cada operacao: repetir nonce com a mesma chave
    # quebraria a seguranca do GCM.
    cipher = _cipher()

    assert cipher.encrypt(FAKE_ACCESS_TOKEN) != cipher.encrypt(FAKE_ACCESS_TOKEN)


def test_chave_errada_nao_decifra():
    cifrado = _cipher().encrypt(FAKE_ACCESS_TOKEN)
    outra_chave = _cipher()

    with pytest.raises(TokenDecryptionError):
        outra_chave.decrypt(cifrado)


def test_texto_cifrado_adulterado_e_detectado():
    # AES-GCM e autenticado: adulteracao e detectada, nao silenciada.
    cipher = _cipher()
    bruto = bytearray(base64.b64decode(cipher.encrypt(FAKE_ACCESS_TOKEN)))
    bruto[-1] ^= 0x01

    with pytest.raises(TokenDecryptionError):
        cipher.decrypt(base64.b64encode(bytes(bruto)).decode())


def test_texto_cifrado_truncado_e_rejeitado():
    cipher = _cipher()
    truncado = base64.b64encode(b"x" * (NONCE_SIZE_BYTES - 1)).decode()

    with pytest.raises(TokenDecryptionError):
        cipher.decrypt(truncado)


def test_valor_que_nao_e_base64_e_rejeitado():
    with pytest.raises(TokenDecryptionError):
        _cipher().decrypt("isto nao e base64 !!!")


def test_chave_de_tamanho_errado_e_rejeitada():
    with pytest.raises(InvalidEncryptionKeyError):
        TokenCipher(b"curta-demais")


def test_chave_fora_de_base64_e_rejeitada():
    with pytest.raises(InvalidEncryptionKeyError):
        TokenCipher.from_base64_key("nao e base64 !!!")


def test_chave_gerada_tem_o_tamanho_certo_e_funciona():
    chave = generate_key_base64()

    assert len(base64.b64decode(chave)) == KEY_SIZE_BYTES
    cipher = TokenCipher.from_base64_key(chave)
    assert cipher.decrypt(cipher.encrypt("x")) == "x"


def test_duas_chaves_geradas_sao_diferentes():
    assert generate_key_base64() != generate_key_base64()


def test_repr_do_cipher_nao_expoe_a_chave():
    chave = _chave()

    assert chave not in repr(TokenCipher.from_base64_key(chave))


def test_erros_de_cifragem_nao_expoem_segredo():
    chave = _chave()
    cifrado = TokenCipher.from_base64_key(chave).encrypt(FAKE_ACCESS_TOKEN)

    with pytest.raises(TokenDecryptionError) as excinfo:
        _cipher().decrypt(cifrado)

    assert chave not in str(excinfo.value)
    assert cifrado not in str(excinfo.value)
    assert FAKE_ACCESS_TOKEN not in str(excinfo.value)


def test_cifragem_nao_acessa_rede(monkeypatch):
    monkeypatch.setattr(
        socket.socket,
        "connect",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("crypto nao deve abrir conexao")),
    )

    cipher = _cipher()
    cipher.decrypt(cipher.encrypt(FAKE_ACCESS_TOKEN))


# =====================================================================
# EncryptedCredentialBackend
# =====================================================================


def test_backend_interno_nunca_ve_o_texto_claro():
    interno = InMemoryCredentialBackend()
    envelopado = EncryptedCredentialBackend(inner=interno, cipher=_cipher())

    envelopado.write("alvo", FAKE_ACCESS_TOKEN)

    assert interno.read("alvo") != FAKE_ACCESS_TOKEN
    assert FAKE_ACCESS_TOKEN not in interno.read("alvo")


def test_leitura_devolve_o_texto_claro():
    envelopado = EncryptedCredentialBackend(inner=InMemoryCredentialBackend(), cipher=_cipher())
    envelopado.write("alvo", FAKE_ACCESS_TOKEN)

    assert envelopado.read("alvo") == FAKE_ACCESS_TOKEN


def test_leitura_de_alvo_inexistente_devolve_none():
    envelopado = EncryptedCredentialBackend(inner=InMemoryCredentialBackend(), cipher=_cipher())

    assert envelopado.read("nunca-gravado") is None


def test_chave_trocada_faz_a_leitura_devolver_none():
    # Desfecho recuperavel: "nao ha token valido" leva o captador a
    # reautorizar, em vez de derrubar a ferramenta de status.
    interno = InMemoryCredentialBackend()
    EncryptedCredentialBackend(inner=interno, cipher=_cipher()).write("alvo", FAKE_ACCESS_TOKEN)

    depois_da_troca = EncryptedCredentialBackend(inner=interno, cipher=_cipher())

    assert depois_da_troca.read("alvo") is None


def test_exclusao_e_delegada_ao_backend_interno():
    interno = InMemoryCredentialBackend()
    envelopado = EncryptedCredentialBackend(inner=interno, cipher=_cipher())
    envelopado.write("alvo", FAKE_ACCESS_TOKEN)

    envelopado.delete("alvo")

    assert interno.read("alvo") is None


def test_token_store_completo_sobre_backend_cifrado():
    interno = InMemoryCredentialBackend()
    store = TokenStore(
        backend=EncryptedCredentialBackend(inner=interno, cipher=_cipher()),
        clock=lambda: 1000.0,
    )

    store.save_access_token(FAKE_ACCESS_TOKEN, expires_at=2000.0)

    assert store.get_access_token() == FAKE_ACCESS_TOKEN
    assert store.has_valid_token() is True
    # O expires_at tambem fica dentro do envelope: o que o backend
    # interno guarda nao e JSON legivel.
    assert "expires_at" not in interno.read(TARGET_NAME)


def test_repr_do_backend_cifrado_nao_expoe_segredo():
    envelopado = EncryptedCredentialBackend(inner=InMemoryCredentialBackend(), cipher=_cipher())
    envelopado.write("alvo", FAKE_ACCESS_TOKEN)

    assert FAKE_ACCESS_TOKEN not in repr(envelopado)


# =====================================================================
# SupabaseCredentialBackend (codigo real, sem rede)
# =====================================================================


def test_gravacao_usa_upsert():
    capturado = {}

    def handler(request):
        capturado["method"] = request.method
        capturado["prefer"] = request.headers.get("Prefer")
        capturado["corpo"] = json.loads(request.content)
        return httpx2.Response(201, text="[]")

    _backend_supabase(handler).write("alvo", "cifrado-ficticio")

    assert capturado["method"] == "POST"
    assert capturado["prefer"] == "resolution=merge-duplicates"
    assert capturado["corpo"] == [{COLUNA_ALVO: "alvo", COLUNA_SEGREDO: "cifrado-ficticio"}]


def test_chave_de_api_vai_em_cabecalho_nunca_na_url():
    capturado = {}

    def handler(request):
        capturado["url"] = str(request.url)
        capturado["apikey"] = request.headers.get("apikey")
        capturado["auth"] = request.headers.get("Authorization")
        return httpx2.Response(201, text="[]")

    _backend_supabase(handler).write("alvo", "cifrado-ficticio")

    assert FAKE_SUPABASE_KEY not in capturado["url"]
    assert capturado["apikey"] == FAKE_SUPABASE_KEY
    assert capturado["auth"] == f"Bearer {FAKE_SUPABASE_KEY}"


def test_leitura_devolve_o_segredo_gravado():
    def handler(request):
        return httpx2.Response(200, text=json.dumps([{COLUNA_SEGREDO: "cifrado-ficticio"}]))

    assert _backend_supabase(handler).read("alvo") == "cifrado-ficticio"


def test_leitura_de_alvo_inexistente_devolve_none():
    def handler(request):
        return httpx2.Response(200, text="[]")

    assert _backend_supabase(handler).read("alvo") is None


def test_leitura_filtra_pelo_alvo_certo():
    capturado = {}

    def handler(request):
        capturado["url"] = str(request.url)
        return httpx2.Response(200, text="[]")

    _backend_supabase(handler).read(TARGET_NAME)

    assert f"{COLUNA_ALVO}=eq." in capturado["url"]
    # TARGET_NAME contem ':', que precisa ser codificado na query.
    assert "mcp-linkedin%3Alinkedin-access-token" in capturado["url"]


def test_exclusao_usa_delete():
    capturado = {}

    def handler(request):
        capturado["method"] = request.method
        return httpx2.Response(204, text="")

    _backend_supabase(handler).delete("alvo")

    assert capturado["method"] == "DELETE"


def test_tabela_e_configuravel():
    capturado = {}

    def handler(request):
        capturado["url"] = str(request.url)
        return httpx2.Response(200, text="[]")

    _backend_supabase(handler, table="outra_tabela").read("alvo")

    assert "/rest/v1/outra_tabela" in capturado["url"]


@pytest.mark.parametrize("status", [400, 401, 403, 404, 500])
def test_erro_http_vira_erro_de_backend(status):
    def handler(request):
        return httpx2.Response(status, text="detalhe interno do postgrest")

    with pytest.raises(TokenStoreBackendError):
        _backend_supabase(handler).write("alvo", "cifrado-ficticio")


def test_corpo_da_resposta_de_erro_nao_vaza_para_a_mensagem():
    def handler(request):
        return httpx2.Response(400, text="detalhe interno que pode ecoar o dado enviado")

    with pytest.raises(TokenStoreBackendError) as excinfo:
        _backend_supabase(handler).write("alvo", "cifrado-ficticio")

    assert "detalhe interno" not in str(excinfo.value)


def test_timeout_vira_erro_de_backend():
    def handler(request):
        raise httpx2.TimeoutException("simulado", request=request)

    with pytest.raises(TokenStoreBackendError):
        _backend_supabase(handler).read("alvo")


def test_falha_de_rede_vira_erro_de_backend():
    def handler(request):
        raise httpx2.ConnectError("simulado", request=request)

    with pytest.raises(TokenStoreBackendError):
        _backend_supabase(handler).read("alvo")


def test_erro_de_backend_nao_expoe_chave_nem_segredo():
    def handler(request):
        raise httpx2.ConnectError("simulado", request=request)

    with pytest.raises(TokenStoreBackendError) as excinfo:
        _backend_supabase(handler).write("alvo", FAKE_ACCESS_TOKEN)

    assert FAKE_SUPABASE_KEY not in str(excinfo.value)
    assert FAKE_ACCESS_TOKEN not in str(excinfo.value)
    # `from None` corta o encadeamento, entao o Request do httpx2 (que
    # carrega cabecalhos e corpo) nao viaja junto no traceback.
    assert excinfo.value.__cause__ is None


def test_resposta_nao_json_vira_erro_de_backend():
    def handler(request):
        return httpx2.Response(200, text="isto nao e json")

    with pytest.raises(TokenStoreBackendError):
        _backend_supabase(handler).read("alvo")


def test_repr_do_backend_supabase_nao_expoe_a_chave():
    def handler(request):
        return httpx2.Response(200, text="[]")

    assert FAKE_SUPABASE_KEY not in repr(_backend_supabase(handler))


def test_backend_supabase_nao_segue_redirecionamento():
    hosts_visitados = []

    def handler(request):
        hosts_visitados.append(request.url.host)
        if request.url.host != "projeto-ficticio.invalid":
            raise AssertionError(f"host inesperado contatado: {request.url.host}")
        return httpx2.Response(307, headers={"location": "https://atacante.invalid/roubo"}, text="")

    # Um redirecionamento nao e resposta valida: vira erro, e o host do
    # atacante nunca chega a ser contatado (a chave de API iria nos
    # cabecalhos da requisicao seguinte).
    with pytest.raises(TokenStoreBackendError):
        _backend_supabase(handler).read("alvo")

    assert hosts_visitados == ["projeto-ficticio.invalid"]


def test_fluxo_cifrado_de_ponta_a_ponta_sobre_o_supabase():
    """
    O caminho real de producao: TokenStore -> cifragem -> Supabase.
    O que trafega para o banco e sempre texto cifrado.
    """
    armazenado = {}

    def handler(request):
        if request.method == "POST":
            linha = json.loads(request.content)[0]
            armazenado[linha[COLUNA_ALVO]] = linha[COLUNA_SEGREDO]
            return httpx2.Response(201, text="[]")
        alvo = str(request.url).split(f"{COLUNA_ALVO}=eq.")[1].split("&")[0]
        from urllib.parse import unquote

        valor = armazenado.get(unquote(alvo))
        return httpx2.Response(200, text=json.dumps([{COLUNA_SEGREDO: valor}] if valor else []))

    store = TokenStore(
        backend=EncryptedCredentialBackend(inner=_backend_supabase(handler), cipher=_cipher()),
        clock=lambda: 1000.0,
    )

    store.save_access_token(FAKE_ACCESS_TOKEN, expires_at=2000.0)

    assert store.get_access_token() == FAKE_ACCESS_TOKEN
    assert store.has_valid_token() is True
    # O que ficou "no banco" e cifrado, nunca o token em claro.
    assert FAKE_ACCESS_TOKEN not in armazenado[TARGET_NAME]


# =====================================================================
# Configuracao do backend de producao
# =====================================================================


def test_configuracao_supabase_completa_e_resolvida():
    config = resolve_linkedin_config(env=_env_supabase())

    assert config.token_store_backend == TOKEN_STORE_BACKEND_SUPABASE
    assert config.supabase_url == FAKE_SUPABASE_URL
    assert config.supabase_key == FAKE_SUPABASE_KEY


@pytest.mark.parametrize(
    "faltante",
    ["MCP_LINKEDIN_SUPABASE_URL", "MCP_LINKEDIN_SUPABASE_KEY", "LINKEDIN_TOKEN_ENCRYPTION_KEY"],
)
def test_supabase_sem_variavel_obrigatoria_falha_na_inicializacao(faltante):
    env = _env_supabase()
    del env[faltante]

    with pytest.raises(InvalidLinkedInConfigError) as excinfo:
        resolve_linkedin_config(env=env)

    assert faltante in str(excinfo.value)


def test_chave_de_cifragem_invalida_falha_na_inicializacao():
    # Erro de configuracao precisa aparecer ANTES de o captador gastar
    # uma autorizacao no LinkedIn, nao na hora de gravar o token.
    with pytest.raises(InvalidLinkedInConfigError):
        resolve_linkedin_config(env=_env_supabase(LINKEDIN_TOKEN_ENCRYPTION_KEY="chave-curta"))


def test_erro_de_configuracao_nao_expoe_valor_de_credencial():
    env = _env_supabase(LINKEDIN_TOKEN_ENCRYPTION_KEY="nao-e-base64-!!!")

    with pytest.raises(InvalidLinkedInConfigError) as excinfo:
        resolve_linkedin_config(env=env)

    assert "nao-e-base64-!!!" not in str(excinfo.value)
    assert FAKE_SUPABASE_KEY not in str(excinfo.value)


def test_repr_da_configuracao_mascara_chaves_do_supabase():
    config = resolve_linkedin_config(env=_env_supabase())
    texto = repr(config)

    assert FAKE_SUPABASE_KEY not in texto
    assert config.token_encryption_key not in texto
    assert FAKE_CLIENT_SECRET not in texto


def test_tabela_padrao_quando_nao_configurada():
    config = resolve_linkedin_config(env=_env_supabase())

    assert config.supabase_table is None  # runtime aplica DEFAULT_TABLE


def test_tabela_pode_ser_configurada():
    config = resolve_linkedin_config(env=_env_supabase(MCP_LINKEDIN_SUPABASE_TABLE="tokens_mobi"))

    assert config.supabase_table == "tokens_mobi"


def test_backend_windows_e_recusado_fora_do_windows(monkeypatch):
    # O footgun que a verificacao de compatibilidade encontrou: antes,
    # esta configuracao era aceita e so falhava no callback, com
    # ModuleNotFoundError, depois de o captador ja ter autorizado.
    import sys as sys_module

    monkeypatch.setattr(sys_module, "platform", "linux")

    with pytest.raises(InvalidLinkedInConfigError) as excinfo:
        resolve_linkedin_config(
            env={
                "LINKEDIN_CLIENT_ID": FAKE_CLIENT_ID,
                "LINKEDIN_CLIENT_SECRET": FAKE_CLIENT_SECRET,
                "MCP_PUBLIC_BASE_URL": FAKE_BASE_URL,
                "LINKEDIN_TOKEN_STORE_BACKEND": "windows",
            }
        )

    assert "supabase" in str(excinfo.value)


def test_backend_windows_continua_valido_no_windows(monkeypatch):
    import sys as sys_module

    monkeypatch.setattr(sys_module, "platform", "win32")

    config = resolve_linkedin_config(
        env={
            "LINKEDIN_CLIENT_ID": FAKE_CLIENT_ID,
            "LINKEDIN_CLIENT_SECRET": FAKE_CLIENT_SECRET,
            "MCP_PUBLIC_BASE_URL": FAKE_BASE_URL,
            "LINKEDIN_TOKEN_STORE_BACKEND": "windows",
        }
    )

    assert config.token_store_backend == "windows"


# =====================================================================
# Montagem do backend pelo runtime
# =====================================================================


def test_runtime_monta_backend_cifrado_sobre_supabase(monkeypatch):
    monkeypatch.setattr(
        socket.socket,
        "connect",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("montar backend nao deve abrir conexao")),
    )

    backend = build_credential_backend(resolve_linkedin_config(env=_env_supabase()))

    assert isinstance(backend, EncryptedCredentialBackend)
    assert isinstance(backend._inner, SupabaseCredentialBackend)


def test_runtime_aplica_a_tabela_padrao():
    backend = build_credential_backend(resolve_linkedin_config(env=_env_supabase()))

    assert backend._inner._table == DEFAULT_TABLE


def test_runtime_respeita_a_tabela_configurada():
    config = resolve_linkedin_config(env=_env_supabase(MCP_LINKEDIN_SUPABASE_TABLE="tokens_mobi"))

    assert build_credential_backend(config)._inner._table == "tokens_mobi"


def test_valores_ficticios_sao_claramente_marcados():
    assert FAKE_SUPABASE_KEY.startswith("FAKE_")
    assert FAKE_ACCESS_TOKEN.startswith("FAKE_")
    assert FAKE_SUPABASE_URL.endswith(".invalid")
