# 24. Desligamento do encaminhamento da editais para a gestao

**Data:** 30/08/2026
**Contas envolvidas:** editais.mobilizando@gmail.com (origem) e gestao.mobilizando@gmail.com (destino)

## O que foi feito

O encaminhamento automático da conta **editais.mobilizando** para a **gestao.mobilizando** foi **desativado**.

- Local: Gmail da editais, aba **Encaminhamento e POP/IMAP**, opção **Desativar encaminhamento**, salvo.
- Confirmação: a página foi recarregada e a opção permaneceu marcada.
- O endereço da gestao continua cadastrado na lista (aparece como "em uso"), mas não recebe mais cópia. Isso é normal e não reativa nada.

## Diagnóstico feito antes

Foram descartadas as outras formas de redirecionamento:

| Verificação | Conta | Resultado |
|---|---|---|
| Encaminhamento automático | editais | **Ativo** para a gestao, com "manter cópia na Caixa de entrada". Causa única. |
| Filtros com "Encaminhar para" | editais | Nenhum filtro cadastrado |
| Encaminhamento automático | gestao | Desativado |
| Download POP | gestao | Desativado |
| Verificar e-mail de outras contas | gestao | Vazio, a gestao não puxava nada |
| Delegação de acesso | gestao | Sem delegados |

## Período em que o encaminhamento esteve ligado

**De 18/08/2026 até 30/08/2026**, por volta das 20h50 (horário do desligamento).

Apuração: na gestao, a busca `to:editais.mobilizando@gmail.com` não retorna nada antes de 18/08, fora 3 mensagens isoladas de junho (2 alertas em 29/06 e um teste "Ola" em 17/06).

## Cruzamento das duas caixas

| Medida | Valor |
|---|---|
| Conversas na editais no período (18/08 a 30/08) | **106** |
| Conversas na gestao com `to:editais.mobilizando@gmail.com` (total) | **96** |
| Conversas na editais no período que **não** são Alerta do Google | **1** |

### Achado principal

**105 das 106 conversas do período são Alerta do Google** (`googlealerts-noreply@google.com`). A única exceção é uma promoção do Google Workspace ("Agora você tem acesso exclusivo aos recursos de IA"), recebida em 30/08 às 21h14, ou seja, **depois** do desligamento. Ela não tem cópia na gestao, e é a prova de que o desligamento funcionou.

### Diferença de 10 conversas

- **1** explicada: a mensagem do Workspace que chegou após o desligamento.
- **9** não conciliadas item a item. A hipótese mais provável é agrupamento de conversas do Gmail (alertas com o mesmo assunto em dias diferentes entram numa conversa só, e as duas contas agrupam de formas distintas). Numa amostragem de 21 e 22/08, a editais mostrou 12 conversas e a gestao 11, e o item "Alerta do Google, apoio projetos de impacto social" de 21/08 não apareceu na listagem da gestao.

**Consequência prática:** não é seguro apagar por faixa de data sozinha. A conferência foi feita por conversa, não mensagem a mensagem.

## Recomendação

1. **O problema real não é duplicata, é volume de alerta.** A caixa da editais não está cheia de editais, está cheia de Alerta do Google. Reduzir ou desativar alertas em <https://www.google.com/alerts> resolve a origem. Apagar as mensagens trata o sintoma e elas voltam amanhã.
2. **Se ainda assim quiser limpar**, use na editais a busca abaixo, revise a tela antes de selecionar e nunca use "selecionar todas as conversas que correspondem":
   ```
   from:googlealerts-noreply@google.com after:2026/08/17 before:2026/08/31
   ```
3. **O conector da AMC IA lê a editais.** Tudo que sair de lá deixa de ser visível para o sistema, mesmo existindo na gestao.

## Teste de confirmação pendente

Enviar um e-mail de um endereço externo para a editais e confirmar que ele **não** aparece na gestao.
