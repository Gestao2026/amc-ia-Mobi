# Nada roda sozinho

> Decisão da captadora em 01/09/2026. Regra registrada no `CLAUDE.md`, seção
> **NADA RODA SOZINHO**, com prioridade absoluta.

Nenhuma automação deste ambiente roda sem ela pedir, na hora em que ela pedir.
Este arquivo é o inventário do que estava ligado no dia da decisão e do que
aconteceu com cada item.

## O que foi desligado em 01/09/2026

| O que era | Como disparava | Estado agora |
|---|---|---|
| Tarefa do Windows "AMC IA - Backup diario para o Google Drive" | todo dia às 12h30 | desabilitada. Já estava desde 28/08 às 16h19, e assim permanece |
| Gancho `sem-travessao.py` | antes de todo Write, Edit e MultiEdit | removido do `.claude/settings.json` |
| Gancho `agentes-status.py` | depois de Write, Edit, Bash e Agent | removido do `.claude/settings.json` |
| Sincronização da carteira na abertura da conversa | toda vez que uma conversa começava | removida da REGRA DE ABERTURA DE SESSÃO |
| Envio automático para o CaptaHub ao fechar etapa | a cada orçamento, avaliação e submissão | agora só com o OK explícito dela |

A cópia anterior do arquivo de configuração ficou em
`.claude/settings.json.bak-2026-09-01`.

## O que já estava desligado antes, e continua

| O que | Desde |
|---|---|
| Sincronização CaptaHub para Airtable | 31/08/2026 |
| Projeto MAPA e painel do Airtable | 31/08/2026 |
| Sincronização entre as cópias da pasta `_82` | 26/08/2026 |
| Leitura da planilha de submissão | 31/08/2026 |
| Encaminhamento da caixa `editais.mobilizando` | 30/08/2026 |
| Leitura da `_82` da Área de Trabalho pelo backup | 28/08/2026 |

Os scripts correspondentes estão em `scripts/desativados/`.

## O que continua ligado, e por quê

Estes não são automações do projeto. São programas do computador dela, que
sincronizam arquivos o tempo todo:

- **Google Drive (GoogleDriveFS)**, que mantém a unidade `G:` montada. Vários
  caminhos deste projeto e a pasta `_82` dependem dele.
- **OneDrive**, que veio com o Windows.

Desligar qualquer um dos dois é decisão dela, e muda o funcionamento da máquina
inteira, não só deste projeto.

Os conectores do Instagram e do LinkedIn também continuam de pé, mas eles não
rodam sozinhos: são servidores que ficam parados até alguém chamar, e quem chama
é uma conversa em andamento.

## A consequência que precisa ficar clara

**Sem o backup diário, nada é copiado sozinho.** `minhas-oscs`, `marketing`,
`base-editais`, `parcerias`, `docs` e a pasta `Credenciais AMC IA` da Área de
Trabalho ficam apenas no disco `C:`, no estado de 28/08/2026, que foi a última
execução.

Para tirar uma cópia, basta pedir: o script `scripts/backup-diario.bat` continua
inteiro e funciona quando executado à mão.
