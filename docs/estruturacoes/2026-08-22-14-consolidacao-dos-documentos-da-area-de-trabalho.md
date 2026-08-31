# 14 - Consolidação dos documentos soltos da Área de Trabalho

| Campo | Valor |
|---|---|
| Data | 2026-08-22 |
| Pasta afetada | `C:\Users\rosep\Desktop`, 10 arquivos `.docx` soltos |
| Tipo | Diagnóstico e consolidação documental |
| Situação | Concluída para a leitura e a consolidação. **Um achado de segurança em aberto** |
| Autorizada por | A captadora, em 22/08/2026, com escolha explícita de formato (`.docx`), alcance da página (6 temas) e tratamento dos segredos (registrar agora, rotacionar depois) |
| Reversível | Sim. Nada foi alterado nos arquivos de origem. Os entregáveis novos podem ser apagados sem efeito colateral |

---

## 1. Por que foi feito

A Área de Trabalho tinha **27 arquivos soltos**, nunca organizados (ver
[ESTADO-ATUAL](ESTADO-ATUAL.md), seção 3). Dez deles são `.docx` com o histórico
das conversas que originaram este projeto: a auditoria de infraestrutura, o
desenho das pastas, a construção dos conectores do LinkedIn e do Instagram, o
manual da planilha de controle e o briefing do Instagram da Mobilizando.

Esse conteúdo estava **fora do repositório e fora do índice de estruturações**.
Somando os dez arquivos são 78.121 caracteres de decisão técnica que ninguém
conseguiria recuperar sem reler documento por documento.

## 2. O que foi decidido, e por quem

- **Organizar por tema, não por arquivo.** Os dez documentos se sobrepõem: o
  mesmo assunto aparece em três deles, em datas diferentes. A consolidação por
  tema é o que torna o histórico consultável.
- **O dossiê sai em Word.** Mesmo formato dos originais, para leitura e edição
  direta.
- **A página explicativa cobre os 6 temas**, não só a parte técnica, para servir
  de mapa geral do projeto.
- **Descartado:** apagar ou mover os `.docx` de origem. Eles permanecem onde
  estão até a captadora decidir. Este registro apenas os indexa.
- **Descartado:** rotacionar os segredos hoje. O `LINKEDIN.docx` registra que a
  infraestrutura acabou de estabilizar, e a rotação derruba a conexão. Fica como
  pendência ordenada.

## 3. Estado antes

| Medida | Valor |
|---|---|
| Arquivos `.docx` soltos na Área de Trabalho | 14 (10 analisados) |
| Volume dos 10 analisados | 210 KB |
| Caracteres de texto | 78.121 |
| Registrados no índice de estruturações | 0 |
| Segredos em texto puro | 5, em 3 arquivos |

## 4. O que foi executado

1. Extração do texto dos 10 arquivos `.docx` para leitura integral, sem alterar
   os originais.
2. Leitura completa e classificação de relevância de cada documento.
3. Agrupamento do conteúdo em 6 temas.
4. Identificação de 5 segredos em texto puro e de 3 divergências entre o que os
   documentos assumem e o que o repositório faz hoje.
5. Redação do dossiê consolidado em Word.
6. Publicação da página explicativa dos 6 temas.

## 5. Estado depois

| Medida | Antes | Depois |
|---|---|---|
| Documentos indexados no histórico | 0 | 10 |
| Temas consolidados | 0 | 6 |
| Divergências mapeadas | 0 | 3 |
| Segredos expostos, catalogados | 0 | 5 |
| Segredos expostos, corrigidos | 0 | 0 |

## 6. Os 10 documentos e o que cada um traz

| Documento | Conteúdo principal | Relevância |
|---|---|---|
| `ALFA-AMC.docx` | Palavra de retomada. Auditoria de infra. Pendência dos MCPs do Google Data Cloud no Antigravity 2.1.1. Desanexar o fork do GitHub. Biblioteca SK-001 a SK-010. Árvore CaptaDrive do cliente | Alta |
| `PROJETO CLAUDE AMC IA.docx` | Divisão de trabalho chat e Claude Code. Estrutura de pastas. `CLAUDE.md` como ponte. Alerta LGPD. Etapas 0 a 4 | Alta |
| `INSTAGRAM.docx` | Briefing do Instagram da Mobilizando em 18 blocos. Pilares, funil, identidade, Reels, métricas, plano de 90 dias | Alta |
| `LINKEDIN.docx` | Checklist do que está pronto na infra do MCP. Escopos autorizados. Rotação de segredos pendente. Claude Code local e na nuvem | Alta |
| `ALFA-AMC.MKT.docx` | Regra de corte entre `marketing/`, `MOBI\06-MARKETING` e `mcp-*`. Fases 1 a 4 do MCP LinkedIn | Alta |
| `RENDER.docx` | Cadastro do conector do Instagram no Claude. Grupos 1, 2 e 3 de exclusão de arquivos | Média-alta |
| `TABELA EXCEL.docx` | Manual da planilha de controle. 5 abas, 15 estágios de status, colunas calculadas | Média-alta |
| `DOC1.docx` | Variáveis de ambiente no Render. Unidade `M:`. Backup diário | Média (já coberto pelo registro 08) |
| `Credenciais AMC IA ----analisar.docx` | Árvore final da pasta de credenciais | Baixa (já é o registro 11) |
| `ABRIR CONFIGURAÇÃO.docx` | Prompt genérico de instalação, com o sistema operacional em branco | Baixa (só a lista de ferramentas) |

## 7. Onde está a rastreabilidade

| Arquivo | O que registra |
|---|---|
| `docs/estruturacoes/2026-08-22-14-consolidacao-dos-documentos-da-area-de-trabalho.md` | Este registro |
| `docs/estruturacoes/_detalhado/2026-08-22-dossie-consolidado.docx` | O dossiê completo, por tema |
| Os 10 `.docx` na Área de Trabalho | As fontes, intactas |

## 8. Backup feito antes

Não foi necessário. Nenhum arquivo de origem foi alterado, movido ou apagado. Os
`.docx` da Área de Trabalho seguem cobertos pela tarefa diária das 12h30.

## 9. O que ficou pendente

### 9.1. Achado de segurança. Cinco segredos em texto puro

Contraria a regra do projeto de que segredo só vive no `.env`. Os três arquivos
estão na Área de Trabalho, que é copiada diariamente para o Google Drive.

| Arquivo | Segredo | Situação |
|---|---|---|
| `INSTAGRAM.docx` | `INSTAGRAM_TOKEN_ENCRYPTION_KEY` | Exposto, valor completo |
| `RENDER.docx` | Segredo da ponte do LinkedIn (Render e HostGator) | Exposto, valor completo |
| `LINKEDIN.docx` | Chave secreta do app do Instagram | Exposto, valor completo |
| `LINKEDIN.docx` | `MCP_CLAUDE_CLIENT_ID` | Exposto, valor completo |
| `LINKEDIN.docx` | ID do app do Instagram | Exposto (identificador, risco menor) |

O próprio `LINKEDIN.docx` já listava três segredos aguardando rotação: `DB_PASS`,
`MCP_LINKEDIN_PONTE_SECRET` e `LINKEDIN_TOKEN_ENCRYPTION_KEY`.

**Ordem sugerida de rotação, um por vez, testando entre cada um:**

1. Chave secreta do app do Instagram, no painel da Meta.
2. `INSTAGRAM_TOKEN_ENCRYPTION_KEY`, no Render. Invalida os tokens guardados,
   exige refazer a autorização do Instagram.
3. `MCP_LINKEDIN_PONTE_SECRET`, nos dois lados (Render e ponte da HostGator).
4. `LINKEDIN_TOKEN_ENCRYPTION_KEY`, no Render. Exige refazer a autorização do
   LinkedIn.
5. `DB_PASS` do MySQL da HostGator.
6. `MCP_CLAUDE_CLIENT_ID`. Exige recadastrar o conector no Claude.

Depois de rotacionar, substituir os valores nos `.docx` por
`***TOKEN_MASCARADO***`.

### 9.2. Três divergências entre os documentos e o repositório

| # | Divergência | Onde |
|---|---|---|
| D1 | A planilha tem **15 estágios** de status. O CaptaHub e o `CLAUDE.md` trabalham com **11**. Nenhum dos dois sabe do outro | `TABELA EXCEL.docx` e `CLAUDE.md` |
| D2 | Quem é a fonte da verdade do controle de editais: a planilha Excel ou o CaptaHub? O `CLAUDE.md` diz CaptaHub. A planilha foi construída como se fosse ela | `TABELA EXCEL.docx` e `CLAUDE.md` |
| D3 | A biblioteca planejada era `SK-001` a `SK-010`. As skills que existem hoje têm outros nomes (`captacao-editais`, `elaboracao-proposta`, `orcamento-tecnico`, `avaliacao-projeto`, `posicionamento-captador`). A numeração nunca foi adotada | `ALFA-AMC.docx` e `.claude/skills/` |

### 9.3. Pendências técnicas herdadas dos documentos

| # | O que | Documento de origem |
|---|---|---|
| P1 | MCPs do Google Data Cloud (Context, Notebooks, Visualization) não chegam ao Claude Code no Antigravity 2.1.1 | `ALFA-AMC.docx` |
| P2 | Descobrir qual processo abre o PowerShell sozinho, pelo processo pai | `ALFA-AMC.docx` |
| P3 | Desanexar `Gestao2026/amc-ia` do fork de `DiegoAlmeidaDev/amc-ia`. Texto do chamado já pronto | `ALFA-AMC.docx` |
| P4 | Ferramentas de negócio do LinkedIn. Falta consultar página e organização | `LINKEDIN.docx` |
| P5 | Escopos de publicação do LinkedIn: confirmar os produtos aprovados antes de pedir `w_member_social` ou `w_organization_social` | `LINKEDIN.docx` |
| P6 | Auditoria do Instagram da Mobilizando, ainda não feita. O briefing de 18 blocos está pronto para virar `/captador-perfil` | `INSTAGRAM.docx` |
| P7 | Rotina de exportação da Visão Cliente da planilha, oferecida e nunca construída | `TABELA EXCEL.docx` |

## 10. Regras que passam a valer

1. **Documento de conversa que traz decisão vira registro.** Não fica solto na
   Área de Trabalho. Entra no índice de estruturações, com tema e pendências.
2. **Nenhum segredo em `.docx`, em print ou em anexo.** Só no `.env`. Ao colar um
   valor sensível em qualquer documento, mascarar na hora.
3. **Divergência encontrada é divergência registrada.** Mesmo sem decisão, ela
   entra na lista, para não ser redescoberta daqui a três meses.
4. **A consolidação não apaga a fonte.** Os `.docx` originais só saem da Área de
   Trabalho por decisão explícita, depois de conferido que o dossiê cobre tudo.
