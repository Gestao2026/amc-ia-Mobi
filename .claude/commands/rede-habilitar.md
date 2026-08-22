---
description: Habilitar uma rede social como conector, do painel de desenvolvedor até a primeira leitura confirmada, na ordem que evita trabalho perdido.
---

# /rede-habilitar

Conduz a habilitação técnica de uma rede social como conector MCP. Cobre as seis etapas, do painel de desenvolvedor até a primeira leitura confirmada contra a API real.

A ordem aqui não é sugestão. Ela existe porque cada etapa pode invalidar a seguinte, e descobrir isso tarde custa horas.

## O Gate de Capacidade (regra de ouro desta habilitação)

> **Nunca escreva código para uma capacidade antes de confirmar que a API a permite para esta conta.**

É o mesmo princípio do Gate de Elegibilidade do Método Captar: ninguém escreve a proposta antes de saber se a OSC pode concorrer. Aqui: ninguém escreve a ferramenta antes de saber se a rede permite.

O que derruba uma capacidade, e não tem contorno técnico:

- **Produto não aprovado no aplicativo.** No LinkedIn, ler métrica exige a Community Management API. Sem ela aprovada, nenhuma configuração resolve.
- **Tipo de conta.** No Instagram, conta Criador entrega menos métrica que Comercial. Conta pessoal não entrega nada.
- **Escopo não concedido.** Pedir um escopo que o aplicativo não tem aprovado faz a rede recusar a autorização **inteira**, derrubando até os escopos válidos.

Antes de qualquer código, produza a tabela: **o que quero, a rede permite, e com qual produto ou escopo.**

## Etapa 1. Levantar o que a conta permite hoje

1. Anuncie:
   ```
   🔍 Próximo passo: levantar o que a API desta rede permite para esta conta (3 passos). Tempo estimado: 3 a 5 minutos.
   ```
2. Peça ao captador a lista de **produtos aprovados** no painel de desenvolvedor da rede, e o **tipo da conta**.
3. Monte a tabela do que será possível e do que não será. Mostre antes de seguir.

**Se algo que ele quer não for possível, diga agora.** Descobrir depois de três horas de código é o pior desfecho.

## Etapa 2. O aplicativo no painel da rede

Cadastro no portal de desenvolvedores. Conteúdo varia por rede; os campos que sempre existem:

| Campo | Cuidado |
|---|---|
| Escopos / permissões | apenas os que têm produto aprovado |
| URI de redirecionamento | precisa bater **caractere por caractere** com o que o servidor envia |

Um `/` a mais no fim do redirecionamento faz a troca do código por token falhar, com mensagem que não explica o motivo.

Peça também a lista de produtos em análise, com prazo. No LinkedIn a análise leva de 10 a 14 dias úteis, e isso muda o cronograma.

## Etapa 3. Publicar o servidor

Hospedagem em Render, plano gratuito, `Root Directory` apontando para a pasta do componente.

Variáveis mínimas:

| Variável | Observação |
|---|---|
| `MCP_TRANSPORT` | `streamable-http` |
| `MCP_PUBLIC_BASE_URL` | a URL do próprio serviço |
| `{REDE}_CLIENT_ID` e `_CLIENT_SECRET` | do painel da rede |
| `{REDE}_SCOPES` | separados por vírgula, **sem espaços** |
| `MCP_CLAUDE_CLIENT_ID` e `_CLIENT_SECRET` | protegem a rota `/mcp` |

## Etapa 4. Onde o token vai morar

**Esta etapa não é opcional, e pular custa caro depois.**

O padrão em Linux é `memory`, e o Render adormece o serviço após cerca de 15 minutos ocioso. Com `memory`, a autorização morre a cada hibernação, e o sintoma que chega ao captador é *"ontem estava conectado e hoje não está"*, sem nenhuma pista da causa.

Use `ponte`, que grava no MySQL da HostGator através de um PHP, com o token cifrado por uma chave que existe **apenas no Render**.

Instalação: `mcp-instagram/ponte-hostgator/README.md`. **Leia as armadilhas antes de tocar em qualquer arquivo**, elas custaram horas na instalação real.

Ao criar a ponte de um componente novo, são **quatro** linhas a mudar no PHP: cabeçalho, caminho do config, alvo e tabela padrão. A do alvo é a mais importante: sem ela, o componente novo grava por cima do token do outro e derruba os dois.

**A chave de cifragem** é base64 de exatamente 32 bytes: `openssl rand -base64 32`, que dá 44 caracteres terminando em `=`. Não use gerador genérico nem o botão "Generate" do painel de hospedagem: o formato não bate e o servidor recusa. Ela vai só no Render, nunca na hospedagem, e cada componente tem a sua.

## Etapa 5. Manter acordado

Um ping externo gratuito, a cada 10 minutos, no horário de trabalho:

```
*/10 8-20 * * 1-5
```

apontando para `/.well-known/oauth-authorization-server`, que é público e minúsculo.

**A janela de horário é obrigatória**, não estética: o Render dá cerca de 750 horas mensais por conta, e dois serviços acordados 24 horas consumiriam 1.460.

**Configure o tempo limite do ping em 30 segundos.** Acordar leva uns 12. Com limite baixo, o ping desiste no meio, o serviço volta a dormir, e o ciclo se repete indefinidamente.

## Etapa 6. Conectar e autorizar

1. Conector personalizado apontando para a URL do servidor **com `/mcp` no final**. A raiz não responde.
2. Chame `{rede}_oauth_iniciar`, entregue a URL ao captador, peça para autorizar. Expira em 10 minutos.
3. Lembre que a senha é digitada **apenas** na tela da própria rede. Se aparecer campo de senha em outro lugar, é para desconfiar.

## Etapa 7. Confirmar com uso real

Habilitação sem teste real não está concluída. Chame uma ferramenta de leitura e mostre o resultado ao captador.

Confirme também que o token foi para a **tabela certa**, e que o token do outro componente continua intacto. É o teste que prova a separação.

## Regras que valem para toda rede

**Somente leitura por padrão.** Publicação é decisão consciente, nunca efeito colateral de um escopo pedido "para garantir". Quando houver publicação, ela exige confirmação em duas etapas: a primeira chamada devolve a prévia, a segunda publica.

**Nada vai ao ar sem o captador ler o texto antes.**

**Documente ao final**, na pasta do componente: o que ele faz, o que ele não faz e por quê, onde o token mora, e as armadilhas que apareceram. Documentação que envelhece e passa a mentir é pior que documentação ausente.

## Ordem de execução, resumida

```
1. levantar o que a API permite      ← o gate; nada de código antes
2. aplicativo no painel da rede
3. publicar o servidor
4. onde o token vai morar            ← pular aqui custa caro depois
5. manter acordado
6. conectar e autorizar
7. confirmar com uso real
```
