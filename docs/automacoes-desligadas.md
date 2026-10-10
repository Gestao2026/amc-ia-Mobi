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
| Quatro automações de e-mail da base do Airtable | 02/09/2026, apagadas |
| Automação "Enviar para Não Submetidos" do Airtable | 02/09/2026, desligada de verdade |
| Leitura da `_82` da Área de Trabalho pelo backup | 28/08/2026 |

Os scripts correspondentes estão em `scripts/desativados/`.

> **Atenção ao Airtable.** O projeto MAPA foi desligado em 31/08/2026, mas as
> automações da base continuaram publicadas e mandando e-mail diário para
> `gestao.mobilizando@gmail.com` até 02/09/2026. Desligar o projeto não desliga
> as automações da base: são coisas separadas. O registro completo, com a
> configuração das cinco, está em `docs/airtable-automacoes/`.

## O que fica ligado para sempre, por decisão dela

> Autorizado pela captadora em 01/09/2026, com as duas na mesa. **Nenhuma destas
> pode ser parada, pausada, desabilitada ou removida até ela pedir.** A regra
> "nada roda sozinho" não alcança nenhuma delas.

**Google Drive (GoogleDriveFS) e OneDrive.** São programas do computador dela,
não automações deste projeto. O Google Drive mantém a unidade `G:` montada, e
dela dependem a pasta `_82` e vários caminhos daqui. Não sugerir desligar, não
encerrar processo, não mexer na inicialização.

**Os conectores do Instagram e do LinkedIn.** A ponte na HostGator e os dois
serviços no Render continuam de pé. Eles não rodam sozinhos: ficam parados até
uma conversa chamar, e por isso nunca feriram a regra. Não desativar serviço, não
remover conector, não revogar token.

**As rotinas agendadas na nuvem do claude.ai.** Autorizadas pela captadora em
13/09/2026. Diferente das anteriores, estas rodam por horário. Não aparecem nas
tarefas do Windows nem no agendador do aplicativo: vivem na conta do claude.ai, e
por isso ficaram fora do levantamento de 01/09.

| Rotina | Situação em 13/09/2026 | Quando roda (Brasília) | Atualiza |
|---|---|---|---|
| Radar de Editais (PPL + Geral) | ligada | todo dia, 08h20 | `painel-geral` e `painel-ppl` |
| Resumo matinal | ligada | segunda a sexta, 08h | `Resumo da manhã` |
| Radar de Mercado e Patrocínio | religada por ela em 13/09, depois de suspensa pela plataforma em 12/09 por computador ausente | todo dia, 09h | `Radar de Mercado e Patrocínio` e dois PDFs entregues na conversa da rotina (até 12/09 iam para a Área de Trabalho) |
| Radar de Editais, cópia antiga | desligada | era 08h | os mesmos dois painéis |

O Radar de Editais e o Radar de Mercado **movem para a lixeira do Gmail os alertas
que processaram**, cada um só os do seu tema. São as únicas escritas externas dessas
rotinas. O Resumo matinal só lê.

Em 13/09/2026 ela decidiu que o Radar de Mercado não depende mais do computador:
os PDFs passam a ser entregues na conversa da rotina. O texto novo está em
`C:\Users\rosep\Downloads\Radar-Mercado-prompt-atualizado.txt` e ainda precisa ser
colado por ela no aplicativo do claude.ai, junto com a retirada da pasta da Área de
Trabalho e do vínculo com o computador. Religar o Radar de
Mercado é decisão dela, e religado ele fica coberto pela mesma exceção. Não
desligar, não pausar, não editar e não apagar nenhuma sem ela pedir.

Se alguma dessas peças precisar mesmo ser mexida, parar e perguntar antes.

## A consequência que precisa ficar clara

**Sem o backup diário, nada é copiado sozinho.** `minhas-oscs`, `marketing`,
`base-editais`, `parcerias`, `docs` e a pasta `Credenciais AMC IA` da Área de
Trabalho ficam apenas no disco `C:`, no estado de 28/08/2026, que foi a última
execução.

Para tirar uma cópia, basta pedir: o script `scripts/backup-diario.bat` continua
inteiro e funciona quando executado à mão.
