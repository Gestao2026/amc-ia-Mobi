# mcp-linkedin. Imagem de producao (Etapa 6B, adaptada para Render na
# Etapa 6D — a infraestrutura escolhida deixou de ser o Fly.io).
#
# Roda o servidor MCP em transporte Streamable HTTP. Nao contem
# nenhuma credencial: Client ID, Client Secret e access token do
# LinkedIn continuam vindo de secrets configurados na infraestrutura
# de deploy (nunca desta imagem). OAuth do Claude e do LinkedIn ainda
# nao estao implementados neste estagio do projeto.
#
# PORT nao e fixado aqui: o Render injeta a variavel PORT no
# container em tempo de execucao (10000 por padrao) e o servidor ja
# le essa variavel dinamicamente (resolve_run_config, server.py). O
# EXPOSE abaixo documenta o valor padrao atual do Render, mas nao e
# a fonte de verdade do runtime.

FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./
COPY src ./src

RUN pip install --no-cache-dir .

ENV MCP_TRANSPORT=streamable-http

EXPOSE 10000

CMD ["python", "-m", "mcp_linkedin.server"]
