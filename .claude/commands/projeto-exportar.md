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
   - `projeto-completo.pdf` (proposta, orçamento, parecer e nota em um arquivo)
   - versões `-impressao.html` para imprimir manualmente, se preferir
5. A seção interna "Notas do CaptaBuilder (não submeter)" é removida automaticamente da versão final.
6. Informe os caminhos absolutos dos arquivos gerados e qual usar conforme o edital:
   - Formulário em Word ou texto: use `proposta.doc`.
   - Anexo em PDF: use `proposta.pdf` ou `projeto-completo.pdf`.
   - Planilha de orçamento: use `orcamento.xls`.

## Observações

- O PDF é gerado automaticamente se o Google Chrome estiver instalado. Se não, abra o arquivo `-impressao.html` no navegador e use Imprimir, depois Salvar como PDF.
- Sempre confira o documento final antes de submeter. A formatação cobre A4, mas alguns editais exigem um modelo oficial próprio; nesse caso, cole o conteúdo do `.doc` no modelo do edital.

## Regras

- Português correto, sem travessão. Não mostre código, informe apenas os caminhos.
