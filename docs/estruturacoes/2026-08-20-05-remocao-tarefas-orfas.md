# 05 - Remoção das tarefas agendadas órfãs

| Campo | Valor |
|---|---|
| Data | 2026-08-20 |
| Onde | Agendador de Tarefas do Windows |
| Tipo | Limpeza de configuração |
| Situação | Concluída |
| Autorizada por | Rosepaula: "6 exclua as tarefas órfãs" |
| Reversível | Sim, reimportando os XML guardados |

---

## 1. Por que foi feito

Quatro tarefas do Agendador apontavam para scripts em `C:\amc-ia\`, pasta que não
existe mais. Ela foi substituída por `C:\amc-ia-Mobi`. As tarefas estavam
desativadas e não executavam nada, mas poluíam o Agendador e davam a falsa
impressão de que havia automações rodando.

Duas delas eram justamente de uma tentativa anterior de sincronizar a pasta `_82`.

## 2. O que foi removido

| Tarefa | Apontava para | Último resultado |
|---|---|---|
| `AMC-IA-Push-Diario` | `C:\amc-ia\scripts\push-diario-seguro.ps1` | erro 3221225786 |
| `AMC-IA-SincronizacaoDiaria` | `C:\amc-ia\scripts\sincronizacao-diaria.py` | 0 |
| `AMC-IA-Sincronizar-Pasta82` | `C:\amc-ia\scripts\sincronizar-pasta-82\sincronizar-pasta-82.ps1` | 0 |
| `AMC-IA-Vigia-Pasta82` | `C:\amc-ia\scripts\sincronizar-pasta-82\verificar-sincronizacao.ps1` | 0 |

## 3. O que foi executado

1. A definição completa de cada tarefa foi exportada em XML **antes** da remoção.
2. As quatro tarefas foram removidas do Agendador.
3. Conferido que nenhuma das quatro existe mais.

## 4. Onde está a rastreabilidade

`C:\Users\rosep\Backups\tarefas-agendadas-removidas-2026-08-20\`, com um XML por
tarefa.

## 5. Como reverter

No PowerShell, para cada tarefa:

```
Register-ScheduledTask -Xml (Get-Content "C:\Users\rosep\Backups\tarefas-agendadas-removidas-2026-08-20\NOME.xml" -Raw) -TaskName "NOME"
```

Vale lembrar que os scripts que elas chamavam **não existem mais**. Restaurar a
tarefa não restaura o script.

## 6. O que permanece no Agendador

Uma única tarefa da AMC IA: **"AMC IA - Backup diario para o Google Drive"**, que
roda `C:\amc-ia-Mobi\scripts\backup-diario.bat` todo dia às 12h30.

## 7. Regras que passam a valer

- Tarefa agendada que aponta para caminho inexistente é removida, nunca deixada desativada. Desativada dá a impressão de que existe e pode voltar.
- Antes de remover, a definição é exportada em XML para `C:\Users\rosep\Backups\`.
- Ao mudar o caminho do projeto, conferir o Agendador na mesma hora.
