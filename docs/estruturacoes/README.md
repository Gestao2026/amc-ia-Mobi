# Estruturações

> Registro de toda ação de organização de pasta feita neste ambiente. Uma
> estruturação por arquivo, em ordem cronológica. Serve para responder, meses
> depois, três perguntas: **o que foi feito, por que, e como voltar atrás.**

> **Onde estamos agora:** [ESTADO-ATUAL.md](ESTADO-ATUAL.md), atualizado em 21/08/2026.

## Índice

| # | Data | Estruturação | Pasta | Situação |
|---|---|---|---|---|
| 01 | 2026-08-20 | [Reorganização da pasta MOBI](2026-08-20-01-pasta-mobi.md) | `Desktop\MOBI` | Concluída |
| 02 | 2026-08-20 | [Diagnóstico da pasta _82](2026-08-20-02-pasta-82-diagnostico.md) | `Desktop\_82` e Drive do dono | Diagnóstico, execução pendente |
| 03 | 2026-08-20 | [Consolidação dos backups](2026-08-20-03-consolidacao-dos-backups.md) | `C:\Users\rosep\Backups` | Concluída |
| 04 | 2026-08-20 | [Renomeação de um .gdoc no Drive do dono](2026-08-20-04-renomeacao-gdoc-levanta-e-brilha.md) | `_82` no Drive, Levanta e Brilha | Concluída |
| 05 | 2026-08-20 | [Remoção das tarefas agendadas órfãs](2026-08-20-05-remocao-tarefas-orfas.md) | Agendador de Tarefas | Concluída |
| 06 | 2026-08-20 | [Reconciliação entre a cópia local e o Drive](2026-08-20-06-reconciliacao-local-drive.md) | `_82` local e no Drive | Concluída |
| 07 | 2026-08-20 | [Higiene de arquivos na cópia local](2026-08-20-07-higiene-de-arquivos-pasta-82.md) | `_82` na Área de Trabalho | Concluída |
| 08 | 2026-08-20 | [Unidade virtual M e backup do Drive](2026-08-20-08-unidade-virtual-e-backup-do-drive.md) | Inicialização e tarefa de backup | Concluída |
| 09 | 2026-08-20 | [Exclusões de redundância e desktop.ini do Drive](2026-08-20-09-exclusoes-e-desktop-ini-do-drive.md) | `MOBI`, `Backups` e `_82` no Drive | Concluída |
| 10 | 2026-08-21 | [Achado: a pasta _82 está aberta por link público](2026-08-21-10-achado-pasta-82-com-link-publico.md) | `_82` no Google Drive | **Achado. Correção pendente com a dona da pasta** |
| 11 | 2026-08-21 | [Consolidação das credenciais dos clientes](2026-08-21-11-consolidacao-das-credenciais.md) | `Área de Trabalho\Credenciais AMC IA` | Concluída |
| 12 | 2026-08-21 | [Primeira carga do backup da _82 e exclusões](2026-08-21-12-primeira-carga-e-exclusoes.md) | `_82` no Drive, `MOBI`, `Backups` | Concluída |

## Como usar

**Antes de mexer numa pasta**, abrir o índice acima e conferir se ela já foi
estruturada. Se já foi, ler o registro antes de decidir qualquer coisa: ele diz o
que ficou pendente e quais regras passaram a valer.

**Ao concluir uma estruturação**, copiar o `_MODELO.md`, renomear para
`AAAA-MM-DD-NN-nome-curto.md`, preencher e acrescentar uma linha no índice.

## As cinco regras do registro

1. **Número, não adjetivo.** "Estava bagunçado" não explica nada. "O caminho mais longo tinha 335 caracteres e 629 arquivos não abriam" explica.
2. **Antes e depois, sempre.** Toda estruturação mostra a medida antes e a medida depois, na mesma unidade.
3. **Registrar o que foi descartado.** As decisões que não foram tomadas, e por quê, evitam refazer a mesma discussão daqui a três meses.
4. **Dizer como reverter.** Se não houver reversão automática, escrever isso com todas as letras.
5. **Pendência é parte do registro.** O que não foi feito, e de quem depende, fica escrito.

## As regras permanentes que saíram destas estruturações

Estas valem para o ambiente todo, não só para a pasta que as originou.

**Sobre backup**
- Todo backup mora em `C:\Users\rosep\Backups\`, uma subpasta por origem.
- Backup nunca apaga nada no destino.
- Backup no mesmo disco do original não protege contra falha do disco. Origem que vive no disco tem segunda camada na nuvem.
- Segredo, token e certificado nunca entram em backup.
- Antes de qualquer estruturação que envolva exclusão, o backup é obrigatório e conferido por contagem e volume.

**Sobre nome e caminho**
- O limite prático do Windows é 260 caracteres no caminho inteiro. O Explorer e o Office travam acima disso, mesmo com a política de caminho longo ligada.
- Quando os nomes de pasta podem mudar: encurtar nome e achatar níveis.
- Quando os nomes de pasta não podem mudar: encurtar o **prefixo** com unidade virtual (`subst`), nunca os nomes.
- O Google Drive na nuvem não tem limite de caminho. Quem falha é o Explorer ao copiar.

**Sobre duplicata**
- Duplicata se identifica por **conteúdo** (hash), nunca por nome.
- Cópia idêntica vai para `_DUPLICADOS` ou `_duplicados`, preservando o caminho de origem.
- Nada é apagado sem ordem expressa da captadora, com a lista conferida antes.

**Sobre pasta de terceiro**
- Pasta compartilhada de que a captadora é apenas Editora não se reorganiza sem o aval de quem é dono.
- Renomear é preferível a excluir. Excluir arquivo de terceiro exige autorização explícita de quem é dono.
- **Conferir as permissões da pasta antes de começar a trabalhar nela**, e não depois de meses de uso.

**Sobre dado pessoal de terceiro**
- Pasta com CNH, CPF, RG ou comprovante de residência nunca fica em "qualquer pessoa com o link". Compartilhamento é sempre nominal, por e-mail.
- O link de uma pasta assim é credencial. Não se cola em conversa, grupo ou e-mail sem pensar.
