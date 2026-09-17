# 31 - A v2 dos alunos entra sem mexer nas regras

| Campo | Valor |
|---|---|
| Data | 2026-09-10 |
| Pasta afetada | `.claude/agents/`, `.claude/commands/`, `.claude/skills/orcamento-tecnico/`, `scripts/`, exemplo `exemplo-instituto-semente` |
| Tipo | Configuração |
| Situação | Concluída |
| Autorizada por | A captadora, em 10/09/2026: "analise a v2 e traga as melhorias para o meu projeto, sem mexer naquilo que já configurei". Durante o trabalho: "coloque toda a exportação parecer do chefe e as cotações e o que tiver mais" |
| Reversível | Sim. Nenhum arquivo foi apagado. As versões anteriores dos 10 arquivos alterados estão em `C:\Users\rosep\Backups\amc-ia-mobi-antes-da-v2-2026-09-10\` |

---

## 1. O que é a v2

A pasta `amc-ia-mobiv2/` é a "versão para os alunos" (repositório `DiegoAlmeidaDev/amc-ia-alunos`, um único commit). Comparada arquivo por arquivo com o projeto, ela se revelou uma **versão mais antiga** do mesmo sistema: não tem o CaptaEstrategista, não tem a regra NADA RODA SOZINHO, não tem os 11 blocos da leitura do edital. Por cima dessa base antiga, ela acrescenta agentes e rotinas novas.

Por isso a regra da incorporação foi: **só entra o que soma. Nada que desfaça decisão da captadora.**

## 2. O que entrou

### Arquivos novos, adaptados às regras do projeto

| Arquivo | O que faz | O que foi adaptado em relação à v2 |
|---|---|---|
| `.claude/agents/captador-anexos.md` e `/projeto-anexos` | Mapeia os anexos, gera as declarações, monta o `checklist-anexos.md` | Parte dos blocos 6 e 7 do `edital.md` em vez de reextrair; três momentos separados; colunas Enviado e Data em branco; representante legal e não o contato; procura no `dossie/`; não abre documento pessoal |
| `.claude/agents/captador-contrato.md` e `/contrato` | Minuta do contrato de assessoria e análise do termo do financiador | Caminhos em `marketing/` (e não `captador/`); captação junto a empresas com o estudo de mercado como anexo do contrato; nada é enviado a ninguém |
| `.claude/agents/captador-chefe.md` e `/projeto-completo` | Chefe do CaptaSuite: triagem entre editais, validação de cada estação, parecer final | Cinco agentes, com o CaptaEstrategista; o chefe **não é porta dura**; as quatro marcas de rotulagem; a nota na escala do edital; nenhuma chamada ao CaptaHub, e o `/projeto-completo` não vale como OK para gravação nenhuma |
| `documentos/modelo-projeto-anexo-ii.md` do exemplo | Formulário oficial fictício do Instituto Semente | Nenhuma |

### Acréscimos em arquivos existentes, sem apagar frase da captadora

| Arquivo | Acréscimo |
|---|---|
| `captador-budget.md`, skill `orcamento-tecnico`, `/projeto-orcamento` | Cotação sistemática na web: 3 fontes por item relevante, mediana como valor, quadro em `cotacoes.md`. Mais a trava de privacidade na busca |
| `revisor-proposta.md`, `/projeto-revisar` | Bloco E (coerência com a OSC real) e o relatório salvo em `revisao.md` |
| `orquestrador-captacao.md` | Estação de anexos na tabela, e os caminhos `/projeto-completo` e `/contrato` |
| `minerador-web.md` | A varredura fica salva em `minhas-oscs/{ativa}/varredura-web/`, e não em `base-editais/`, porque traz o perfil do cliente |
| `scripts/verificar-acentuacao.py` | Separa CORRIGIR de CONFERIR e para de apontar nome de arquivo, caminho e comando |
| `scripts/exportar-projeto.py` | Gera PDF no Windows (Chrome ou Edge) e exporta os documentos novos |

### A exportação, por decisão da captadora durante o trabalho

A entrega final passou a levar também: `cotacoes`, `checklist-anexos`, `elegibilidade`, `score`, `revisao` e `parecer-chefe` (cada um em Word e PDF, cotações e checklist também em planilha) e a pasta `declaracoes/`. O `projeto-completo.pdf` reúne tudo.

- Elegibilidade, nota, revisão e parecer do chefe saem **marcados como uso interno, não anexar na submissão**.
- Por isso o `/projeto-exportar` deixou de indicar o `projeto-completo.pdf` como anexo de submissão: ele virou dossiê de trabalho.
- O `estrategia.md` e o `edital.md` **continuam fora**, porque essa exclusão é regra da captadora. A frase "e para qualquer arquivo da pasta que o edital não tenha pedido" foi substituída pela decisão de 10/09.

## 3. O que não entrou, e por quê

| Da v2 | Motivo |
|---|---|
| `CLAUDE.md` | Traz sincronização automática na abertura e PATCH automático no CaptaHub. Fere NADA RODA SOZINHO |
| `.claude/settings.json` e os três ganchos (`acentuacao.py`, `sem-travessao.py`, `agentes-status.py`) | Ganchos disparam sozinhos. Desligados por decisão de 01/09 |
| `.claude/rules/metodo-captar.md` e `tempo-estimado.md` | Apagam o CaptaEstrategista e voltam aos 4 agentes |
| CaptaScore com nota fixa de 0 a 10 | A regra é a escala do próprio edital |
| CaptaDoc e `/edital-analisar` antigos | Voltam à lista de 8 pontos e à reextração do edital |
| `/osc-nova` e `/osc-trocar` antigos | Sincronização automática e o fim do "contexto mínimo" |
| `/sala-agentes`, `/assessoria-estruturar`, skill `posicionamento-captador` | Voltam atrás: gancho ativo, e o fim do estudo de mercado |
| Troca de `marketing/` por `captador/` | A estrutura da captadora é `marketing/` |
| `.gitignore` | Apaga as proteções de credenciais e de relatórios detalhados |
| `base-editais/*.json` e os PDFs do exemplo | Cache e resultado de exportação, não melhoria |
| README e COMO-USAR | Texto dos alunos; ficam para decisão da captadora |

## 4. Teste

A exportação foi rodada numa cópia do exemplo, em pasta temporária, com parecer do chefe, cotações, checklist, revisão, uma declaração e um `estrategia.md` de mentira. Resultado: 28 arquivos gerados, PDFs incluídos, parecer marcado como uso interno, colunas Enviado e Data presentes, declaração sem rodapé, e **nenhum vestígio da estratégia**. Nenhum arquivo do projeto real foi tocado pelo teste.

O verificador de acentuação e a busca por travessão passaram em todos os arquivos criados ou alterados.

## 5. Pendências, todas para decisão da captadora

1. Acrescentar os três comandos e os três agentes novos às listas do `CLAUDE.md`, à tabela "Onde salvar cada entrega" e ao `tempo-estimado.md`. Não foi feito porque são arquivos de regra dela.
2. A pasta `amc-ia-mobiv2/` continua dentro do projeto, e por isso as skills dela aparecem em dobro no menu. Movê-la para fora é decisão dela.
3. Os mapas da Sala dos Agentes (`agentes-status.py`) não conhecem os agentes novos. O gancho está desligado, então não faz diferença até ela religar.
