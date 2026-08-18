---
description: CaptaBudget. Montar o orçamento técnico por rubrica, com memória de cálculo, dentro das regras do edital.
---

# /projeto-orcamento

Aciona o CaptaBudget para transformar a proposta em um orçamento técnico defensável.

## Passos

1. Leia `minhas-oscs/.ativa` e identifique o projeto.
2. Verifique se existe `proposta.md`. Se não, rode `/projeto-escrever` antes: o orçamento nasce das atividades da proposta.
3. Anuncie:
   ```
   🔍 Próximo passo: montar o orçamento técnico por rubrica (CaptaBudget). Tempo estimado: 2 a 4 minutos.
   ```
4. Acione o agente `captador-budget`. Ele lê as regras financeiras do edital, deriva os itens das atividades, monta o quadro por rubrica com memória de cálculo e sinaliza tetos, despesas vedadas, glosa e exigência de 3 cotações.
5. Mostre o orçamento para aprovação (aprovar e salvar / ajustar).
6. Após aprovar, confirme o salvamento em `orcamento.md` e informe o caminho.
7. Próximo passo: `/projeto-avaliar`.

## Regras

- Coerência absoluta entre proposta e orçamento.
- Respeitar teto total e por categoria. Português correto, sem travessão.
