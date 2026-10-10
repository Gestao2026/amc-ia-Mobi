---
description: Alternar entre as OSCs cadastradas e definir qual é a ativa.
---

# /osc-trocar

Mostra a carteira (sincronizada com o CaptaHub) e troca a OSC ativa.

## Passos

1. **Sincronize a carteira.** Se o CaptaHub estiver conectado (`CAPTAHUB_API_TOKEN` no `.env`), puxe a carteira automaticamente: `python3 scripts/captahub-api.py clientes`. Essa é a lista da verdade das OSCs.
2. Varra `minhas-oscs/` pelas pastas locais (cada uma com `perfil-osc.md`, ignore `MODELO-perfil-osc.md`). Ligue cada pasta à OSC do CaptaHub pelo id ("ID CaptaHub" no perfil; na falta, por nome).
3. Apresente uma lista unificada e numerada, marcando o estado de cada OSC:
   - **no CaptaHub + local** (já tem perfil aqui): pronta para trabalhar.
   - **só no CaptaHub** (ainda sem perfil local): ao escolher, importe primeiro com `/osc-importar`.
   - **só local** (não está na carteira): sinalize como fora do CaptaHub.
   Mostre nome, UF, área e quantos projetos abertos (contagem de `projetos/`). Marque a ativa atual (de `minhas-oscs/.ativa`).
4. Pergunte qual passar a ativa.
5. Se a escolhida for "só no CaptaHub", importe primeiro (`/osc-importar`). Depois grave o slug em `minhas-oscs/.ativa` e confirme: "OSC ativa agora: {nome}".
6. **Contexto mínimo suficiente para decidir.** Depois de confirmar a troca, traga **apenas o que muda a decisão ou a próxima ação imediata**: prazo vencido ou próximo do vencimento; pendência bloqueante que trava submissão ou habilitação; inconsistência ou contradição entre fontes do cadastro; mudança relevante desde o último contexto de trabalho; oportunidade ou risco que exija atenção agora. Cada um com o que fazer a respeito, ou com a pergunta que o resolve.

   **Não repita o perfil da organização.** Nada de ficha, tabela de identificação, missão, CNPJ, ID do CaptaHub ou número de contrato: isso já está no `perfil-osc.md` e não muda decisão nenhuma no momento da troca. Não liste a carteira. Não rode o ritual de abertura.

   **Se não houver gatilho nenhum, confirme a troca e pare.** Ausência de alerta é resposta legítima quando não há alerta, e inventar um para parecer útil é erro.
7. Sugira `/edital-minerar` para pegar editais novos ou retomar um projeto aberto dessa OSC.

## Regras

- A carteira é espelho do CaptaHub: a lista de OSCs vem de lá, o perfil local é a cópia de trabalho.
- Se o CaptaHub não estiver conectado, trabalhe só com as locais e ofereça `/captahub-conectar`.
- Português correto, sem travessão.
