# 09 - Exclusões de redundância e retirada dos desktop.ini do Drive

> ⚠️ **Corrigido em 21/08/2026.** A parte dos `desktop.ini` deste registro estava
> errada: eles voltaram sozinhos, porque o Google Drive os recria, e nunca
> existiram na nuvem. Ver a
> [estruturação 12](2026-08-21-12-primeira-carga-e-exclusoes.md).

| Campo | Valor |
|---|---|
| Data | 2026-08-20 |
| Onde | `Desktop\MOBI`, `C:\Users\rosep\Backups` e a pasta `_82` no Drive da mentora |
| Tipo | Exclusão de redundância |
| Situação | Concluída |
| Autorizada por | Rosepaula, item por item, a partir de uma lista com números apresentada antes |
| Reversível | Parcialmente. Ver item 5 |

---

## 1. Por que foi feito

Depois das estruturações anteriores, o mesmo conteúdo existia em até quatro
lugares ao mesmo tempo. A lista de candidatos foi apresentada em três grupos, por
grau de risco, e a captadora escolheu quatro itens.

## 2. Verificação de segurança feita antes

Como a quarentena da higiene e o backup datado saíram juntos, foi conferido que
nada ficaria sem cópia. Tudo que estava neles continua na pasta do Drive:

| O que | Existe no Drive |
|---|---|
| 5 planilhas `backup antes de...` | sim |
| 3 duplicatas por codificação de acento | sim, 6 ocorrências |
| 4 arquivos com emoji no nome | sim, 6 ocorrências |
| Cópia local do `_82` | intacta, 2.712 arquivos |

## 3. O que foi excluído

| Item | O que | Arquivos | Espaço |
|---|---|---|---|
| Grupo 1, item 3 | `MOBI\90-BACKUPS-BRUTOS\82 - Rosepaula...-Backup.zip` | 1 | **1,52 GB** |
| Grupo 1, item 4 | `Backups\pasta-82\_higiene-2026-08-20\` | 781 | 0,01 GB |
| Grupo 2, item 8 | `Backups\pasta-82\2026-08-20\` | 3.490 | **5,40 GB** |

Antes de apagar a quarentena, o registro `higiene.csv` foi preservado em
`C:\Users\rosep\Backups\pasta-82\higiene-2026-08-20.csv`. Ele guarda as 784 ações
da higiene, com origem e destino de cada arquivo.

**Espaço em disco recuperado: de 259,6 GB livres para 266,6 GB, ou seja 7 GB.**

## 4. Os desktop.ini da pasta do Drive

| | |
|---|---|
| Encontrados | 1.226 |
| Retirados | **1.226** |
| Falhas | 0 |
| Restantes na pasta do Drive | **0** |

**Não foram apagados, foram movidos** para
`C:\Users\rosep\Backups\pasta-82\_desktop-ini-do-drive-2026-08-20\`, preservando o
caminho de origem, com um `desktop-ini-retirados.csv` listando cada um.

A operação foi feita pela unidade `M:`, que é a mesma pasta do Drive com caminho
curto. **Isso alterou a pasta da mentora**, e ela precisa ser avisada. São
arquivos de configuração visual do Windows, sem conteúdo, mas a pasta é dela.

| | Antes | Depois |
|---|---|---|
| Arquivos na pasta `_82` do Drive | 6.023 | **4.795** |
| Volume | 10,43 GB | 10,43 GB |

O volume não muda porque os 1.226 arquivos somam cerca de 300 KB.

## 5. Como reverter

| O que | Dá para voltar? |
|---|---|
| Os 1.226 `desktop.ini` do Drive | **Sim.** Copiar de volta pelo `desktop-ini-retirados.csv` |
| O zip de 1,52 GB | Não. Era um backup antigo da pasta `_82`, que hoje tem cópia diária |
| A quarentena da higiene | Não diretamente, mas todo o conteúdo dela continua na pasta do Drive |
| O backup datado de 5,40 GB | Não. Era cópia da pasta local, que está intacta |

## 6. O que ficou pendente

- **Avisar a mentora** que os 1.226 `desktop.ini` saíram da pasta dela. As pastas perdem ícone personalizado, se tiverem.
- **A primeira carga do backup diário da pasta do Drive ainda não rodou.** Até ela rodar, o conteúdo que só existe no Drive não tem cópia sob controle da captadora.

## 7. Regras que passam a valer

- **Antes de excluir duas coisas parecidas de uma vez, conferir que a terceira cópia existe.** Foi o que evitou perder as planilhas antigas aqui.
- Registro de rastreabilidade nunca é apagado junto com o que ele registra. O `higiene.csv` saiu da pasta antes.
- Em pasta de terceiro, **mover para quarentena, nunca apagar**, mesmo quando o arquivo não tem valor de conteúdo.
- Exclusão só acontece a partir de uma lista com números, aprovada item por item.
