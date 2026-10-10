---
description: Captador (chefe do CaptaSuite). Conduzir a linha de montagem completa, da escolha do edital à entrega final, com o chefe validando cada estação.
---

# /projeto-completo

Coloca o Captador, chefe do CaptaSuite, no comando da elaboração inteira: escolher o edital, analisar, verificar elegibilidade, decidir a estratégia, escrever, orçar, preparar os anexos, avaliar, revisar e exportar, com a validação do chefe entre as estações.

É um comando que a captadora dá e acompanha. Nada fica agendado nem roda em segundo plano: o fluxo anda enquanto a conversa está aberta e para em cada ponto de aprovação dela.

## Passos

1. Leia `minhas-oscs/.ativa` e o `perfil-osc.md` da OSC ativa. Se não houver OSC ativa, conduza `/osc-nova` ou `/osc-importar` primeiro.
2. Se já existir um projeto em andamento em `projetos/{edital-slug}/`, pergunte se é para continuar dele ou começar do zero. Continuando, retome da estação apontada pelo `estado.md`.
3. Pergunte se o edital já está escolhido:
   ```
   1. Sim, já tenho o edital (vai direto para a análise)
   2. Não, quero minerar e escolher
   ```
4. Anuncie:
   ```
   🔍 Próximo passo: conduzir a elaboração completa com o chefe validando cada estação (12 etapas). Tempo estimado: 30 a 50 minutos, com as suas aprovações no caminho.
   ```
5. **Mineração** (só na opção 2). Rode o fluxo do `/edital-minerar` (CaptaHub ou cache local; complemento web se preciso).
6. **Escolha do chefe** (só na opção 2). Acione o agente `captador-chefe` com a lista minerada. Ele entrega o ranking de até 3 finalistas e UMA recomendação com justificativa técnica e jurídica. Mostre e peça a escolha da captadora (opções numeradas).
7. **Análise e Gate.** Rode o fluxo do `/edital-analisar` (11 blocos) no edital escolhido e depois o `/projeto-elegibilidade` (CaptaDoc). Acione o `captador-chefe` para validar o parecer. Com INAPTO NO MOMENTO, este edital para: volte ao passo 6 com o próximo finalista, ou encerre se o edital veio escolhido por ela.
8. **Estratégia.** Rode o fluxo do `/projeto-estrategia` (CaptaEstrategista). Com 🟢 ou 🟡, siga. Com 🟠 ou 🔴, mostre o motivo e pergunte se ela confirma seguir; com a confirmação, siga, e a decisão fica registrada no `estrategia.md` com a data.
9. **Elaboração.** Na ordem, com validação do chefe depois de cada estação: `/projeto-escrever` (CaptaBuilder, no modelo oficial do edital quando houver), `/projeto-orcamento` (CaptaBudget, com cotação na web) e `/projeto-anexos` (declarações e checklist de anexos).
10. **Reta final.** `/projeto-avaliar` (CaptaScore), parecer final do chefe (libera ou não libera a submissão), `/projeto-revisar` e `/projeto-exportar`.
11. Ao fim, confirme os caminhos de tudo que foi salvo e a lista de pendências que dependem da captadora (assinaturas, certidões, submissão na plataforma). Lembre de atualizar o status do projeto no CaptaHub quando ela submeter.

## Regras

- **Um só Gate duro, o da elegibilidade.** Sem APTO ou APTO COM PENDÊNCIAS, nenhuma proposta é escrita.
- **O resto alerta, não trava.** O 🟠 e o 🔴 do CaptaEstrategista, o "Refazer" e o "não libera" do chefe mostram o motivo e esperam a decisão dela. Se ela seguir, a decisão fica registrada com a data e o trabalho continua.
- **Cada estação mantém a própria aprovação.** Proposta, orçamento, anexos e avaliação passam pelo "1. Aprovar e salvar / 2. Quero ajustar algo" de cada comando. Este comando não pula nenhuma.
- **CaptaHub, estação por estação.** Cada comando chamado aqui segue a própria classificação do CLAUDE.md. A leitura necessária roda (a mineração puxa os editais). Toda gravação na carteira (abrir o projeto depois do APTO, valor solicitado, nota, status de submetido) é oferecida em uma linha e espera o OK, uma de cada vez. Dar o `/projeto-completo` não é OK para gravação nenhuma.
- Nenhum agente chama a API do CaptaHub; quem oferece e grava é o comando.
- O `estrategia.md` nunca entra na exportação. O `parecer-chefe.md` entra marcado como uso interno e nunca é anexado na submissão.
- Português correto, sem travessão.
