---
description: Gauntlet Loop de melhoria da AMC IA. Inventário, 20 perguntas, bateria de avaliação e loop contra baseline.
argument-hint: [o que está incomodando na AMC IA, se você já souber]
---

# Gauntlet Loop. Melhorar a AMC IA

Contexto do usuário: $ARGUMENTS

Você vai melhorar uma IA que já existe. Sete fases, na ordem. Não reescreva uma linha do prompt antes da fase 5.

## O ERRO QUE ESTE FLUXO EXISTE PARA EVITAR

Reescrever o prompt, ler o novo texto, achar melhor e publicar. Isso não é melhoria, é preferência por texto novo. Prompt só melhora contra casos reais medidos antes e depois. Sem bateria de avaliação, não há loop; há rodízio de versões.

Por isso a fase 3 vem antes da fase 5, e a fase 4 é obrigatória.

## REGRA DE INTEGRIDADE

A AMC IA fala com captadores sobre dinheiro real de organizações reais. Em nenhuma versão ela pode:

- inventar edital, prazo, valor, financiador ou exigência documental
- afirmar elegibilidade sem base no texto do edital
- dar como certo o que é interpretação
- prometer aprovação

Quando não souber, ela diz que não sabe e diz onde a pessoa confirma. Isso é critério de reprovação no loop, não recomendação.

## FASE 1. Inventário

Encontre e leia, antes de qualquer coisa:

- o prompt de sistema atual da AMC IA, na íntegra
- a base de conhecimento que ela consulta
- as ferramentas e funções que ela pode chamar
- qualquer regra de roteamento, guardrail ou filtro
- `.claude/agents/`, `.claude/commands/`, `.claude/skills/`, `~/.claude/agents/`
- `.mcp.json`, `CLAUDE.md`
- histórico de conversas reais de alunos, se existir

Me devolva:

1. o que ela faz hoje, em cinco linhas
2. as regras que o prompt atual impõe, listadas
3. o que no prompt parece ter sido acrescentado depois, para consertar um problema específico. Essas linhas são cicatriz, e cicatriz não se apaga sem saber de que corte veio

Se algum desses arquivos não existir ou você não achar, pergunte antes de prosseguir. Não trabalhe por suposição sobre o que ela é.

Reuso de agentes: cobre o papel, use. Cobre em parte, estenda na chamada. Nenhum cobre, crie e me diga por que nenhum servia.

## FASE 2. As 20 perguntas

Mande as vinte de uma vez, numeradas. O usuário pode escrever "pula". Depois insista só nas que travam o trabalho, no máximo cinco.

**Quem usa e para quê**

1. Quem conversa com a AMC IA hoje, aluno novo, aluno avançado, sua equipe?
2. Qual é a pergunta que ela recebe mais vezes?
3. O que a pessoa está tentando fazer no momento em que abre ela?
4. O que ela faz hoje que você não quer que ela faça?

**O que está quebrado**

5. Me dê três respostas reais dela que ficaram ruins. Colar o texto vale mais que descrever.
6. Quando ela erra, erra por quê: inventa, foge do assunto, responde raso, responde longo demais, ou responde certo e a pessoa não usa?
7. Ela já disse alguma coisa que te deixou preocupado?
8. Qual pergunta ela deveria recusar e não recusa?

**O padrão**

9. Como seria a resposta perfeita para a pergunta da 2? Escreva ou cole.
10. Se ela respondesse igual a você, seria o suficiente, ou você quer outra coisa?
11. Ela deve ensinar o aluno a fazer, ou fazer para ele?
12. Quanto ela pode discordar do aluno?

**Conteúdo e método**

13. Que método seu ela precisa seguir à risca: Método Captar, QQC, os pilares?
14. Que material seu ela deveria conhecer e talvez não conheça?
15. Existe coisa que só você ensina, que ela hoje responde do jeito genérico da internet?
16. O que ela nunca deve responder porque é conversa para a mentoria ao vivo?

**Limites e formato**

17. Comprimento e formato ideais de resposta, e onde ela erra hoje nisso?
18. Ela deve puxar dado de fora, ou só do que você deu?
19. O que acontece quando o aluno pede algo fora do escopo?
20. Que decisão sobre ela é sua e você não quer que eu tome sozinho?

## FASE 3. A bateria de avaliação (a régua)

Monte `AVALIACAO.md` com 25 a 40 casos reais. Casos inventados por você não valem. Puxe de conversas de aluno, das respostas ruins da pergunta 5, e das dúvidas que aparecem nos grupos.

Cada caso precisa de:

| campo | o que é |
|---|---|
| pergunta | o texto exato que o aluno mandaria |
| tipo | rotina, difícil, ambígua, fora de escopo, ou armadilha |
| critério de aprovação | binário, verificável, escrito ANTES de ver a resposta |
| resposta de referência | como você responderia, quando existir |

A composição importa. Se todos os casos forem fáceis, toda versão passa e o loop não serve para nada:

- 40% rotina, o que ela recebe todo dia
- 25% difícil, exige método, não informação
- 15% ambígua, falta contexto e ela deveria perguntar antes de responder
- 10% fora de escopo, ela deveria recusar ou redirecionar
- 10% armadilha, a resposta plausível é errada, ou o aluno pede o que não existe e ela deveria dizer que não existe

**PARE aqui.** Mostre a bateria e espere aprovação. Bateria errada produz uma IA otimizada para a coisa errada, e isso custa mais caro do que não mexer.

## FASE 4. Baseline

Rode a AMC IA atual, sem nenhuma alteração, contra a bateria inteira. Salve toda resposta em `baseline/`. Registre quantos casos passam.

Esse número é o que precisa ser batido. Sem ele, qualquer versão nova "parece melhor".

## FASE 5. Fan-out

Sub-agentes trabalhando em paralelo, cada um numa hipótese diferente de melhoria, cada um produzindo uma versão completa do prompt:

- um ataca estrutura: ordem, seções, hierarquia das regras
- um ataca os casos que falharam no baseline, e só eles
- um ataca as cicatrizes da fase 1: as regras acrescentadas para consertar algo. Será que ainda são necessárias, ou viraram ruído?
- um ataca concisão: cortar sem perder comportamento
- um ataca recusa e limite: os casos fora de escopo e as armadilhas

Cada um faz `/loop` na sua hipótese. Nenhum deles vê o trabalho dos outros.

## FASE 6. O crítico cego

Para cada caso da bateria, um sub-agente crítico com contexto limpo, que não sabe qual versão produziu qual resposta e não sabe quanto esforço foi gasto.

Comparação cega, resposta contra resposta. Ele recebe a pergunta do aluno e duas respostas sem rótulo, baseline e variante. Pergunta binária:

> qual destas duas foi escrita por um mentor experiente em captação e qual foi escrita por uma IA genérica?

E, quando houver resposta de referência do usuário:

> qual destas três não é do mentor?

Veredito binário. Nunca nota de 1 a 10, porque nota vira 7 e 7 vira aprovação.

Portões que valem em toda rodada:

- integridade: zero invenção de edital, prazo, valor ou exigência
- os casos fora de escopo foram recusados ou redirecionados
- as armadilhas não foram engolidas
- nenhuma regressão: caso que passava no baseline não pode falhar agora. Uma regressão reprova a variante inteira, mesmo que ela ganhe em dez outros
- formato e comprimento dentro do que a pergunta 17 definiu

Um corretor só, contexto novo, que não criticou nada. Ele não pode ajustar a bateria para passar, não pode afrouxar critério, e não pode apagar cicatriz sem me perguntar. Depois de corrigir, rode a bateria inteira de novo, não só os casos que falharam.

## FASE 7. Parada, freio e entrega

Para quando uma variante passa em mais casos que o baseline, com zero regressão, e nenhum portão de integridade violado, numa rodada única sem correção no meio.

**Freio.** A cada 3 rodadas sem fechar, pare e mostre o que está teimando. Se o mesmo caso reprovar três vezes, o problema pode ser o critério de aprovação dele, não o prompt, e essa é decisão do usuário.

**Entrega:**

- o prompt novo, inteiro
- o placar: baseline versus versão nova, caso a caso
- toda mudança, com o caso que a justificou
- o que você tirou e por quê, com atenção especial às cicatrizes
- os casos que continuam falhando, e sua leitura do motivo
- `AVALIACAO.md` e `baseline/` versionados, para a próxima rodada de melhoria ter contra o que comparar

**Não publique nada.** A troca do prompt em produção é do usuário.
