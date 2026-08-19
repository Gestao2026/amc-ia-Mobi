"""
Leitura de configuracao do mcp-linkedin (Camada 2, mcp-linkedin ->
LinkedIn), Etapa 7B.

Funcao pura, no mesmo padrao de `resolve_run_config` e
`resolve_claude_auth_config` (server.py): so decide QUAL configuracao
usar, a partir de um Mapping de ambiente. Nao abre porta, nao acessa
rede, nao constroi cliente HTTP e nao toca no LinkedIn.

O redirect_uri NAO e uma variavel propria: e sempre derivado de
MCP_PUBLIC_BASE_URL + LINKEDIN_CALLBACK_PATH. Isso garante uma unica
fonte da verdade, porque o mesmo valor precisa estar cadastrado no
LinkedIn Developer Portal, ser enviado na URL de autorizacao e ser
reenviado na troca code -> token; se divergirem, o LinkedIn recusa a
troca. Uma variavel separada so criaria a chance de divergirem.

LINKEDIN_CLIENT_SECRET e lido aqui, mas `LinkedInConfig.__repr__` o
mascara, e nenhuma funcao deste modulo o imprime, loga ou inclui em
mensagem de erro.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Mapping

from mcp_linkedin.auth_linkedin.crypto import InvalidEncryptionKeyError, TokenCipher

# Path fixo do callback OAuth do LinkedIn neste servidor. Precisa ser
# constante porque o valor completo (base publica + este path) e o que
# fica cadastrado no LinkedIn Developer Portal.
LINKEDIN_CALLBACK_PATH = "/oauth/linkedin/callback"

# Escopos minimos do OpenID Connect, presentes em qualquer app do
# LinkedIn com "Sign In with LinkedIn using OpenID Connect" habilitado.
# Deliberadamente conservador: pedir um escopo que o app nao tem
# aprovado faz o LinkedIn recusar a autorizacao inteira. Os escopos de
# leitura e publicacao da Pagina (r_organization_social,
# w_organization_social, w_member_social etc) so devem entrar aqui, via
# LINKEDIN_SCOPES, depois de confirmados como aprovados no app Mobi.
DEFAULT_LINKEDIN_SCOPES = ("openid", "profile", "email")

TOKEN_STORE_BACKEND_WINDOWS = "windows"
TOKEN_STORE_BACKEND_MEMORY = "memory"
TOKEN_STORE_BACKEND_SUPABASE = "supabase"
VALID_TOKEN_STORE_BACKENDS = {
    TOKEN_STORE_BACKEND_WINDOWS,
    TOKEN_STORE_BACKEND_MEMORY,
    TOKEN_STORE_BACKEND_SUPABASE,
}

# Variaveis exigidas somente pelo backend de producao. Nomes proprios
# do componente: a regra de isolamento do CLAUDE.md proibe reaproveitar
# o SUPABASE_KEY do .env da raiz do AMC-IA-Mobi.
REQUIRED_SUPABASE_ENV_VARS = (
    "MCP_LINKEDIN_SUPABASE_URL",
    "MCP_LINKEDIN_SUPABASE_KEY",
    "LINKEDIN_TOKEN_ENCRYPTION_KEY",
)

# Variaveis sem as quais a Camada 2 nao pode funcionar.
REQUIRED_LINKEDIN_ENV_VARS = ("LINKEDIN_CLIENT_ID", "LINKEDIN_CLIENT_SECRET", "MCP_PUBLIC_BASE_URL")


class InvalidLinkedInConfigError(ValueError):
    """Configuracao da Camada 2 invalida. Nunca contem segredo."""


@dataclass(frozen=True)
class LinkedInConfig:
    """Configuracao resolvida da Camada 2 (mcp-linkedin <-> LinkedIn)."""

    client_id: str
    client_secret: str
    redirect_uri: str
    scopes: tuple[str, ...]
    token_store_backend: str
    # Preenchidos somente quando token_store_backend == "supabase".
    supabase_url: str | None = None
    supabase_key: str | None = None
    supabase_table: str | None = None
    token_encryption_key: str | None = None

    def __repr__(self) -> str:
        # Nunca expor client_secret, chave do Supabase ou chave de
        # cifragem, mesmo que este objeto va parar num log ou traceback
        # por acidente.
        return (
            "LinkedInConfig("
            f"client_id={self.client_id!r}, "
            "client_secret='***', "
            f"redirect_uri={self.redirect_uri!r}, "
            f"scopes={self.scopes!r}, "
            f"token_store_backend={self.token_store_backend!r}, "
            f"supabase_url={self.supabase_url!r}, "
            f"supabase_key={'***' if self.supabase_key else None!r}, "
            f"supabase_table={self.supabase_table!r}, "
            f"token_encryption_key={'***' if self.token_encryption_key else None!r})"
        )


def missing_linkedin_env_vars(env: Mapping[str, str] | None = None) -> list[str]:
    """
    Devolve os NOMES (nunca os valores) das variaveis obrigatorias da
    Camada 2 que estao ausentes ou vazias. Serve para o operador
    descobrir o que falta configurar no Render sem nunca expor
    conteudo de credencial.
    """
    env = env if env is not None else os.environ
    return [nome for nome in REQUIRED_LINKEDIN_ENV_VARS if not env.get(nome)]


def default_token_store_backend(plataforma: str | None = None) -> str:
    """
    Backend padrao do TokenStore para a plataforma atual: o Windows
    Credential Manager em desenvolvimento local (Windows), memoria no
    restante (o container de producao no Render roda Linux, onde
    pywin32 nem existe).
    """
    plataforma = plataforma if plataforma is not None else sys.platform
    return TOKEN_STORE_BACKEND_WINDOWS if plataforma == "win32" else TOKEN_STORE_BACKEND_MEMORY


def resolve_linkedin_config(env: Mapping[str, str] | None = None) -> LinkedInConfig | None:
    """
    Le a configuracao da Camada 2 do ambiente informado (por padrao,
    os.environ) e devolve um LinkedInConfig, ou None se qualquer uma
    das variaveis obrigatorias (ver REQUIRED_LINKEDIN_ENV_VARS)
    estiver ausente: nesse caso a Camada 2 fica desligada, e o
    servidor continua subindo normalmente sem ela.

    Levanta InvalidLinkedInConfigError somente quando uma variavel
    esta presente porem invalida (backend desconhecido, lista de
    escopos vazia), porque ai houve intencao de configurar e o silencio
    esconderia um erro do operador.
    """
    env = env if env is not None else os.environ

    if missing_linkedin_env_vars(env):
        return None

    client_id = env["LINKEDIN_CLIENT_ID"].strip()
    client_secret = env["LINKEDIN_CLIENT_SECRET"]
    base_url = env["MCP_PUBLIC_BASE_URL"].strip().rstrip("/")

    escopos_brutos = env.get("LINKEDIN_SCOPES")
    if escopos_brutos is None:
        scopes = DEFAULT_LINKEDIN_SCOPES
    else:
        scopes = tuple(escopos_brutos.split())
        if not scopes:
            raise InvalidLinkedInConfigError("LINKEDIN_SCOPES foi definida mas esta vazia.")

    backend = env.get("LINKEDIN_TOKEN_STORE_BACKEND")
    backend = backend.strip().lower() if backend else default_token_store_backend()
    if backend not in VALID_TOKEN_STORE_BACKENDS:
        raise InvalidLinkedInConfigError(
            "LINKEDIN_TOKEN_STORE_BACKEND invalido: use 'windows', 'supabase' ou 'memory'."
        )

    # O backend 'windows' depende do Credential Manager via pywin32,
    # que nao existe fora do Windows (o proprio mcp declara
    # pywin32 com o marcador sys_platform == 'win32'). Sem esta
    # checagem, a configuracao seria aceita, o servidor subiria, o
    # captador autorizaria no LinkedIn, e so entao a gravacao no
    # callback falharia com ModuleNotFoundError: a pior hora possivel.
    # Melhor recusar aqui, na inicializacao, com mensagem clara.
    if backend == TOKEN_STORE_BACKEND_WINDOWS and sys.platform != "win32":
        raise InvalidLinkedInConfigError(
            "LINKEDIN_TOKEN_STORE_BACKEND='windows' so funciona no Windows "
            "(depende do Credential Manager). Em producao use 'supabase'."
        )

    supabase_url = supabase_key = supabase_table = token_encryption_key = None

    if backend == TOKEN_STORE_BACKEND_SUPABASE:
        ausentes = [nome for nome in REQUIRED_SUPABASE_ENV_VARS if not env.get(nome)]
        if ausentes:
            raise InvalidLinkedInConfigError(
                "LINKEDIN_TOKEN_STORE_BACKEND='supabase' exige as variaveis: "
                + ", ".join(ausentes)
                + "."
            )

        supabase_url = env["MCP_LINKEDIN_SUPABASE_URL"].strip().rstrip("/")
        supabase_key = env["MCP_LINKEDIN_SUPABASE_KEY"]
        supabase_table = (env.get("MCP_LINKEDIN_SUPABASE_TABLE") or "").strip() or None
        token_encryption_key = env["LINKEDIN_TOKEN_ENCRYPTION_KEY"]

        # Valida a chave aqui, na inicializacao, e nao na primeira
        # gravacao de token: uma chave malformada e erro de
        # configuracao, e precisa aparecer antes de o captador gastar
        # uma autorizacao no LinkedIn.
        try:
            TokenCipher.from_base64_key(token_encryption_key)
        except InvalidEncryptionKeyError as erro:
            # A mensagem de InvalidEncryptionKeyError nunca contem a
            # chave (ver crypto.py), entao pode ser repassada.
            raise InvalidLinkedInConfigError(f"LINKEDIN_TOKEN_ENCRYPTION_KEY invalida: {erro}") from None

    return LinkedInConfig(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=f"{base_url}{LINKEDIN_CALLBACK_PATH}",
        scopes=scopes,
        token_store_backend=backend,
        supabase_url=supabase_url,
        supabase_key=supabase_key,
        supabase_table=supabase_table,
        token_encryption_key=token_encryption_key,
    )
