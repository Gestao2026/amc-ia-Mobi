---
description: CaptaBuilder. Escrever a proposta completa do projeto, bloco a bloco, ancorada no edital.
---

# /projeto-escrever

Aciona o CaptaBuilder para elaborar a proposta completa do projeto.

## Passos

1. Leia `minhas-oscs/.ativa` e identifique o projeto.
2. **Gate de Elegibilidade.** Verifique `elegibilidade.md`. Se ausente, rode `/projeto-elegibilidade` antes. Se o veredito for INAPTO, não prossiga: explique e oriente outro edital. **Este é o único Gate duro.**
3. **Estratégia, que não é Gate.** Verifique `estrategia.md`.
   - Ausente: ofereça `/projeto-estrategia` antes, porque a proposta escrita sem saber quais critérios decidem nasce cega. **Não trave:** se ela quiser escrever assim mesmo, escreva.
   - Presente com 🟢 ou 🟡: siga, usando o que ele definiu como critérios decisivos, evidências e posicionamento.
   - Presente com 🟠 ou **🔴**: mostre em uma linha o motivo e **pergunte se ela confirma seguir**. Com a confirmação, escreva normalmente e registre a decisão dela no `estado.md`, com a data.
4. Anuncie:
   ```
   🔍 Próximo passo: elaborar a proposta completa do projeto (CaptaBuilder). Tempo estimado: 4 a 8 minutos.
   ```
5. Acione o agente `captador-builder`. Ele coleta por blocos (uma pergunta por vez, usando o que já está no perfil) e escreve a proposta.
6. Mostre a proposta para aprovação:
   ```
   1. Aprovar e salvar
   2. Quero ajustar algo
   ```
7. Após aprovar, confirme o salvamento em `proposta.md` e informe o caminho.
8. Próximo passo: `/projeto-orcamento`.

## Regras

- Não escreva nada sem a elegibilidade verificada.
- Português correto, sem travessão. Não mostre código.
