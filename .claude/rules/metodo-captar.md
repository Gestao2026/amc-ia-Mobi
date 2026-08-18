# Método Captar 2.0. Referência Completa

> Base metodológica da AMC IA. Consultar antes de qualquer geração de parecer, proposta, orçamento ou avaliação. Equivale, na captação, ao que a metodologia VTSD é no marketing.

O Método Captar organiza a captação de recursos em 3 fases e 10 pilares, do encontrar o edital até renovar o contrato de assessoria.

---

## FASE 1. CAPTAR (dominar a técnica com IA)

### Pilar 1. Mineração. Encontrar os editais certos
Localizar recursos nacionais e internacionais filtrados pelo perfil da OSC. Eliminar a garimpagem manual em Google, Diário Oficial e grupos de WhatsApp. Manter uma fila de oportunidades qualificadas. Critérios de filtro: escopo (municipal, estadual, nacional, internacional), valor, prazo, área temática, natureza do proponente exigida.
Ferramenta no sistema: `/edital-minerar` (base local de editais) e o agente `minerador-editais`.

### Pilar 2. Requisito. Validar elegibilidade antes de escrever
O erro mais caro é escrever um projeto para um edital que a OSC nunca poderia ganhar. Antes de qualquer elaboração, cruzar os critérios do edital com o perfil da organização: natureza jurídica, tempo de existência, território, área de atuação, certidões e documentos obrigatórios. Veredito: APTO, APTO COM PENDÊNCIAS ou INAPTO.
Ferramenta: agente CaptaDoc, comando `/projeto-elegibilidade`. Esta etapa é protegida pelo Gate de Elegibilidade (ver CLAUDE.md).

### Pilar 3. Projeto. Elaborar proposta e orçamento
Escrever a proposta com estrutura técnica profissional, bloco a bloco, sempre ancorada nos critérios do edital. Montar o orçamento detalhado por rubrica, com memória de cálculo, dentro das regras financeiras do edital.
Ferramentas: agentes CaptaBuilder (`/projeto-escrever`) e CaptaBudget (`/projeto-orcamento`).

### Pilar 4. Submissão. Avaliar antes de enviar
Antes de submeter, auditar a proposta cruzando-a com os critérios do edital. Receber nota por item, estimativa de chance de aprovação por fase e a lista do que melhorar. Reescrever os campos mais críticos.
Ferramenta: agente CaptaScore, comando `/projeto-avaliar`.

---

## FASE 2. POSICIONAR (marketing como captador profissional)

### Pilar 5. Audiência. Criar conteúdo estratégico
Montar presença digital (site, redes) e se posicionar como referência em captação para atrair OSCs. Esta fase reaproveita as competências de marketing (conteúdo, página, oferta).

### Pilar 6. Assessoria. Estruturar o serviço
Definir escopo, precificar (faixa de R$ 3.000 a R$ 8.000 por proposta avulsa, ou contrato anual de R$ 20.000 a R$ 30.000), montar a proposta comercial e posicionar o contrato anual como investimento para a OSC.

### Pilar 7. Oferta. Reunião consultiva e fechamento
Conduzir a reunião consultiva com a OSC prospectada, apresentar o serviço, responder objeções e fechar o contrato.

---

## FASE 3. ASSESSORAR (entregar, faturar e renovar)

### Pilar 8. Prospecção. Abordar OSCs com perfil ideal
Identificar e abordar sistematicamente organizações com perfil para contratar a assessoria, usando os canais construídos na Fase 2.

### Pilar 9. Pitch de vendas. Fechar contratos anuais
Apresentar a proposta de assessoria com script estruturado e objeções mapeadas, fechando contratos recorrentes.
Ferramenta: comando `/assessoria-pitch`.

### Pilar 10. Prestação do serviço. Entregar e renovar
Entregar a captação como assessor usando o método completo e documentar resultados para renovar o contrato. A gestão da carteira (pipeline, clientes, prazos) fica no CaptaHub.
Ferramentas: o estúdio inteiro (4 agentes, exportação). Gestão no CaptaHub.

---

## OS 4 AGENTES EM DETALHE

### CaptaDoc. Triagem e elegibilidade
- Lê o edital e identifica quem pode e quem não pode participar.
- Valida o proponente: CNPJ, natureza jurídica, território, tempo de existência, certidões.
- Monta o checklist de documentos obrigatórios e identifica riscos de inabilitação.
- Classifica: APTO, APTO COM PENDÊNCIAS ou INAPTO NO MOMENTO.
- Diz se pode avançar para o CaptaBuilder.
- Entrada: edital + perfil da OSC. Saída: parecer de elegibilidade + checklist + pendências + recomendação.

### CaptaBuilder. Elaboração da proposta
- Lê o edital e identifica o que mais pontua e o que derruba nota.
- Conduz por blocos: identificação, justificativa, problema, público, objetivos, metas, metodologia, cronograma, equipe, resultados, sustentabilidade, contrapartida, diferenciais, riscos.
- Escreve a proposta completa em formato profissional, adaptada ao formulário oficial quando houver.
- Entrega pontos fortes, fragilidades e estimativa de desempenho.
- Entrada: edital + elegibilidade + respostas por blocos. Saída: proposta completa.

### CaptaBudget. Orçamento técnico
- Lê as regras financeiras do edital: teto, despesas permitidas e vedadas, limites por categoria.
- Lê a proposta e identifica todos os itens necessários, verificando coerência entre projeto e orçamento.
- Monta o quadro por rubrica com memória de cálculo e justificativa técnica.
- Verifica exigência de 3 cotações e alerta sobre itens com risco de glosa.
- Entrada: proposta + edital + modelo de orçamento (se houver). Saída: orçamento técnico + memória de cálculo + pendências.

### CaptaScore. Avaliação e chance de aprovação
- Cruza edital com proposta em análise comparativa profunda.
- Atribui nota de 0 a 10 por critério (usa os critérios reais do edital quando disponíveis).
- Estima a chance de aprovação por fase: eliminatória, técnica e contemplação final.
- Identifica riscos de desclassificação, pontos fortes, fragilidades e inconsistências internas.
- Sugere melhorias práticas e oferece reescrita dos campos mais críticos (versão nota 9,5).
- Entrada: edital + proposta/orçamento. Saída: nota técnica + probabilidade + riscos + sugestões + reescrita.

---

## OS 4 MOTIVOS RECORRENTES DE REPROVAÇÃO

Todo projeto reprova por um (ou mais) destes quatro motivos. Cada agente trata um deles antes do envio:

| Motivo de reprovação | Agente que resolve |
|---|---|
| Edital errado (perfil não alinhado) | Mineração + CaptaDoc |
| Elegibilidade falha (documento, natureza, prazo) | CaptaDoc |
| Texto fraco (não responde aos critérios) | CaptaBuilder + CaptaScore |
| Orçamento furado (teto, item vedado, glosa) | CaptaBudget |

---

## VOCABULÁRIO E TOM (Portal do Captador)

Linguagem de comunidade e prática: faixa preta e faixa branca, pulo do gato, edital, rubrica, parecerista, OSC, glosa, contrapartida, termo de fomento, termo de colaboração. Próxima e cotidiana, sem distância de palestrante. Mantras: "está no edital", "feito é melhor que perfeito", "confia no processo", "direção é mais importante que velocidade", "não seja o avestruz".
