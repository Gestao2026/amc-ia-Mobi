# mcp-instagram

Conexão de uma conta profissional do Instagram ao Claude, pelo método oficial da Meta.

Este componente é **somente leitura**. Ele estabelece e mantém a autorização, lê o perfil, lista as publicações com engajamento e lê as métricas da conta. Ele não publica, não edita, não exclui, não comenta, não responde mensagens, não altera configurações e não administra anúncios.

A limitação é estrutural, não uma promessa de boa vontade. Duas travas a sustentam:

1. O transporte usado pelas ferramentas de negócio (`TransporteGraphHttpx`) expõe **apenas** `get`. Sem `post`, `put`, `patch` ou `delete`, nenhuma ferramenta de escrita pode ser construída sobre ele por engano.
2. Os escopos padrão (`instagram_business_basic` e `instagram_business_manage_insights`) não concedem escrita. Ampliar permissão exige mudar `INSTAGRAM_SCOPES`, o que fica visível como mudança de configuração revisável.

Os testes `test_nenhuma_ferramenta_de_escrita_existe` e `test_o_cliente_de_leitura_nao_expoe_metodo_de_escrita` guardam as duas travas.

**Ferramentas de leitura disponíveis:**

| Ferramenta | O que devolve |
|---|---|
| `instagram_perfil` | Nome de usuário, tipo de conta, seguidores, total de publicações, biografia |
| `instagram_publicacoes` | Publicações recentes com legenda, tipo, link, data, curtidas e comentários (1 a 50) |
| `instagram_metricas_publicacao` | Alcance, curtidas, comentários, salvamentos, compartilhamentos, interações e visualizações de uma publicação |
| `instagram_metricas_conta` | Alcance, visualizações, interações e contas engajadas na janela pedida (1 a 30 dias) |

Arquitetura idêntica à do `mcp-linkedin`, com duas camadas de autorização independentes:

```
Claude  --(Camada 1, OAuth)-->  mcp-instagram  --(Camada 2, OAuth)-->  Instagram (Meta)
```

## Permissões solicitadas

Somente leitura. Estes são os dois escopos padrão, e são os únicos declarados no `render.yaml`:

| Escopo | O que permite | Publicar | Editar | Excluir | Mensagens | Métricas | Anúncios |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|
| `instagram_business_basic` | Identificar a conta, ler nome de usuário, foto, seguidores e a lista de publicações existentes | não | não | não | não | não | não |
| `instagram_business_manage_insights` | Ler alcance, impressões, visualizações de perfil, desempenho por publicação e audiência | não | não | não | não | sim | não |

Escopos deliberadamente **não** solicitados: `instagram_business_content_publish` (publicar), `instagram_business_manage_comments` (responder e apagar comentários), `instagram_business_manage_messages` (Direct), `ads_management` e `ads_read` (anúncios).

Dois pontos que costumam gerar dúvida:

- A API da Meta **não oferece** permissão para editar ou apagar uma publicação já feita. Isso só é possível no aplicativo, na mão.
- Nenhuma permissão da Meta dá acesso a senha, e-mail de login ou configurações da conta.

Se alguém acrescentar um escopo de escrita via `INSTAGRAM_SCOPES`, a ferramenta `instagram_mcp_status` passa a devolver `somente_leitura: false` e lista quais escopos de escrita estão ativos. A ampliação não passa despercebida.

## Requisitos

- Conta do Instagram do tipo **Comercial (Business)** ou **Criador de conteúdo**. Contas pessoais não são atendidas pela API da Meta.
- Um aplicativo registrado no painel de desenvolvedores da Meta, com o produto "API do Instagram com login do Instagram".
- Um endereço público HTTPS para este servidor (o Render resolve isso).

## Passo a passo da conexão

### 1. Registrar o aplicativo na Meta

No painel de desenvolvedores da Meta, criar um aplicativo e adicionar a configuração da API do Instagram com login do Instagram. Anotar o **ID do aplicativo** e a **Chave secreta**.

Na tela de configurações do login da empresa, a Meta exige os três endereços abaixo e não deixa salvar sem eles.

| Campo | Valor |
|---|---|
| URIs de redirecionamento do OAuth | `https://SEU-ENDERECO-PUBLICO/oauth/instagram/callback` |
| URL de retorno de chamada de desautorização | `https://SEU-ENDERECO-PUBLICO/oauth/instagram/desautorizar` |
| URL de solicitação de exclusão de dados | `https://SEU-ENDERECO-PUBLICO/oauth/instagram/exclusao-de-dados` |

O primeiro precisa bater caractere por caractere com o que este servidor envia, senão a Meta recusa a troca de token. Por isso ele não é uma variável separada: é sempre derivado de `MCP_PUBLIC_BASE_URL`.

Os dois últimos não são endereços de fachada. São rotas reais deste servidor, e as duas conferem uma assinatura HMAC-SHA256 feita com o Client Secret antes de agir. Sem essa verificação, qualquer pessoa que descobrisse a URL apagaria a autorização do captador com um POST vazio.

- **Desautorização**: chamada quando a pessoa remove o aplicativo nas configurações do Instagram. Apaga a autorização guardada.
- **Exclusão de dados**: chamada quando a pessoa pede exclusão. Apaga a autorização e devolve, no formato exigido pela Meta, um código de confirmação consultável em `/oauth/instagram/exclusao-de-dados/status`.

O único dado pessoal que este servidor guarda é o próprio token de acesso, junto do identificador da conta. Não há histórico, cópia de publicação nem métrica arquivada, porque nenhuma ferramenta de leitura de conteúdo existe aqui. Apagar o token é, literalmente, apagar tudo.

Por fim, vincular a conta profissional do Instagram ao aplicativo.

### 2. Publicar o servidor

Conectar este diretório no Render como serviço Docker, com **Root Directory** apontando para `mcp-instagram/`. O `render.yaml` já define transporte, backend de token e escopos.

Cadastrar como secrets no painel do Render, nunca em arquivo:

| Variável | Conteúdo |
|---|---|
| `MCP_PUBLIC_BASE_URL` | endereço público do serviço, com `https://`, sem barra no final |
| `INSTAGRAM_CLIENT_ID` | ID do aplicativo na Meta |
| `INSTAGRAM_CLIENT_SECRET` | chave secreta do aplicativo |
| `MCP_INSTAGRAM_PONTE_URL` | URL da ponte HTTPS na HostGator |
| `MCP_INSTAGRAM_PONTE_SECRET` | segredo compartilhado com o `config.php` da ponte |
| `INSTAGRAM_TOKEN_ENCRYPTION_KEY` | chave AES-256 em base64, própria deste componente |
| `MCP_CLAUDE_CLIENT_ID` | identificador do conector do lado do Claude |
| `MCP_CLAUDE_CLIENT_SECRET` | opcional, se o conector for confidencial |

A chave de cifragem se gera uma única vez com:

```bash
python -c "from mcp_instagram.auth_instagram.crypto import generate_key_base64; print(generate_key_base64())"
```

Use uma chave **diferente** da do `mcp-linkedin`. Trocar a chave depois invalida o token guardado, e basta reautorizar.

### 3. Reaproveitar ou publicar a ponte de armazenamento

O backend `ponte` guarda o token cifrado num MySQL da HostGator, através de um `token.php` que nunca recebe a chave AES. A ponte já publicada para o `mcp-linkedin` **serve aqui sem alteração**: ela guarda por "alvo", e o alvo deste componente é `mcp-instagram:instagram-access-token`, distinto do alvo do LinkedIn. Os dois tokens convivem na mesma tabela sem colidir.

Se preferir isolar completamente, publique uma segunda cópia da ponte com segredo próprio e aponte `MCP_INSTAGRAM_PONTE_URL` para ela.

### 4. Adicionar o conector no Claude

Nas configurações de conectores do Claude, adicionar um conector MCP remoto apontando para `https://SEU-ENDERECO-PUBLICO/mcp`. A autorização da Camada 1 acontece na própria interface do Claude.

### 5. Autorizar o Instagram

Com o conector ativo, chamar a ferramenta `instagram_oauth_iniciar`. Ela devolve:

- a URL oficial de autorização da Meta;
- a lista exata de permissões solicitadas, com o que cada uma permite;
- a confirmação de que a conexão é somente leitura;
- como revogar depois.

Abrir a URL no navegador, entrar com a conta profissional e autorizar. A senha é digitada **apenas no site do Instagram**: este servidor nunca pede, nunca recebe e nunca guarda senha, código de verificação ou código de recuperação.

Depois de autorizar, conferir com `instagram_oauth_status`.

## Ferramentas expostas

| Ferramenta | O que faz |
|---|---|
| `instagram_mcp_status` | Diagnóstico do componente, escopos configurados e se a conexão é somente leitura. Não acessa o Instagram. |
| `instagram_oauth_iniciar` | Monta a URL de autorização e descreve cada permissão antes de o captador autorizar. Não acessa o Instagram. |
| `instagram_oauth_status` | Informa se há autorização válida, qual conta está conectada e quando expira. Nunca devolve o token. |
| `instagram_desconectar` | Apaga a autorização guardada neste servidor. Não altera nada na conta do Instagram. |

Além das ferramentas, o servidor expõe três rotas HTTP que só a Meta chama: o callback do OAuth, a desautorização e a exclusão de dados. Nenhuma delas é acessível ao modelo como ferramenta.

## Como revogar o acesso

Três caminhos independentes:

1. **No Instagram**: Configurações e privacidade, Aplicativos e sites, selecionar o aplicativo, Remover.
2. **Neste servidor**: ferramenta `instagram_desconectar`, que apaga o token guardado na hora.
3. **No Claude**: remover o conector nas configurações, o que corta a Camada 1.

O caminho 1 é o definitivo: ele invalida o token do lado da Meta, independentemente do que exista aqui.

## Validade do token

O token de longa duração da Meta vale **60 dias**. A troca é feita em duas etapas na autorização (o token de uma hora é trocado pelo de 60 dias antes de qualquer coisa ser gravada), e um token de curta duração nunca é aceito como conexão estabelecida.

A renovação automática antes do vencimento (endpoint `refresh_access_token`) **não está implementada** nesta etapa. Hoje, ao expirar, basta rodar `instagram_oauth_iniciar` de novo. Implementar a renovação é o passo natural seguinte se a conexão for ficar permanente.

## Onde o token fica guardado, e por que isso importa

Definido pela variável `INSTAGRAM_TOKEN_STORE_BACKEND`. Em produção o valor é `ponte`: o token vai para o MySQL da HostGator através de um arquivo PHP, cifrado com uma chave que existe **apenas no Render**.

O padrão em Linux, quando a variável não é declarada, é `memory`. E foi assim que este componente rodou até 21/08/2026, com uma consequência que chegava à captadora como um mistério: **"ontem estava conectado e hoje não está"**.

A explicação é que o plano gratuito do Render adormece o serviço após cerca de 15 minutos ocioso, e memória se apaga. A autorização morria a cada hibernação, sem aviso.

Por isso `instagram_mcp_status` passou a responder três campos novos:

```json
"onde_o_token_fica_guardado": "ponte",
"autorizacao_sobrevive_a_reinicio": true,
"aviso_de_persistencia": null
```

Com o backend `memory`, o terceiro campo traz um aviso explicando que a autorização será perdida. Antes disso, esse diagnóstico exigia acesso ao painel da hospedagem; agora a própria ferramenta responde.

Instalação da ponte: [`ponte-hostgator/`](ponte-hostgator/). **Leia a seção das armadilhas antes de começar**, ela poupa horas.

## A hibernação derruba a conexão, e o token não é o culpado

Vale separar duas coisas que somem juntas quando o serviço adormece:

| O que morre | Sintoma | Resolvido pela ponte? |
|---|---|---|
| Token do Instagram | conta desautorizada | **sim** |
| Sessão do Claude | conector pede "Reconectar" | não |

A sessão da Camada 1 vive em memória por decisão explícita da v1 (ver `auth_claude/session_store.py`), então ela morre mesmo com a ponte configurada.

Contorno em uso desde 21/08/2026: um ping externo (cron-job.org) chama `/.well-known/oauth-authorization-server` a cada 10 minutos, das 8h às 20h em dias úteis:

```
*/10 8-20 * * 1-5
```

**A janela de horário não é preferência, é necessidade.** O Render oferece cerca de 750 horas de instância por mês na conta inteira, e dois serviços acordados 24 horas consumiriam 1.460.

**Aumente o tempo limite do ping para 30 segundos.** O primeiro ping depois de um período parado encontra o serviço dormindo, e acordar leva uns 12 segundos. Com o limite baixo, o ping desiste no meio, o serviço volta a dormir, e o ciclo se repete indefinidamente. Foi exatamente o que aconteceu na primeira tentativa: o LinkedIn acertou de primeira e nunca mais dormiu, o Instagram errou de primeira e ficou preso no ciclo.

## Segurança

- Nenhum segredo em arquivo versionado. Tudo vem do ambiente, e o `.env` está no `.gitignore`.
- O token é cifrado com AES-256-GCM **antes** de sair do processo para o armazenamento remoto. Banco e chave ficam em domínios de confiança diferentes: um dump vazado do banco, sozinho, não entrega o token.
- Nenhum `__repr__` deste componente expõe client secret, segredo da ponte, chave de cifragem, authorization code, state ou access token.
- Nenhuma mensagem de erro contém segredo, e as exceções de rede são convertidas com `from None` para o traceback não carregar o objeto da requisição.
- O `state` do OAuth é de uso único e expira em 10 minutos, o que bloqueia replay de callback.
- Uma exceção honesta: na etapa 2 da troca, a Meta só documenta o endpoint como GET com o client secret na query string. Não existe variante POST. A mitigação está descrita no topo de `auth_instagram/token_exchange.py`.

## Testes

```bash
python -m pytest -q
```

346 testes, nenhum acessa o Instagram, abre navegador ou usa credencial real. O transporte HTTP é sempre falso ou um `MockTransport` em processo, e vários testes bloqueiam ativamente qualquer conexão que não seja loopback.
