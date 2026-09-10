---
description: CaptaScore. Avaliar o projeto, dar nota por critério e estimar a chance de aprovação antes de submeter.
---

# /projeto-avaliar

Aciona o CaptaScore para auditar o projeto com visão de banca antes da submissão. É o diferencial do método: você sabe a chance antes de enviar.

## Passos

1. Leia `minhas-oscs/.ativa` e identifique o projeto.
2. Verifique se existem `proposta.md` e `orcamento.md`. Avalie o que existir e avise o que não pôde ser pontuado.
3. Anuncie:
   ```
   🔍 Próximo passo: avaliar o projeto e estimar a chance de aprovação (CaptaScore). Tempo estimado: 2 a 3 minutos.
   ```
4. Acione o agente `captador-score`. Ele extrai os critérios do edital, dá nota de 0 a 10 por critério, estima a chance por fase, aponta riscos de desclassificação e reescreve os campos críticos.
5. Apresente: nota geral, chance por fase, nota por critério, riscos e as reescritas "nota 9,5". Informe o caminho de `score.md`.
6. Próximo passo:
   - Se PRONTO PARA SUBMETER: sugira `/projeto-revisar` e a submissão.
   - Se AJUSTAR ANTES: aplique as reescritas (voltando ao `/projeto-escrever` ou `/projeto-orcamento` conforme o caso) e reavalie.

## Regras

- Avaliação honesta e específica. Toda crítica vem com a correção ao lado.
- Português correto, sem travessão.
