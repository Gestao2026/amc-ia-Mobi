"""
Servidor MCP do mcp-linkedin.

Ferramentas expostas: `linkedin_mcp_status` (diagnostico),
`linkedin_oauth_iniciar` e `linkedin_oauth_status` (Camada 2). Nenhuma
ferramenta de negocio do LinkedIn (leitura ou publicacao) existe
ainda.

OAuth do LinkedIn (Camada 2, Etapa 7B): `resolve_linkedin_config`
(config.py) le LINKEDIN_CLIENT_ID/LINKEDIN_CLIENT_SECRET/
MCP_PUBLIC_BASE_URL do ambiente e, se presentes, liga o fluxo
completo (URL de autorizacao -> callback -> troca de code por token ->
TokenStore). Se ausentes, a Camada 2 fica desligada e o servidor sobe
normalmente sem ela. O inicio do fluxo e uma FERRAMENTA MCP, nao uma
pagina: nenhuma interface HTML existe neste componente. A unica rota
HTTP propria e o callback, que o proprio LinkedIn chama, e que
responde JSON.

OAuth do Claude (Camada 1, Etapa 7A): `resolve_claude_auth_config`
le MCP_CLAUDE_CLIENT_ID/MCP_CLAUDE_CLIENT_SECRET/MCP_PUBLIC_BASE_URL
do ambiente e, se presentes, protege a rota /mcp com um
Authorization Server minimo (client estatico, sem DCR, sem tela de
consentimento, PKCE S256 validado pelo proprio SDK). Se essas
variaveis nao estiverem definidas (ex. desenvolvimento local via
stdio), a Camada 1 fica desligada e o comportamento e identico ao de
antes desta etapa.

Transporte: o mesmo servidor roda em dois modos, decididos pela
variavel de ambiente MCP_TRANSPORT, sem duplicar codigo:

  MCP_TRANSPORT=stdio            (padrao, uso local/Claude Code)
      python -m mcp_linkedin.server

  MCP_TRANSPORT=streamable-http  (uso remoto/producao)
      PORT=<porta fornecida pela infraestrutura> \
      MCP_TRANSPORT=streamable-http \
      python -m mcp_linkedin.server

Em streamable-http, host e path sao fixos (0.0.0.0 e /mcp, conforme
decisao ja tomada); a porta nunca e fixada no codigo, so lida de
PORT. `resolve_run_config` e uma funcao pura que so decide QUAL
configuracao usar, sem nunca iniciar o servidor; quem inicia e
`main()`.
"""

import os
from dataclasses import dataclass
from typing import Mapping

from mcp.server.auth.provider import ProviderTokenVerifier
from mcp.server.auth.settings import AuthSettings, ClientRegistrationOptions, RevocationOptions
from mcp.server.mcpserver import MCPServer
from starlette.requests import Request
from starlette.responses import JSONResponse

from mcp_linkedin.auth_claude.provider import ClaudeAuthProvider
from mcp_linkedin.auth_claude.session_store import ClaudeSessionStore
from mcp_linkedin.auth_linkedin.oauth_callback import CallbackOutcome, CallbackParams
from mcp_linkedin.auth_linkedin.runtime import LinkedInOAuthRuntime, build_runtime
from mcp_linkedin.auth_linkedin.token_exchange import TokenExchangeError, TransportError
from mcp_linkedin.config import (
    LINKEDIN_CALLBACK_PATH,
    missing_linkedin_env_vars,
    resolve_linkedin_config,
)

mcp = MCPServer("mcp-linkedin")


# =====================================================================
# Camada 2: runtime OAuth do LinkedIn (Etapa 7B)
# =====================================================================
#
# O runtime precisa ser de vida longa e unico no processo: o state
# gerado por `linkedin_oauth_iniciar` so pode ser validado pelo mesmo
# StateStore quando o LinkedIn chamar o callback, e o token gravado
# pelo callback so e visivel para as demais ferramentas se o TokenStore
# for o mesmo objeto.
#
# A resolucao e preguicosa (na primeira utilizacao, nao no import) para
# que o modulo continue importavel sem nenhuma variavel de ambiente
# definida. O sentinela abaixo distingue "ainda nao resolvido" de
# "resolvido como None" (Camada 2 desligada), sem precisar de uma API
# de reset so para testes: um teste que queira injetar um runtime
# proprio atribui diretamente a `_linkedin_runtime` e restaura o
# sentinela no final.

_RUNTIME_NAO_RESOLVIDO = object()
_linkedin_runtime: LinkedInOAuthRuntime | None | object = _RUNTIME_NAO_RESOLVIDO


def resolve_linkedin_runtime(env=None) -> LinkedInOAuthRuntime | None:
    """
    Monta o runtime da Camada 2 a partir do ambiente, ou devolve None
    se ela nao estiver configurada. Nao acessa rede.
    """
    config = resolve_linkedin_config(env)
    if config is None:
        return None
    return build_runtime(config)


def get_linkedin_runtime() -> LinkedInOAuthRuntime | None:
    """Devolve o runtime unico do processo, resolvendo-o na primeira chamada."""
    global _linkedin_runtime
    if _linkedin_runtime is _RUNTIME_NAO_RESOLVIDO:
        _linkedin_runtime = resolve_linkedin_runtime()
    return _linkedin_runtime  # type: ignore[return-value]


@mcp.tool()
def linkedin_mcp_status() -> dict:
    """Retorna o status do componente e da conexao com o LinkedIn, sem acessar o LinkedIn."""
    runtime = get_linkedin_runtime()

    if runtime is None:
        return {
            "componente": "mcp-linkedin",
            "oauth": "nao_configurado",
            "linkedin": "nao_conectado",
            "status": "operacional",
            "variaveis_ausentes": missing_linkedin_env_vars(),
        }

    return {
        "componente": "mcp-linkedin",
        "oauth": "configurado",
        "linkedin": "conectado" if runtime.has_valid_token() else "nao_conectado",
        "status": "operacional",
        "variaveis_ausentes": [],
    }


@mcp.tool()
def linkedin_oauth_iniciar() -> dict:
    """
    Inicia a autorizacao do LinkedIn e devolve a URL que o captador
    precisa abrir no navegador para autorizar o acesso.

    Nao acessa o LinkedIn e nao abre navegador: so monta a URL. Depois
    que o captador autorizar, o proprio LinkedIn chama o callback deste
    servidor, que conclui a troca por token automaticamente.
    """
    runtime = get_linkedin_runtime()

    if runtime is None:
        return {
            "status": "nao_configurado",
            "detalhe": (
                "A conexao com o LinkedIn ainda nao foi configurada neste servidor. "
                "Configure as variaveis listadas em variaveis_ausentes e reinicie o servico."
            ),
            "variaveis_ausentes": missing_linkedin_env_vars(),
        }

    autorizacao = runtime.start_authorization()

    return {
        "status": "aguardando_autorizacao",
        "url_autorizacao": autorizacao.url,
        "escopos_solicitados": list(runtime.config.scopes),
        "detalhe": (
            "Abra a URL acima no navegador, entre com a conta que administra a Pagina e "
            "autorize o acesso. A autorizacao expira em 10 minutos. Depois de autorizar, "
            "confira o resultado com a ferramenta linkedin_oauth_status."
        ),
    }


@mcp.tool()
def linkedin_oauth_status() -> dict:
    """
    Informa se existe um access token valido do LinkedIn guardado
    neste servidor. Nunca devolve o token em si.
    """
    runtime = get_linkedin_runtime()

    if runtime is None:
        return {
            "status": "nao_configurado",
            "detalhe": "A conexao com o LinkedIn ainda nao foi configurada neste servidor.",
            "variaveis_ausentes": missing_linkedin_env_vars(),
        }

    if runtime.has_valid_token():
        return {
            "status": "conectado",
            "detalhe": "Existe uma autorizacao valida do LinkedIn guardada neste servidor.",
        }

    return {
        "status": "nao_conectado",
        "detalhe": (
            "Nao existe autorizacao valida do LinkedIn. Use a ferramenta "
            "linkedin_oauth_iniciar para autorizar."
        ),
    }


@mcp.custom_route(LINKEDIN_CALLBACK_PATH, methods=["GET"])
async def linkedin_oauth_callback(request: Request) -> JSONResponse:
    """
    Callback OAuth chamado pelo proprio LinkedIn depois que o captador
    autoriza. Rota publica por necessidade do protocolo (o LinkedIn nao
    envia o Bearer da Camada 1); a protecao contra chamada forjada e o
    `state` de uso unico, validado por `process_callback` antes de
    qualquer coisa acontecer com o authorization code.

    Responde JSON, nunca HTML: este componente nao tem interface web.
    Nenhuma resposta inclui o authorization code, o state ou o access
    token.
    """
    runtime = get_linkedin_runtime()

    if runtime is None:
        return JSONResponse(
            {
                "status": "nao_configurado",
                "detalhe": "A conexao com o LinkedIn nao esta configurada neste servidor.",
            },
            status_code=503,
        )

    params = CallbackParams(
        code=request.query_params.get("code"),
        state=request.query_params.get("state"),
        error=request.query_params.get("error"),
        error_description=request.query_params.get("error_description"),
    )

    try:
        resultado = runtime.handle_callback(params)
    except (TokenExchangeError, TransportError, ValueError):
        # A mensagem original fica de fora da resposta de proposito:
        # ela pertence ao operador do servico, nao ao navegador que
        # chegou no callback. Nenhuma delas contem segredo, mas expor
        # detalhe interno a quem abriu a URL nao traz beneficio.
        return JSONResponse(
            {
                "status": "erro_na_troca_de_token",
                "detalhe": "A autorizacao foi recebida, mas a troca por token falhou. Tente novamente.",
            },
            status_code=502,
        )

    if resultado.outcome is CallbackOutcome.TOKEN_EXCHANGE_STARTED:
        return JSONResponse(
            {
                "status": "conectado",
                "detalhe": "LinkedIn autorizado com sucesso. Pode fechar esta pagina.",
            },
            status_code=200,
        )

    corpo = {
        "status": "rejeitado",
        "motivo": resultado.outcome.value,
        "detalhe": resultado.detail,
    }
    if resultado.oauth_error:
        corpo["erro_linkedin"] = resultado.oauth_error

    return JSONResponse(corpo, status_code=400)


STREAMABLE_HTTP_HOST = "0.0.0.0"
STREAMABLE_HTTP_PATH = "/mcp"
VALID_TRANSPORTS = {"stdio", "streamable-http"}


class InvalidTransportConfigError(ValueError):
    """MCP_TRANSPORT ou PORT invalidos/incompletos. Nunca contem segredo."""


@dataclass(frozen=True)
class StdioRunConfig:
    """Configuracao de execucao local, via entrada/saida padrao do processo."""

    transport: str = "stdio"


@dataclass(frozen=True)
class StreamableHttpRunConfig:
    """Configuracao de execucao remota, via HTTP."""

    transport: str = "streamable-http"
    host: str = STREAMABLE_HTTP_HOST
    port: int = 0
    streamable_http_path: str = STREAMABLE_HTTP_PATH


def resolve_run_config(env: Mapping[str, str] | None = None):
    """
    Le MCP_TRANSPORT (e PORT, quando aplicavel) do ambiente informado
    (por padrao, os.environ) e devolve StdioRunConfig ou
    StreamableHttpRunConfig. Nao inicia nenhum servidor, nao abre
    porta, nao acessa rede.
    """
    env = env if env is not None else os.environ

    transport = env.get("MCP_TRANSPORT", "stdio").strip()

    if transport not in VALID_TRANSPORTS:
        raise InvalidTransportConfigError(
            "MCP_TRANSPORT invalido: use 'stdio' ou 'streamable-http'."
        )

    if transport == "stdio":
        return StdioRunConfig()

    porta_bruta = env.get("PORT")
    if not porta_bruta:
        raise InvalidTransportConfigError(
            "MCP_TRANSPORT=streamable-http exige a variavel PORT definida."
        )

    try:
        porta = int(porta_bruta)
    except ValueError:
        raise InvalidTransportConfigError("PORT precisa ser um numero inteiro.") from None

    if not (0 < porta <= 65535):
        raise InvalidTransportConfigError("PORT fora do intervalo valido (1-65535).")

    return StreamableHttpRunConfig(port=porta)


@dataclass(frozen=True)
class ClaudeAuthConfig:
    """Configuracao resolvida da Camada 1 (Claude.ai <-> mcp-linkedin), ou None se desligada."""

    provider: ClaudeAuthProvider
    token_verifier: ProviderTokenVerifier
    auth_settings: AuthSettings


def resolve_claude_auth_config(env: Mapping[str, str] | None = None) -> ClaudeAuthConfig | None:
    """
    Le a configuracao da Camada 1 do ambiente informado (por padrao,
    os.environ) e devolve um ClaudeAuthConfig, ou None se
    MCP_CLAUDE_CLIENT_ID ou MCP_PUBLIC_BASE_URL nao estiverem
    definidos (Camada 1 desligada -- comportamento identico ao de
    antes da Etapa 7A). Nao inicia nenhum servidor, nao acessa rede.

    DCR (/register) e revogacao (/revoke) ficam desligados aqui de
    proposito (decisao da Etapa 7A): so um cliente estatico e
    reconhecido, pre-registrado via MCP_CLAUDE_CLIENT_ID (e,
    opcionalmente, MCP_CLAUDE_CLIENT_SECRET, se o fluxo exigir
    cliente confidencial). Nenhum desses valores e logado aqui.
    """
    env = env if env is not None else os.environ

    client_id = env.get("MCP_CLAUDE_CLIENT_ID")
    base_url = env.get("MCP_PUBLIC_BASE_URL")

    if not client_id or not base_url:
        return None

    client_secret = env.get("MCP_CLAUDE_CLIENT_SECRET") or None
    base_url = base_url.rstrip("/")

    store = ClaudeSessionStore()
    provider = ClaudeAuthProvider(client_id=client_id, client_secret=client_secret, store=store)
    token_verifier = ProviderTokenVerifier(provider)

    auth_settings = AuthSettings(
        issuer_url=base_url,
        resource_server_url=f"{base_url}{STREAMABLE_HTTP_PATH}",
        client_registration_options=ClientRegistrationOptions(enabled=False),
        revocation_options=RevocationOptions(enabled=False),
    )

    return ClaudeAuthConfig(provider=provider, token_verifier=token_verifier, auth_settings=auth_settings)


def apply_claude_auth_config(server: MCPServer, auth_config: ClaudeAuthConfig) -> None:
    """
    Aplica a configuracao da Camada 1 num MCPServer ja construido.

    MCPServer nao expoe um setter publico para isto (confirmado por
    inspecao do codigo-fonte do SDK mcp 2.0.0 na Etapa 7A): estes sao
    os mesmos atributos "privados" (`_auth_server_provider`,
    `_token_verifier`) e a configuracao (`settings.auth`) que
    `streamable_http_app()`/`run()` leem em tempo de chamada, nao em
    tempo de construcao. Essa mutacao pos-construcao e o mecanismo
    necessario nesta versao do SDK -- nao uma escolha de conveniencia
    nossa -- e nao deve ser trocada sem reconferir contra uma versao
    futura do SDK. Extraida como funcao propria (em vez de inline em
    main()) para que o teste de integracao possa exercitar exatamente
    este mesmo caminho, sem duplicar a logica.
    """
    server._auth_server_provider = auth_config.provider
    server._token_verifier = auth_config.token_verifier
    server.settings.auth = auth_config.auth_settings


def main() -> None:
    config = resolve_run_config()

    if isinstance(config, StreamableHttpRunConfig):
        auth_config = resolve_claude_auth_config()
        if auth_config is not None:
            apply_claude_auth_config(mcp, auth_config)

        mcp.run(
            transport="streamable-http",
            host=config.host,
            port=config.port,
            streamable_http_path=config.streamable_http_path,
        )
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
