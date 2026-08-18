# Integração com a API pública do CaptaHub

> Conector que liga a AMC IA à API REST do CaptaHub (já em produção). O CaptaHub
> é a fonte da verdade: editais (globais, leitura), pipeline de projetos e clientes (OSCs),
> ambos por usuário. O contrato completo do servidor está em `docs/prompt-api-captahub.md`.

## 1. Configuração (.env)

Tudo no `.env` (gitignorado, único lugar autorizado para segredos):

```
CAPTAHUB_API_URL=https://pkwwnajskprfutfavylq.supabase.co/functions/v1/api
CAPTAHUB_API_TOKEN=cpth_***   (token pessoal; nunca exibir sem máscara)
```

Toda chamada manda `Authorization: Bearer ${CAPTAHUB_API_TOKEN}`. O token é multi-tenant:
só enxerga e altera o pipeline e os clientes do próprio dono. Editais são globais.

## 2. O conector (`scripts/captahub-api.py`)

Módulo único, só biblioteca padrão (mesmo padrão dos outros scripts do projeto). Tem a
classe `CaptaHubClient` (injeta base URL + Bearer, faz GET/POST/PATCH, trata paginação e
normaliza erro) e uma linha de comando que os comandos e agentes invocam via Bash. A saída traz um
bloco legível para o chat e um bloco `=== JSON ===` para os agentes consumirem.

| Subcomando | O que faz | Endpoint |
|---|---|---|
| `testar` / `me` | testa a conexão, mostra dono e escopos | `GET /v1/me` |
| `editais [filtros]` | lista editais (globais) | `GET /v1/editais` |
| `edital --id` | um edital | `GET /v1/editais/{id}` |
| `estagios` | os 11 estágios do pipeline | `GET /v1/pipeline/estagios` |
| `projetos [filtros]` | lista a carteira do usuário | `GET /v1/projetos` |
| `projeto --id` | um projeto | `GET /v1/projetos/{id}` |
| `projeto-criar` | cria projeto (edital + cliente) | `POST /v1/projetos` |
| `projeto-atualizar` | move estágio, grava nota e valores | `PATCH /v1/projetos/{id}` |
| `clientes [filtros]` | lista as OSCs do usuário | `GET /v1/clientes` |
| `cliente --id` | uma OSC | `GET /v1/clientes/{id}` |
| `cliente-criar` | cria OSC | `POST /v1/clientes` |
| `cliente-atualizar` | edita OSC (parcial) | `PATCH /v1/clientes/{id}` |

Filtros de editais: `--scope` (Municipal/Estadual/Nacional/Internacional), `--category`,
`--q`, `--value-min`, `--value-max`, `--deadline-after`, `--deadline-before`,
`--is-continuous`, `--only-open`, `--limit` (máx 200, padrão 50), `--offset`, `--all`
(percorre todas as páginas). Listas respondem `{ data, total, limit, offset, has_next }`.

Exemplos:

```
python3 scripts/captahub-api.py testar
python3 scripts/captahub-api.py editais --scope Nacional --only-open --limit 20
python3 scripts/captahub-api.py projeto-atualizar --id <uuid> --status submetido --nota-tecnica 9 --data-submissao 2026-07-01
python3 scripts/captahub-api.py cliente-criar --nome "OSC Teste" --uf PE
```

## 3. Mapeamento de campos (API → modelos da AMC IA)

A AMC IA guarda os dados em arquivos markdown. O conector traduz entre os campos da
API e esses modelos. Datas sempre ISO (AAAA-MM-DD); valores monetários em reais (número),
não centavos; campo desconhecido vem `null` (nunca string vazia nem 0).

### 3.1 Edital → `base-editais/*.json` e `projetos/{slug}/edital.md`

| Campo da API | Modelo da AMC IA | Observação |
|---|---|---|
| `id` (uuid) | id do edital (referência ao CaptaHub) | usado em `edital_id` ao criar projeto |
| `title` | Título do edital | nunca nulo |
| `institution` | Órgão / financiador | |
| `category` | Categoria | |
| `scope` | Escopo (Municipal/Estadual/Nacional/Internacional) | nunca nulo |
| `value` | Valor | **`null` = "não informado"** (nunca 0) |
| `deadline` | Prazo de submissão | `null` = sem data; vencido é descartado por `only_open` |
| `is_continuous` | Fluxo contínuo | |
| `url` | Link do edital | |
| `description` | Descrição / objeto | base para `/edital-analisar` |
| `tags` | Palavras-chave | array ou null |
| `data_publicacao` | Data de publicação | timestamp ISO |

### 3.2 Cliente/OSC → `minhas-oscs/{slug}/perfil-osc.md`

| Campo da API | Seção/campo no `perfil-osc.md` |
|---|---|
| `nome` | Nome da organização |
| `sigla` | Sigla / nome fantasia |
| `cnpj` | CNPJ |
| `natureza_juridica` | Natureza jurídica |
| `fundacao` (AAAA-MM-DD) | Data de fundação / tempo de existência |
| `municipio`, `uf` | Município e UF (sede) |
| `territorios` (array) | Territórios de atuação |
| `areas_tematicas` (array) | Área(s) temática(s) |
| `missao` | Missão |
| `site` | Site e redes |
| `email`, `telefone` | Contato |
| `status_documental` (objeto de booleanos) | Situação documental (checklist do CaptaDoc) |
| `historico_aprovacoes` (array {financiador, valor, ano}) | Projetos já aprovados |

Chaves esperadas em `status_documental`: `cnpj_ativo`, `estatuto`, `cebas`,
`certidao_federal`, `certidao_estadual`, `certidao_municipal`, `fgts`, `cndt`,
`transferegov` (cada uma booleana). O checklist do `perfil-osc.md` (CNPJ ativo, Estatuto,
CEBAS, certidões federal/estadual/municipal, FGTS, CNDT, Transferegov) mapeia direto.

### 3.3 Projeto → estado do projeto e entregáveis dos 4 agentes

O projeto na API é o cartão da carteira no CaptaHub. A AMC IA elabora localmente
(`elegibilidade.md`, `proposta.md`, `orcamento.md`, `score.md`) e sincroniza o resultado
de volta para o cartão.

| Campo da API | Origem na AMC IA |
|---|---|
| `nome` | título do projeto/edital |
| `cliente_id` | id da OSC ativa no CaptaHub |
| `edital_id` | id do edital (do `/v1/editais`) |
| `descricao` | resumo do projeto |
| `status` | etapa da linha de montagem (um dos 11 estágios) |
| `nota_tecnica` (0..10) | nota do **CaptaScore** (`score.md`) |
| `chance_aprovacao` (string) | chance estimada pelo **CaptaScore** |
| `valor_solicitado` | total do **CaptaBudget** (`orcamento.md`) |
| `valor_aprovado` | valor contemplado (pós-resultado) |
| `data_submissao` (AAAA-MM-DD) | data de envio |

Estágios canônicos, em ordem: `selecionado`, `encontrar_cliente`, `checklist`, `contrato`,
`separar_documentos`, `elaborar_projeto`, `submetido`, `aprovado`, `reprovado`,
`pagamento_pendente`, `pagamento_recebido`.

## 4. Gotchas (cuidados que o conector já trata)

- **`value` de edital vem `null`** quando desconhecido (nunca 0). A exibição mostra "não informado".
- **`status_documental` no PATCH SUBSTITUI o objeto inteiro** (não faz merge). Para mudar um
  documento, envie o objeto completo. O conector deixa isso explícito.
- **Multi-tenant:** o token só vê os dados do próprio dono. `GET` de um id de outro usuário
  retorna 404 por design.
- **Erros normalizados:** `{ "error": { "code", "message" } }`, status 400/401/403/404/422/429/500,
  traduzidos para mensagem em português pela classe `CaptaHubAPIError`.
- **Paginação:** `--all` percorre todas as páginas usando `has_next`/`offset`.

## 5. Fronteira de posicionamento

O CaptaHub continua sendo a casa da carteira (pipeline e CRM). Este conector não traz gestão
de pipeline para dentro da AMC IA; ele permite **ler** editais e a carteira e
**sincronizar de volta** o resultado da elaboração (criar o projeto, gravar nota, valores e
status). É complementar, como manda o CLAUDE.md.
