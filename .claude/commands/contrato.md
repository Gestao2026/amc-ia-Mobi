---
description: Contratos. Minutar o contrato de assessoria com a OSC ou analisar o termo de fomento ou colaboração do financiador.
---

# /contrato

Aciona o agente de contratos nos dois momentos da jornada: fechar o serviço com a OSC ou preparar a assinatura da parceria com o financiador.

## Passos

1. Leia `minhas-oscs/.ativa` e o `perfil-osc.md` da OSC ativa.
2. Pergunte qual contrato trabalhar:
   ```
   1. Contrato de assessoria (entre você e a OSC cliente)
   2. Termo com o financiador (análise da minuta anexa ao edital)
   ```
3. No modo 2, identifique o projeto e confira se a minuta do termo está em `projetos/{edital-slug}/documentos/`. Se não estiver, pergunte se ela quer anexar agora ou seguir com uma análise preliminar.
4. Anuncie:
   ```
   🔍 Próximo passo: preparar a minuta ou a análise do contrato (3 passos). Tempo estimado: 2 a 4 minutos.
   ```
5. Acione o agente `captador-contrato` no modo escolhido:
   - **Modo 1:** ele entrevista, uma pergunta por vez, sobre formato (avulso, anual ou captação junto a empresas), escopo, honorários, prazo e quem assina pela OSC, e minuta o contrato de prestação de serviço.
   - **Modo 2:** ele localiza a minuta do termo nos anexos do edital, monta o mapa de cláusulas (atenção, padrão, a negociar) e cruza com a proposta, o cronograma e o orçamento.
6. Mostre a entrega para aprovação:
   ```
   1. Aprovar e salvar
   2. Quero ajustar algo
   ```
7. Confirme o salvamento e informe o caminho: `minhas-oscs/{slug}/contrato-assessoria.md` (modo 1) ou `projetos/{edital-slug}/contrato/analise-termo.md` (modo 2).

## Regras

- Toda entrega sai com o aviso: minuta de trabalho, revisão por advogado obrigatória antes de assinar.
- No modo 2, sem a minuta real do edital a análise é preliminar e fica marcada como tal.
- O sistema não envia a minuta a ninguém. Mandar para a OSC ou para o financiador é decisão da captadora, feita por ela.
- Este comando não grava nada no CaptaHub.
- Português correto, sem travessão.
