# 12 - Primeira carga do backup da _82, exclusões e uma correção

| Campo | Valor |
|---|---|
| Data | 2026-08-21, a partir das 18h |
| Onde | `_82` no Google Drive, `Desktop\MOBI`, `C:\Users\rosep\Backups` |
| Tipo | Backup, exclusão de redundância e correção de um registro anterior |
| Situação | Concluída |
| Autorizada por | Rosepaula: "pode", ao plano do Grupo A |
| Reversível | O backup sim. As exclusões não |

---

## 1. A primeira carga do backup da pasta _82

O bloco suspenso em 21/08 foi religado com o aval da captadora, às 18h combinadas.

| Medida | Resultado |
|---|---|
| Arquivos copiados | **6.018 de 6.021** |
| Volume | **10,43 GB** |
| Tempo | 27 minutos e 30 segundos |
| Velocidade | 68 MB por segundo |
| Falhas | 3 |

**As 3 falhas são os arquivos `.gdoc`**, que são ponteiros para Google Docs e não
têm conteúdo próprio. Somam 594 bytes e o robocopy não consegue copiá-los, o que
é esperado. São o `EDITAL DE CONVOCAÇÃO.gdoc` e o `Lista de presença AGE
26_02_2026`, de Levanta e Brilha, e o `Projeto_Elas_no_Esporte`, de Ponto
Cultural.

O robocopy retornou código 9, que é 8 mais 1: houve cópia com sucesso e houve
falha. Não é erro de configuração.

**A partir de agora a pasta `_82` tem cópia diária sob o controle da captadora,
em `C:\Users\rosep\Backups\pasta-82\atual`.** Era a última lacuna de proteção.

## 2. Correção da estruturação 09: os desktop.ini voltaram

A [estruturação 09](2026-08-20-09-exclusoes-e-desktop-ini-do-drive.md) registrou
que os 1.226 `desktop.ini` tinham sido retirados da pasta do Drive e que
restavam zero. **Isso não se sustentou.**

Ao conferir hoje, os 1.226 estavam de volta, todos **criados em 21/08/2026 às
17h48**. O Google Drive para Desktop os recria sozinho.

Investigando mais fundo, uma consulta direta à nuvem mostrou o que estava
acontecendo: **esses arquivos nunca existiram na nuvem.** A pasta
`3- DOCUMENTOS INSTITUCIONAIS ANTERIORES` tem, no Google Drive, exatamente dois
itens, os dois documentos. Nenhum `desktop.ini`.

Ou seja:

- Os `desktop.ini` são **artefato local** do Google Drive para Desktop, usados para o ícone da pasta no Windows.
- Eles **não sobem para a nuvem** e nunca subiriam.
- Apagá-los é inútil: o Drive os recria na próxima sincronização.

**O que a estruturação 09 dizia de errado:** que eles "subiriam para a nuvem como
1.226 itens". Não subiriam. A retirada foi inofensiva, mas também foi inócua.

**A correção prática:** em vez de brigar com eles, o backup passa a ignorá-los. O
`scripts/backup-diario.bat` ganhou `/XF desktop.ini *.gdoc *.gsheet *.gslides` no
robocopy da pasta `_82`. Os 1.226 que tinham entrado na primeira carga foram
retirados do backup.

| Backup da `_82` | |
|---|---|
| Arquivos | **4.792** |
| Volume | **10,43 GB** |
| `desktop.ini` | 0 |

## 3. Exclusões de redundância

| Item | O que | Arquivos | Espaço |
|---|---|---|---|
| A4 | Instaladores de programa em `MOBI\90-BACKUPS-BRUTOS` | 20 | **1,72 GB** |
| A5 | `MOBI\_DUPLICADOS` inteira | 1.626 | **1,05 GB** |

Os instaladores eram Power BI, Antigravity IDE, Chrome, C6 Bank, Java, Git, Node,
Office, Teams, WhatsApp e o gerenciador de Python. Todos baixáveis de novo.

A `_DUPLICADOS` guardava cópias já confirmadas byte a byte na
[estruturação 01](2026-08-20-01-pasta-mobi.md).

Registro em `C:\Users\rosep\Backups\excluidos-2026-08-21.csv`, com nome, tamanho
e caminho de origem de cada um.

## 4. Ajuste de tratamento nos registros anteriores

Os registros de 20/08 foram escritos tratando quem é dona da pasta `_82` no
masculino. Sete arquivos foram corrigidos para "a dona" e "a mentora".

## 5. O que ficou pendente

- **Avisar a mentora** de três coisas feitas na pasta dela: o `.gdoc` renomeado, as duas planilhas atualizadas e os `desktop.ini` retirados, que de todo modo voltaram sozinhos.
- **A pasta continua aberta por link público.** Ver [estruturação 10](2026-08-21-10-achado-pasta-82-com-link-publico.md). Nada mudou até 21/08 às 18h.
- **A unidade `M:` ainda não passou por um login real.** Hoje ela caiu entre duas verificações e precisou ser remontada à mão. A confirmação de que a inicialização funciona só vem no próximo reinício da máquina.

## 6. Regras que passam a valer

- **Não brigar com arquivo que o sistema recria.** `desktop.ini` do Google Drive volta sempre. Ignorar no backup resolve; apagar não.
- **Antes de afirmar que um arquivo "vai para a nuvem", conferir na nuvem.** A consulta direta desmentiu a suposição.
- Código 9 do robocopy não é falha de configuração: é 8 mais 1, cópia com sucesso e alguma falha. Ler o log antes de concluir qualquer coisa.
- Arquivo de ponteiro do Google (`.gdoc`, `.gsheet`, `.gslides`) não entra em backup. Não tem conteúdo próprio.
- **Registro errado se corrige com um registro novo, não apagando o antigo.** A estruturação 09 continua lá, e esta explica onde ela errou.
