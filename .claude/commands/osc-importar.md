---
description: Importar uma OSC da carteira do CaptaHub para o perfil local e defini-la como ativa.
---

# /osc-importar

Traz uma organização que já existe na carteira do CaptaHub para dentro da AMC IA, criando o perfil local e definindo-a como ativa. Evita recadastrar do zero uma OSC que já está no CaptaHub.

## Passo 0. Contexto

Verifique a conexão com o CaptaHub (`CAPTAHUB_API_TOKEN` no `.env`). Se não houver token, oriente `/captahub-conectar` ou, se o captador preferir cadastrar do zero, `/osc-nova`.

## Passo 1. Listar a carteira

Rode `python3 scripts/captahub-api.py clientes --all` e apresente a lista numerada das OSCs do dono do token: nome, UF, município e área temática. Se o captador já disse qual quer (nome ou id), pule direto para o Passo 2.

## Passo 2. Escolher e buscar a OSC

Após a escolha, rode `python3 scripts/captahub-api.py cliente --id {id}` para trazer o registro completo. Leia o bloco `=== CLIENTE ===` (JSON) com todos os campos.

## Passo 3. Mapear para o perfil local

Crie a pasta `minhas-oscs/{slug}/` (slug em kebab-case do nome, ex: `instituto-crianca-feliz`) e a subpasta `projetos/`. Gere o `perfil-osc.md` segundo o modelo `minhas-oscs/MODELO-perfil-osc.md`, preenchendo a partir dos campos do CaptaHub:

| Campo do CaptaHub | Campo no perfil |
|---|---|
| `nome` | Nome da organização |
| `sigla` | Sigla / nome fantasia |
| `cnpj` | CNPJ |
| `natureza_juridica` | Natureza jurídica |
| `fundacao` | Data de fundação |
| `municipio`, `uf` | Município e UF |
| `territorios` | Territórios de atuação |
| `areas_tematicas` | Área(s) temática(s) |
| `missao` | Missão |
| `site`, `email`, `telefone` | Contato |
| `status_documental` (booleanos) | Situação documental (checklist do CaptaDoc) |
| `historico_aprovacoes` | Projetos já aprovados |

Para cada campo que vier `null` ou vazio no CaptaHub, marque no perfil como "a confirmar com a OSC" em vez de inventar. Guarde o `id` do cliente do CaptaHub no perfil (linha "ID CaptaHub: {id}"), para depois sincronizar projetos de volta na carteira.

## Passo 4. Confirmação e salvamento

Resuma o que foi importado e o que ficou "a confirmar". Após o OK:
1. Salve `minhas-oscs/{slug}/perfil-osc.md`.
2. Grave o slug em `minhas-oscs/.ativa`.
3. Informe o caminho do arquivo.

## Passo 5. Próximo passo

Sugira `/osc-perfil` para completar os campos que ficaram "a confirmar", ou `/edital-minerar` para já buscar editais alinhados (puxando do CaptaHub ao vivo).

## Regras

- Não invente dado que não veio do CaptaHub. Campo vazio vira "a confirmar com a OSC".
- O perfil local é mais rico que o registro do CaptaHub; o captador completa o resto pelo `/osc-perfil`.
- Português correto, sem travessão.
