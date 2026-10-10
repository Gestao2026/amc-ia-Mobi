# Fazer o conector parar de pedir "Reconectar"

> Escrito em 01/09/2026. Vale para os dois conectores, Instagram e LinkedIn.

## O problema, em uma frase

Toda segunda de manhã, e depois de cada publicação de código, o Instagram e o LinkedIn somem da conversa e é preciso clicar em **Reconectar** no painel.

Isso nunca foi defeito de configuração. Era uma pendência conhecida do código, escrita com todas as letras no próprio arquivo que a causava:

> Escopo desta v1: memória do processo, exclusivamente. Reiniciar o processo derruba todas as sessões, exigindo nova autorização do Claude.

São duas autorizações diferentes, e só uma se perdia:

| O que | Onde morava | Sobrevivia ao serviço dormir? |
|---|---|---|
| Autorização da conta (o token do Instagram, o do LinkedIn) | ponte na HostGator, cifrada | sim, desde 21/08/2026 |
| Sessão do Claude com o servidor | memória do processo | **não**, e era este o clique que se repetia |

Por isso reconectar era rápido e não pedia a senha da rede social: a conta continuava autorizada. O que morria era só o crachá que o Claude usa para falar com o servidor.

## O que mudou no código

`ClaudeSessionStore` passou a aceitar um armazenamento persistente injetado, o mesmo `CredentialBackend` que a Camada 2 já usava para o token da conta. Access token e refresh token agora vão cifrados para a ponte.

A chave de cada linha é o **SHA-256 do token**, nunca o token. Quem lesse o banco encontraria hash na chave e conteúdo cifrado no valor, e não conseguiria montar credencial nenhuma.

O authorization code continua só em memória, de propósito: ele vive 5 minutos, no meio de um aperto de mão que não atravessa reinício.

Persistir nunca derruba autenticação. Se a ponte estiver fora do ar, a falha é engolida e a sessão segue em memória: o pior caso volta a ser o comportamento antigo, que é pedir para reconectar.

## O perigo que apareceu no caminho

Ao conferir o PHP publicado, apareceu um problema sério, e é a razão de existir uma trava.

O `token-instagram.php` **ignora o alvo enviado** e grava sempre na mesma linha:

```php
// O cliente NAO envia o alvo.
$alvo = 'mcp-instagram:instagram-access-token';
```

Ou seja: com o PHP antigo, gravar a sessão pela ponte **sobrescreveria o token do Instagram**, e a ação de excluir o apagaria. A conta cairia e precisaria ser reautorizada, sem aviso nenhum. O `token.php` do LinkedIn é mais defensivo, recusa o alvo diferente, então lá o efeito seria só a sessão não persistir em silêncio.

Os dois arquivos em `ponte-hostgator/` já estão corrigidos: passam a aceitar, além do alvo do token, o formato fechado `mcp-{rede}:claude-(access|refresh):<64 hexadecimais>`. Continua não sendo armazenamento genérico, e continua impossível varrer chave alheia ou inventar uma.

## Como publicar, e por que a ordem importa

> **A ordem não é preferência.** Ligar a variável antes de publicar o PHP destrói o token do Instagram. Publicar o PHP antes da variável não faz mal nenhum: o PHP novo é compatível com o cliente antigo.

### Passo 1. Publicar os dois arquivos PHP

Suba, pelo cPanel da HostGator, substituindo os que estão lá:

| Arquivo do repositório | Vai para |
|---|---|
| `mcp-instagram/ponte-hostgator/token-instagram.php` | `/home2/rosepa59/home2/rosepa59/ponte-mcp/public/` |
| `mcp-linkedin/ponte-hostgator/token.php` | a mesma pasta |

Duas coisas a favor desta vez: são arquivos que **já existem** e já estão liberados no `.htaccess`, então não nascem com 403. E o caminho com `home2` repetido não é erro de digitação, é o caminho real.

Antes de subir, leia `mcp-instagram/ponte-hostgator/README.md`. O Gerenciador de Arquivos do cPanel já negou arquivo que existia e escondeu o `.htaccess`.

### Passo 2. Confirmar que a ponte continua de pé

```bash
curl -s -o /dev/null -w '%{http_code}\n' -X POST https://ponte.mobilizando.org/token-instagram.php -H 'Content-Type: application/json' -d '{"acao":"ler"}'
```

**401 é o resultado certo**: no ar, configuração completa, recusando por falta do segredo. Se vier 500, o PHP subiu quebrado, e o passo 3 não pode acontecer.

Repita trocando `token-instagram.php` por `token.php`.

### Passo 3. Confirmar que o Instagram continua conectado

Antes de ligar a variável, verifique no Claude que `instagram_mcp_status` ainda responde com a conta conectada. Se o passo 1 tiver dado errado de alguma forma, é aqui que aparece, e ainda dá para voltar atrás.

### Passo 4. Ligar a variável nos dois serviços do Render

Em cada serviço, `mcp-instagram-rosepaula` e `mcp-linkedin-run7`, acrescente:

```
MCP_CLAUDE_SESSION_STORE_PONTE=1
```

Publicar essa mudança reinicia o serviço, o que derruba a sessão atual. É a **última** vez que precisa reconectar por esse motivo.

### Passo 5. Reconectar uma última vez e comprovar

1. Reconecte os dois em claude.ai, Configurações, Conectores.
2. Abra uma conversa nova e confirme que as ferramentas respondem.
3. Espere o serviço hibernar (fora das 8h às 20h de dias úteis, ou uns 20 minutos sem ping).
4. Volte e use uma ferramenta. Se responder devagar mas responder, sem pedir Reconectar, funcionou.

## Se algo der errado

Tirar a variável `MCP_CLAUDE_SESSION_STORE_PONTE` do Render devolve o comportamento antigo na hora: a sessão volta a viver só em memória. Não é preciso reverter o PHP, que é compatível com as duas situações.

## O que isto não resolve

**A hibernação continua.** O plano gratuito do Render adormece o serviço após cerca de 15 minutos ocioso, e a primeira chamada depois disso leva de 13 a 22 segundos. A diferença é que agora ela **acorda já autorizado**, em vez de pedir para reconectar.

Manter os dois acordados o tempo todo não cabe no plano gratuito: são 750 horas por mês na conta inteira, e dois serviços ininterruptos pediriam 1.460.

**O token do Instagram continua vencendo por volta de 20/10/2026.** São 60 dias, sem renovação automática implementada. Essa é outra pendência, de outro nível: quando chegar a hora, o sintoma muda de "peça para reconectar" para "a conta caiu", e a solução é reautorizar.

## Uma limitação conhecida que fica

Quando o refresh rotaciona, o access token antigo não é apagado do banco. A tabela acumula cerca de uma linha por hora de uso. Linha vencida some quando alguém tenta lê-la, mas as que ninguém procura ficam.

Não incomoda nesta escala. Numa faxina eventual, apagar as linhas cujo `target_name` começa com `mcp-instagram:claude-access:` é seguro: elas valem uma hora.

## Onde está cada coisa

| O que | Caminho |
|---|---|
| A persistência em si | `src/mcp_*/auth_claude/session_store.py` |
| A escolha do armazenamento e a trava | `src/mcp_*/server.py`, `build_claude_session_backend` |
| O PHP da ponte | `ponte-hostgator/token-instagram.php` e `ponte-hostgator/token.php` |
| Testes do store | `tests/test_auth_claude_session_persistencia.py` |
| Testes da trava e da ligação | `tests/test_claude_session_backend_ligacao.py` |
| Teste da cadeia inteira contra a ponte | `tests/test_ponte_sessao.py` |
