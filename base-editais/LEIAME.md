# Base de Editais. Cache do CaptaHub

> Esta pasta é um cache local dos editais que vêm do CaptaHub (a fonte da verdade). O comando `/edital-minerar` atualiza este cache puxando do CaptaHub (`scripts/captahub-editais.py`) e depois filtra pelo perfil da OSC. Sem conexão com o CaptaHub, o sistema usa o último cache baixado. Conecte com `/captahub-conectar`.

## Arquivos

| Arquivo | Uso |
|---|---|
| `editais-abertos.json` | Dados completos (todos os campos) |
| `editais-index.json` | Índice leve para busca rápida (9 campos) |
| `por-escopo/Municipal.json` | Editais municipais |
| `por-escopo/Estadual.json` | Editais estaduais |
| `por-escopo/Nacional.json` | Editais nacionais e internacionais |

## Estrutura de cada edital

```json
{
  "id": "uuid",
  "title": "Nome do edital",
  "institution": "Órgão responsável",
  "category": "Edital | Chamamento | etc.",
  "scope": "Municipal | Estadual | Nacional",
  "value": 100000,
  "deadline": "2026-06-30",
  "is_continuous": false,
  "url": "https://...",
  "description": "Descrição resumida"
}
```

## Como o sistema busca

- **Por escopo:** abre o arquivo de `por-escopo/`.
- **Por palavra-chave:** varre `editais-abertos.json`.
- **Por prazo, valor ou categoria:** usa o índice leve `editais-index.json`.

O comando `/edital-minerar` cruza esses dados com o perfil da OSC ativa e devolve uma lista priorizada por aderência, valor e prazo. O script `scripts/minerar-editais.py` faz a filtragem.

## Atualizar

A base é um retrato do momento da exportação. Para refazer a busca e regenerar os arquivos, use `/configurar`. Editais com prazo vencido devem ser descartados na mineração (o script compara `deadline` com a data atual).
