# 20 - Desligamento das sincronizações entre as cópias da _82

| Campo | Valor |
|---|---|
| Data | 2026-08-26 |
| Pasta afetada | `scripts/` do projeto. Nenhuma pasta de documento foi tocada |
| Tipo | Desativação de automação |
| Situação | Concluída |
| Autorizada por | A captadora, no pedido de parar as sincronizações da `_82` entre as cópias |
| Reversível | Sim, por completo. Ver item 8 |

---

## 1. Por que foi feito

A captadora abriu a `06 - Clientes` da `_82` e concluiu que a estrutura tinha sido
bagunçada de novo, depois de ter corrigido as 21 pastas de cliente à mão na madrugada
de 25/08.

A investigação mostrou que **nada tinha sido alterado**. A `06 - Clientes` do Drive não
teve nenhuma pasta nem nenhum arquivo modificado desde 25/08, o que foi confirmado por
dois caminhos independentes: a API do Google, que responde pelo servidor, e a leitura
do disco pela unidade `G:`.

O que existe são **três cópias da `_82` em estados diferentes**, e a confusão vem de
olhar a errada. O risco real não era o que já tinha acontecido, era o que estava
prestes a acontecer na primeira vez que alguém rodasse o sincronizador.

## 2. O que foi decidido, e por quem

Decisão da captadora: **parar as sincronizações da `_82` entre as cópias.**

Descartado, por escolha de quem escreve este registro e sinalizado a ela: desligar
também o bloco 2 do backup diário, que copia a `_82` do Drive para
`C:\Users\rosep\Backups\pasta-82\atual`. Ele é leitura de mão única para um cofre, não
mexe em nenhuma das três cópias de trabalho, e é a única proteção que existe hoje
contra o dono da pasta apagar algo ou revogar o acesso. Fica ligado até ela dizer o
contrário.

## 3. Estado antes

As três cópias, no dia 26/08/2026:

| Cópia | Caminho | Estado |
|---|---|---|
| Drive, a viva | `G:\.shortcut-targets-by-id\1YxXksuP6SHlVKA4bT5gaC0WG4Wy4OXej\_82 ...`, também `M:` | **Corrigida.** 21 clientes numerados de 01 a 21, sem número repetido, mais `_Outros Modelos`. Todos com `01 - Gestão Documental` e `02 - Editais` |
| Área de Trabalho | `C:\Users\rosep\Desktop\_82 ...` | **Anterior à correção.** 18 clientes, com dois 08, dois 09, dois 11 e dois 12, faltando do 14 ao 21, com `12 - Adapte_Clientes` e `18 - Outros Modelos` |
| Meu Drive local | `C:\Users\rosep\Meu Drive\_82 ...` | **Mais antiga ainda.** Tem `08 - Quintal Eh`, nome de antes de virar Cinestratégico, além de `Cliente X` e `Clientes Standby` |

O que podia escrever numa delas:

| Mecanismo | O que fazia | Situação |
|---|---|---|
| `scripts/sincronizar-82.ps1` | Sincronizava Drive e Área de Trabalho **nos dois sentidos**, de forma aditiva | Existia, nunca tinha sido executado |
| `scripts/backup-diario.bat`, bloco 2 | **Lê** a `_82` do Drive e grava em `Backups\pasta-82\atual` | Ativo, todo dia às 12h30 |
| Google Drive para computador | Espelhamento de pasta local | **Desligado.** A tabela `roots` do `root_preference_sqlite.db` está vazia. O Drive roda só em streaming, pelo `G:` |
| Tarefas agendadas | Uma só, a do backup das 12h30 | Sem nenhuma outra ligada à `_82` |
| `scripts/montar-unidade-82.ps1` e o item de inicialização | Montam a unidade virtual `M:` | Não copiam nada, ficam como estão |

## 4. O perigo que motivou o desligamento

O `sincronizar-82.ps1` é **aditivo e nunca apaga**. Isso é uma proteção quando as duas
pontas estão alinhadas, e vira o problema quando elas divergiram.

No estado do item 3, rodar com `-Executar` levaria os nomes antigos da Área de Trabalho
para dentro do Drive. Como nada é apagado, a `06 - Clientes` ficaria com as duas versões
lado a lado: o `10 - CaptaDrive - Núcleo Arte e Música Esperança` correto convivendo com
o `08 - CaptaDrive - Núcleo Arte e Música Esperança` antigo, e assim por diante.

O trabalho de correção não seria sobrescrito, seria **afogado na duplicação**, que é
mais trabalhoso de desfazer do que uma sobrescrita, porque exige decidir pasta a pasta
qual das duas fica.

## 5. O que foi executado

1. Auditadas todas as tarefas agendadas, os itens de inicialização e os scripts do
   projeto, atrás de qualquer coisa que escrevesse na `_82`.
2. Inspecionado o banco de preferências do Google Drive para descartar espelhamento de
   pasta local. A tabela `roots` está vazia; os caminhos que apareciam numa leitura crua
   do arquivo eram registros já apagados, sobra em página livre do banco.
3. Criada a pasta `scripts/desativados/`, com `LEIA-ME.md` explicando a regra.
4. Movido `scripts/sincronizar-82.ps1` para
   `scripts/desativados/sincronizar-82.ps1.desativado`. A extensão trocada impede que
   ele seja chamado por engano.
5. Acrescentada uma trava dentro do próprio arquivo, logo depois do bloco de parâmetros,
   que interrompe a execução com a explicação do motivo, caso alguém renomeie de volta
   sem ler o cabeçalho.
6. Testada a trava numa cópia isolada, em ambiente separado. Ela barrou a execução, não
   criou nenhuma pasta de relatório nem de versões, e não montou a unidade `N:`.
7. Corrigido o `docs/backup.md`, que ainda afirmava que a `_82` não entrava no backup
   diário. Ela entra desde 21/08/2026.

## 6. Estado depois

| Medida | Antes | Depois |
|---|---|---|
| Sincronizadores de duas vias ativos | 1 | 0 |
| Scripts capazes de escrever na `_82` | 1 | 0 |
| Cópias de mão única para cofre | 1 | 1, mantida de propósito |
| Espelhamento do Google Drive | 0 | 0 |
| Travas contra religar sem ler | 0 | 2, a extensão e o bloco interno |

## 7. Backup feito antes

| Origem | Destino | Conferido |
|---|---|---|
| Nenhum | Nenhum | Nenhum documento foi tocado. A mudança é de script, e o arquivo foi movido, não excluído |

## 8. Como reverter

Renomear `scripts/desativados/sincronizar-82.ps1.desativado` de volta para
`scripts/sincronizar-82.ps1` e apagar o bloco de trava do cabeçalho.

**Antes de fazer isso**, alinhar as duas pontas em sentido único, do Drive para a Área
de Trabalho. Enquanto a Área de Trabalho estiver na versão anterior à correção, religar
o script nos dois sentidos reproduz exatamente o problema descrito no item 4.

## 9. O que ficou pendente

- **A Área de Trabalho continua na versão anterior à correção.** Ela não foi atualizada
  aqui, porque atualizar significa criar e renomear pastas, e a regra é que nada em
  `06 - Clientes` se mexe sem a captadora avisar. Quando ela quiser, o caminho é cópia de
  mão única do Drive para a Área de Trabalho.
- **Três nomes fora do padrão `NN - Nome` no Drive**, não corrigidos por causa da mesma
  regra: `03 - CaptaDrive - Inter SG` tem `01 - Gestão documental` com "d" minúsculo,
  e `11- CaptaDrive - Geórgia` e `14- CaptaDrive - Berê Xicrkin` estão sem o espaço antes
  do hífen.
- **`C:\Users\rosep\Meu Drive` é sobra** de um espelhamento antigo do Google Drive, hoje
  desligado. A pasta está marcada como somente leitura e não sincroniza com nada. Fica
  onde está, porque nenhuma pasta `_82` se apaga.
- **Decisão sobre o bloco 2 do backup diário**, descrita no item 2.

## 10. Regras que passam a valer

**Sincronização de duas vias entre cópias que divergiram é destrutiva, mesmo quando não
apaga nada.** Sincronizador aditivo duplica em vez de sobrescrever, e duplicação em
estrutura de pasta é mais cara de desfazer do que perda de arquivo, porque exige decidir
item a item.

**A `_82` do Drive é a fonte da verdade da estrutura.** A cópia da Área de Trabalho é
derivada. Quando as duas divergirem, o alinhamento é sempre do Drive para a Área de
Trabalho, em sentido único.

**Antes de afirmar que um trabalho se desfez, conferir a data de alteração dos dois
lados e identificar qual cópia está na tela.** Três pastas com o mesmo nome em três
lugares fazem parecer que a estrutura voltou atrás sozinha.

**Script que não deve mais rodar vai para `scripts/desativados/` com a extensão trocada
e uma trava dentro.** Apagar perde o motivo; deixar no lugar convida ao acidente.
