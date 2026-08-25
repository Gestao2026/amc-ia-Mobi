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
| 13 | 2026-08-21 | [Análise da pasta Documentos e comparação com a MOBI](2026-08-21-13-analise-pasta-documentos.md) | `OneDrive\Documentos` e `Desktop\MOBI` | **Apenas diagnóstico. Plano aguardando aprovação** |
| 14 | 2026-08-22 | [Consolidação dos documentos soltos da Área de Trabalho](2026-08-22-14-consolidacao-dos-documentos-da-area-de-trabalho.md) | `Desktop`, 10 arquivos `.docx` | Concluída. **Achado de segurança: 5 segredos em texto puro** |
| 15 | 2026-08-23 | [Consolidação dos editais entre a MOBI e a _82](2026-08-23-15-consolidacao-editais-mobi-vs-82.md) | `MOBI\03-EDITAIS` e `_82\04 - Controle de Submissão_` | Concluída. **3 pendências de decisão** |
| 16 | 2026-08-23 | [Os 4 logos repetidos na pasta APLICAVEIS são intencionais](2026-08-23-16-duplicatas-de-logo-intencionais.md) | `OneDrive E-missão\Documentos\9. MOBILIZANDO MKT LOGO` | Concluída. Diagnóstico, nada foi excluído |
| 17 | 2026-08-24 | [Consolidação do marketing numa pasta única](2026-08-24-17-consolidacao-do-marketing.md) | `MOBI\06-MARKETING` (extinta) e `Documentos\9. MOBILIZANDO MKT LOGO` | Concluída. **3 pendências de decisão** |

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
- **Pasta de acesso rápido não é duplicata.** Quando poucos arquivos escolhidos de uma árvore grande vivem numa pasta de uso diário, a repetição é a função dela. Medir quantos arquivos daquela pasta são exclusivos antes de apontar duplicidade.
- Ganho abaixo de 1 MB não justifica excluir arquivo em uso. O tempo de reencontrá-lo custa mais que o espaço.
- Nome diferente é informação. A duplicata que carrega o nome mais claro não se apaga.
- **Nenhuma exclusão sem confirmar que sobra pelo menos uma cópia do mesmo conteúdo.** A conferência é por hash, arquivo a arquivo, antes de mover para a Lixeira.
- **Antes de apagar uma pasta, verificar se ela está contida em outra.** Pasta cujo conteúdo inteiro já existe na irmã sai por completo, sem perda. Foi o caso da `MOÇAMBIQUE 5`, 22 de 22 arquivos já presentes na `MOÇAMBIQUE`.
- **Repetição com função não é duplicata.** Seleção curada, contexto duplo (a mesma foto arquivada no evento e no cliente) e atalho de uso rápido são organização, não desperdício.
- **Ao juntar arquivos numa pasta comum, checar se o movimento criou duplicata que antes não existia.** Duas cópias que serviam a contextos diferentes viram redundância quando param lado a lado.

**Sobre pasta vazia**
- **Pasta vazia não se apaga.** Decisão da captadora em 24/08/2026. Pasta sem documento dentro é estrutura criada de propósito, esperando o documento chegar. Não é sobra, não é lixo e não é pendência.
- Vale para todo o ambiente, e nomeadamente para `06 - Clientes` da `_82` no Drive (unidade `M:`) e para `Desktop\_82 ...\06 - Clientes\18 - Outros Modelos`, que é o modelo em branco da estrutura: 97 pastas, 52 delas vazias de propósito. Ali a pasta vazia é o próprio produto.
- **Pasta vazia não entra em relatório como problema.** Contar quantas existem é informação. Chamar de pendência é erro de leitura.
- **Ao replicar uma estrutura em outro lugar, replicar também as pastas vazias.** Elas fazem parte do desenho.
- Nenhuma operação automática que remova diretório vazio roda sem aviso antes. Isso inclui script de limpeza, sincronização com espelhamento e `robocopy /MIR`.
- Enquanto a captadora estiver corrigindo a estrutura à mão, nada se cria, renomeia, move ou apaga na pasta em que ela está trabalhando, até ela avisar que terminou.

**Sobre a pasta `_82`**
- **Nenhuma pasta chamada `_82 - Rosepaula Aparecida Andrade Rodrigues` se apaga**, nem no Google Drive nem na Área de Trabalho. Vale para a raiz e para qualquer subpasta, em qualquer nível, com ou sem conteúdo.
- Inclui a pasta compartilhada no Drive (unidade `M:`), a cópia da Área de Trabalho, a cópia em `C:\Users\rosep\Meu Drive` e o backup em `C:\Users\rosep\Backups\pasta-82`.
- Não apagar, não mover para a Lixeira, não "aposentar", não substituir por atalho, não deixar script tocar nelas. Se um plano de organização levar a remover qualquer uma, **o plano muda, não a pasta**.
- A pasta do Drive não é da captadora. Ela é Editora, não dona.

**Sobre o que não cabe em nenhuma pasta**
- **A máquina não usa a Lixeira. Nunca.** Nem para duplicata conferida, nem para lixo de sistema, nem para pasta inteira já consolidada em outro lugar. Excluir é decisão da captadora, tomada por ela, na hora que ela quiser.
- Ao trabalhar numa pasta, o que não couber em nenhuma estrutura existente **não fica solto, não vai para a Lixeira e não sai da pasta**. Vai para uma subpasta de triagem dentro da própria estrutura, chamada `_VERIFICAR-EXCLUIR-ANALISAR`.
- `EXCLUIR` no nome da subpasta é **proposta**, não ação executada. O arquivo continua inteiro, esperando o aval.
- Dentro dela, cada grupo ganha uma subpasta que **começa pelo verbo em caixa alta**: `VERIFICAR`, `EXCLUIR` ou `ANALISAR`, seguido do motivo. O nome já diz o que se espera.
- Um `LEIA-ME.md` na raiz da triagem descreve cada grupo: o que é, como foi conferido e qual decisão falta.
- A triagem é sala de espera, não depósito. Ao decidir, o arquivo sai: vai para a pasta definitiva ou para a Lixeira. Subpasta vazia é removida.
- **Pasta de triagem nunca entra em leitura automática.** Não alimenta perfil, proposta nem análise.
- O underscore na frente do nome é proposital: mantém a triagem no topo da listagem, junto de `_LOGS` e `_DUPLICADOS`.

**Sobre a base de leitura do marketing**
- A pasta única de marketing é `OneDrive E-missão\Documentos\9. MOBILIZANDO MKT LOGO`. Ela é lida para gerar o perfil de captador, então só entra ali o que é marketing da Mobilizando.
- Foto de projeto de cliente é portfólio, não arquivo morto: mora em `FOTOS\PROJETOS DE CLIENTES\{cliente}\{ação}\`.
- Foto pessoal vai para `Documentos\2. PESSOAL`, documento de cliente para `_82\06 - Clientes\{cliente}`, credencial para `Desktop\Credenciais AMC IA`, o resto para `Desktop\MOBI` pela numeração dela.
- **Documento que mistura conteúdo útil com token não entra na base de leitura.** Extrair a parte útil para um arquivo novo, conferir que nenhuma cadeia longa sobrou e deixar o original onde está.

**Sobre pasta de terceiro**
- Pasta compartilhada de que a captadora é apenas Editora não se reorganiza sem o aval de quem é dono.
- Renomear é preferível a excluir. Excluir arquivo de terceiro exige autorização explícita de quem é dono.
- **Conferir as permissões da pasta antes de começar a trabalhar nela**, e não depois de meses de uso.

**Sobre dado pessoal de terceiro**
- Pasta com CNH, CPF, RG ou comprovante de residência nunca fica em "qualquer pessoa com o link". Compartilhamento é sempre nominal, por e-mail.
- O link de uma pasta assim é credencial. Não se cola em conversa, grupo ou e-mail sem pensar.
