---
description: Conectar a AMC IA ao CaptaHub para puxar os editais e usar a carteira de lá.
---

# /captahub-conectar

Liga a AMC IA ao CaptaHub. O CaptaHub é a fonte da verdade: é de lá que vêm os editais e onde fica a carteira (pipeline e clientes). A AMC IA é o estúdio que recebe um edital e produz o projeto. Esta conexão faz o Claude entrar no CaptaHub para puxar os editais ao vivo.

## Passo 0. Contexto

A conexão usa credenciais do CaptaHub guardadas no `.env` (e só no `.env`). Os valores nunca aparecem em outro arquivo nem são exibidos no chat sem máscara.

Há dois caminhos de conexão (o token da API é o recomendado):

- **API por token (recomendado).** Token pessoal gerado na aba API do CaptaHub. Dá acesso a editais, ao pipeline e aos clientes do dono do token (multi-tenant). Variáveis: `CAPTAHUB_API_URL` e `CAPTAHUB_API_TOKEN`. Detalhes em `docs/integracao-captahub-api.md`.
- **Banco direto (legado).** Leitura dos editais via PostgREST. Variáveis: `SUPABASE_URL`, `SUPABASE_KEY`, `CAPTAHUB_EDITAIS_TABLE`. Serve de fallback de cache de editais.

## Passos (API por token, recomendado)

1. Pergunte ao captador se ele já tem o token da API do CaptaHub (gerado na aba API). Se não tiver, oriente a gerá-lo lá.
2. Receba e grave no `.env` (criando o arquivo se não existir), sem ecoar o valor:
   - `CAPTAHUB_API_URL`
   - `CAPTAHUB_API_TOKEN`
   Ao confirmar, mostre apenas mascarado: `CAPTAHUB_API_TOKEN = (salvo, mascarado)`.
3. Teste a conexão rodando `python3 scripts/captahub-api.py testar`. Informe o dono do token e os escopos concedidos.
4. A partir daí, editais (`editais`), carteira (`projetos`) e clientes (`clientes`) ficam disponíveis pelo conector. Veja os subcomandos em `docs/integracao-captahub-api.md`.

## Passos (banco direto, legado/fallback de editais)

1. Receba e grave no `.env` (sem ecoar): `SUPABASE_URL`, `SUPABASE_KEY`, `CAPTAHUB_EDITAIS_TABLE` (opcional, padrão `editais`).
2. Teste com `python3 scripts/captahub-editais.py --testar`. Informe quantos editais o CaptaHub respondeu.
3. Para atualizar o cache local de editais, rode `python3 scripts/captahub-editais.py` (sem o `--testar`).

## Quando não há conexão

Sem as credenciais, o sistema continua funcionando com o último cache local de editais baixado. A mineração avisa que está usando o cache, não dados ao vivo.

## Sobre a carteira (pipeline e CRM)

A gestão da carteira (pipeline de projetos, clientes, prazos) vive no CaptaHub, não aqui. A AMC IA foca em produzir o projeto. Com o token da API, o conector já lê a carteira e os clientes e sincroniza de volta o resultado da elaboração (criar o projeto, gravar nota técnica, valores e mover de estágio). Isso é complementar: a gestão continua no CaptaHub; daqui só lemos e devolvemos o resultado. Subcomandos em `docs/integracao-captahub-api.md`.

## Regras

- Credenciais só no `.env`. Mascare na exibição. Nunca ecoe o valor recebido.
- Português correto, sem travessão.
