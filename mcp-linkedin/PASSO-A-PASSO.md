# Passo a passo da conexão do LinkedIn ao Claude

Guia em linguagem comum, para seguir clicando. Escrito depois da instalação real de 21/08/2026, então descreve o que de fato aconteceu, incluindo as armadilhas que custaram tempo.

O endereço usado como exemplo é `https://mcp-linkedin-run7.onrender.com`. Se o nome do serviço for outro, troque em todos os lugares.

## O que dá e o que não dá, antes de começar

Vale saber antes de investir tempo, porque isso não muda com esforço:

| Quero | Dá? | Por quê |
|---|---|---|
| Publicar no meu perfil pessoal | **sim** | produto "Compartilhe no LinkedIn" |
| Saber quem sou (nome, foto, e-mail) | **sim** | Login com OpenID Connect |
| Ler métricas e engajamento | **não** | exige Community Management API |
| Publicar como Página da organização | **não** | mesma API |
| Ler minhas publicações existentes | **não** | mesma API |

A Community Management API é a mais criteriosa do LinkedIn e precisa ser solicitada e aprovada. Se ela não estiver no seu aplicativo, nenhuma configuração deste guia contorna isso.

---

## Etapa 0. Conferência antes de começar

### 1. Uma conta do LinkedIn

Pode ser sua conta pessoal. Ela não precisa administrar Página nenhuma para publicar no próprio perfil.

### 2. Acesso ao painel de desenvolvedores

Entre em `developer.linkedin.com` com a sua conta do LinkedIn. Na primeira entrada o LinkedIn pode pedir confirmação de e-mail e aceite dos termos de desenvolvedor. Resolva antes de seguir.

### 3. Uma Página do LinkedIn para vincular o aplicativo

Esta é a exigência que costuma travar: **todo aplicativo do LinkedIn precisa estar vinculado a uma Página**, mesmo que ele só vá publicar em perfil pessoal. Você precisa ser administrador dessa Página.

Se você não tem Página, crie uma antes. É gratuito e leva poucos minutos.

---

## Etapa 1. Criar o aplicativo

Em `developer.linkedin.com`, vá em **My apps** e crie um aplicativo.

| Campo | O que preencher |
|---|---|
| App name | um nome que você reconheça, ex. `MCP LinkedIn Mobi` |
| LinkedIn Page | a Página que você administra |
| App logo | qualquer imagem quadrada |

Depois de criar, o LinkedIn pede para **verificar** o aplicativo. A verificação é feita por um administrador da Página, clicando num link que o próprio painel gera. Se a Página é sua, você mesmo verifica.

---

## Etapa 2. Pedir os produtos

Na aba **Products** do aplicativo, solicite:

| Produto | Para quê | Aprovação |
|---|---|---|
| **Sign In with LinkedIn using OpenID Connect** | saber quem é o autor | imediata |
| **Share on LinkedIn** | publicar no perfil | imediata |

Os dois costumam ser liberados na hora, sem análise humana.

Se você também quiser métricas algum dia, é a **Community Management API** que precisa ser pedida. Ela passa por análise e não é garantida.

Confira na aba Products que os dois aparecem em **Added products** antes de seguir.

---

## Etapa 3. Hospedar o servidor no Render

Só depois de ter o aplicativo, porque o endereço de retorno depende da hospedagem.

1. Em `render.com`, **New** → **Web Service**, conectando o repositório
2. **Root Directory:** `mcp-linkedin`
3. **Runtime:** Docker
4. **Plan:** Free

Variáveis de ambiente:

| Variável | Valor |
|---|---|
| `MCP_TRANSPORT` | `streamable-http` |
| `MCP_PUBLIC_BASE_URL` | `https://mcp-linkedin-run7.onrender.com` |
| `LINKEDIN_CLIENT_ID` | da aba Auth do aplicativo |
| `LINKEDIN_CLIENT_SECRET` | da aba Auth do aplicativo |
| `LINKEDIN_SCOPES` | `openid,profile,email,w_member_social` |
| `MCP_CLAUDE_CLIENT_ID` | um identificador que você inventa |
| `MCP_CLAUDE_CLIENT_SECRET` | gere com `openssl rand -base64 32` |

**Atenção ao `LINKEDIN_SCOPES`:** separado por vírgula, **sem espaços**. E nunca inclua escopo de organização (`r_organization_social`, `w_organization_social`) sem ter o produto aprovado: o LinkedIn recusa a autorização **inteira**, e nem os escopos válidos funcionam.

O armazenamento do token vem na Etapa 5. Sem ele, o servidor sobe e funciona, mas a autorização se perde a cada reinício.

---

## Etapa 4. Cadastrar o endereço de retorno

Volte ao aplicativo, aba **Auth**, e em **Authorized redirect URLs** acrescente exatamente:

```
https://mcp-linkedin-run7.onrender.com/oauth/linkedin/callback
```

Esse valor precisa bater **caractere por caractere** com o que o servidor envia. Um `/` a mais no fim já faz o LinkedIn recusar a troca do código por token, com uma mensagem que não explica o motivo.

---

## Etapa 5. O armazenamento do token na HostGator

Sem esta etapa a autorização morre a cada reinício, e reinício acontece toda vez que você publica código novo.

Ver [`ponte-hostgator/README.md`](ponte-hostgator/README.md) para a instalação completa. Em resumo:

1. Criar a tabela `mcp_linkedin_tokens` no MySQL
2. Subir o `token.php` no docroot do subdomínio
3. Subir o `.htaccess` no mesmo lugar
4. Subir o arquivo de configuração **um nível acima** do docroot
5. Acrescentar no Render: `LINKEDIN_TOKEN_STORE_BACKEND=ponte`, `MCP_LINKEDIN_PONTE_URL`, `MCP_LINKEDIN_PONTE_SECRET` e `LINKEDIN_TOKEN_ENCRYPTION_KEY`

**A chave de cifragem** precisa ser base64 de exatamente 32 bytes. Gere com `openssl rand -base64 32`, que produz 44 caracteres terminando em `=`. Não use gerador de senha genérico nem o botão "Generate" do Render: o formato não bate e o servidor recusa na primeira gravação.

Ela vai **apenas no Render**, nunca na HostGator. É essa separação que faz um vazamento do banco entregar só texto cifrado.

---

## Etapa 6. Conectar ao Claude

No painel de conectores, adicione um conector personalizado apontando para:

```
https://mcp-linkedin-run7.onrender.com/mcp
```

Repare no `/mcp` no final. A raiz do endereço não responde.

---

## Etapa 7. Autorizar a conta

Na conversa, peça para iniciar a autorização do LinkedIn. O servidor devolve uma URL. Abra no navegador, entre na conta e autorize.

A senha é digitada **apenas** na tela do próprio LinkedIn. Nenhum outro passo deste processo pede senha.

A URL expira em 10 minutos. Depois de autorizar, o LinkedIn chama o servidor sozinho e a resposta deve ser:

```json
{"status":"conectado","detalhe":"LinkedIn autorizado com sucesso. Pode fechar esta pagina."}
```

---

## O que esperar depois, e não é defeito

### O conector vai pedir "Reconectar"

O plano gratuito do Render adormece o serviço após cerca de 15 minutos ocioso. A sessão entre o Claude e o servidor vive em memória e morre junto.

O token **não** se perde, porque está na ponte. Só a sessão.

Contorno: um ping externo a cada 10 minutos, das 8h às 20h em dias úteis. Serve `cron-job.org`, gratuito, com esta expressão:

```
*/10 8-20 * * 1-5
```

apontando para `https://mcp-linkedin-run7.onrender.com/.well-known/oauth-authorization-server`, que é um endereço público e minúsculo.

**A janela de horário é obrigatória.** O Render dá cerca de 750 horas mensais por conta; dois serviços acordados o tempo todo consumiriam 1.460 e seriam desligados.

**Aumente o tempo limite do ping para 30 segundos.** O primeiro ping da segunda-feira encontra o servidor dormindo, e acordar leva uns 12 segundos. Com o padrão baixo, o ping desiste no meio, o servidor volta a dormir, e o ciclo se repete a semana toda.

### Trocar os escopos exige autorizar de novo

Autorização vale para o conjunto de permissões pedido no momento em que foi dada. Ao acrescentar `w_member_social` a um aplicativo já autorizado, é preciso refazer a autorização, senão a publicação recusa com "sem permissão".

---

## Quando algo falhar

| Sintoma | Causa provável |
|---|---|
| LinkedIn recusa a autorização inteira | escopo pedido que não tem produto aprovado |
| Erro na troca do código por token | Redirect URL diferente entre o aplicativo e o servidor |
| Publicação recusada com 403 | falta `w_member_social`, ou autorização anterior à mudança |
| Conector pede "Reconectar" | hibernação, ver acima |
| Servidor não sobe depois de mexer nas variáveis | chave de cifragem fora do formato base64 de 32 bytes |
