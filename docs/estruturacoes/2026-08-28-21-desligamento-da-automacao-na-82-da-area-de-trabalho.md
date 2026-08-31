# 21 - Desligamento de toda automação sobre a _82 da Área de Trabalho

| Campo | Valor |
|---|---|
| Data | 2026-08-28 |
| Pasta afetada | `scripts/backup-diario.bat` e a tarefa agendada do Windows. Nenhum arquivo dentro de `C:\Users\rosep\Desktop\_82 - Rosepaula Aparecida Andrade Rodrigues` foi tocado |
| Tipo | Desativação de automação |
| Situação | Concluída |
| Autorizada por | A captadora, pedido direto: "desligue e exclua qualquer atualização, inclusão e exclusão que esta sendo comandada para a pasta" |
| Reversível | Sim, por completo. Ver item 8 |

---

## 1. Por que foi feito

A captadora relatou, na manhã de 28/08/2026, ter encontrado a `_82` da Área de Trabalho
com arquivos que ela tinha ajustado na véspera para subir ao Drive aparentemente
apagados. A apuração (mesma sessão) investigou quatro frentes antes de qualquer ação:

- **Lixeira do Windows.** Achados 43 itens excluídos entre 26/08 23h50 e 28/08 00h13,
  a maioria saindo de `06 - Clientes\08 - Núcleo Arte e Música Esperança` e
  `09 - Centro de Arte Almira Lopes`. O caso mais relevante: uma pasta duplicada
  `02 - Edital PNAB - Ciclo 2` (rascunhos soltos) foi excluída, enquanto a pasta
  organizada `02 - PNAB Ciclo 2` (sete subpastas, conteúdo completo do edital)
  permaneceu intacta e atualizada até 27/08 23h59.
- **Tarefas agendadas do Windows.** Nenhuma tarefa, além da já conhecida de backup,
  faz referência a essa pasta.
- **Windows Defender.** Sem nenhuma detecção ou quarentena no histórico.
- **OneDrive e Google Drive.** A Área de Trabalho não está redirecionada para nenhuma
  nuvem (`C:\Users\rosep\Desktop` é pasta local comum, confirmado pela API de Known
  Folder e pelas duas chaves de registro que controlam isso). O Google Drive
  (`GoogleDriveFS.exe`) não tem nenhum vínculo com essa pasta.
- **Cópias de sombra e pontos de restauração.** Nenhum dos dois existe no disco C:,
  então não há uma "versão anterior" oculta do Windows para recuperar por aí.

Não foi achado nenhum mecanismo automático apagando arquivo. O padrão (exclusões
concentradas numa janela de duas horas, de pastas com nome parecido e conteúdo
duplicado) tem cara de organização manual, não de falha de sistema.

Mesmo assim, a captadora pediu que **nenhuma automação continue tocando essa pasta**,
para eliminar de vez a hipótese e trabalhar sem esse ruído enquanto organiza o conteúdo.

## 2. O que foi decidido, e por quem

- Desligar a tarefa agendada do Windows que dispara o backup diário.
- Remover do script o único bloco que lê essa pasta, não só desligar a tarefa que o
  aciona, para que religar a tarefa por engano no futuro não volte a tocar a pasta.

## 3. Estado antes

| Medida | Valor |
|---|---|
| Tarefas agendadas do Windows lendo essa pasta | 1 ("AMC IA - Backup diario para o Google Drive", ativa, rodava 12h30) |
| Blocos do `backup-diario.bat` que leem essa pasta | 1 (bloco 5, incluído mais cedo no mesmo dia) |
| Scripts capazes de escrever nessa pasta | 0 (o único que um dia teve esse poder, `sincronizar-82.ps1`, já estava desativado e travado desde 26/08) |
| Itens da Lixeira originários dessa pasta | 41, todos de 27/08 e madrugada de 28/08 |

## 4. O que foi executado

1. Investigadas as quatro frentes do item 1, nenhuma automação encontrada como causa.
2. Desativada a tarefa agendada "AMC IA - Backup diario para o Google Drive" no
   Agendador de Tarefas do Windows.
3. Removido do `scripts/backup-diario.bat` o bloco 5 inteiro (o que lia
   `C:\Users\rosep\Desktop\_82 - Rosepaula Aparecida Andrade Rodrigues` para gravar em
   `Backups\desktop-82\atual`), deixando um comentário no lugar explicando o motivo e
   como reverter.

## 5. Estado depois

| Medida | Antes | Depois |
|---|---|---|
| Tarefa agendada ativa sobre a pasta | 1 | 0 |
| Blocos de script lendo a pasta | 1 | 0 |
| Scripts capazes de escrever na pasta | 0 | 0 |
| Backup existente da Área de Trabalho (`Backups\desktop-82\`) | Mantido, não foi apagado | Mantido, só parou de ser atualizado |

## 6. Onde está a rastreabilidade

| Arquivo | O que registra |
|---|---|
| `scripts/backup-diario.bat` | O comentário no lugar do bloco 5 explica a data, o motivo e como religar |
| Este arquivo | O raciocínio completo da investigação e a decisão |

## 7. Backup feito antes

| Origem | Destino | Conferido |
|---|---|---|
| Nenhum | Nenhum | Nenhum documento dentro da `_82` foi tocado. A mudança é só no script |

## 8. Como reverter

1. No Agendador de Tarefas do Windows, achar "AMC IA - Backup diario para o Google
   Drive" e Habilitar de novo.
2. Em `scripts/backup-diario.bat`, devolver o bloco robocopy original do item 5
   (disponível no histórico do Git, commit anterior a 28/08/2026, ou no registro 20
   citado acima).

## 9. O que ficou pendente

- **Esta alteração ainda não foi commitada no Git.** Fica como mudança local até a
  captadora pedir o commit.
- **A causa exata das exclusões continua sendo, com mais confiança, ação manual**, não
  falha de sistema, mas isso não foi confirmado com a captadora com todas as letras,
  porque a conversa seguiu para outros pontos antes disso.
- **O backup da Área de Trabalho (`Backups\desktop-82\`) parou de se atualizar.**
  Continua existindo com o estado de 28/08, mas não vai acompanhar mudanças futuras
  até a automação ser religada.

## 10. Regras que passam a valer

- **Pasta sob suspeita de perda de arquivo pode ser isolada de toda automação,
  mesmo automação só de leitura, a pedido da captadora.** Não é preciso provar que a
  automação é a causa para desligá-la.
- **Desligar não é só desativar a tarefa que aciona o script, é também tirar o trecho
  do script que toca a pasta.** Duas camadas de proteção contra religar por engano.
