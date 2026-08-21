# 03 - Consolidação dos backups em um único lugar

| Campo | Valor |
|---|---|
| Data | 2026-08-20 |
| Pasta afetada | `C:\Users\rosep\Backups` e `C:\amc-ia-Mobi\scripts` |
| Tipo | Configuração |
| Situação | Concluída e testada |
| Autorizada por | Rosepaula: "tudo que for backup do projeto vamos salvar sempre em `C:\Users\rosep\Backups\`" |
| Reversível | Sim, editando `scripts/backup-diario.bat` e a tarefa agendada |

---

## 1. Por que foi feito

Os backups estavam espalhados e sem regra: o do projeto ia para o Google Drive, o
da pasta `_82` foi feito à mão num terceiro lugar. Sem um endereço único, a
dúvida "onde está a cópia de segurança disso" reaparecia a cada vez.

## 2. O que foi decidido

- **Endereço único de backup: `C:\Users\rosep\Backups\`.** Toda cópia de segurança nasce aqui.
- Uma subpasta por origem, nome previsível.
- A regra antiga continua valendo: **o backup nunca apaga nada no destino**.

## 3. Como ficou

```
C:\Users\rosep\Backups\
├── _historico-backup.log        registro de cada execução
├── amc-ia-mobi\                 backup do Projeto AMC IA (diário, 12h30)
│   ├── minhas-oscs\
│   ├── captador\
│   ├── base-editais\
│   ├── parcerias\
│   └── docs\
└── pasta-82\
    └── 2026-08-20\              backup da cópia local da pasta dos mentores
```

## 4. O que foi executado

1. Criada a estrutura `Backups\amc-ia-mobi` e `Backups\pasta-82`.
2. O backup manual do `_82`, que estava em `Backups\_82-Rosepaula_2026-08-20`, foi movido para `Backups\pasta-82\2026-08-20`.
3. O script `scripts/backup-para-drive.bat` foi substituído por `scripts/backup-diario.bat`, com o novo destino e duas pastas a mais no escopo (`parcerias` e `docs`).
4. A tarefa agendada "AMC IA - Backup diario para o Google Drive" passou a apontar para o novo script. Horário mantido: **todo dia às 12h30**.
5. O script foi executado uma vez para teste. Código de retorno 0, sem falhas.

## 5. Sobre a segunda camada na nuvem

O script mantém, além da cópia local, a cópia do projeto em
`G:\Meu Drive\AMC-IA-Backup`. O motivo é simples: **um backup no mesmo disco do
original não protege contra falha do disco.** Se o C: morrer, a cópia morre
junto.

Com as duas camadas, o desenho fica coerente:

| O que | Origem | Cópia local | Cópia na nuvem |
|---|---|---|---|
| Projeto AMC IA | disco | `Backups\amc-ia-mobi` | `G:\Meu Drive\AMC-IA-Backup` |
| Pasta `_82` | Drive da dona | `Backups\pasta-82` | não se aplica, a origem já é nuvem |

Para desligar a camada na nuvem, basta comentar as três últimas linhas de
robocopy em `scripts/backup-diario.bat`.

## 6. O que NÃO é copiado, e por quê

- **O arquivo `.env`**, que guarda o token do CaptaHub. Segredo não vai para backup.
- **`_credenciais-nao-sincronizar\`**, com certificado digital e senha.
- **O código do sistema** (comandos, agentes, scripts), que já está no GitHub.

## 7. Como restaurar

Copiar a pasta de volta de `C:\Users\rosep\Backups\amc-ia-mobi\` para
`C:\amc-ia-Mobi\`. São arquivos comuns, não há ferramenta nem procedimento.

Depois de restaurar em outra máquina, reconectar o CaptaHub com
`/captahub-conectar`, porque o `.env` não vem no backup.

## 8. O que ficou pendente

- **A pasta `_82` no Drive da dona ainda não entrou no backup diário.** Depende de decidir como resolver a primeira carga de 10,43 GB, já que a pasta é streaming e o Drive precisaria baixar tudo.

## 9. Regras que passam a valer

- **Todo backup mora em `C:\Users\rosep\Backups\`.** Sem exceção, sem pasta nova em outro canto.
- Uma subpasta por origem, com nome igual ao da origem.
- Backup de operação pontual leva a data no nome da pasta (`pasta-82\2026-08-20`). Backup contínuo não leva data, porque é atualizado no lugar.
- Backup nunca apaga no destino.
- Segredo e credencial nunca entram em backup.
