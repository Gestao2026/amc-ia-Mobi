"""
Leitura de configuração do mcp-instagram (Camada 2, mcp-instagram para
Instagram).

Função pura, no mesmo padrão de `resolve_run_config` e
`resolve_claude_auth_config` (server.py): só decide QUAL configuração
usar, a partir de um Mapping de ambiente. Não abre porta, não acessa
rede, não constrói cliente HTTP e não toca no Instagram.

O redirect_uri NÃO é uma variável própria: é sempre derivado de
MCP_PUBLIC_BASE_URL + INSTAGRAM_CALLBACK_PATH. Isso garante uma única
fonte da verdade, porque o mesmo valor precisa estar cadastrado no
painel do aplicativo na Meta, ser enviado na URL de autorização e ser
reenviado na troca code para token. Se divergirem, a Meta recusa a
troca.

INSTAGRAM_CLIENT_SECRET é lido aqui, mas `InstagramConfig.__repr__` o
mascara, e nenhuma função deste módulo o imprime, registra em log ou
inclui em mensagem de erro.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Mapping

from mcp_instagram.auth_instagram.crypto import InvalidEncryptionKeyError, TokenCipher

# Path fixo do callback OAuth do Instagram neste servidor. Precisa ser
# constante porque o valor completo (base pública + este path) é o que
# fica cadastrado no painel do aplicativo na Meta.
INSTAGRAM_CALLBACK_PATH = "/oauth/instagram/callback"

# Rotas exigidas pela Meta para qualquer aplicativo do Instagram, e que
# ela chama por POST com uma requisição assinada. Também precisam ser
# constantes: os endereços completos ficam cadastrados no painel da Meta.
#
#   desautorização    a pessoa removeu o aplicativo no Instagram
#   exclusão de dados a pessoa pediu que os dados sejam apagados
#   status            página de acompanhamento do pedido de exclusão,
#                     cujo endereço a Meta exige que seja devolvido na
#                     resposta ao pedido
INSTAGRAM_DEAUTHORIZE_PATH = "/oauth/instagram/desautorizar"
INSTAGRAM_DATA_DELETION_PATH = "/oauth/instagram/exclusao-de-dados"
INSTAGRAM_DATA_DELETION_STATUS_PATH = "/oauth/instagram/exclusao-de-dados/status"

# Escopos padrão deste componente: leitura de perfil e leitura de
# métricas. Nada além disso.
#
# `instagram_business_basic` permite identificar a conta e ler o que já
# está publicado. `instagram_business_manage_insights` permite ler
# alcance, impressões e desempenho.
#
# Deliberadamente AUSENTES, e que não devem ser acrescentados sem
# decisão explícita do captador, porque dão poder de escrita ou acesso
# a conversa privada:
#   instagram_business_content_publish   publicar
#   instagram_business_manage_comments   responder e apagar comentários
#   instagram_business_manage_messages   ler e responder o Direct
#   ads_management / ads_read            administrar anúncios
DEFAULT_INSTAGRAM_SCOPES = (
    "instagram_business_basic",
    "instagram_business_manage_insights",
)

# Escopos que concedem escrita na conta ou acesso a mensagem privada.
# Não são proibidos aqui (a decisão é do captador, via
# INSTAGRAM_SCOPES), mas `escopos_de_escrita` os identifica para que o
# servidor possa avisar com clareza, na ferramenta de status, que a
# conexão deixou de ser somente leitura.
SCOPES_DE_ESCRITA = frozenset(
    {
        "instagram_business_content_publish",
        "instagram_business_manage_comments",
        "instagram_business_manage_messages",
        "instagram_content_publish",
        "instagram_manage_comments",
        "instagram_manage_messages",
        "ads_management",
        "ads_read",
        "pages_manage_posts",
        "pages_manage_engagement",
    }
)

TOKEN_STORE_BACKEND_WINDOWS = "windows"
TOKEN_STORE_BACKEND_MEMORY = "memory"
TOKEN_STORE_BACKEND_SUPABASE = "supabase"
TOKEN_STORE_BACKEND_PONTE = "ponte"
VALID_TOKEN_STORE_BACKENDS = {
    TOKEN_STORE_BACKEND_WINDOWS,
    TOKEN_STORE_BACKEND_MEMORY,
    TOKEN_STORE_BACKEND_SUPABASE,
    TOKEN_STORE_BACKEND_PONTE,
}

# Variáveis exigidas pelo backend da ponte HTTPS (HostGator). A senha do
# MySQL NÃO está aqui de propósito: nesta arquitetura o Render nunca
# fala com o MySQL, só com a ponte. A senha do banco existe apenas no
# config.php da HostGator.
REQUIRED_PONTE_ENV_VARS = (
    "MCP_INSTAGRAM_PONTE_URL",
    "MCP_INSTAGRAM_PONTE_SECRET",
    "INSTAGRAM_TOKEN_ENCRYPTION_KEY",
)

# Variáveis exigidas somente pelo backend alternativo de produção.
# Nomes próprios do componente: a regra de isolamento do CLAUDE.md
# proíbe reaproveitar o SUPABASE_KEY do .env da raiz do AMC-IA-Mobi.
REQUIRED_SUPABASE_ENV_VARS = (
    "MCP_INSTAGRAM_SUPABASE_URL",
    "MCP_INSTAGRAM_SUPABASE_KEY",
    "INSTAGRAM_TOKEN_ENCRYPTION_KEY",
)

# Variáveis sem as quais a Camada 2 não pode funcionar.
REQUIRED_INSTAGRAM_ENV_VARS = (
    "INSTAGRAM_CLIENT_ID",
    "INSTAGRAM_CLIENT_SECRET",
    "MCP_PUBLIC_BASE_URL",
)


class InvalidInstagramConfigError(ValueError):
    """Configuração da Camada 2 inválida. Nunca contém segredo."""


def _validar_chave_de_cifragem(chave: str) -> None:
    """
    Confere a chave na INICIALIZAÇÃO, não na primeira gravação de token:
    uma chave malformada é erro de configuração, e precisa aparecer
    antes de o captador gastar uma autorização no Instagram.
    """
    try:
        TokenCipher.from_base64_key(chave)
    except InvalidEncryptionKeyError as erro:
        # A mensagem de InvalidEncryptionKeyError nunca contém a chave
        # (ver crypto.py), então pode ser repassada.
        raise InvalidInstagramConfigError(
            f"INSTAGRAM_TOKEN_ENCRYPTION_KEY inválida: {erro}"
        ) from None


@dataclass(frozen=True)
class InstagramConfig:
    """Configuração resolvida da Camada 2 (mcp-instagram e Instagram)."""

    client_id: str
    client_secret: str
    redirect_uri: str
    scopes: tuple[str, ...]
    token_store_backend: str
    # Preenchidos somente quando token_store_backend == "supabase".
    supabase_url: str | None = None
    supabase_key: str | None = None
    supabase_table: str | None = None
    # Preenchidos somente quando token_store_backend == "ponte".
    ponte_url: str | None = None
    ponte_secret: str | None = None
    # Exigida pelos dois backends remotos.
    token_encryption_key: str | None = None

    @property
    def public_base_url(self) -> str:
        """
        Endereço público raiz deste servidor, sem barra no final.

        Derivado do redirect_uri em vez de guardado separadamente, para
        manter a fonte da verdade única: os dois precisam concordar, e um
        campo a mais só criaria a chance de divergirem.
        """
        return self.redirect_uri[: -len(INSTAGRAM_CALLBACK_PATH)]

    @property
    def escopos_de_escrita(self) -> tuple[str, ...]:
        """
        Escopos configurados que dão poder de escrita na conta ou acesso
        a mensagem privada. Vazio na configuração padrão, que é somente
        leitura. Serve para o servidor declarar isso com honestidade na
        ferramenta de status.
        """
        return tuple(escopo for escopo in self.scopes if escopo in SCOPES_DE_ESCRITA)

    @property
    def somente_leitura(self) -> bool:
        """True quando nenhum escopo configurado permite escrita."""
        return not self.escopos_de_escrita

    def __repr__(self) -> str:
        # Nunca expor client_secret, chave do Supabase, segredo da ponte
        # ou chave de cifragem, mesmo que este objeto vá parar num log
        # ou traceback por acidente.
        return (
            "InstagramConfig("
            f"client_id={self.client_id!r}, "
            "client_secret='***', "
            f"redirect_uri={self.redirect_uri!r}, "
            f"scopes={self.scopes!r}, "
            f"token_store_backend={self.token_store_backend!r}, "
            f"supabase_url={self.supabase_url!r}, "
            f"supabase_key={'***' if self.supabase_key else None!r}, "
            f"supabase_table={self.supabase_table!r}, "
            f"ponte_url={self.ponte_url!r}, "
            f"ponte_secret={'***' if self.ponte_secret else None!r}, "
            f"token_encryption_key={'***' if self.token_encryption_key else None!r})"
        )


def missing_instagram_env_vars(env: Mapping[str, str] | None = None) -> list[str]:
    """
    Devolve os NOMES (nunca os valores) das variáveis obrigatórias da
    Camada 2 que estão ausentes ou vazias. Serve para o operador
    descobrir o que falta configurar sem nunca expor conteúdo de
    credencial.
    """
    env = env if env is not None else os.environ
    return [nome for nome in REQUIRED_INSTAGRAM_ENV_VARS if not env.get(nome)]


def default_token_store_backend(plataforma: str | None = None) -> str:
    """
    Backend padrão do TokenStore para a plataforma atual: o Windows
    Credential Manager em desenvolvimento local (Windows), memória no
    restante (o container de produção no Render roda Linux, onde o
    pywin32 nem existe).
    """
    plataforma = plataforma if plataforma is not None else sys.platform
    return TOKEN_STORE_BACKEND_WINDOWS if plataforma == "win32" else TOKEN_STORE_BACKEND_MEMORY


def resolve_instagram_config(env: Mapping[str, str] | None = None) -> InstagramConfig | None:
    """
    Lê a configuração da Camada 2 do ambiente informado (por padrão,
    os.environ) e devolve um InstagramConfig, ou None se qualquer uma
    das variáveis obrigatórias (ver REQUIRED_INSTAGRAM_ENV_VARS) estiver
    ausente. Nesse caso a Camada 2 fica desligada e o servidor continua
    subindo normalmente sem ela.

    Levanta InvalidInstagramConfigError somente quando uma variável está
    presente porém inválida (base pública sem HTTPS, backend
    desconhecido, lista de escopos vazia), porque aí houve intenção de
    configurar e o silêncio esconderia um erro do operador.
    """
    env = env if env is not None else os.environ

    if missing_instagram_env_vars(env):
        return None

    client_id = env["INSTAGRAM_CLIENT_ID"].strip()
    client_secret = env["INSTAGRAM_CLIENT_SECRET"]
    base_url = env["MCP_PUBLIC_BASE_URL"].strip().rstrip("/")

    # A Meta recusa redirect_uri que não seja HTTPS. Recusar aqui, na
    # inicialização, evita que o captador descubra isso só depois de
    # abrir a tela de autorização e receber um erro do próprio
    # Instagram.
    if not base_url.lower().startswith("https://"):
        raise InvalidInstagramConfigError(
            "MCP_PUBLIC_BASE_URL precisa começar com https://: a Meta recusa "
            "redirect_uri sem HTTPS."
        )

    escopos_brutos = env.get("INSTAGRAM_SCOPES")
    if escopos_brutos is None:
        scopes = DEFAULT_INSTAGRAM_SCOPES
    else:
        # Aceita espaço ou vírgula como separador na variável de
        # ambiente, por conveniência de quem configura. A vírgula que a
        # Meta exige na URL é aplicada só na montagem da URL de
        # autorização (oauth_flow.py), não aqui.
        scopes = tuple(escopos_brutos.replace(",", " ").split())
        if not scopes:
            raise InvalidInstagramConfigError("INSTAGRAM_SCOPES foi definida mas está vazia.")

    backend = env.get("INSTAGRAM_TOKEN_STORE_BACKEND")
    backend = backend.strip().lower() if backend else default_token_store_backend()
    if backend not in VALID_TOKEN_STORE_BACKENDS:
        raise InvalidInstagramConfigError(
            "INSTAGRAM_TOKEN_STORE_BACKEND inválido: use 'windows', 'ponte', "
            "'supabase' ou 'memory'."
        )

    # O backend 'windows' depende do Credential Manager via pywin32, que
    # não existe fora do Windows. Sem esta checagem, a configuração seria
    # aceita, o servidor subiria, o captador autorizaria no Instagram, e
    # só então a gravação no callback falharia: a pior hora possível.
    if backend == TOKEN_STORE_BACKEND_WINDOWS and sys.platform != "win32":
        raise InvalidInstagramConfigError(
            "INSTAGRAM_TOKEN_STORE_BACKEND='windows' só funciona no Windows "
            "(depende do Credential Manager). Em produção use 'ponte'."
        )

    supabase_url = supabase_key = supabase_table = token_encryption_key = None
    ponte_url = ponte_secret = None

    if backend == TOKEN_STORE_BACKEND_PONTE:
        ausentes = [nome for nome in REQUIRED_PONTE_ENV_VARS if not env.get(nome)]
        if ausentes:
            raise InvalidInstagramConfigError(
                "INSTAGRAM_TOKEN_STORE_BACKEND='ponte' exige as variáveis: "
                + ", ".join(ausentes)
                + "."
            )

        ponte_url = env["MCP_INSTAGRAM_PONTE_URL"].strip()
        ponte_secret = env["MCP_INSTAGRAM_PONTE_SECRET"]
        token_encryption_key = env["INSTAGRAM_TOKEN_ENCRYPTION_KEY"]

        # HTTPS obrigatório. O envelope AES-GCM já protege o token, mas o
        # segredo da ponte viaja em cabeçalho: em HTTP simples ele iria
        # em claro pela internet.
        if not ponte_url.lower().startswith("https://"):
            raise InvalidInstagramConfigError(
                "MCP_INSTAGRAM_PONTE_URL precisa começar com https:// "
                "(HTTP simples é recusado)."
            )

        _validar_chave_de_cifragem(token_encryption_key)

    if backend == TOKEN_STORE_BACKEND_SUPABASE:
        ausentes = [nome for nome in REQUIRED_SUPABASE_ENV_VARS if not env.get(nome)]
        if ausentes:
            raise InvalidInstagramConfigError(
                "INSTAGRAM_TOKEN_STORE_BACKEND='supabase' exige as variáveis: "
                + ", ".join(ausentes)
                + "."
            )

        supabase_url = env["MCP_INSTAGRAM_SUPABASE_URL"].strip().rstrip("/")
        supabase_key = env["MCP_INSTAGRAM_SUPABASE_KEY"]
        supabase_table = (env.get("MCP_INSTAGRAM_SUPABASE_TABLE") or "").strip() or None
        token_encryption_key = env["INSTAGRAM_TOKEN_ENCRYPTION_KEY"]
        _validar_chave_de_cifragem(token_encryption_key)

    return InstagramConfig(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=f"{base_url}{INSTAGRAM_CALLBACK_PATH}",
        scopes=scopes,
        token_store_backend=backend,
        supabase_url=supabase_url,
        supabase_key=supabase_key,
        supabase_table=supabase_table,
        ponte_url=ponte_url,
        ponte_secret=ponte_secret,
        token_encryption_key=token_encryption_key,
    )
