# 00_INDICE. Automações, rotinas e conectores

> Versão 1, de 18/09/2026. Arquivo de contexto da frente de automações: o que roda sozinho, o que foi desligado, o que só roda quando a captadora pede e onde está o detalhe de cada peça.
>
> Este arquivo está no repositório público. Por isso **não traz endereço de e-mail, endereço de página, token nem identificador de conta**. Esses dados ficam no `.env` e na memória local (`.claude/memoria/`, fora do Git).
>
> **Atualizar sempre que** uma rotina for criada, religada, desligada ou mudar de horário ou de destino. A regra que manda em tudo isto é a seção **NADA RODA SOZINHO** do `CLAUDE.md`.

---

## 1. A regra em uma linha

Nada deste ambiente inicia uma operação por conta própria. As únicas coisas que rodam sem ela pedir são as quatro exceções da seção 2, e nenhuma delas se desliga sem ela pedir.

---

## 2. O que fica ligado para sempre (as quatro exceções)

| # | O quê | Quando roda | O que faz | Desde |
|---|---|---|---|---|
| 1 | Google Drive e OneDrive | sempre | Programas do computador. O Google Drive mantém a unidade `G:`, de que depende a `_82` | 01/09/2026 |
| 2 | Conectores do Instagram e do LinkedIn | só quando uma conversa chama | Ponte na HostGator e dois serviços no Render, parados até serem chamados | 01/09/2026 |
| 3a | Radar de Editais (PPL + Geral), na nuvem do claude.ai | todo dia, 08h20 | Lê os Alertas do Google, atualiza os painéis Geral e PPL, move para a lixeira do Gmail os alertas que processou | 13/09/2026 |
| 3b | Resumo matinal, na nuvem do claude.ai | segunda a sexta, 08h | Lê agenda e Gmail só para consulta, atualiza a página Resumo da manhã e notifica | 13/09/2026 |
| 3c | Radar de Mercado e Patrocínio, na nuvem do claude.ai | todo dia, 09h | Atualiza a página do radar, move para a lixeira os alertas de mercado processados e grava dois PDFs em `Área de Trabalho\RADARES DO DIA` | religado em 13/09/2026 |
| 4 | Cópia dos radares na Área de Trabalho, no agendador do aplicativo Claude | todo dia, 9h30, com o aplicativo aberto | Converte as quatro páginas em PDF (`scripts/radares-do-dia-pdf.ps1`) e grava em `RADARES DO DIA`, substituindo os do dia anterior | 15/09/2026 |

As rotinas 3a, 3b e 3c só aparecem na listagem de rotinas remotas do claude.ai, não nas tarefas do Windows nem no agendador do aplicativo. A 3c depende do computador ligado às 9h e pode atrasar ou ser suspensa: suspensa por computador ausente não é desligada por ela, e religar deve ser oferecido.

---

## 3. O que foi desligado

| O quê | Desde |
|---|---|
| Tarefa do Windows de backup diário | 28/08/2026 (confirmado em 01/09) |
| Ganchos `sem-travessao.py` e `agentes-status.py` | 01/09/2026 |
| Sincronização da carteira na abertura da conversa | 01/09/2026 |
| Envio automático ao CaptaHub ao fechar etapa | 01/09/2026 (agora só com o OK dela) |
| Sincronização CaptaHub para Airtable, projeto MAPA e automações da base | 31/08 e 02/09/2026 |
| Sincronização entre as cópias da `_82` | 26/08/2026 |
| Encaminhamento da caixa de editais | 30/08/2026 |
| Cópia antiga do Radar de Editais | não se religa |

Inventário completo do dia do desligamento: [automacoes-desligadas.md](automacoes-desligadas.md). **Atenção:** aquele arquivo descreve o Radar de Mercado como está em 13/09 (PDFs entregues na conversa). Em 16/09 ela decidiu o contrário: os PDFs voltam a ser gravados no computador, em `RADARES DO DIA`. Vale o que está neste índice e no `CLAUDE.md`.

---

## 4. O que só roda quando ela pede

| O quê | Como pedir | Observação |
|---|---|---|
| Backup no disco e no Google Drive | "roda o backup" (`scripts/backup-diario.bat`) | Copia a `_82` do Drive, a memória e o projeto. Sem `/MIR`: nunca apaga no destino. O `.env` fica fora |
| Sincronizar com o CaptaHub | `/captahub-sincronizar` | Puxa e sobe dentro do comando |
| Puxar editais | `/edital-minerar` | Sem conexão, usa o cache de `base-editais/` |
| Verificar acentuação | `scripts/verificar-acentuacao.py` | Não é gancho: roda só sob pedido |

---

## 5. Pendências abertas

| Pendência | Quem resolve |
|---|---|
| Trocar, no aplicativo do claude.ai, o caminho dos PDFs da rotina 3c para `Área de Trabalho\RADARES DO DIA` | Rosepaula |
| Acrescentar na rotina 3c a busca de alertas de mercado atrasados (mais de 48h), para que todo alerta lido vá para a lixeira. Texto pronto em `estruturacoes/_detalhado/2026-09-21-todo-alerta-lido-vai-para-a-lixeira.md` | Rosepaula, no aplicativo do claude.ai |
| Token do Instagram vence por volta de 20/10/2026 | Rosepaula, com apoio |
| Rotacionar as chaves pendentes | Rosepaula |
| Excluir a tarefa desativada "NÃO USAR, teste de 13/09" no claude.ai | Rosepaula |

---

## 6. Onde está o detalhe

- Regra geral: `CLAUDE.md`, seções **NADA RODA SOZINHO** e **REGRA DE ABERTURA DE SESSÃO**.
- Memória local, seções **Automações e rotinas**, **Marketing, comercial e redes** (conectores) e **Segurança** do `MEMORY.md`.
- Conectores: `docs/persistencia-sessao-conectores.md` e os `README.md` de `mcp-instagram/` e `mcp-linkedin/`.
- Backup: `docs/backup.md`.

---

## 7. Decisões

| Data | Decisão | Situação |
|---|---|---|
| 01/09/2026 | Nada roda sozinho; Drive e conectores ficam ligados para sempre | ATUAL |
| 04/09/2026 | Chamada necessária a um comando que ela deu roda sem pedir confirmação; escrita externa não necessária pede o OK | ATUAL |
| 13/09/2026 | As rotinas da nuvem do claude.ai viram a exceção 3; o Resumo da manhã abre toda conversa | ATUAL |
| 15/09/2026 | Cópia dos radares na Área de Trabalho vira a exceção 4 | ATUAL |
| 16/09/2026 | Radar de Mercado volta a gravar PDFs no computador, em `RADARES DO DIA` | ATUAL, troca de caminho pendente no aplicativo |
| 18/09/2026 | Criado este índice como contexto único da frente de automações | ATUAL |
| 21/09/2026 | Todo alerta lido vai para a lixeira. A 3a já cumpre; a 3c só lê as últimas 48h e deixa alerta de mercado antigo na caixa | ATUAL, conserto da 3c pendente no aplicativo |
