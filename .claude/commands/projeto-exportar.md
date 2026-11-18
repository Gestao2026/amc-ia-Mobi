---
description: Exportar a proposta e o orçamento em arquivos prontos para submeter (Word, PDF e planilha).
---

# /projeto-exportar

Transforma a proposta e o orçamento (que estão em markdown) nos arquivos finais que o financiador aceita: Word editável, PDF e planilha. É o último passo antes de submeter.

## Passos

1. Leia `minhas-oscs/.ativa` e identifique o projeto. Se houver vários, pergunte qual.
2. **Gate.** Confira que existem `proposta.md` e `orcamento.md` no projeto. Se faltar algum, avise e oriente rodar `/projeto-escrever` ou `/projeto-orcamento` antes. Pode exportar só o que existir, mas avise o que está faltando.
3. Anuncie:
   ```
   🔍 Próximo passo: gerar a entrega final em Word, PDF e planilha. Tempo estimado: cerca de 30 segundos.
   ```
4. Rode `scripts/exportar-projeto.py {osc-slug} {edital-slug}`. O script gera, na pasta `entrega-final/` do projeto:
   - `proposta.doc` (abre e edita no Word ou Google Docs)
   - `proposta.pdf` (pronto para anexar)
   - `orcamento.xls` e `orcamento.csv` (abrem no Excel ou Google Sheets)
   - `orcamento.pdf`
   - `cotacoes.doc`, `cotacoes.pdf`, `cotacoes.xls` e `cotacoes.csv` (o quadro de cotações do CaptaBudget, se existir)
   - `checklist-anexos.doc`, `.pdf`, `.xls` e `.csv` (o checklist de anexos, se existir)
   - `elegibilidade`, `score`, `revisao` e `parecer-chefe`, cada um em `.doc` e `.pdf`, **marcados como uso interno, não anexar na submissão**
   - `declaracoes/`, com cada declaração gerada pelo agente de anexos em `.doc` e `.pdf`, sem capa nem rodapé, para assinar
   - `projeto-completo.pdf` (proposta, orçamento e todos os documentos acima em um arquivo só: é o dossiê de trabalho)

   **O `estrategia.md` nunca entra na exportação.** Nem solto, nem dentro do `projeto-completo.pdf`. Ele é documento interno de trabalho: traz leitura da concorrência, avaliação das fraquezas da própria organização e a conta de esforço contra retorno. Nada disso vai para o financiador. O mesmo vale para o `edital.md`, que é leitura interna. Os demais documentos de trabalho (parecer do chefe, revisão, elegibilidade e nota) entram por decisão da captadora em 10/09/2026, sempre marcados como uso interno.
   - versões `-impressao.html` para imprimir manualmente, se preferir
5. A seção interna "Notas do CaptaBuilder (não submeter)" é removida automaticamente da versão final.
6. Informe os caminhos absolutos dos arquivos gerados e qual usar conforme o edital:
   - Formulário em Word ou texto: use `proposta.doc`.
   - Anexo em PDF: use `proposta.pdf`. **O `projeto-completo.pdf` não é peça de submissão:** ele reúne documentos de uso interno (parecer do chefe, revisão, nota) e serve para a captadora e para o cliente.
   - Planilha de orçamento: use `orcamento.xls`.
   - Pesquisa de preços, quando o edital pedir: `cotacoes.pdf` ou `cotacoes.xls`. A cotação da web é referência de valor; se o edital exigir proposta assinada de fornecedor, ela entra à parte.
   - Declarações: os arquivos de `declaracoes/`, depois de assinados.

## Observações

- O PDF é gerado automaticamente se o Google Chrome ou o Microsoft Edge estiver instalado. Se não, abra o arquivo `-impressao.html` no navegador e use Imprimir, depois Salvar como PDF.
- Sempre confira o documento final antes de submeter. A formatação cobre A4, mas alguns editais exigem um modelo oficial próprio; nesse caso, cole o conteúdo do `.doc` no modelo do edital.

## Regras

- Português correto, sem travessão. Não mostre código, informe apenas os caminhos.
