# 16 - Os 4 logos repetidos na pasta APLICAVEIS são intencionais

| Campo | Valor |
|---|---|
| Data | 2026-08-23 |
| Pasta afetada | `C:\Users\rosep\OneDrive - Organizacao Multidisciplinar De Voluntariado E-missao\Documentos\9. MOBILIZANDO MKT LOGO` |
| Tipo | Diagnóstico (decisão de não excluir) |
| Situação | Concluída. Nenhum arquivo foi alterado |
| Autorizada por | A captadora, em 23/08/2026, ao pedir a verificação e aprovar o registro |
| Reversível | Não se aplica. Nada foi movido, renomeado ou excluído |

---

## 1. Por que foi feito

Na triagem de duplicatas da pasta `9. MOBILIZANDO MKT LOGO`, o Nível 3 apontava 4 imagens de logo que existem ao mesmo tempo em `APLICAVEIS\LOGO APLICAVÉIS\` e na biblioteca `ARQUIVOS LOGO MOBILIZANDO_V2\Logo completa\JPG\`. O ganho previsto com a exclusão era de 0,4 MB.

A dúvida concreta: a repetição é descuido ou é uso. Antes de apagar, a captadora pediu a verificação.

## 2. O que foi decidido, e por quem

- **Não excluir os 4 logos.** Decisão da captadora, confirmada pela verificação por hash.
- Descartada a exclusão automática por duplicidade: 0,42 MB não paga a perda da pasta de acesso rápido.
- Descartada também a ideia de substituir os arquivos por atalhos para a biblioteca. Atalho quebra ao anexar em formulário de edital e ao arrastar para o Canva ou para o WhatsApp, que é justamente o uso da pasta.
- Registrado que `Simbolo Roxo.jpg` foi renomeado de propósito e o nome local é melhor que o da biblioteca.

## 3. Estado antes

| Medida | Valor |
|---|---|
| Arquivos em `APLICAVEIS` | 22 (em 1 subpasta) |
| Volume de `APLICAVEIS` | 5,49 MB |
| Arquivos na biblioteca `ARQUIVOS LOGO MOBILIZANDO_V2` | 125 (em 77 subpastas) |
| Volume da biblioteca | 135,88 MB |
| JPG na árvore `Logo completa\JPG` | 18 |
| Duplicatas apontadas pelo Nível 3 | 4 arquivos, 0,4 MB |

## 4. O que foi executado

1. Localização das duas pastas. Elas não estão na Área de Trabalho nem na MOBI: vivem no `OneDrive - Organizacao Multidisciplinar De Voluntariado E-missao\Documentos`.
2. Cálculo do hash MD5 dos 22 arquivos de `APLICAVEIS` e dos 125 arquivos da biblioteca V2, comparando por conteúdo e não por nome.
3. Confirmação das 4 duplicatas e do total exato: 443.374 bytes, 0,42 MB.
4. Contagem de quantos arquivos de `APLICAVEIS` são exclusivos dela: 18 dos 22.
5. Nenhuma exclusão, nenhuma movimentação.

**As 4 duplicatas confirmadas byte a byte**

| Arquivo em `APLICAVEIS\LOGO APLICAVÉIS\` | Bytes | Cópia idêntica em `ARQUIVOS LOGO MOBILIZANDO_V2\Logo completa\JPG\` |
|---|---|---|
| Logo fundo escuro (versão 1)-1.jpg | 102.011 | `Versão 1\Azul\Logo fundo escuro (versão 1)-1.jpg` |
| Logo fundo escuro (versão 2)-1.jpg | 112.383 | `Versão 2\Azul\Logo fundo escuro (versão 2)-1.jpg` |
| Logo fundo escuro (versão 2).jpg | 94.684 | `Versão 2\Verde\Logo fundo escuro (versão 2).jpg` |
| Simbolo Roxo.jpg | 134.296 | `Símbolo\Roxo\Símbolo fundo escuro-2.jpg` |

## 5. Estado depois

| Medida | Antes | Depois |
|---|---|---|
| Arquivos em `APLICAVEIS` | 22 | 22 |
| Volume de `APLICAVEIS` | 5,49 MB | 5,49 MB |
| Duplicatas do Nível 3 em aberto | 4, sem veredito | 4, classificadas como intencionais |

## 6. Onde está a rastreabilidade

| Arquivo | O que registra |
|---|---|
| Este registro | A verificação por hash, os 4 pares e a decisão de manter |
| `README.md` deste diário | Linha 16 do índice |

## 7. Backup feito antes

Não se aplica. A verificação foi somente de leitura (cálculo de hash). Nenhum arquivo foi tocado, então não havia o que preservar.

## 8. Como reverter

Não há o que reverter. Se um dia a decisão mudar, os 4 arquivos de `APLICAVEIS\LOGO APLICAVÉIS\` podem ser excluídos com segurança, porque a cópia idêntica na biblioteca V2 está confirmada por hash. O que se perde nesse caso é a conveniência da pasta e o nome "Simbolo Roxo", não o arquivo.

## 9. O que ficou pendente

- Nada neste item. O Nível 3 está fechado.
- Continua fora deste registro o resto da triagem da pasta `9. MOBILIZANDO MKT LOGO`, que tem 135,88 MB só na biblioteca de logo.

## 10. Regras que passam a valer

- **Pasta de acesso rápido não é duplicata.** Quando uma pasta reúne poucos arquivos escolhidos de uma árvore grande, a repetição é a função dela. Antes de apontar duplicidade, medir quantos arquivos daquela pasta são exclusivos: em `APLICAVEIS` são 18 de 22, o que a define como seleção curada e não como cópia.
- **Ganho abaixo de 1 MB não justifica exclusão** quando o arquivo está em uso no dia a dia. O custo de reencontrar o arquivo na árvore completa é maior que o espaço economizado.
- **Nome diferente é informação.** `Simbolo Roxo.jpg` diz a cor. `Símbolo fundo escuro-2.jpg`, o nome de origem, não diz. Renomear na pasta de trabalho é prática legítima e a duplicata que carrega o nome melhor não se apaga.
- **A pasta de marca da Mobilizando fica no OneDrive da E-missão**, em `Documentos\9. MOBILIZANDO MKT LOGO`, e não na MOBI da Área de Trabalho. Procurar ali antes de dar por perdido.
