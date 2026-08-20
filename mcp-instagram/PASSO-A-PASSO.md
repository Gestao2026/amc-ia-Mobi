# Passo a passo da conexão do Instagram ao Claude

Guia em linguagem comum, para seguir clicando. Nenhuma etapa aqui pede senha do Instagram, código de verificação, 2FA ou código de recuperação. A senha é digitada uma única vez, na tela oficial do Instagram, no momento em que você autorizar.

O endereço usado como exemplo é `https://mcp-instagram-rosepaula.onrender.com`. Se o nome do serviço for outro, troque em todos os lugares.

## Por que nesta ordem

O cadastro na Meta vem primeiro porque é onde moram as surpresas: pedido de verificação da conta do Facebook, aceite de termos de desenvolvedor, conta do Instagram que não está de fato como profissional. Descobrir isso no começo evita hospedar algo que fica parado esperando.

O único campo que depende da hospedagem é o endereço de retorno, e por isso ele ficou separado, na Etapa 3. Assim você cola um endereço já conferido em vez de digitá-lo de cabeça, que é o erro que mais derruba esse tipo de conexão.

Tempo realista: 20 a 30 minutos no painel da Meta, cerca de 15 minutos na hospedagem, 2 minutos para autorizar. O painel da Meta é a parte lenta, porque tem muita tela.

---

## Etapa 0. Conferência antes de começar

Três pontos. Se algum falhar, o resto não anda.

### 1. A conta do Instagram é profissional

Precisa estar como **Comercial** ou **Criador de conteúdo**. Os dois funcionam, com uma ressalva logo abaixo.

Como conferir: abra o Instagram, vá no seu perfil e veja se aparece **Painel profissional** logo abaixo da bio. Se aparecer, a conta é profissional. Para ver qual dos dois tipos, entre em Configurações e privacidade e procure **Tipo de conta e ferramentas**.

Se estiver como pessoal, a API da Meta não atende. A conversão é feita nessa mesma tela, no próprio aplicativo do Instagram, e leva menos de um minuto.

**Comercial rende mais que Criador.** Os dois funcionam, mas o tipo Criador de conteúdo entrega um conjunto mais enxuto de métricas: algumas informações de audiência não vêm. Como o objetivo é gestão estratégica da rede, e métrica é metade disso, vale conferir e, se for o caso, trocar para Comercial antes de começar. A troca não muda nada visível para quem segue a conta.

### 2. Uma conta do Facebook para entrar no painel de desenvolvedores

Pode ser sua conta pessoal do Facebook. Ela **não** precisa administrar nenhuma Página, não precisa ter relação com a conta do Instagram que será conectada e não aparece para ninguém. Serve apenas como porta de entrada em `developers.facebook.com`, porque a Meta não permite acesso ao painel sem uma conta do Facebook.

Nesta rota, a que usa login do Instagram, nenhuma Página do Facebook entra na conexão. Quem autoriza é a conta do Instagram, na Etapa 5.

Duas coisas podem acontecer na primeira entrada, e são normais:

- A Meta pode pedir para **confirmar e-mail ou telefone** da conta do Facebook.
- Pode pedir para **aceitar os termos de desenvolvedor**.

Resolva as duas antes de seguir, porque o painel não abre sem isso.

### 3. Acesso ao login do Instagram da conta a ser conectada

Você vai precisar entrar na conta na Etapa 5, na tela oficial do Instagram, para autorizar. Se o login estiver com outra pessoa da equipe, alinhe antes. A senha é digitada apenas lá, nunca em outro lugar deste processo.

---

## Etapa 1. Criar o aplicativo no painel da Meta

Acesse o painel de desenvolvedores da Meta em `developers.facebook.com` e entre com a conta do Facebook da Etapa 0.

> Os nomes exatos dos botões mudam com frequência no painel da Meta. O que está descrito aqui é o conteúdo de cada campo, não a posição do botão. Se um rótulo estiver diferente, procure pelo campo equivalente.

### 1.1. Criar o aplicativo

| Campo | O que preencher |
|---|---|
| Caso de uso | A opção voltada a **outros** casos, e não as de anúncios ou jogos. É a que libera a API do Instagram. |
| Nome do aplicativo | `AMC IA` (ou o nome que preferir; aparece na tela de autorização) |
| E-mail de contato | Seu e-mail administrativo |
| Tipo | **Empresa (Business)** |

### 1.2. Adicionar o produto do Instagram

Dentro do aplicativo recém-criado, adicione o produto **API do Instagram** e escolha a configuração **com login do Instagram**, não a que exige Página do Facebook.

Essa é a escolha que mais confunde no painel, e é a que decide se vai funcionar. A rota com login do Instagram funciona com conta profissional (Comercial ou Criador de conteúdo) sem precisar vincular Página do Facebook.

### 1.3. Anotar as duas chaves

Na tela de configuração da API do Instagram, você encontra:

| Chave | Onde vai ser usada |
|---|---|
| **ID do aplicativo do Instagram** | vira a variável `INSTAGRAM_CLIENT_ID` |
| **Chave secreta do aplicativo do Instagram** | vira a variável `INSTAGRAM_CLIENT_SECRET` |

Guarde as duas num lugar seguro. A chave secreta é uma senha de sistema: ela nunca deve ser colada em conversa, e-mail, documento compartilhado ou arquivo do projeto. Ela vai direto para o painel de hospedagem, na Etapa 2.

### 1.4. Vincular a conta do Instagram

Na área de configuração da conta do Instagram do aplicativo, adicione a conta profissional a ser conectada (@rosepaula_rodrigues).

Enquanto o aplicativo estiver em modo de desenvolvimento, apenas contas ligadas ao aplicativo podem autorizar. Como a conta é sua, isso é suficiente e **não é preciso passar por análise da Meta**. A análise só seria necessária para conectar contas de terceiros. Se aparecer alguma menção a "análise do aplicativo" no painel, pode ignorar.

### 1.5. Configurações do login da empresa

Na seção **Configurar o login da empresa no Instagram**, clique em **Configurações do login da empresa**. A Meta exige os três campos abaixo preenchidos para deixar salvar.

| Campo | O que colar |
|---|---|
| URIs de redirecionamento do OAuth | `https://mcp-instagram-rosepaula.onrender.com/oauth/instagram/callback` |
| URL de retorno de chamada de desautorização | `https://mcp-instagram-rosepaula.onrender.com/oauth/instagram/desautorizar` |
| URL de solicitação de exclusão de dados | `https://mcp-instagram-rosepaula.onrender.com/oauth/instagram/exclusao-de-dados` |

Os dois últimos não são endereços de fachada. São rotas reais do servidor:

- **Desautorização**: quando você remover o aplicativo nas configurações do Instagram, a Meta avisa esse endereço e o servidor apaga a autorização guardada na hora.
- **Exclusão de dados**: quando você pedir exclusão, o servidor apaga a autorização e devolve um código de confirmação consultável.

As duas conferem uma assinatura criptográfica antes de agir. Sem isso, qualquer pessoa que descobrisse o endereço poderia apagar sua autorização com uma requisição vazia.

Uma observação honesta sobre o que existe para apagar: o único dado pessoal guardado por este servidor é o próprio token de acesso, junto do identificador da conta. Não há histórico, cópia de publicação nem métrica arquivada, porque nenhuma ferramenta de leitura de conteúdo existe. Apagar o token é, literalmente, apagar tudo.

### 1.6. O endereço de retorno fica para depois

Você vai encontrar o campo **URI de redirecionamento do OAuth** nesta mesma tela. Deixe para a Etapa 3, depois que a hospedagem estiver no ar e você puder copiar o endereço real. Se preferir já preencher, use a linha abaixo, e confira na Etapa 3 se ficou idêntica:

```
https://mcp-instagram-rosepaula.onrender.com/oauth/instagram/callback
```

---

## Etapa 2. Colocar o servidor no ar

O programa a ser hospedado é a pasta `mcp-instagram/` deste repositório. Use a **mesma conta do Render** já usada pelo LinkedIn.

### 2.1. Criar o serviço

No Render, criar um serviço do tipo **Web Service**, apontando para este repositório, com:

| Configuração | Valor |
|---|---|
| Root Directory | `mcp-instagram` |
| Runtime | Docker |
| Nome | `mcp-instagram-rosepaula` |

O arquivo `render.yaml` já traz o resto pronto, inclusive os escopos travados em somente leitura.

Enquanto a construção roda (leva alguns minutos), siga para o passo 2.2.

### 2.2. Gerar a chave de cifragem

Uma única vez, no computador, dentro da pasta `mcp-instagram`:

```bash
python -c "from mcp_instagram.auth_instagram.crypto import generate_key_base64; print(generate_key_base64())"
```

O resultado é a `INSTAGRAM_TOKEN_ENCRYPTION_KEY`. Use uma chave **diferente** da do LinkedIn. É ela que garante que, se o banco de dados vazar, o token continue ilegível.

### 2.3. Cadastrar as variáveis

No painel do Render, na área de variáveis de ambiente. **Nunca em arquivo do projeto.**

| Variável | Conteúdo |
|---|---|
| `MCP_PUBLIC_BASE_URL` | `https://mcp-instagram-rosepaula.onrender.com` |
| `INSTAGRAM_CLIENT_ID` | o ID do aplicativo, do passo 1.3 |
| `INSTAGRAM_CLIENT_SECRET` | a chave secreta, do passo 1.3 |
| `MCP_INSTAGRAM_PONTE_URL` | a mesma URL da ponte já usada pelo LinkedIn |
| `MCP_INSTAGRAM_PONTE_SECRET` | o mesmo segredo da ponte do LinkedIn |
| `INSTAGRAM_TOKEN_ENCRYPTION_KEY` | a chave gerada no passo 2.2 |
| `MCP_CLAUDE_CLIENT_ID` | um identificador à sua escolha, usado na Etapa 4 |

A ponte de armazenamento já publicada para o LinkedIn atende os dois sistemas sem alteração: ela guarda por identificador, e o do Instagram é diferente do LinkedIn. Não é preciso criar nada novo.

---

## Etapa 3. Fechar o endereço de retorno

Com o serviço no ar, o endereço a usar na Meta é este, com o caminho completo:

```
https://mcp-instagram-rosepaula.onrender.com/oauth/instagram/callback
```

Confirme que o endereço do serviço no Render é exatamente esse. Se o nome tiver saído diferente (acontece quando o nome já está em uso por outra pessoa), use o endereço real que o Render mostrou, e corrija nos dois lugares:

1. No campo **URI de redirecionamento do OAuth**, no painel da Meta.
2. Na variável `MCP_PUBLIC_BASE_URL`, no painel do Render, sem o `/oauth/instagram/callback` e sem barra no final.

Os dois precisam contar a mesma história. É o ponto que mais falha, e é o único que exige atenção literal, caractere por caractere.

---

## Etapa 4. Adicionar o conector no Claude

Nas configurações de conectores do Claude, adicionar um conector remoto apontando para:

```
https://mcp-instagram-rosepaula.onrender.com/mcp
```

---

## Etapa 5. Autorizar

Com o conector ativo, peça a autorização do Instagram. O sistema devolve:

- o link oficial de autorização da Meta;
- a lista exata das permissões pedidas, com o que cada uma permite;
- a confirmação de que a conexão é somente leitura;
- como revogar depois.

Abra o link, entre com a conta profissional a ser conectada (@rosepaula_rodrigues) e autorize.

### O que será pedido

| Permissão | O que permite | Publicar | Editar | Excluir | Mensagens | Métricas | Anúncios |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|
| Leitura básica do perfil | Identificar a conta, ler nome de usuário, foto, seguidores e a lista de publicações existentes | não | não | não | não | não | não |
| Leitura de métricas | Alcance, impressões, visualizações de perfil, desempenho por publicação e audiência | não | não | não | não | sim | não |

Nada além disso é pedido. Publicar, responder comentários, ler o Direct e administrar anúncios são permissões separadas, que não estão no pedido.

---

## Se der errado

Os três problemas que aparecem, em ordem de frequência:

| Sintoma | Causa quase certa |
|---|---|
| A Meta recusa no último clique, sem explicar | Endereço de retorno diferente entre o painel da Meta e a variável `MCP_PUBLIC_BASE_URL` |
| A tela de autorização nem abre, ou reclama do tipo de conta | Foi escolhida a configuração com login do Facebook em vez da com login do Instagram, no passo 1.2 |
| Autoriza, mas depois aparece como não conectado | Alguma variável do Render ficou em branco ou com espaço sobrando |

Em qualquer um dos três, me mande a mensagem que apareceu na tela e eu resolvo.

---

## Como revogar depois

Três caminhos, todos independentes:

1. **No Instagram**: Configurações e privacidade, Aplicativos e sites, selecionar o aplicativo, Remover. Este é o definitivo.
2. **No sistema**: a ferramenta de desconectar apaga a autorização guardada na hora, sem alterar nada na conta.
3. **No Claude**: remover o conector nas configurações.

---

## Validade e manutenção

A autorização vale 60 dias. A renovação automática antes do vencimento ainda não foi implementada. Ao expirar, basta autorizar de novo pelo caminho da Etapa 5.

Uma observação sobre o plano gratuito do Render: o serviço "dorme" quando fica sem uso, e a primeira chamada depois disso demora cerca de um minuto para responder. Isso não derruba a conexão com o Instagram, porque o token fica guardado na ponte, que é permanente. O efeito é apenas essa demora ocasional.
