"""
Servidor MCP do mcp-linkedin.

Ferramentas expostas nesta etapa: somente `linkedin_mcp_status`, de
teste, que devolve dados estaticos sem acessar o LinkedIn nem
qualquer outro servico. OAuth do Claude (Camada 1), OAuth do LinkedIn
(Camada 2), callback HTTP e endpoints /.well-known/* ainda NAO estao
implementados neste arquivo.

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

from mcp.server.mcpserver import MCPServer

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


def main() -> None:
    config = resolve_run_config()

    if isinstance(config, StreamableHttpRunConfig):
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
