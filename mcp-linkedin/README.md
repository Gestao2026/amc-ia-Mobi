# mcp-linkedin

## Status

O servidor MCP está implementado com as **duas camadas de OAuth prontas**: a Camada 1 (Claude.ai ↔ este servidor, Etapa 7A) e a Camada 2 (este servidor ↔ LinkedIn, Etapa 7B). O fluxo `MCP → autorização → callback → troca do authorization code → armazenamento do token` está completo e coberto por testes, mas **nunca foi executado contra o LinkedIn real**: depende de cadastrar o Redirect URI no LinkedIn Developer Portal e configurar as credenciais no Render.

**Nenhuma ferramenta de negócio do LinkedIn** (ler publicações, engajamento, comentários, ou publicar) existe ainda. Nenhum deploy foi feito.

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

## Etapa 7A. OAuth Claude ↔ mcp-linkedin (Camada 1)

- **O que foi implementado:** um Authorization Server mínimo para proteger a rota `/mcp`, permitindo o Claude.ai se conectar via "Adicionar conector personalizado". Reaproveita quase inteiramente o SDK oficial (`mcp.server.auth`): descoberta RFC 8414/RFC 9728, o handshake `401 + WWW-Authenticate`, e a validação PKCE S256 já vêm prontos do SDK; este componente só implementa o `OAuthAuthorizationServerProvider`.
- [`src/mcp_linkedin/auth_claude/client_registry.py`](src/mcp_linkedin/auth_claude/client_registry.py): registro de um único cliente estático (sem DCR), pré-registrado via `MCP_CLAUDE_CLIENT_ID`/`MCP_CLAUDE_CLIENT_SECRET`, com o redirect_uri fixo e público `https://claude.ai/api/mcp/auth_callback`.
- [`src/mcp_linkedin/auth_claude/session_store.py`](src/mcp_linkedin/auth_claude/session_store.py): authorization codes (TTL de 5 minutos, uso único), access tokens (TTL de 1 hora) e refresh tokens (TTL de 30 dias, com rotação a cada uso), **somente em memória** — decisão explícita desta v1, só para validar o fluxo no Render. Reiniciar o processo derruba as sessões.
- [`src/mcp_linkedin/auth_claude/provider.py`](src/mcp_linkedin/auth_claude/provider.py): o `OAuthAuthorizationServerProvider`. Sem tela de consentimento (decisão explícita): depois que o SDK já validou client_id/redirect_uri/response_type, autoriza e redireciona imediatamente. DCR (`/register`) e revogação (`/revoke`) ficam desligados.
- [`server.py`](src/mcp_linkedin/server.py): nova função pura `resolve_claude_auth_config` (mesmo padrão de `resolve_run_config`), lendo `MCP_CLAUDE_CLIENT_ID`, `MCP_CLAUDE_CLIENT_SECRET` (opcional) e `MCP_PUBLIC_BASE_URL` do ambiente. Se ausentes, a Camada 1 fica desligada (comportamento idêntico ao de antes desta etapa). `main()` só passa a configurar isso quando o transporte é `streamable-http`.
- **PKCE S256:** não implementado manualmente — confirmado por inspeção do código-fonte do SDK que o próprio `TokenHandler` calcula e compara o `code_challenge`, rejeitando com `invalid_grant` em caso de divergência.
- **Nenhum acesso ao LinkedIn ou ao Claude.ai real.** Todos os 51 testes novos desta etapa usam valores fictícios (`FAKE_...`) e rodam inteiramente em processo (via `TestClient`), com bloqueio de qualquer conexão de rede que não seja loopback.
- **Achado de implementação:** quando `resource_server_url` não está na raiz (`<issuer>/mcp`), o SDK publica os metadados RFC 9728 em `/.well-known/oauth-protected-resource/mcp` (com o sufixo do path), não em `/.well-known/oauth-protected-resource` sozinho — confirmado testando contra o SDK real antes de escrever os testes.
- **Pendências conhecidas, fora do escopo desta etapa:** armazenamento em memória (não sobrevive a reinício do processo no Render); ausência de tela de consentimento visível (a segurança desta v1 depende do `client_id` permanecer conhecido só por quem o configurou no Claude.ai, mais o PKCE obrigatório).

## Etapa 7B. OAuth mcp-linkedin ↔ LinkedIn (Camada 2)

- **O que foi implementado:** a infraestrutura OAuth completa da Camada 2, ligando as peças que existiam soltas desde as Etapas 3 e 4 num fluxo único e funcional: `MCP → URL de autorização → LinkedIn → callback → troca do authorization code → armazenamento do token`. **Nenhuma ferramenta de negócio do LinkedIn (leitura ou publicação) foi implementada nesta etapa**, e nenhuma chamada à API do LinkedIn existe além do endpoint de token.
- [`config.py`](src/mcp_linkedin/config.py): `resolve_linkedin_config`, função pura no mesmo padrão de `resolve_run_config`, lendo `LINKEDIN_CLIENT_ID`, `LINKEDIN_CLIENT_SECRET`, `MCP_PUBLIC_BASE_URL` e as opcionais `LINKEDIN_SCOPES` e `LINKEDIN_TOKEN_STORE_BACKEND`. Se qualquer obrigatória faltar, a Camada 2 fica desligada e o servidor sobe normalmente sem ela. `LinkedInConfig.__repr__` mascara o Client Secret.
- **O `redirect_uri` não é uma variável própria:** é sempre derivado de `MCP_PUBLIC_BASE_URL` + `/oauth/linkedin/callback`. O mesmo valor precisa estar cadastrado no LinkedIn Developer Portal, ser enviado na URL de autorização e ser reenviado na troca por token; se divergirem, o LinkedIn recusa a troca. Uma variável separada só criaria a chance de divergirem.
- [`auth_linkedin/http_transport.py`](src/mcp_linkedin/auth_linkedin/http_transport.py) **(novo):** `HttpxTransport`, a primeira implementação real do Protocol `HttpTransport`. É o único ponto do componente que abre conexão de rede para o LinkedIn. Usa `httpx2` (a linha 2.x do httpx), que já vinha instalada como dependência do próprio `mcp` 2.0.0, então **nenhuma instalação nova foi necessária**. Timeout de 10s, redirecionamento automático desligado (para o corpo com as credenciais nunca ser reenviado a outro host) e conversão das exceções do httpx2 em `TransportError` com `from None`, para o traceback encadeado não carregar o objeto `Request` que referencia o corpo com o Client Secret.
- [`auth_linkedin/runtime.py`](src/mcp_linkedin/auth_linkedin/runtime.py) **(novo):** `LinkedInOAuthRuntime` compõe as peças existentes com estado compartilhado de vida longa. É o motivo de o módulo existir: o `state` gerado ao iniciar a autorização só pode ser validado depois, no callback, pelo **mesmo** `StateStore`.
- [`auth_linkedin/token_store.py`](src/mcp_linkedin/auth_linkedin/token_store.py): novo `InMemoryCredentialBackend`, necessário porque o container de produção no Render roda Linux, onde o Windows Credential Manager (e o próprio `pywin32`) não existe. Não persiste: reiniciar o processo exige nova autorização, mesma decisão já tomada para as sessões da Camada 1.
- [`server.py`](src/mcp_linkedin/server.py): rota `GET /oauth/linkedin/callback` via `custom_route` (rotas assim não exigem autorização no SDK, necessário porque o LinkedIn não envia o Bearer da Camada 1; a proteção é o `state` de uso único). **Responde JSON, nunca HTML: este componente não tem interface web.** Três ferramentas MCP: `linkedin_oauth_iniciar` (devolve a URL de autorização, sem o state isolado), `linkedin_oauth_status` (informa se há token válido, nunca o token) e `linkedin_mcp_status` (agora dinâmica, reportando também quais variáveis faltam configurar, por nome, nunca por valor).
- **Escopos:** o padrão é conservador (`openid profile email`, o conjunto mínimo do OpenID Connect), configurável por `LINKEDIN_SCOPES`. Pedir um escopo que o app não tem aprovado faz o LinkedIn recusar a autorização inteira, então os escopos de Página só devem entrar depois de confirmados como aprovados no app Mobi.
- **Nenhum acesso ao LinkedIn real nos testes.** Os 70 testes novos usam valores fictícios (prefixo `FAKE_`, domínio `.invalid` da RFC 2606), transporte HTTP falso ou `httpx2.MockTransport` (que exercita o `post` real de produção sem nenhum pacote sair da máquina), `InMemoryCredentialBackend` no lugar do Credential Manager real, e vários bloqueiam ativamente qualquer conexão que não seja loopback. Suíte total: **231 passed**.
- **Pendências conhecidas, fora do escopo desta etapa:** armazenamento do token em memória (não sobrevive a reinício do processo no Render); `StateStore` também em memória, então a janela de 10 minutos da autorização não sobrevive a um restart; nenhum refresh automático do token do LinkedIn.

## Etapa 7C. Backend de produção do token (Supabase com cifragem em envelope)

### O problema verificado

O `Win32CredentialBackend` **instancia** normalmente no Linux (o import de `win32cred` é preguiçoso, dentro de cada método), mas toda operação real falha com `ModuleNotFoundError`: `write` (`win32cred`), `read` e `delete` (`pywintypes`). O `pywin32` nem chega a ser instalado lá, porque o próprio `mcp` o declara como `pywin32>=311; sys_platform == 'win32'`.

O agravante é **quando** isso quebraria: o servidor sobe, `linkedin_oauth_iniciar` devolve a URL, o captador autoriza no LinkedIn, e só então a gravação no callback explode, virando um 502. A falha chega depois de a pessoa já ter feito o trabalho, e sem token gravado.

### O que foi implementado

- [`auth_linkedin/crypto.py`](src/mcp_linkedin/auth_linkedin/crypto.py) **(novo):** cifragem em envelope com **AES-256-GCM** (autenticado), nonce aleatório de 12 bytes por operação, no formato `base64(nonce || ciphertext)`. A chave vem de `LINKEDIN_TOKEN_ENCRYPTION_KEY`, nunca do banco: **banco e chave ficam em domínios de confiança diferentes**, então um dump vazado do banco, sozinho, não entrega o token. É a mesma propriedade que o DPAPI dá localmente.
- [`auth_linkedin/supabase_backend.py`](src/mcp_linkedin/auth_linkedin/supabase_backend.py) **(novo):** `SupabaseCredentialBackend`, sobre a API REST (PostgREST) via `httpx2`. Sem SDK novo, no mesmo padrão de `scripts/captahub-api.py`. Chave de API só em cabeçalho, nunca na URL. Qualquer resposta fora de 2xx é erro, **inclusive 3xx**: com `follow_redirects` desligado, um redirecionamento significa que a requisição não foi atendida, e o host de destino nunca chega a receber os cabeçalhos com a chave.
- [`auth_linkedin/token_store.py`](src/mcp_linkedin/auth_linkedin/token_store.py): `EncryptedCredentialBackend`, que envelopa **qualquer** outro backend. Composição em vez de acoplamento: a cifragem é testável sem rede, e o backend do Supabase não precisa saber que existe cifragem. No Windows local **não** se aplica cifragem, porque o DPAPI já protege e uma segunda chave só acrescentaria gestão sem ganho.
- **Falha de decifragem devolve `None`, não exceção.** O efeito prático é "não há token válido", que leva o captador a reautorizar. É o desfecho recuperável correto quando a chave foi trocada ou o dado corrompeu, e evita derrubar a ferramenta de status por causa disso.
- [`config.py`](src/mcp_linkedin/config.py): novo backend `supabase`, que exige `MCP_LINKEDIN_SUPABASE_URL`, `MCP_LINKEDIN_SUPABASE_KEY` e `LINKEDIN_TOKEN_ENCRYPTION_KEY`. A chave de cifragem é **validada na inicialização**, não na primeira gravação: erro de configuração precisa aparecer antes de o captador gastar uma autorização no LinkedIn.
- **Footgun corrigido:** `LINKEDIN_TOKEN_STORE_BACKEND=windows` fora do Windows era aceito sem reclamar e só falhava no callback. Agora é recusado na inicialização, com mensagem apontando para `supabase`.
- **Isolamento (regra do CLAUDE.md):** credenciais próprias (`MCP_LINKEDIN_SUPABASE_*`), nunca o `SUPABASE_KEY` do `.env` da raiz do AMC-IA-Mobi.
- **55 testes novos** (total: **286 passed**), nenhum acessando o Supabase real: `httpx2.MockTransport` intercepta dentro do próprio httpx2, então o código de produção roda inteiro sem nenhum pacote sair da máquina.

### Tabela a criar no Supabase

```sql
create table if not exists mcp_linkedin_tokens (
  target_name text primary key,
  secret      text not null,
  updated_at  timestamptz not null default now()
);

-- O conteúdo já chega cifrado, mas a tabela não deve ser exposta
-- pela API pública: só a chave de serviço deste componente a acessa.
alter table mcp_linkedin_tokens enable row level security;
```

A chave primária em `target_name` é o que faz o upsert (`Prefer: resolution=merge-duplicates`) funcionar.

### Como gerar a chave de cifragem

```bash
python -c "from mcp_linkedin.auth_linkedin.crypto import generate_key_base64; print(generate_key_base64())"
```

Gere **uma vez**, guarde como secret no Render, e não versione. Trocar a chave invalida o token guardado, o que só custa uma reautorização.

### Restrição registrada, sem trabalho agora

O `StateStore` continua em memória. Pela TTL de 10 minutos ele **não** precisa de durabilidade, mas exige que o callback caia na **mesma instância** que emitiu o state. No plano free (instância única) está correto; se o serviço escalar para mais de uma instância, o state precisa ir para o armazenamento compartilhado, senão as autorizações passam a falhar de forma intermitente.

## Etapa 7D. Ponte HTTPS na HostGator (backend de produção atual)

### Por que trocar o Supabase pela ponte

Decisão de infraestrutura: o armazenamento de produção passou a ser o MySQL da HostGator. A conexão **direta** Render → MySQL foi **descartada** e não deve ser implementada: os IPs de saída do Render são faixas CIDR **compartilhadas com todos os clientes da mesma região** ([Render Docs](https://render.com/docs/outbound-ip-addresses)), e liberá-las em Remote MySQL deixaria o banco alcançável por qualquer serviço hospedado no Render. IPs dedicados são add-on pago.

A ponte resolve isso: o MySQL continua escutando **só em localhost**, e nada precisa ser liberado.

```
Render (mcp-linkedin) --HTTPS autenticado--> ponte.mobilizando.org/token.php --> MySQL localhost
```

### O que foi implementado

- [`auth_linkedin/ponte_backend.py`](src/mcp_linkedin/auth_linkedin/ponte_backend.py) **(novo):** `PonteCredentialBackend`, mesma forma do backend do Supabase. **Nenhuma dependência nova:** o `httpx2` já cobria tudo (a rota do MySQL direto teria exigido o PyMySQL).
- [`ponte-hostgator/`](ponte-hostgator/) **(novo):** `token.php`, `.htaccess`, `mcp-linkedin-config.exemplo.php` e o guia de instalação. **Não são deployados pelo Render**, vão por FTP/cPanel.
- **Autenticação:** segredo compartilhado em cabeçalho, validado com **`hash_equals()`** (tempo constante). O `token.php` aceita `X-MCP-Ponte-Secret` **e** `Authorization: Bearer`, porque em hospedagem compartilhada o `Authorization` costuma ser removido pelo CGI/FastCGI antes de chegar ao PHP. Sem essa redundância, a autenticação funcionaria nos testes e falharia em produção.
- **HTTPS obrigatório nas duas pontas:** o `config.py` recusa uma URL que não comece com `https://` na inicialização, e o `token.php` recusa requisição que não chegue por HTTPS. O envelope AES protege o token, mas o segredo da ponte viaja em cabeçalho e iria em claro por HTTP.
- **PDO com prepared statements**, `ATTR_EMULATE_PREPARES => false`, upsert por `ON DUPLICATE KEY UPDATE`. Erros do PDO nunca são ecoados nem registrados: a mensagem pode conter usuário e host do banco.
- **O alvo é fixo no servidor.** O `token.php` valida o `alvo` recebido contra o esperado, então a ponte não serve como armazenamento genérico nem permite varrer outras chaves.
- **A senha do MySQL não é variável do Render.** Nesta arquitetura o Render nunca fala com o banco, só com a ponte; a senha existe apenas no `config.php` da HostGator, fora do `public_html`, com permissão 600.

### AES-GCM: inalterado

A cifragem **não mudou uma linha**. O `EncryptedCredentialBackend` passou a envelopar o `PonteCredentialBackend` exatamente como envelopa o do Supabase.

**O PHP nunca recebe, conhece ou guarda a chave AES.** Ela existe apenas no ambiente do Render. Um comprometimento total da HostGator entrega **apenas ciphertext**. Há testes que provam cada parte disso: `test_a_ponte_nunca_recebe_a_chave_aes`, `test_ciphertext_e_o_unico_conteudo_que_chega_na_ponte` e `test_quem_tem_o_banco_da_ponte_nao_consegue_ler_o_token`.

### Correção de um defeito encontrado nesta rodada

`TokenStoreBackendError` escapava do `try` da rota de callback, então uma falha do armazenamento remoto (ponte fora do ar, Supabase indisponível) virava **HTTP 500 com traceback** em vez de um 502 limpo. A exceção passou a viver em `token_store.py`, compartilhada pelos dois backends remotos, e a rota agora a captura. Coberto por `test_callback_com_falha_de_armazenamento_responde_502`.

### O backend do Supabase continua disponível

Mantido conforme decisão, selecionável por `LINKEDIN_TOKEN_STORE_BACKEND=supabase`, com todos os seus testes. Há um teste que protege isso (`test_backend_supabase_continua_disponivel`).

### Testes

**331 passed.** Os do lado Python usam `httpx2.MockTransport`, que exercita o código real sem nenhum pacote sair da máquina. O contrato que o `token.php` precisa cumprir está codificado como **especificação executável** na classe `PonteFalsa` de [`tests/test_ponte.py`](tests/test_ponte.py).

**Limitação honesta:** não há PHP neste ambiente de desenvolvimento, então o `token.php` **não tem teste automatizado**. A verificação dele é o roteiro de `curl` em [`ponte-hostgator/README.md`](ponte-hostgator/README.md), a ser rodado depois do upload.

## O que é

`mcp-linkedin` é um componente isolado dentro do repositório `amc-ia-Mobi`, com dependências, configuração e credenciais próprias, separado do restante do projeto (agentes de captação, comandos, skills). O AMC-IA-Mobi continua um sistema CLI e não é transformado em servidor web por causa deste componente.

O objetivo final deste componente é permitir que o Claude, através do protocolo MCP, leia dados da Página Mobilizando no LinkedIn (publicações, engajamento, comentários, eventos, relatórios de anúncio quando autorizados) e publique conteúdo, tanto no perfil pessoal quanto na Página Mobilizando, sempre mediante confirmação explícita.

## O que ainda não existe (pendente de autorização futura)

- **Cliente HTTP para a API do LinkedIn.** Ainda não implementado. O `HttpxTransport` da Etapa 7B fala só com o endpoint de token, não com a API de conteúdo.
- **Ferramentas MCP de negócio** (leitura ou publicação do LinkedIn). Ainda não implementadas.
- **Autorização real no app Mobi.** O fluxo da Etapa 7B nunca foi executado contra o LinkedIn de verdade: depende de cadastrar o Redirect URI no LinkedIn Developer Portal e de configurar as credenciais no Render.
- **Criar a tabela no Supabase e configurar as credenciais.** O backend de produção está implementado (Etapa 7C), mas a tabela ainda não existe e nenhuma credencial foi configurada no Render.
- **Refresh automático do token do LinkedIn.** Ainda não implementado: quando o token expira, é preciso rodar `linkedin_oauth_iniciar` de novo.
- **Domínio próprio (`mcp.mobilizando.org`).** Ainda não configurado; o serviço roda hoje só no domínio temporário do Render.

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
│       ├── server.py            # servidor MCP, transporte, Camada 1, rota de callback e ferramentas OAuth
│       ├── config.py            # configuracao da Camada 2 (Etapa 7B)
│       ├── auth_claude/         # Camada 1: Claude.ai <-> este servidor (Etapa 7A)
│       │   ├── client_registry.py
│       │   ├── session_store.py
│       │   └── provider.py
│       ├── auth_linkedin/       # Camada 2: este servidor <-> LinkedIn (Etapa 7B, ligada)
│       │   ├── state_store.py
│       │   ├── oauth_flow.py
│       │   ├── oauth_callback.py
│       │   ├── token_exchange.py
│       │   ├── token_store.py       # backends: Windows, memoria, cifrado
│       │   ├── crypto.py            # cifragem em envelope (AES-256-GCM)
│       │   ├── supabase_backend.py  # backend de producao (Etapa 7C)
│       │   ├── http_transport.py    # unico ponto que abre rede para o LinkedIn
│       │   └── runtime.py           # compoe o fluxo, com StateStore/TokenStore compartilhados
│       ├── linkedin_client/     # cliente HTTP da API do LinkedIn (vazio nesta etapa)
│       └── tools/                # ferramentas MCP de negocio futuras (vazio nesta etapa)
└── tests/                        # 286 testes, nenhum acessa rede real (Etapa 7C)
```

## Segredos

Nenhuma credencial real existe neste componente ainda. `.env.example` lista apenas os nomes das variáveis que serão necessárias no futuro, sem valores. Um `.env` real, se algum dia criado, nunca deve ser versionado e nunca deve ser o mesmo `.env` usado pelo restante do AMC-IA-Mobi.

## Próximos passos

Qualquer implementação (OAuth, cliente HTTP, ferramentas MCP, servidor funcional, infraestrutura de deploy) depende de nova autorização explícita, etapa por etapa, conforme o plano técnico já aprovado.
