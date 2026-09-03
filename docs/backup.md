# Cópia de segurança

> Configurada em 20/08/2026 e consolidada no mesmo dia.
> Registro completo da mudança em [docs/estruturacoes/](estruturacoes/README.md).

## A regra de endereço

**Todo backup mora em `C:\Users\rosep\Backups\`.** Uma subpasta por origem, nome
igual ao da origem. Sem exceção e sem pasta de backup em outro canto.

```
C:\Users\rosep\Backups\
├── _historico-backup.log        registro de cada execução
├── amc-ia-mobi\                 o Projeto AMC IA, atualizado todo dia
├── credenciais\                 senhas dos clientes, só no disco, nunca na nuvem
└── pasta-82\
    └── 2026-08-20\              cópia pontual, com a data no nome
```

## Como funciona

A tarefa do Windows **"AMC IA - Backup diario para o Google Drive"** roda todo dia
às **12h30** e executa `scripts/backup-diario.bat`.

| O que é copiado | Para onde |
|---|---|
| `minhas-oscs/` | `C:\Users\rosep\Backups\amc-ia-mobi\minhas-oscs\` |
| `marketing/` | `C:\Users\rosep\Backups\amc-ia-mobi\marketing\` |
| `base-editais/` | `C:\Users\rosep\Backups\amc-ia-mobi\base-editais\` |
| `parcerias/` | `C:\Users\rosep\Backups\amc-ia-mobi\parcerias\` |
| `docs/` | `C:\Users\rosep\Backups\amc-ia-mobi\docs\` |
| `Área de Trabalho\Credenciais AMC IA\` | `C:\Users\rosep\Backups\credenciais\` |

## As credenciais, e por que elas param no disco

Desde 21/08/2026 a pasta `Credenciais AMC IA`, na Área de Trabalho, entra no
backup diário. Ela guarda a planilha de acessos dos clientes, as senhas e o
certificado digital e-CNPJ da MUPA.

**Ela é copiada só para o disco local, nunca para o Google Drive.** Decisão da
captadora, tomada com as três opções na mesa. O motivo: quem tiver o `.pfx` e a
senha dele assina em nome da organização, e uma cópia desse certificado já foi
parar no Drive uma vez, em 20/08/2026.

A consequência precisa ficar clara: **esse backup protege contra apagar sem
querer, não contra o disco C: morrer.** A cópia mora no mesmo disco do original.
Se a proteção contra falha de disco passar a ser prioridade, a saída não é subir
a pasta como está, é um cofre de senhas ou um arquivo criptografado.

## A segunda camada, na nuvem

O mesmo script mantém uma cópia de `minhas-oscs`, `marketing` e `base-editais` em
`G:\Meu Drive\AMC-IA-Backup`. Só essas três. A pasta de credenciais fica de fora
de propósito, conforme a seção acima.

O motivo: **um backup no mesmo disco do original não protege contra falha do
disco.** Se o C: morrer, a cópia local morre junto. A camada na nuvem cobre isso.

Para desligar, comentar as três últimas linhas de robocopy em
`scripts/backup-diario.bat`.

## A regra mais importante

**A cópia nunca apaga nada no destino.** Se um arquivo for excluído por engano
aqui, ele continua existindo no backup. Isso é proposital: um backup que espelha
exclusões apaga junto com o erro.

A contrapartida é que arquivos apagados de propósito continuam ocupando espaço.
Com 262 GB livres e 1,56 GB de uso, isso não é problema por muitos anos.

## O que NÃO é copiado, e por quê

- **O arquivo `.env`**, que guarda o token do CaptaHub. Segredo não vai para backup. Ao restaurar em outra máquina, reconectar com `/captahub-conectar`.
- **O código do sistema** (instruções, comandos, scripts), que já está no GitHub.
- **Para a nuvem**, nada da pasta de credenciais. Ver a seção sobre credenciais.

> A pasta `_credenciais-nao-sincronizar/` deixou de existir em 21/08/2026. Todo o
> conteúdo dela foi conferido arquivo por arquivo e já estava na pasta
> `Credenciais AMC IA` da Área de Trabalho, que é agora o lugar único.

## A pasta `_82` do Drive

Desde 21/08/2026 ela **entra** no backup diário. O script lê
`G:\.shortcut-targets-by-id\...\_82 - Rosepaula Aparecida Andrade Rodrigues` e grava em
`C:\Users\rosep\Backups\pasta-82\atual`. A primeira carga baixou 10,43 GB; as
seguintes copiam só o que mudou.

O sentido importa: **a origem é a nuvem e o destino é o disco.** É o inverso dos
outros blocos. Protege contra o dono da pasta apagar algo ou revogar o acesso, já
que a captadora é apenas Editora, não dona.

Ficam de fora os `desktop.ini`, que o Drive recria sozinho na máquina e não
existem na nuvem, e os ponteiros `.gdoc`, `.gsheet` e `.gslides`, que não têm
conteúdo próprio.

> A frase anterior desta seção, que dizia que a `_82` não entrava no backup,
> ficou desatualizada entre 21/08 e 26/08/2026. Corrigida no registro
> [20 das estruturações](estruturacoes/2026-08-26-20-desligamento-das-sincronizacoes-da-82.md).

## Sincronização entre as cópias da `_82`: desligada

Existem três cópias da `_82`, em estados diferentes: a do Drive, que é a fonte da
verdade da estrutura, a da Área de Trabalho e a de `C:\Users\rosep\Meu Drive`,
que é sobra de um espelhamento antigo e não sincroniza com nada.

**Desde 26/08/2026 nenhuma automação sincroniza essas cópias entre si.** O script
que fazia isso nos dois sentidos foi desligado e está em
`scripts/desativados/sincronizar-82.ps1.desativado`.

O motivo está no registro 20 acima. Em resumo: ele é aditivo e nunca apaga, então,
com as duas pontas divergentes, rodar não sobrescreve, duplica. A `06 - Clientes`
ficaria com a estrutura corrigida e a antiga lado a lado.

O backup descrito na seção anterior continua ligado, porque é leitura de mão única
para um cofre e não altera nenhuma das três cópias de trabalho.

## Como restaurar

Copiar a pasta de volta de `C:\Users\rosep\Backups\amc-ia-mobi\` para
`C:\amc-ia-Mobi\`. Não há procedimento nem ferramenta, são arquivos comuns.

## Cuidado com privacidade

A pasta contém CNH, CPF, RG e comprovantes de terceiros. No Google Drive ela deve
permanecer **privada** e nunca ser compartilhada por link. Não usar o OneDrive
corporativo de nenhum cliente para isso: documentos de um cliente não podem ficar
no ambiente de outro.

## Como mudar o horário

Abrir o Agendador de Tarefas do Windows e editar a tarefa
"AMC IA - Backup diario para o Google Drive".
