---
description: Conexões e integrações do projeto (CaptaHub e opcionais).
---

# /configurar

Centraliza as conexões e integrações da AMC IA.

## Opções

Pergunte o que o captador quer fazer:

1. **Conectar ao CaptaHub.** Encaminhe para `/captahub-conectar`. É de lá que vêm os editais. Configura `SUPABASE_URL`, `SUPABASE_KEY` e `CAPTAHUB_EDITAIS_TABLE` no `.env` e testa a conexão.
2. **Atualizar os editais agora.** Rode `scripts/captahub-editais.py` para puxar os editais do CaptaHub e atualizar o cache local.
3. **Configurar geração de imagens (opcional).** Para criativos da Fase 2, configure `OPENROUTER_API_KEY` no `.env`.

## Regras

- Tokens e chaves só no `.env`. Nunca escreva valores sensíveis em outro arquivo. Mascare na exibição.
- A gestão da carteira (pipeline, clientes) é no CaptaHub, não aqui.
- Português correto, sem travessão.
