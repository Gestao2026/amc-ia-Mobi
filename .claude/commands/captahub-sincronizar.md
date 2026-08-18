---
description: Reconciliar a carteira e o pipeline com o CaptaHub nos dois sentidos (puxar atualizações e subir o que está só local).
---

# /captahub-sincronizar

Coloca a AMC IA e o CaptaHub em dia, nos dois sentidos. Roda a sincronização bidirecional (ver a regra no CLAUDE.md) de uma vez, em vez de esperar cada etapa. Útil ao abrir a sessão, ao terminar uma etapa importante, ou quando o captador quer garantir que a carteira está espelhada.

## Passo 0. Contexto

Verifique a conexão (`CAPTAHUB_API_TOKEN` no `.env`). Sem token, oriente `/captahub-conectar` e pare. Anuncie: "🔍 Próximo passo: sincronizar a carteira e o projeto atual com o CaptaHub (cerca de 30 segundos)."

## Passo 1. Puxar do CaptaHub (CaptaHub para a AMC IA)

1. `python3 scripts/captahub-api.py clientes --all` para a carteira de OSCs.
2. `python3 scripts/captahub-editais.py` para atualizar o cache de editais (mostra os novos por id).

## Passo 2. Cruzar carteira local x CaptaHub

Para cada OSC, case por `ID CaptaHub` no `perfil-osc.md` (na falta, por nome) e classifique:
- **no CaptaHub + local:** em dia.
- **só no CaptaHub:** existe lá, não tem perfil aqui (importável com `/osc-importar`).
- **só local:** tem perfil aqui, não está na carteira.

## Passo 3. Subir o que está só local (AMC IA para o CaptaHub)

Com idempotência (nunca duplicar, sempre conferir o id antes de criar):
1. **OSC só local:** crie o cliente no CaptaHub (`cliente-criar` com os campos do perfil) e grave o `id` retornado no `perfil-osc.md`.
2. **Projeto da OSC ativa:** para cada projeto em `projetos/{edital}/`, se ainda não tem `ID CaptaHub projeto` no `estado.md`, crie (`projeto-criar --nome --cliente-id --edital-id`) e grave o id. Depois faça o PATCH dos campos que já existem localmente:
   - valor do orçamento (`orcamento.md`) para `--valor-solicitado`;
   - nota e chance do `score.md` para `--nota-tecnica` e `--chance-aprovacao`;
   - etapa atual para `--status` (um dos 11 estágios);
   - data de submissão para `--data-submissao`, se já submetido.

## Passo 4. Relatório

Mostre um resumo em tabela: o que foi puxado (OSCs e editais novos), o que foi criado no CaptaHub, o que foi atualizado, e o que ficou pendente (ex: API falhou em um item). Confirme em linguagem de captador, sem detalhe técnico.

## Regras

- Idempotência: confira o id antes de criar. Nunca duplique OSC nem projeto.
- A identidade é o id, nunca a URL nem o título.
- `status_documental` no PATCH substitui o objeto inteiro: mande o checklist completo.
- Se a API falhar em algo, não trave: liste como pendente e siga.
- Português correto, sem travessão.
