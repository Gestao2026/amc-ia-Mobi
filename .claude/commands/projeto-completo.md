---
description: Captador (chefe do CaptaSuite). Conduzir a linha de montagem completa, da mineração à entrega final, com o chefe validando cada estação.
---

# /projeto-completo

Coloca o Captador, chefe do CaptaSuite, no comando da elaboração inteira: minerar, escolher o edital, verificar elegibilidade, escrever, orçar, preparar anexos, avaliar e exportar, com validação do chefe entre as estações.

## Passos

1. Leia `minhas-oscs/.ativa` e o `perfil-osc.md` da OSC ativa. Se não houver OSC ativa, conduza `/osc-nova` ou `/osc-importar` primeiro.
2. Se já existir um projeto em andamento em `projetos/{edital-slug}/`, pergunte se é para continuar dele ou começar do zero. Continuando, retome da estação apontada pelo `estado.md`.
3. Anuncie:
   ```
   🔍 Próximo passo: conduzir a elaboração completa sob o comando do chefe (8 estações). Tempo estimado: 20 a 40 minutos, com as suas aprovações no caminho.
   ```
4. **Mineração.** Rode o fluxo do `/edital-minerar` (CaptaHub ou cache local; complemento web se preciso).
5. **Escolha do chefe.** Acione o agente `captador-chefe` com a lista minerada. Ele entrega o ranking de até 3 finalistas e UMA recomendação com justificativa técnica e jurídica. Mostre ao captador e peça a aprovação da escolha (opções numeradas).
6. **Análise e gate.** Rode o fluxo do `/edital-analisar` no edital escolhido e depois o `/projeto-elegibilidade` (CaptaDoc). Acione o `captador-chefe` para validar o parecer. Se INAPTO, volte ao passo 5 com o próximo finalista.
7. **Elaboração.** Na ordem, com validação do chefe após cada estação: `/projeto-escrever` (CaptaBuilder, usando o modelo oficial do edital quando houver), `/projeto-orcamento` (CaptaBudget, com cotações na web), `/projeto-anexos` (declarações e checklist de anexos).
8. **Reta final.** `/projeto-avaliar` (CaptaScore), parecer final do chefe (libera ou não libera a submissão), `/projeto-revisar` e `/projeto-exportar`.
9. Ao fim, confirme os caminhos de tudo que foi salvo e a lista de pendências que dependem do captador (assinaturas, certidões, submissão na plataforma).

## Regras

- O Gate de Elegibilidade vale dentro do fluxo: sem APTO ou APTO COM PENDÊNCIAS, nenhuma proposta é escrita.
- As aprovações do captador acontecem nos pontos-chave: escolha do edital, proposta, orçamento e liberação final.
- Veredito "Refazer" do chefe volta a estação para o agente responsável antes de avançar.
- Português correto, sem travessão.
