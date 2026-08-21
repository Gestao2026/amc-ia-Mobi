# 08 - Unidade virtual M e backup diário da pasta do Drive

| Campo | Valor |
|---|---|
| Data | 2026-08-20 |
| Onde | Inicialização do usuário, tarefa de backup, e a pasta `_82` no Drive da mentora |
| Tipo | Configuração |
| Situação | Concluída e testada |
| Autorizada por | Rosepaula: "sim quero" ao arranjo proposto |
| Reversível | Sim, ver item 5 |

---

## 1. O problema que isto resolve

A pasta `_82` fica no Drive da mentora e chega ao Windows por um caminho de
**104 caracteres de prefixo**:

```
G:\.shortcut-targets-by-id\1YxXksuP6SHlVKA4bT5gaC0WG4Wy4OXej\_82 - Rosepaula Aparecida Andrade Rodrigues\
```

Com esse prefixo, **2.588 dos 6.023 arquivos** passavam de 260 caracteres e não
abriam no Explorer nem no Office. Como nenhum nome de pasta pode mudar, a única
saída era encurtar o prefixo.

## 2. A unidade M

Uma unidade virtual do Windows (`subst`) aponta a letra `M:` para essa pasta. O
prefixo cai de **104 para 2 caracteres**.

**A unidade não guarda nada.** É um apelido para a mesma pasta. Um arquivo só,
dois caminhos para chegar nele. Zero byte de espaço.

| | Caminho | Maior caminho | Arquivos acima de 260 |
|---|---|---|---|
| Antes | `G:\.shortcut-targets-by-id\...` | 478 | 2.588 |
| Depois | `M:\` | **252** | **0** |

Testado: o arquivo mais profundo (252 caracteres) abre com acesso comum, sem
truque nenhum.

Zero arquivos acima do limite só foi possível porque a
[estruturação 04](2026-08-20-04-renomeacao-gdoc-levanta-e-brilha.md) já tinha
encurtado o nome do único arquivo que ainda estourava.

## 3. Como a unidade sobe sozinha

Criar tarefa agendada exigiria elevação de administrador. Foi usada a
inicialização do usuário, que não exige:

| Onde | Valor |
|---|---|
| `HKCU:\Software\Microsoft\Windows\CurrentVersion\Run` | `AMC IA - Unidade M pasta 82` |
| Comando | `powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File "C:\amc-ia-Mobi\scripts\montar-unidade-82.ps1"` |

O script `scripts/montar-unidade-82.ps1` **espera até 5 minutos** o Google Drive
montar a unidade G: antes de criar a M:, porque no login o Drive costuma demorar.
Cada execução é anotada em `C:\Users\rosep\Backups\_historico-backup.log`.

## 4. O backup diário da pasta do Drive

Acrescentado ao `scripts/backup-diario.bat`, na tarefa que já roda às 12h30.

| Origem | Destino |
|---|---|
| `G:\.shortcut-targets-by-id\...\_82 - Rosepaula...` | `C:\Users\rosep\Backups\pasta-82\atual\` |

Repare no sentido: **a origem é a nuvem e o destino é o disco**, ao contrário do
backup do projeto. O motivo é que a captadora é apenas **Editora** dessa pasta,
não dona. Se a mentora revogar o acesso ou apagar algo, o backup local é a única
via de recuperação.

A leitura é feita pelo caminho real do Drive e não pela unidade M:, para o backup
não depender da unidade virtual estar montada. O `robocopy` lida com caminho
longo sozinho.

Se a pasta estiver indisponível (Drive fora do ar, acesso revogado), o script
anota no log e segue, sem travar o resto do backup.

## 5. Como reverter

- **Unidade M:** apagar a entrada `AMC IA - Unidade M pasta 82` de `HKCU:\Software\Microsoft\Windows\CurrentVersion\Run` e rodar `subst M: /D`.
- **Backup da pasta:** apagar o bloco `--- 2. Pasta _82` de `scripts/backup-diario.bat`.

## 6. O que ficou pendente

- **A primeira carga do backup, de 10,43 GB.** A pasta do Drive é streaming, então o primeiro backup força o download de tudo. Vai acontecer sozinho às 12h30, mas pode pesar na internet. Marcar a pasta como "Disponível offline" no Drive resolve de vez e deixa o backup diário instantâneo.
- **O identificador da pasta está fixo no script.** Se a mentora recriar o compartilhamento, o id muda e o backup para de achar a pasta. O script anota isso no log em vez de falhar em silêncio.

## 7. Regras que passam a valer

- **Caminho longo se resolve encurtando o prefixo, nunca renomeando pasta de terceiro.**
- A unidade virtual é apelido, não armazenamento. Apagar algo por ela apaga no original.
- Backup de pasta de terceiro sempre vai da nuvem para o disco, porque o risco ali é perder o acesso, não perder o disco.
- Script de backup nunca trava por origem indisponível. Anota e segue.
