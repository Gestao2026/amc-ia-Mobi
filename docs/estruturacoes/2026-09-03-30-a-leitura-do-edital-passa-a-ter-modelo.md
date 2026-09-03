# 30 - A leitura do edital passa a ter modelo

| Campo | Valor |
|---|---|
| Data | 2026-09-03 |
| Pasta afetada | `.claude/commands/`, `.claude/agents/`, `.claude/rules/`, `minhas-oscs/MODELO-edital.md`, `CLAUDE.md` |
| Tipo | Configuração |
| Situação | Concluída |
| Autorizada por | A captadora, em 03/09/2026: "faça as três" (as três amarrações), depois "grave edital.md com as informações que você colocou que ele faz e deve fazer, para sempre que chamar ele possa fazer a leitura com os campos definidos e não ficar sem saber o que fazer" |
| Reversível | Sim. Nenhum arquivo foi apagado. Reverter é desfazer o commit e apagar `minhas-oscs/MODELO-edital.md` |

---

## 1. Por que foi feito

A informação de um edital chegava partida em três lugares, e nenhum deles entregava tudo:

| Onde | O que entregava | O que faltava |
|---|---|---|
| `/edital-analisar`, Passo 3 | Lista livre de 8 pontos. Um deles era "documentos exigidos para habilitação", em uma linha | Momento de entrega, validade, onde emitir, escala de pontuação |
| `/edital-dossie`, Passo 5 | A ficha documental completa, nos três momentos | Só saía dentro de um Word de 14 partes, com 6 a 12 minutos de execução e duas perguntas antes |
| `captador-doc` (CaptaDoc) | "Checklist documental: tem, falta ou renovar" | Só o momento da inscrição. E ele reextraía o edital inteiro, refazendo o trabalho do `/edital-analisar` |

A captadora, ao ver o resultado: **"não tenho um documento que me entrega tudo que preciso saber, está aparecendo tudo separado."**

Havia ainda um efeito colateral: como não existia comando de checklist, quando ela digitava "faça um checklist desse edital" **nada disparava**. O sistema decidia na hora o que perguntar, e o resultado variava de leitura para leitura.

## 2. O que foi decidido, e por quem

Decisões da captadora, em 03/09/2026:

- O `edital.md` passa a ter **forma fixa**, com os campos definidos por escrito, "para sempre que chamar ele possa fazer a leitura com os campos definidos e não ficar sem saber o que fazer".
- **É um padrão**, não um modelo de uma vez só (palavras dela: "então esse é um padrão").
- As três amarrações são feitas: `/edital-analisar`, `captador-doc` e `/edital-dossie`.
- **O padrão de tela continua sendo uma tela.** Edital normal, inclusive edital extenso, cabe no semáforo e na ficha. O detalhe sai no dossiê, sob pedido dela.
- Descartado: criar um comando novo de checklist. O checklist passa a ser o bloco 6 do modelo, dentro da leitura, em vez de virar mais uma porta de entrada.

## 3. Estado antes

| Medida | Valor |
|---|---|
| Lugares que descreviam o que extrair de um edital | 3, divergentes entre si |
| Campos definidos por escrito para o `edital.md` | 8 pontos em lista livre |
| Momentos separados na ficha documental | 1 (só a inscrição), fora do dossiê |
| Comando que atende "faça um checklist desse edital" | Nenhum |
| Comandos que liam o edital inteiro do zero | 3 |

## 4. O que foi executado

1. Criado `minhas-oscs/MODELO-edital.md`, com **11 blocos e 9 tabelas**, seguindo o padrão do `MODELO-perfil-osc.md` que já existia.
2. `/edital-analisar`: o Passo 3 deixou de ser lista de 8 pontos e passou a mandar ler o modelo antes de começar, ler o edital **e cada anexo**, com as 6 regras de preenchimento. O Passo 4 passou a mandar mostrar **apenas os blocos 1 e 2 na tela**. O anúncio de tempo mudou de "8 pontos, 2 a 4 minutos" para "11 blocos, 4 a 8 minutos".
3. `captador-doc`: o item 1 do trabalho passou a começar com "**não reextraia o edital**". Ele trabalha sobre os blocos 3, 6, 7 e 9, e o checklist não se refaz: usa a ficha do bloco 6 e acrescenta a situação da OSC.
4. `/edital-dossie`: deixou de reler o edital. Virou formatação do `edital.md` em Word e PDF, mais três partes que só existem na entrega: cronograma completo, a carteira e a ficha de autoavaliação. Caiu de 6 a 12 minutos para 2 a 4.
5. `CLAUDE.md`: a tabela ONDE SALVAR passou a apontar para o modelo.
6. `.claude/rules/tempo-estimado.md`: as duas faixas corrigidas.
7. Teste real de ponta a ponta com o Edital de Seleção Pública de Patrocínio Embratur 2026, 31 páginas e 4 anexos, para a cliente Centro de Artes Almira Lopes.

## 5. Estado depois

| Medida | Antes | Depois |
|---|---|---|
| Lugares que descrevem o que extrair | 3, divergentes | 1, o modelo |
| Campos definidos por escrito | 8 pontos em lista livre | 11 blocos, 9 tabelas, cerca de 70 campos nomeados |
| Momentos separados na ficha documental | 1 | 3, com onde emitir, validade e colunas Enviado e Data |
| Comandos que leem o edital do zero | 3 | 1 |
| Tempo do dossiê | 6 a 12 minutos | 2 a 4 minutos |

## 6. Onde está a rastreabilidade

| Arquivo | O que registra |
|---|---|
| `minhas-oscs/MODELO-edital.md` | Os 11 blocos e as regras de preenchimento |
| `.claude/commands/edital-analisar.md` | A primeira leitura, e a regra de mostrar só os blocos 1 e 2 na tela |
| `.claude/agents/captador-doc.md` | A proibição de reextrair e o uso da ficha do bloco 6 |
| `.claude/commands/edital-dossie.md` | O mapa das 14 partes do dossiê contra os 11 blocos |
| Memória `primeira-leitura-do-edital-tem-modelo` | A decisão e como aplicar |
| `melhoria-amc-ia/INVENTARIO.md` | O diagnóstico de 01/09 que apontou o problema |

## 7. Backup feito antes

Não se aplica. Nenhum arquivo foi apagado nem sobrescrito com perda: as alterações são edições cirúrgicas em arquivos versionados no git, recuperáveis pelo histórico.

## 8. Como reverter

1. Desfazer o commit desta estruturação: `git revert` no commit correspondente.
2. Apagar `minhas-oscs/MODELO-edital.md`.
3. Apagar a memória `primeira-leitura-do-edital-tem-modelo.md` e a linha correspondente no `MEMORY.md`.

Os arquivos gerados no teste (a pasta do edital da Embratur dentro de `minhas-oscs/centro-de-arte-almira-lopes/`) não fazem parte da configuração e podem ficar onde estão.

## 9. O que ficou pendente

- **A memória dos agentes continua vazia.** `.claude/agents-memory/` tem só o README e o arquivo do painel. Seis agentes abrem com "leia a memória" e leem o vazio desde o primeiro dia. Não foi tratado aqui.
- **O Gauntlet Loop está parado na fase 4.** A bateria de 34 casos existe em `melhoria-amc-ia/AVALIACAO.md` e ainda não foi aprovada. O baseline não rodou, e a pasta `melhoria-amc-ia/baseline/` está vazia.
- **As mudanças de hoje alteram o baseline.** Quando o loop retomar, o baseline honesto tem que ser tirado da versão anterior a estas alterações, guardada no histórico do git.
- Os casos R1, R2 e R4 da bateria ficaram com critério mais frouxo do que este modelo cobra. Precisam ser apertados antes do baseline.
- O `edital.md` do FSA/BRDE, feito em 31/08 no formato antigo, não foi convertido para os 11 blocos.

## 10. Regras que passam a valer

- **Toda leitura de edital abre o `MODELO-edital.md` antes da primeira linha** e segue os 11 blocos na ordem.
- **Cada campo cita o item** do edital ou do anexo. Campo sem previsão vira **não encontrado**, com onde foi procurado. Nada se deduz pelo que é comum no setor.
- **Na tela saem só os blocos 1 e 2.** Documento longo só quando a captadora pedir.
- **Os três momentos da ficha documental nunca se misturam**: inscrição, habilitação, prestação de contas.
- **Ninguém relê o edital duas vezes.** Quem precisa de informação do edital lê o `edital.md`. Se faltar algo, completa-se lá, para que arquivo e dossiê nunca divirjam.
