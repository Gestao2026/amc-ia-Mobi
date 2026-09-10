---
description: Abrir a Sala dos Agentes, o escritório ao vivo onde os agentes da captação circulam e trabalham conforme o sistema executa.
---

# /sala-agentes

Abre a Sala dos Agentes: um escritório em pixel art onde cada agente da captação tem a sua estação e circula em tempo real, mostrando o que está fazendo a cada passo do sistema.

## Como funciona

O hook `agentes-status.py` (PostToolUse, já registrado no `settings.json`) grava o status do agente ativo em `.claude/agents-memory/agents-status.js` a cada ação. A página `sala-dos-agentes.html` (na raiz do projeto) lê esse arquivo a cada 2 segundos, move o boneco do agente responsável até a estação dele e mostra a atividade num balão. Funciona sem servidor, abrindo direto no navegador.

## Passos

1. Informe ao captador o caminho absoluto para abrir no navegador:
   `{raiz-do-projeto}/sala-dos-agentes.html`
2. Oriente a deixar a aba aberta em uma janela ao lado enquanto trabalha. A cada passo (analisar edital, checar elegibilidade, escrever proposta, montar orçamento, avaliar, posicionar), o agente correspondente anda até a estação e trabalha.

## O elenco (as salas do escritório)

- **MINERADOR.** Busca os editais na base.
- **CAPTADOC.** Checa a elegibilidade.
- **CAPTABUILDER.** Escreve a proposta.
- **CAPTABUDGET.** Monta o orçamento.
- **CAPTASCORE.** Avalia a chance de aprovação.
- **POSICIONADOR.** Cuida do marketing da assessoria (Fase 2).
- **ORQUESTRADOR.** Conduz o fluxo da elaboração e cuida do projeto atual.

## Regras

- O selo "claude ativo/inativo" no topo acende quando há atividade recente. Se tudo estiver parado, é só porque nada aconteceu nos últimos segundos.
- Português correto, sem travessão.
