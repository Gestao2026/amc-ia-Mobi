# 15 - Consolidação dos editais entre a MOBI e a _82

| Campo | Valor |
|---|---|
| Data | 2026-08-23 |
| Pasta afetada | `Desktop\MOBI\03-EDITAIS` e `Desktop\_82 ...\04 - Controle de Submissão_` |
| Tipo | Reorganização |
| Situação | Concluída, com uma pendência de decisão |
| Autorizada por | A captadora, nestes termos: a `_82\04 - Controle de Submissão_` é a pasta verdadeira e de confiança; o que estiver realmente duplicado pode sair; o que existir só na MOBI vai para uma pasta de avaliação dentro da _82 |
| Reversível | Sim. Os dois CSVs em `MOBI\_LOGS` trazem origem e destino de cada arquivo |

---

## 1. Por que foi feito

Os editais viviam em dois lugares com o mesmo esqueleto de subpastas e ninguém
sabia qual valia. A `MOBI\03-EDITAIS` tinha 182 arquivos e 506,0 MB; a
`_82\04 - Controle de Submissão_` tinha 166 arquivos e 145,1 MB. Havia ainda uma
terceira casca na Área de Trabalho, `CONTROLE EDITAIS`, com a subpasta
`1. EDITAIS` vazia, que foi o que fez a captadora achar que os editais tinham
sumido.

## 2. O que foi decidido, e por quem

- A `_82\04 - Controle de Submissão_` é a fonte da verdade dos editais. Decisão da captadora.
- Comparação por hash SHA-256 do conteúdo, não por nome. Nome igual não prova arquivo igual.
- Duplicado real vai para `MOBI\_DUPLICADOS`, o mesmo mecanismo da estruturação 01, em vez de exclusão direta. Nada é apagado do disco enquanto a captadora não conferir.
- Comparação restrita a `MOBI\03-EDITAIS`. As outras 12 categorias da MOBI são financeiro, marketing e formação, sem relação com submissão de edital.
- As 6 gravações de tela do portal Transferegov ficaram retidas na MOBI, fora da operação. Motivo no item 9.

## 3. Estado antes

| Medida | Valor |
|---|---|
| Arquivos na `_82\04` | 166 (164 conteúdos distintos), 145,1 MB |
| Arquivos na `MOBI\03-EDITAIS` | 182 (182 conteúdos distintos), 506,0 MB |
| Idênticos nas duas | 80 arquivos, 53,7 MB |
| Só na MOBI | 102 arquivos, 452,3 MB |
| Só na _82 | 84 arquivos |

## 4. O que foi executado

1. Indexação das duas pastas por SHA-256, 348 arquivos lidos, zero erros de leitura.
2. Os 80 arquivos da MOBI com conteúdo idêntico na _82 foram movidos para `MOBI\_DUPLICADOS\vs-82-2026-08-23`, preservando o caminho de origem.
3. Os 96 arquivos exclusivos da MOBI (102 menos as 6 gravações) foram movidos para `_82 ...\04 - Controle de Submissão_\07 - AVALIAR MOBI`.
4. Os nomes de primeiro nível foram encurtados no destino (`copias-de-submissoes` virou `copias`, `anexos-e-formularios` virou `anexos`) para não estourar o limite de caminho do Windows. O destino mais longo ficou em 255 caracteres.
5. As pastas que ficaram vazias na `MOBI\03-EDITAIS` foram removidas.

## 5. Estado depois

| Medida | Antes | Depois |
|---|---|---|
| Arquivos na `_82\04` | 166 | 262 (166 originais mais 96 a avaliar) |
| Arquivos na `MOBI\03-EDITAIS` | 182 | 6 (só as gravações de tela) |
| Arquivos acima de 259 caracteres | 0 | 0 |
| Cópias duplicadas em circulação | 80 | 0 |

## 6. Onde está a rastreabilidade

| Arquivo | O que registra |
|---|---|
| `MOBI\_LOGS\2026-08-23-duplicados-vs-82.csv` | Os 80 duplicados: origem e destino |
| `MOBI\_LOGS\2026-08-23-avaliar-mobi.csv` | Os 96 movidos para avaliação: origem e destino |
| `MOBI\_LOGS\2026-08-23-comparacao-hash.json` | O resultado bruto da comparação, com hash de cada arquivo |

## 7. Backup feito antes

| Origem | Destino | Conferido |
|---|---|---|
| Nenhum backup novo | A `_82` não foi alterada, só recebeu conteúdo. Os 80 duplicados continuam no disco, em `_DUPLICADOS` | Sim. A `_82\04` segue com os mesmos 166 arquivos originais |

## 8. Como reverter

Abrir o CSV correspondente em `MOBI\_LOGS`, que traz a coluna Origem e a coluna
Destino de cada arquivo, e mover de volta. Para desfazer só os duplicados, basta
mover o conteúdo de `MOBI\_DUPLICADOS\vs-82-2026-08-23` de volta para
`MOBI\03-EDITAIS`, mantendo a estrutura de subpastas que está lá dentro.

## 9. O que ficou pendente

- **As 6 gravações de tela do portal Transferegov**, 385 MB em `.mp4`, seguem em `MOBI\03-EDITAIS\transferegov`. Não foram movidas porque a `_82` está com link público em aberto (estruturação 10) e gravação de portal com sessão logada pode expor dado de acesso. Decisão da captadora: mover assim que o link for fechado, guardar em outro lugar, ou descartar.
- **Os 80 duplicados** estão em `_DUPLICADOS`, não foram apagados do disco. Aguardam a conferência da captadora para exclusão definitiva.
- **A pasta `Desktop\CONTROLE EDITAIS`**, com 17 arquivos e a `1. EDITAIS` vazia, não foi tocada. Falta decidir se some ou se vira a pasta viva de entrada.

## 10. Regras que passam a valer

- Edital novo entra pela `_82\04 - Controle de Submissão_`. É a única fonte da verdade de editais fora do CaptaHub.
- A `MOBI\03-EDITAIS` deixa de receber edital. É arquivo morto.
- Comparação entre pastas se faz por hash de conteúdo, nunca por nome de arquivo.
