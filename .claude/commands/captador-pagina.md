---
description: Gerar a página da assessoria de captação (captura de leads de OSC), copy e HTML. Pilar 5 e 6.
---

# /captador-pagina

Gera a página que capta OSCs interessadas na assessoria do captador. Copy completa mais HTML de arquivo único.

## Passo 0. Contexto

Leia `captador/perfil-captador.md`. Se não existir, oriente `/captador-perfil`. Se já existe uma oferta estruturada em `captador/oferta.md` (gerada por `/assessoria-estruturar`), use-a. Consulte `.claude/skills/posicionamento-captador/SKILL.md` (estrutura e design da página).

## Passo 1. Entrevista

1. Objetivo da página (1. captar leads para uma reunião de diagnóstico, 2. vender direto um pacote de assessoria).
2. Provas disponíveis (projetos aprovados, depoimentos com resultado, números).
3. Chamada para ação principal (agendar diagnóstico, chamar no WhatsApp, preencher formulário).

## Passo 2. Geração

Anuncie e acione o agente `posicionador-captador`. Ele escreve a copy das 9 seções (dobra inicial, problema real, método dos 4 agentes, prova, como funciona, oferta, autoridade, objeções/FAQ, chamada final) e gera o HTML de arquivo único no design de referência (navy e ciano).

## Passo 3. Entrega

Não mostre o código no chat. Salve o HTML em `captador/entregas/pagina/` e a copy em markdown ao lado. Informe os caminhos absolutos e oriente abrir o HTML no navegador.

## Regras

- Estrutura e design conforme a base de posicionamento. Placeholders para foto e logo.
- Light Copy adaptada: sem travessão, sem exclamação, lead na dor do gestor, prova com resultado.
- Português correto.
