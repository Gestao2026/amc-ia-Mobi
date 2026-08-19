# Ponte de armazenamento na HostGator

Arquivos deste diretório **não** são deployados pelo Render. Eles vão para a HostGator, por FTP ou pelo Gerenciador de Arquivos do cPanel.

```
Render (mcp-linkedin) --HTTPS autenticado--> ponte.mobilizando.org/token.php --> MySQL localhost
```

## Por que a ponte existe

O MySQL da HostGator só aceita conexão externa se um IP for liberado em **Remote MySQL**. Os IPs de saída do Render são faixas CIDR **compartilhadas com todos os outros clientes da mesma região** (IPs dedicados são um add-on pago). Liberar essa faixa deixaria o banco alcançável por qualquer serviço hospedado no Render.

Com a ponte, o MySQL continua escutando **só em localhost** e nada precisa ser liberado.

## A propriedade de segurança central

**O PHP nunca recebe, conhece ou guarda a chave AES.** O valor que chega em `secret` já vem cifrado com AES-256-GCM pelo Render, e só o Render tem a chave (`LINKEDIN_TOKEN_ENCRYPTION_KEY`).

Consequência prática: um comprometimento total desta hospedagem (banco, PHP e `config.php`) entrega **apenas texto cifrado**, inútil sem a chave. Há um teste automatizado que prova exatamente isso (`test_quem_tem_o_banco_da_ponte_nao_consegue_ler_o_token`).

## O que enviar, e para onde

Supondo o subdomínio `ponte.mobilizando.org` com docroot em `/home/rosepa59/ponte.mobilizando.org/`:

| Arquivo | Destino | Permissão |
|---|---|---|
| `token.php` | `.../ponte.mobilizando.org/token.php` | 644 |
| `.htaccess` | `.../ponte.mobilizando.org/.htaccess` | 644 |
| `mcp-linkedin-config.exemplo.php` | renomeado para `mcp-linkedin-config.php`, **um nível ACIMA** do docroot | **600** |

O `config.php` fica **fora do docroot** de propósito: mesmo que o PHP pare de ser interpretado (uma falha real e comum em hospedagem compartilhada), o arquivo não pode ser baixado pela web. O `token.php` o procura em `__DIR__ . '/../mcp-linkedin-config.php'`.

## Passo a passo

**1. Criar o subdomínio** `ponte.mobilizando.org` no cPanel e confirmar que o **AutoSSL** emitiu certificado. Sem HTTPS válido a ponte não funciona: o `token.php` recusa HTTP, e o Render recusa uma URL que não comece com `https://`.

**2. Criar a tabela** no banco `rosepa59_mcp_linkedin` (phpMyAdmin → SQL):

```sql
CREATE TABLE IF NOT EXISTS mcp_linkedin_tokens (
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

O mesmo valor vai em `PONTE_SECRET` (config.php) e em `MCP_LINKEDIN_PONTE_SECRET` (Render). Não existe em nenhum outro lugar.

**4. Preencher o `config.php`** a partir do exemplo, com `DB_PASS` sendo a senha já definida do usuário `rosepa59_mcp_linkedin`.

**5. Enviar os arquivos** conforme a tabela acima e conferir as permissões (`600` no config).

**6. Rodar o roteiro de verificação** (abaixo).

## Roteiro de verificação com curl

Rode do seu computador, substituindo `SEGREDO` pelo valor real. Os cinco primeiros testes **não tocam** no token de produção, porque usam um alvo inválido ou credencial errada.

```bash
URL=https://ponte.mobilizando.org/token.php
ALVO='mcp-linkedin:linkedin-access-token'
```

**1. Sem segredo → 401**
```bash
curl -s -o /dev/null -w '%{http_code}\n' -X POST "$URL" -H 'Content-Type: application/json' -d '{"acao":"ler","alvo":"mcp-linkedin:linkedin-access-token"}'
```

**2. Segredo errado → 401**
```bash
curl -s -o /dev/null -w '%{http_code}\n' -X POST "$URL" -H 'X-MCP-Ponte-Secret: errado' -H 'Content-Type: application/json' -d '{"acao":"ler","alvo":"mcp-linkedin:linkedin-access-token"}'
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
curl -s -o /dev/null -w '%{http_code}\n' --max-redirs 0 -X POST http://ponte.mobilizando.org/token.php -H 'X-MCP-Ponte-Secret: SEGREDO' -H 'Content-Type: application/json' -d '{"acao":"ler","alvo":"mcp-linkedin:linkedin-access-token"}'
```

**6. Ciclo completo gravar → ler → excluir → ler.** Faça isto **antes** de autorizar no LinkedIn, ou você apagará o token real.
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
curl -s -o /dev/null -w '%{http_code}\n' https://ponte.mobilizando.org/mcp-linkedin-config.php
```

Se o teste 1 devolver 200 em vez de 401, **pare**: a autenticação não está funcionando e a ponte está aberta.

## Se o teste 1 ou 2 falhar

Quase sempre é o cabeçalho `Authorization` sendo removido pelo CGI/FastCGI antes de chegar ao PHP. Por isso o `token.php` aceita também `X-MCP-Ponte-Secret`, que é o que o Render envia primeiro. Se ainda assim falhar, confirme que o `.htaccess` foi enviado e que o `mod_rewrite` está ativo no plano.

## Contrato que o `token.php` cumpre

Está codificado como especificação executável na classe `PonteFalsa` em [`tests/test_ponte.py`](../tests/test_ponte.py). Se o PHP se comportar como ela, a ponte funciona. Ao mexer no PHP, use aqueles testes como referência.
