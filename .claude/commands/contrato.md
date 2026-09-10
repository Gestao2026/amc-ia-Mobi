---
description: Agente de contratos. Minutar o contrato de assessoria com a OSC ou analisar o termo de fomento ou colaboração do financiador.
---

# /contrato

Aciona o agente de contratos nos dois momentos da jornada: fechar o serviço com a OSC ou preparar a assinatura da parceria com o financiador.

## Passos

1. Leia `minhas-oscs/.ativa` e o `perfil-osc.md` da OSC ativa.
2. Pergunte qual contrato trabalhar (opções numeradas):
   ```
   1. Contrato de assessoria (entre você e a OSC cliente)
   2. Termo com o financiador (análise da minuta anexa ao edital)
   ```
3. Anuncie:
   ```
   🔍 Próximo passo: preparar o contrato (agente de contratos). Tempo estimado: 2 a 4 minutos.
   ```
4. Acione o agente `captador-contrato` no modo escolhido:
   - **Modo 1:** ele entrevista sobre formato (avulso ou anual), escopo, honorários e prazo, e minuta o contrato de prestação de serviço.
   - **Modo 2:** ele localiza a minuta do termo nos anexos do edital, monta o mapa de cláusulas (atenção, padrão, a negociar) e cruza com proposta e orçamento.
5. Mostre a entrega para aprovação (aprovar e salvar / ajustar).
6. Confirme o salvamento e informe o caminho: `contrato-assessoria.md` na pasta da OSC (modo 1) ou `projetos/{edital-slug}/contrato/analise-termo.md` (modo 2).

## Regras

- Toda entrega sai com o aviso: minuta de trabalho, revisão por advogado obrigatória antes de assinar.
- No modo 2, sem a minuta real do edital a análise é preliminar e fica marcada como tal.
- Português correto, sem travessão.
