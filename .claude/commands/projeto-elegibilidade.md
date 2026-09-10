---
description: CaptaDoc. Verificar a elegibilidade da OSC para um edital antes de elaborar qualquer coisa.
---

# /projeto-elegibilidade

Aciona o CaptaDoc para cruzar o edital com o perfil da OSC e emitir o veredito de elegibilidade. É o Gate de Elegibilidade do Método Captar: ninguém escreve proposta antes deste passo.

## Passos

1. Leia `minhas-oscs/.ativa`. Identifique o projeto. Se houver vários projetos, pergunte qual edital. Se o edital ainda não foi analisado (`edital.md` ausente), oriente `/edital-analisar` primeiro.
2. Anuncie:
   ```
   🔍 Próximo passo: verificar a elegibilidade da OSC para este edital (CaptaDoc). Tempo estimado: cerca de 90 segundos.
   ```
3. Acione o agente `captador-doc` para o projeto escolhido.
4. Apresente o veredito (APTO, APTO COM PENDÊNCIAS, INAPTO NO MOMENTO), o checklist documental e os riscos. Informe o caminho de `elegibilidade.md`.
5. Próximo passo conforme o veredito:
   - APTO: sugira `/projeto-escrever`.
   - APTO COM PENDÊNCIAS: liste o que falta resolver e diga que a elaboração pode começar em paralelo.
   - INAPTO: explique o impedimento e sugira buscar outro edital com `/edital-minerar`.

## Regras

- Português correto, sem travessão. Não mostre código.
