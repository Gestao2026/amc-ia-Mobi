---
description: CaptaBuilder. Escrever a proposta completa do projeto, bloco a bloco, ancorada no edital.
---

# /projeto-escrever

Aciona o CaptaBuilder para elaborar a proposta completa do projeto.

## Passos

1. Leia `minhas-oscs/.ativa` e identifique o projeto.
2. **Gate de Elegibilidade.** Verifique `elegibilidade.md`. Se ausente, rode `/projeto-elegibilidade` antes. Se o veredito for INAPTO, não prossiga: explique e oriente outro edital.
3. Anuncie:
   ```
   🔍 Próximo passo: elaborar a proposta completa do projeto (CaptaBuilder). Tempo estimado: 4 a 8 minutos.
   ```
4. Acione o agente `captador-builder`. Ele coleta por blocos (uma pergunta por vez, usando o que já está no perfil) e escreve a proposta.
5. Mostre a proposta para aprovação:
   ```
   1. Aprovar e salvar
   2. Quero ajustar algo
   ```
6. Após aprovar, confirme o salvamento em `proposta.md` e informe o caminho.
7. Próximo passo: `/projeto-orcamento`.

## Regras

- Não escreva nada sem a elegibilidade verificada.
- Português correto, sem travessão. Não mostre código.
