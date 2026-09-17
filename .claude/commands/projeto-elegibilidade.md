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
   - APTO: sugira **`/projeto-estrategia`**. O sinal verde diz que a OSC pode entrar; a etapa estratégica diz se vale a pena e como ganhar. A escrita vem depois dela.
   - APTO COM PENDÊNCIAS: liste o que falta resolver, e sugira **`/projeto-estrategia`** em paralelo. Não faz sentido regularizar documento para um edital em que a organização não tem chance.
   - INAPTO: explique o impedimento e sugira buscar outro edital com `/edital-minerar`. **Não ofereça a etapa estratégica:** não existe estratégia para quem não pode entrar.

## Regras

- Português correto, sem travessão. Não mostre código.
