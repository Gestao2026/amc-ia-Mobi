# 07 - Higiene de arquivos na cópia local da pasta _82

| Campo | Valor |
|---|---|
| Data | 2026-08-20 |
| Pasta afetada | `C:\Users\rosep\Desktop\_82 - Rosepaula Aparecida Andrade Rodrigues` |
| Tipo | Limpeza de arquivos. **Nenhum nome de pasta foi alterado** |
| Situação | Concluída |
| Autorizada por | Rosepaula: "3 faça a higiene" |
| Reversível | Sim, tudo que saiu está guardado com o caminho de origem |

---

## 1. Por que foi feito

Quatro problemas de arquivo atrapalhavam o trabalho e atrapalhariam mais ainda
numa sincronização com o Google Drive:

- **Pilha de versões de planilha.** Cinco arquivos `1 - Controle de Submissão_ (backup antes de...)` convivendo com o arquivo vivo, sem que o nome dissesse qual é o atual.
- **Emoji no nome de arquivo.** Quatro documentos de projeto. Emoji sincroniza, mas costuma quebrar em link compartilhado e em sistema de cliente.
- **Acento em duas codificações.** Três pares de arquivos com o mesmo nome na tela e o mesmo conteúdo, mas um deles gravado no padrão do Mac (acento como caractere separado) e outro no do Windows. O Windows os trata como arquivos distintos.
- **772 arquivos `desktop.ini`**, em 772 pastas. São configuração visual do Windows, sem valor de conteúdo, e subiriam para a nuvem como 772 itens.

## 2. Onde as coisas retiradas foram parar

**Fora da estrutura dos mentores, para não criar pasta nova lá dentro.** Tudo foi
para `C:\Users\rosep\Backups\pasta-82\_higiene-2026-08-20\`:

```
_higiene-2026-08-20\
├── higiene.csv           as 784 ações, com origem e destino
├── versoes-antigas\      as 5 planilhas antigas
├── duplicados-acento\    as 3 versões em codificação de Mac
└── desktop-ini\          os 772 desktop.ini, com o caminho de origem preservado
```

## 3. O que foi executado

**a) Cinco versões antigas de planilha, retiradas.** O arquivo vivo,
`1 - Controle de Submissão_.xlsx`, ficou onde estava.

**b) Quatro nomes com emoji, renomeados no lugar.** O arquivo não saiu da pasta.

| Antes | Depois |
|---|---|
| `🔥 MATRIZ DE VINCULAÇÃO FINANCEIRA.docx` | `MATRIZ DE VINCULAÇÃO FINANCEIRA.docx` |
| `🔥 PROJETO TRAJETÓRIAS FINAL.docx` | `PROJETO TRAJETÓRIAS FINAL.docx` |
| `🔥 PROJETO TRAJETÓRIAS ORÇAMENTOS.docx` | `PROJETO TRAJETÓRIAS ORÇAMENTOS.docx` |
| `🧩 ESTRUTURA DO PROJETO PRIVADOS DE LIBERDADE.docx` | `ESTRUTURA DO PROJETO PRIVADOS DE LIBERDADE.docx` |

Os três primeiros estão em `02 - CaptaDrive - E-Missão\02 - Editais\02 - Edital TJMG VEC\04 - Projeto`
e o quarto em `03 - Edital Fundo Brasil\04- Projeto`.

**c) Três duplicatas por codificação de acento, retiradas.** Antes de mover,
**o conteúdo dos dois arquivos de cada par foi comparado por hash MD5 e confirmado
idêntico**. A versão do Windows ficou na pasta, a do Mac foi para a quarentena.

- `_Alteração Estatutária Registrada E-missão.pdf`, em E-Missão, `03 - Atas e Constituição`
- `Orçamento - Santo Escritório_Temporada 01.xlsx`, em Bandeja Films, `01 - Documentos`
- `Orçamento - Santo Escritório_Temporada 02.xlsx`, na mesma pasta

**d) Os 772 `desktop.ini`, retirados.** Todos os 772, sem nenhuma falha. As
pastas perdem ícone personalizado, se tiverem. O conteúdo não é afetado.

## 4. Estado antes e depois

| Medida | Antes | Depois |
|---|---|---|
| Arquivos na pasta | 3.492 | **2.712** |
| Volume | 5,40 GB | 5,40 GB |
| Arquivos em quarentena | 0 | **780** |
| Soma (confere) | 3.492 | **3.492** |
| `desktop.ini` restantes | 772 | **0** |
| Nomes com emoji | 4 | **0** |
| Planilhas `backup antes` | 5 | **0** |
| Pares por codificação de acento | 3 | **0** |
| Maior caminho relativo | 249 | 249 |

O volume não muda porque o que saiu pesa 80 KB de `desktop.ini` mais alguns MB de
planilha. O ganho é de clareza, não de espaço.

## 5. Como reverter

O arquivo `higiene.csv` tem as 784 ações com o caminho de origem e o de destino.
Para desfazer, copiar de volta cada arquivo da coluna `Para` para o caminho da
coluna `De`, dentro da pasta `_82`.

Para os quatro renomeados por emoji, o nome antigo está na coluna `De`.

## 6. O que ficou pendente

- **Nada disso foi aplicado na pasta do Drive da dona.** Lá continuam os 1.226 `desktop.ini`, os arquivos com emoji e as duplicatas por acento. Mexer neles exige o aval da dona.
- `Conferencia de links 14-08-2026.xlsx` continua em `01 - Planejamento de Submissões`. Não é backup de versão, é um arquivo de trabalho, e por isso não foi tocado.

## 7. Regras que passam a valer

- **Um nome, um arquivo vivo.** Nada de `V2`, `FINAL`, `REV1` ou `backup antes de`. Ao melhorar, sobrescreve, e a versão anterior vai para a quarentena datada em `C:\Users\rosep\Backups\`.
- **Nada de emoji em nome de arquivo.** Quebra em link compartilhado e em sistema de cliente.
- **Duplicata se confirma por hash antes de sair do lugar.** Nome igual e tamanho igual não bastam.
- **O que sai de uma pasta de trabalho vai para quarentena com o caminho de origem preservado, nunca para a lixeira.**
- Quando a estrutura de pastas é intocável, o que sai vai para **fora** dela, e não para uma pasta nova criada dentro.
