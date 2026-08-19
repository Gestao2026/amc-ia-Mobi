"""
Servidor MCP do mcp-linkedin.

Ferramentas expostas nesta etapa: somente `linkedin_mcp_status`, de
teste, que devolve dados estaticos sem acessar o LinkedIn nem
qualquer outro servico. OAuth do LinkedIn (Camada 2) ainda NAO esta
implementado neste arquivo.

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

from mcp_linkedin.auth_claude.provider import ClaudeAuthProvider
from mcp_linkedin.auth_claude.session_store import ClaudeSessionStore

mcp = MCPServer("mcp-linkedin")


@mcp.tool()
def linkedin_mcp_status() -> dict:
    """Retorna o status estatico do componente, sem acessar o LinkedIn."""
    return {
        "componente": "mcp-linkedin",
        "ambiente": "local",
        "linkedin": "nao_conectado",
        "oauth": "nao_implementado",
        "status": "operacional",
    }


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
