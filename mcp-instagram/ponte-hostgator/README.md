# Ponte de armazenamento na HostGator

Arquivos deste diretório **não** são deployados pelo Render. Eles vão para a HostGator, por FTP ou pelo Gerenciador de Arquivos do cPanel.

```
Render (mcp-instagram) --HTTPS autenticado--> ponte.mobilizando.org/token-instagram.php --> MySQL localhost
```

---

## LEIA ISTO ANTES: os caminhos reais da conta rosepa59

Instalado e funcionando em 21/08/2026. Esta seção existe porque a instalação levou horas por causa de duas armadilhas que nenhuma ferramenta mostrava com clareza. Ler daqui poupa esse tempo.

### Armadilha 1. Existem duas pastas `ponte-mcp`

A raiz da conta é `/home2/rosepa59`, e **dentro dela existe outra pasta chamada `home2`**. A árvore real é:

```
/home2/rosepa59/
├── home2/rosepa59/ponte-mcp/        ← ESTA é a que o servidor web usa
│   ├── mcp-linkedin-config.php
│   ├── mcp-instagram-config.php
│   └── public/                      ← docroot de ponte.mobilizando.org
│       ├── .well-known/             (validação do certificado SSL)
│       ├── .htaccess
│       ├── token.php
│       └── token-instagram.php
│
└── ponte-mcp/                       ← duplicata, IGNORAR
    └── public/
```

**Como saber qual é a certa:** a verdadeira contém o `token.php` que responde na web e a pasta `.well-known/acme-challenge`, que só existe em raiz de site de verdade.

O caminho de destino ao mover arquivos, portanto, é:

```
/home2/rosepa59/home2/rosepa59/ponte-mcp/public
```

Parece errado. Não é.

### Armadilha 2. O Gerenciador de Arquivos do cPanel mente

Durante a instalação ele, em sequência:

- afirmou que `token-instagram.php` não existia, enquanto o próprio cPanel respondia `File exists` ao tentar criá-lo;
- escondeu o `.htaccess` mesmo com "mostrar arquivos ocultos" ligado;
- listou uma pasta com um item quando ela tinha quatro.

**A busca funciona quando a listagem falha.** Use o campo de pesquisa do gerenciador para encontrar arquivos, e clique duas vezes no resultado para abrir a pasta que os contém.

**Não confie na listagem para concluir que algo não existe.** Confie no servidor: um `curl` do endereço público responde com a verdade.

### Armadilha 3. O diálogo "Copiar" espera uma pasta, não um nome de arquivo

Informar `/caminho/arquivo-novo.php` faz o cPanel tratar isso como pasta de destino e criar a estrutura inteira em duplicata. Foi assim que a segunda `ponte-mcp` nasceu.

Para copiar renomeando, copie para outra pasta e renomeie depois, ou crie o arquivo e cole o conteúdo.

### Armadilha 4. O `.htaccess` é compartilhado e fecha a porta por padrão

Existe **um único** `.htaccess` no docroot, servindo os dois componentes. A regra libera uma lista fechada de nomes:

```apache
<FilesMatch "^(?!(token|token-instagram)\.php$).*$">
    Require all denied
</FilesMatch>
```

Um arquivo novo naquela pasta **nasce bloqueado com 403** até ser acrescentado a essa lista. Se o seu arquivo responde 403, é aqui.

### Armadilha 5. O `token.php` em produção difere do que estava no repositório

Na versão que roda, o alvo **não** vem do arquivo de configuração: está escrito dentro do próprio programa, numa seção "Alvo FIXO". Trocar `ALVO` no config não tem efeito.

Ao criar a ponte de um componente novo, são **quatro** linhas a mudar, não uma:

| Linha | De | Para |
|---|---|---|
| cabeçalho | LinkedIn | Instagram |
| `$caminhoConfig` | `mcp-linkedin-config.php` | `mcp-instagram-config.php` |
| `$alvo` | `mcp-linkedin:linkedin-access-token` | `mcp-instagram:instagram-access-token` |
| `$tabela` (padrão) | `mcp_linkedin_tokens` | `mcp_instagram_tokens` |

A terceira é a mais importante: sem ela o Instagram grava com a etiqueta do LinkedIn, **sobrescreve o token dele e derruba os dois**.

### Armadilha 6. O config do LinkedIn não declara `DB_TABLE`

Ele funciona porque o PHP cai no padrão `mcp_linkedin_tokens`. Ao copiar esse arquivo como base para outro componente, **é obrigatório acrescentar a linha `DB_TABLE`**, senão o componente novo grava na tabela errada.

### Como confirmar que ficou certo, sem depender do cPanel

```bash
curl -s -o /dev/null -w '%{http_code}\n' -X POST \
  https://ponte.mobilizando.org/token-instagram.php \
  -H 'Content-Type: application/json' -d '{"acao":"ler"}'
```

| Resposta | Significado |
|---|---|
| **401** | **certo.** No ar, config lido e completo, recusando por falta do segredo |
| 403 | bloqueado pelo `.htaccess` |
| 404 | arquivo não está no docroot real (ver Armadilha 1) |
| 500 | config não encontrado, ou com campo vazio |

Vale testar também um arquivo que não existe: se responder **403** em vez de 404, o `.htaccess` está ativo.

## Por que a ponte existe

O MySQL da HostGator só aceita conexão externa se um IP for liberado em **Remote MySQL**. Os IPs de saída do Render são faixas CIDR **compartilhadas com todos os outros clientes da mesma região** (IPs dedicados são um add-on pago). Liberar essa faixa deixaria o banco alcançável por qualquer serviço hospedado no Render.

Com a ponte, o MySQL continua escutando **só em localhost** e nada precisa ser liberado.

## A propriedade de segurança central

**O PHP nunca recebe, conhece ou guarda a chave AES.** O valor que chega em `secret` já vem cifrado com AES-256-GCM pelo Render, e só o Render tem a chave (`INSTAGRAM_TOKEN_ENCRYPTION_KEY`).

Consequência prática: um comprometimento total desta hospedagem (banco, PHP e `config.php`) entrega **apenas texto cifrado**, inútil sem a chave. Há um teste automatizado que prova exatamente isso (`test_quem_tem_o_banco_da_ponte_nao_consegue_ler_o_token`).

## O que enviar, e para onde

A instalação real nesta conta (conferida em 20/08/2026 pelo gerenciador de
arquivos do cPanel) usa estes caminhos, e não os genéricos que este guia
supunha antes:

```
/home2/rosepa59/home2/rosepa59/ponte-mcp/
├── mcp-linkedin-config.php     0600   config do LinkedIn, fora da web
├── mcp-instagram-config.php    0600   config do Instagram, fora da web
└── public/                     0750   docroot do subdomínio ponte.mobilizando.org
    ├── .htaccess               0644   serve os dois componentes
    ├── token.php               0644   ponte do LinkedIn
    └── token-instagram.php     0644   ponte do Instagram
```

O que importa não é o nome das pastas, é a relação entre elas: o config fica
sempre **um nível acima** do docroot, porque o PHP o procura em
`__DIR__ . '/../mcp-instagram-config.php'`. Aqui o docroot chama-se `public/`
e a pasta-mãe `ponte-mcp/`; em outra conta os nomes podem mudar, a relação não.

| Arquivo | Destino | Permissão |
|---|---|---|
| `token-instagram.php` | `.../ponte.mobilizando.org/token-instagram.php` | 644 |
| `.htaccess` | `.../ponte.mobilizando.org/.htaccess` | 644 |
| `mcp-instagram-config.exemplo.php` | renomeado para `mcp-instagram-config.php`, **um nível ACIMA** do docroot | **600** |

O `config.php` fica **fora do docroot** de propósito: mesmo que o PHP pare de ser interpretado (uma falha real e comum em hospedagem compartilhada), o arquivo não pode ser baixado pela web. O `token-instagram.php` o procura em `__DIR__ . '/../mcp-instagram-config.php'`.

## Passo a passo

**1. Criar o subdomínio** `ponte.mobilizando.org` no cPanel e confirmar que o **AutoSSL** emitiu certificado. Sem HTTPS válido a ponte não funciona: o `token-instagram.php` recusa HTTP, e o Render recusa uma URL que não comece com `https://`.

**2. Criar a tabela** no banco `rosepa59_mcp_instagram` (phpMyAdmin → SQL):

```sql
CREATE TABLE IF NOT EXISTS mcp_instagram_tokens (
  target_name VARCHAR(191) NOT NULL PRIMARY KEY,
  secret      TEXT NOT NULL,
  updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

`VARCHAR(191)` e não `TEXT` na chave primária porque hospedagem compartilhada costuma rodar MySQL 5.7, onde o limite de índice do InnoDB (767 bytes) com `utf8mb4` dá exatamente 191 caracteres.

**3. Gerar o segredo da ponte**, uma vez:

```bash
openssl rand -base64 32
```

O mesmo valor vai em `PONTE_SECRET` (config.php) e em `MCP_INSTAGRAM_PONTE_SECRET` (Render). Não existe em nenhum outro lugar.

**4. Preencher o `config.php`** a partir do exemplo, com `DB_PASS` sendo a senha já definida do usuário `rosepa59_mcp_instagram`.

**5. Enviar os arquivos** conforme a tabela acima e conferir as permissões (`600` no config).

**6. Rodar o roteiro de verificação** (abaixo).

## Roteiro de verificação com curl

Rode do seu computador, substituindo `SEGREDO` pelo valor real. Os cinco primeiros testes **não tocam** no token de produção, porque usam um alvo inválido ou credencial errada.

```bash
URL=https://ponte.mobilizando.org/token-instagram.php
ALVO='mcp-instagram:instagram-access-token'
```

**1. Sem segredo → 401**
```bash
curl -s -o /dev/null -w '%{http_code}\n' -X POST "$URL" -H 'Content-Type: application/json' -d '{"acao":"ler","alvo":"mcp-instagram:instagram-access-token"}'
```

**2. Segredo errado → 401**
```bash
curl -s -o /dev/null -w '%{http_code}\n' -X POST "$URL" -H 'X-MCP-Ponte-Secret: errado' -H 'Content-Type: application/json' -d '{"acao":"ler","alvo":"mcp-instagram:instagram-access-token"}'
```

**3. Alvo diferente → 400** (prova que não é armazenamento genérico)
```bash
curl -s -o /dev/null -w '%{http_code}\n' -X POST "$URL" -H 'X-MCP-Ponte-Secret: SEGREDO' -H 'Content-Type: application/json' -d '{"acao":"ler","alvo":"outra-coisa"}'
```

**4. GET em vez de POST → 405**
```bash
curl -s -o /dev/null -w '%{http_code}\n' "$URL" -H 'X-MCP-Ponte-Secret: SEGREDO'
```

**5. HTTP simples → recusado** (não deve devolver 200)
```bash
curl -s -o /dev/null -w '%{http_code}\n' --max-redirs 0 -X POST http://ponte.mobilizando.org/token-instagram.php -H 'X-MCP-Ponte-Secret: SEGREDO' -H 'Content-Type: application/json' -d '{"acao":"ler","alvo":"mcp-instagram:instagram-access-token"}'
```

**6. Ciclo completo gravar → ler → excluir → ler.** Faça isto **antes** de autorizar no Instagram, ou você apagará o token real.
```bash
curl -s -X POST "$URL" -H 'X-MCP-Ponte-Secret: SEGREDO' -H 'Content-Type: application/json' \
  -d "{\"acao\":\"gravar\",\"alvo\":\"$ALVO\",\"secret\":\"VALOR_DE_TESTE\"}"      # {"status":"ok"}

curl -s -X POST "$URL" -H 'X-MCP-Ponte-Secret: SEGREDO' -H 'Content-Type: application/json' \
  -d "{\"acao\":\"ler\",\"alvo\":\"$ALVO\"}"                                       # {"status":"ok","secret":"VALOR_DE_TESTE"}

curl -s -X POST "$URL" -H 'X-MCP-Ponte-Secret: SEGREDO' -H 'Content-Type: application/json' \
  -d "{\"acao\":\"excluir\",\"alvo\":\"$ALVO\"}"                                   # {"status":"ok"}

curl -s -X POST "$URL" -H 'X-MCP-Ponte-Secret: SEGREDO' -H 'Content-Type: application/json' \
  -d "{\"acao\":\"ler\",\"alvo\":\"$ALVO\"}"                                       # {"status":"vazio"}
```

**7. O `config.php` não é acessível pela web** (deve dar 403 ou 404, nunca 200 com conteúdo)
```bash
curl -s -o /dev/null -w '%{http_code}\n' https://ponte.mobilizando.org/mcp-instagram-config.php
```

Se o teste 1 devolver 200 em vez de 401, **pare**: a autenticação não está funcionando e a ponte está aberta.

## Se o teste 1 ou 2 falhar

Quase sempre é o cabeçalho `Authorization` sendo removido pelo CGI/FastCGI antes de chegar ao PHP. Por isso o `token-instagram.php` aceita também `X-MCP-Ponte-Secret`, que é o que o Render envia primeiro. Se ainda assim falhar, confirme que o `.htaccess` foi enviado e que o `mod_rewrite` está ativo no plano.

## Contrato que o `token-instagram.php` cumpre

Está codificado como especificação executável na classe `PonteFalsa` em [`tests/test_ponte.py`](../tests/test_ponte.py). Se o PHP se comportar como ela, a ponte funciona. Ao mexer no PHP, use aqueles testes como referência.
