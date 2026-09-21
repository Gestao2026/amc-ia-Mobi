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
Logo depois do sinal verde, e antes de escrever, o CaptaEstrategista (`/projeto-estrategia`) diz se vale a pena entrar e como ganhar. Não é porta dura: o vermelho dele alerta e pede a confirmação do captador.

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
Ferramentas: o estúdio inteiro (5 agentes, exportação). Gestão no CaptaHub.

---

## OS 5 AGENTES EM DETALHE

### CaptaDoc. Triagem e elegibilidade
- Lê o edital e identifica quem pode e quem não pode participar.
- Valida o proponente: CNPJ, natureza jurídica, território, tempo de existência, certidões.
- Monta o checklist de documentos obrigatórios e identifica riscos de inabilitação.
- Classifica: APTO, APTO COM PENDÊNCIAS ou INAPTO NO MOMENTO.
- Diz se pode avançar para o CaptaBuilder.
- Entrada: edital + perfil da OSC. Saída: parecer de elegibilidade + checklist + pendências + recomendação.

### CaptaEstrategista. Estratégia de entrada
- Entra **depois** do sinal verde da elegibilidade e **antes** de qualquer linha de proposta.
- Responde a pergunta que a elegibilidade não responde: dado que podemos entrar, **vale a pena**, e qual é a melhor estratégia para aumentar a chance de aprovação?
- Oito análises: aderência estratégica (aderência real contra encaixe forçado), atratividade da oportunidade, força competitiva, esforço contra retorno em horas, riscos e pontos cegos, estratégia de entrada, como ganhar, e a recomendação final.
- Recomenda em quatro estados: prioridade alta; oportunidade condicionada a ajustes nomeados; baixa prioridade por esforço elevado e retorno incerto; não recomendar entrada.
- Trabalha em dois modos: **com projeto**, avaliando o que existe, e **sem projeto**, dizendo que formato ganharia naquele edital. O segundo modo é o que impede o encaixe forçado.
- Toda afirmação vem rotulada em uma de quatro marcas: exigência do edital com o item, dado com a fonte, inferência com o salto exposto, ou recomendação. Não existe uma quinta marca.
- É o único agente Capta com acesso à web, para levantar concorrência e histórico do financiador. A busca **nunca** contém dado da organização.
- **Não é porta dura.** O único Gate que trava a elaboração é o da elegibilidade.
- Entrada: edital analisado + parecer de elegibilidade + perfil + histórico. Saída: `estrategia.md` com as oito análises e o semáforo, seguindo `minhas-oscs/MODELO-estrategia.md`. Comando: `/projeto-estrategia`.

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

## O CHEFE E OS ESPECIALISTAS DE APOIO (CaptaSuite completo)

### Captador (captador-chefe). O chefe do CaptaSuite
- Consultor sênior com mais de 25 anos de mercado. Domina o MROSC (Lei 13.019/2014), as leis de incentivo (Rouanet, Esporte, FIA, Fundo do Idoso) e as regras de prestação de contas.
- Escolhe a melhor oportunidade entre os editais minerados, com justificativa técnica e jurídica (e diz qual edital não disputar).
- Valida a entrega de cada estação (Aprovado, Aprovado com ressalvas, Refazer) e emite o parecer final de submissão.
- Entrada: perfil da OSC + editais minerados + entregas das estações. Saída: `parecer-chefe.md`. Comando: `/projeto-completo`.

### Agente de declarações e anexos (captador-anexos)
- Mapeia todos os anexos exigidos pelo edital, citando o item que exige cada um.
- Gera as declarações que o sistema consegue produzir com os dados do perfil (modelo do edital quando houver), cruza com os documentos que a OSC já tem e cobra do captador o que só ele pode fornecer, com prazo.
- Entrada: edital + elegibilidade + perfil e documentos da OSC. Saída: declarações + `checklist-anexos.md`. Comando: `/projeto-anexos`.

### Agente de contratos (captador-contrato)
- Modo assessoria: minuta o contrato de prestação de serviço entre o captador e a OSC (avulso ou anual).
- Modo financiador: analisa a minuta do termo de fomento ou colaboração anexa ao edital, com mapa de cláusulas de risco cruzado com proposta e orçamento.
- Toda entrega sai com o aviso de revisão obrigatória por advogado. Saída: `contrato-assessoria.md` ou `contrato/analise-termo.md`. Comando: `/contrato`.

---

## OS 5 MOTIVOS RECORRENTES DE REPROVAÇÃO

Todo projeto reprova por um (ou mais) destes cinco motivos. Cada agente trata um deles antes do envio:

| Motivo de reprovação | Agente que resolve |
|---|---|
| Edital errado (perfil não alinhado) | Mineração + CaptaDoc |
| Elegibilidade falha (documento, natureza, prazo) | CaptaDoc |
| **Entrar sem chance ou sem estratégia** (aderência forçada, disputa ignorada, esforço maior que o retorno) | **CaptaEstrategista** |
| Texto fraco (não responde aos critérios) | CaptaBuilder + CaptaScore |
| Orçamento furado (teto, item vedado, glosa) | CaptaBudget |

---

## VOCABULÁRIO E TOM (Portal do Captador)

Linguagem de comunidade e prática: faixa preta e faixa branca, pulo do gato, edital, rubrica, parecerista, OSC, glosa, contrapartida, termo de fomento, termo de colaboração. Próxima e cotidiana, sem distância de palestrante. Mantras: "está no edital", "feito é melhor que perfeito", "confia no processo", "direção é mais importante que velocidade", "não seja o avestruz".
