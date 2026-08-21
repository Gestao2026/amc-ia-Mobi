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
| `captador/` | `C:\Users\rosep\Backups\amc-ia-mobi\captador\` |
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

O mesmo script mantém uma cópia de `minhas-oscs`, `captador` e `base-editais` em
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

## O que ainda não está protegido

**A pasta `_82` no Google Drive do mentor não entra no backup diário.** Só existe
a cópia pontual de 20/08/2026, que é da versão local. Os arquivos que só existem
no Drive, entre eles dois documentos de identidade de dirigente do Levanta e
Brilha, seguem sem cópia sob controle da captadora.

Pendência registrada em
[docs/estruturacoes/2026-08-20-02-pasta-82-diagnostico.md](estruturacoes/2026-08-20-02-pasta-82-diagnostico.md).

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
