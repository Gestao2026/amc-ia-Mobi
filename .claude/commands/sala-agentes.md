---
description: Abrir a Sala dos Agentes, o escritório ao vivo onde os agentes da captação circulam e trabalham conforme o sistema executa.
---

# /sala-agentes

Abre a Sala dos Agentes: um escritório em pixel art onde cada agente da captação tem a sua estação e circula em tempo real, mostrando o que está fazendo a cada passo do sistema.

## Como funciona

> **A sala está parada desde 01/09/2026.** O gancho que a alimentava, `.claude/hooks/agentes-status.py`, foi retirado do `.claude/settings.json` quando a regra NADA RODA SOZINHO desligou todos os ganchos. O script continua no disco, intacto, mas **não está ativo**. A página abre e mostra o último estado gravado antes do desligamento; nenhum boneco se move. Reativar depende de a captadora pedir, com todas as letras.

Quando estava ativo, o funcionamento era este: o gancho `agentes-status.py` (PostToolUse) gravava o status do agente em `.claude/agents-memory/agents-status.js` a cada ação, e a página `sala-dos-agentes.html` (na raiz do projeto) lia esse arquivo a cada 2 segundos, movia o boneco até a estação e mostrava a atividade num balão. Funcionava sem servidor, abrindo direto no navegador.

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
