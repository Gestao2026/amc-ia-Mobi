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
4. Acione o agente `captador-score`. **A primeira coisa que ele estabelece é a escala do edital, com o item.** Se o edital não tiver pontuação, ele diz isso e **não produz número nenhum**: nem nota por critério, nem média, nem chance em porcentagem. Se tiver, usa a escala dele, inclusive quando ela for por degrau, sem valor intermediário.
5. Apresente o que existir: a escala e sua fonte, a leitura por critério, os riscos e as reescritas. **Nota geral e chance por fase só quando o edital tiver escala.** Informe o caminho de `score.md`.
6. Próximo passo:
   - Se PRONTO PARA SUBMETER: sugira `/projeto-revisar` e a submissão.
   - Se AJUSTAR ANTES: aplique as reescritas (voltando ao `/projeto-escrever` ou `/projeto-orcamento` conforme o caso) e reavalie.

## Regras

- Avaliação honesta e específica. Toda crítica vem com a correção ao lado.
- Português correto, sem travessão.
