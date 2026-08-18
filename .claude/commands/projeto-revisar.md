---
description: Revisão final do projeto antes da submissão (completude, coerência, conformidade e português).
---

# /projeto-revisar

Faz a última checagem antes de submeter. Aciona o agente `revisor-proposta`.

## Passos

1. Leia `minhas-oscs/.ativa` e identifique o projeto. Confira que existem `proposta.md` e `orcamento.md`.
2. Anuncie:
   ```
   🔍 Próximo passo: revisão final do projeto antes da submissão. Tempo estimado: cerca de 60 segundos.
   ```
3. Acione o agente `revisor-proposta`. Ele aplica os blocos A (completude), B (coerência interna), C (conformidade com o edital, teto, prazo) e D (português, travessão).
4. Apresente o relatório: itens já corrigidos, itens que exigem decisão do captador, e o veredito PRONTO PARA SUBMETER ou AJUSTAR ANTES.
5. Se PRONTO, lembre o captador da forma de submissão indicada no `edital.md` (plataforma, anexos, prazo), atualize o `estado.md` para "pronto para submeter" e sugira `/projeto-exportar` para gerar os arquivos finais em Word, PDF e planilha.

## Regras

- Não altere conteúdo que exige decisão sem perguntar. Corrija só português e formatação.
- Português correto, sem travessão.
