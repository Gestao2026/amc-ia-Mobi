# mcp-linkedin

## Status

Um **servidor MCP local mínimo** está implementado, apenas para validar a comunicação `mcp-linkedin → servidor MCP → ferramenta`. Ele expõe uma única ferramenta de teste, `linkedin_mcp_status`, que devolve dados estáticos e não faz nenhuma chamada externa. Nenhuma autenticação, nenhum acesso ao LinkedIn e nenhum deploy remoto existem nesta etapa.

## Etapa 2. MCP local mínimo

- **O que foi implementado:** [`src/mcp_linkedin/server.py`](src/mcp_linkedin/server.py) sobe um servidor MCP usando o SDK oficial (`mcp` 2.0.0, classe `MCPServer` de `mcp.server.mcpserver`), registrando só a ferramenta `linkedin_mcp_status`.
- **`linkedin_mcp_status` é apenas de teste.** Ela não consulta o LinkedIn nem qualquer serviço externo. Retorna sempre os mesmos campos estáticos: `componente`, `ambiente`, `linkedin` (`nao_conectado`), `oauth` (`nao_implementado`) e `status` (`operacional`).
- **OAuth do LinkedIn (Camada 2) ainda não foi implementado.** Nenhum Client ID, Client Secret, token ou chamada à API do LinkedIn existe no código.
- **OAuth do Claude (Camada 1) ainda não foi implementado.** O servidor roda hoje só em transporte local (stdio), sem endpoint HTTP público e sem fluxo de autorização para o Claude.ai.
- **Nenhuma comunicação externa é realizada nesta etapa.** O servidor só responde ao próprio processo que o invoca localmente.
- **Como executar localmente** (dependência `mcp` já instalada nesta etapa):
  ```
  python -m mcp_linkedin.server
  ```
  Sobe o servidor em transporte stdio e fica aguardando um cliente MCP (ex. Claude Code) se conectar via entrada/saída padrão do processo.
- **Como rodar o teste automatizado:**
  ```
  pytest
  ```
  O teste em [`tests/test_server.py`](tests/test_server.py) chama `linkedin_mcp_status` diretamente e verifica os cinco campos estáticos, sem subir o transporte MCP nem tocar em rede. Executado nesta etapa: **1 passed**.

## Etapa 6B. Preparação do container e do Fly.io

- **O que foi preparado:** os arquivos necessários para empacotar o `mcp-linkedin` como uma imagem Docker e descrever, conceitualmente, como ela rodaria no Fly.io. **Nenhum deploy foi feito.** Nenhuma conta ou app no Fly.io existe. Nenhum domínio, DNS ou secret real foi configurado.
- [`Dockerfile`](Dockerfile): baseado em `python:3.12-slim`, instala o pacote com `pip install .` (usando o layout `src/mcp_linkedin/`, agora declarado explicitamente em `pyproject.toml`) e executa `python -m mcp_linkedin.server` com `MCP_TRANSPORT=streamable-http`. **Porta atualizada na Etapa 6D** (era `8080`, pensada para o Fly.io; ver seção abaixo). Não contém, nem copia para dentro da imagem, nenhuma credencial, `.env`, `.venv` ou segredo.
- [`.dockerignore`](.dockerignore): garante que `.env`, `.env.*`, `secrets/`, `.venv/`, chaves (`*.key`, `*.pem`, `*.enc`) e caches locais nunca sejam copiados para a imagem.
- [`fly.toml`](fly.toml): configuração conceitual do Fly.io criada nesta etapa. **Fly.io — legado / não utilizado**, ver Etapa 6D.
- **Backend de produção do `TokenStore` ainda não foi implementado.** A decisão entre um armazenamento persistente + arquivo criptografado, um KV externo ou um banco fica para uma etapa própria; nada disso está presente nesta preparação.
- **Validação local:** Docker não está disponível neste ambiente de desenvolvimento no momento desta etapa, então nenhum `docker build` foi executado (e não seria executado sem autorização explícita, já que baixaria a imagem base `python:3.12-slim` da internet).

## Etapa 6D. Migração de Fly.io para Render

- **Decisão:** a infraestrutura de produção deixou de ser o Fly.io e passou a ser o **Render**. O Fly CLI chegou a ser instalado e o login não foi concluído; a decisão de migrar veio antes de qualquer deploy real, então **nenhum app e nenhum recurso chegaram a ser criados no Fly.io**.
- **`fly.toml` — Fly.io — legado / não utilizado.** O arquivo permanece no repositório como registro histórico da Etapa 6B, mas não é mais referenciado por nenhum processo de deploy deste componente.
- [`render.yaml`](render.yaml) **(novo):** configuração mínima do Render — serviço web, runtime Docker, plano `free`, região `virginia` (US East). Não existe hoje uma região do Render em São Paulo/Brasil (há apenas um pedido de recurso em aberto na Render para isso); `virginia` foi escolhida por ser, entre as regiões atualmente oferecidas (`oregon`, `ohio`, `virginia`, `frankfurt`, `singapore`), a mais próxima geograficamente da América do Sul. Sem `healthCheckPath` (não existe endpoint simples de "estou vivo" hoje, só `/mcp`, que espera o protocolo MCP) e sem `PORT` declarada (o Render já fornece essa variável automaticamente, `10000` por padrão).
- **`Dockerfile` alterado:** removida a variável `ENV PORT=8080` (premissa específica do Fly.io); `EXPOSE` passou de `8080` para `10000`, documentando o padrão atual do Render. `MCP_TRANSPORT=streamable-http` continua fixado na imagem. Nenhuma alteração de código Python foi necessária: `resolve_run_config` (Etapa 5C) já lê `PORT` do ambiente dinamicamente, então o servidor se adapta ao valor real fornecido pelo Render sem nenhuma mudança.
- **Nenhum deploy foi feito nesta etapa.** Nenhuma conta Render foi acessada, nenhum CLI do Render instalado, nenhum repositório conectado ao Render.

## O que é

`mcp-linkedin` é um componente isolado dentro do repositório `amc-ia-Mobi`, com dependências, configuração e credenciais próprias, separado do restante do projeto (agentes de captação, comandos, skills). O AMC-IA-Mobi continua um sistema CLI e não é transformado em servidor web por causa deste componente.

O objetivo final deste componente é permitir que o Claude, através do protocolo MCP, leia dados da Página Mobilizando no LinkedIn (publicações, engajamento, comentários, eventos, relatórios de anúncio quando autorizados) e publique conteúdo, tanto no perfil pessoal quanto na Página Mobilizando, sempre mediante confirmação explícita.

## O que ainda não existe (pendente de autorização futura)

- **OAuth Claude → mcp-linkedin (Camada 1).** Ainda não implementado. Será o servidor de autorização que o Claude.ai usa para se conectar a este componente como um conector personalizado.
- **OAuth mcp-linkedin → LinkedIn (Camada 2).** Ainda não implementado. Será o fluxo pelo qual este componente se autentica na API do LinkedIn em nome do app Mobi.
- **Cliente HTTP para a API do LinkedIn.** Ainda não implementado.
- **Ferramentas MCP funcionais** (leitura ou publicação). Ainda não implementadas.
- **Servidor MCP em funcionamento** (transporte stdio ou Streamable HTTP). Ainda não implementado.
- **Decisão de infraestrutura de deploy.** Ainda não tomada. As opções em avaliação (Cloudflare Workers ou hospedagem Python persistente) estão descritas no plano técnico, mas nenhuma foi contratada ou configurada.
- **Domínio e endpoint HTTPS público.** Ainda não definidos.

## Fora do escopo desta etapa e das próximas etapas imediatas

Os seguintes produtos do LinkedIn permanecem **fora de qualquer implementação** até que sejam explicitamente aprovados e autorizados:

- Lead Sync
- Conversions API
- Ad Library
- Matched Audiences

Ter o escopo visível no aplicativo Mobi do LinkedIn Developer Portal não significa que o produto correspondente está aprovado para uso em produção. Cada capacidade será verificada individualmente antes de qualquer código ser escrito para ela.

## Estrutura

```
mcp-linkedin/
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
├── Dockerfile              # imagem de producao, adaptada ao Render na Etapa 6D
├── .dockerignore           # impede .env/secrets/.venv de entrarem na imagem
├── fly.toml                # Fly.io -- legado / nao utilizado (Etapa 6D)
├── render.yaml             # configuracao do Render (Etapa 6D), sem secrets
├── src/
│   └── mcp_linkedin/
│       ├── server.py            # servidor MCP local mínimo, tool linkedin_mcp_status
│       ├── config.py            # leitura de configuração (vazio nesta etapa)
│       ├── auth_claude/         # Camada 1: Claude.ai <-> este servidor (vazio nesta etapa)
│       ├── auth_linkedin/       # Camada 2: este servidor <-> LinkedIn (vazio nesta etapa)
│       ├── linkedin_client/     # cliente HTTP da API do LinkedIn (vazio nesta etapa)
│       └── tools/                # ferramentas MCP funcionais futuras (vazio nesta etapa)
└── tests/
    └── test_server.py           # testa linkedin_mcp_status, sem chamada externa
```

## Segredos

Nenhuma credencial real existe neste componente ainda. `.env.example` lista apenas os nomes das variáveis que serão necessárias no futuro, sem valores. Um `.env` real, se algum dia criado, nunca deve ser versionado e nunca deve ser o mesmo `.env` usado pelo restante do AMC-IA-Mobi.

## Próximos passos

Qualquer implementação (OAuth, cliente HTTP, ferramentas MCP, servidor funcional, infraestrutura de deploy) depende de nova autorização explícita, etapa por etapa, conforme o plano técnico já aprovado.
