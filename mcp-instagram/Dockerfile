# mcp-instagram. Imagem de produção.
#
# Roda o servidor MCP em transporte Streamable HTTP. Não contém nenhuma
# credencial: Client ID, Client Secret e access token do Instagram vêm
# de secrets configurados na infraestrutura de deploy, nunca desta
# imagem.
#
# PORT não é fixada aqui: o Render injeta a variável PORT no container
# em tempo de execução (10000 por padrão) e o servidor lê essa variável
# dinamicamente (resolve_run_config, server.py). O EXPOSE abaixo
# documenta o valor padrão atual do Render, mas não é a fonte de verdade
# do runtime.

FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml ./
COPY src ./src

RUN pip install --no-cache-dir .

ENV MCP_TRANSPORT=streamable-http

EXPOSE 10000

CMD ["python", "-m", "mcp_instagram.server"]
