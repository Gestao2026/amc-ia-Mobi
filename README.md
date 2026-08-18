# AMC IA

Assistente de captação de recursos para o terceiro setor, construído sobre o Claude Code. Transforma editais em projetos aprovados seguindo o Método Captar 2.0 do Portal do Captador.

É o sistema irmão do Fluxo Criativo (marketing), re-skinado para a captação. Onde o Fluxo Criativo escreve copy, a AMC IA analisa edital, escreve projeto, monta orçamento e estima a chance de aprovação.

## Relação com o CaptaHub

A AMC IA é o **estúdio de elaboração**, e trabalha junto com o CaptaHub, sem competir com ele:

- **CaptaHub** descobre editais e gerencia a carteira (pipeline, clientes, prazos). É a fonte da verdade dos editais.
- **AMC IA** recebe um edital e uma OSC e produz o projeto aprovado pelos 4 agentes, e exporta pronto.

Os editais são puxados do CaptaHub. A gestão da carteira fica no CaptaHub. Aqui o foco é elaborar o projeto.

---

## Para quem é

Mentorados da AMC IA: captadores autônomos, gestores de OSC, produtores culturais e profissionais em transição para o terceiro setor que precisam elaborar projetos para editais com método e velocidade.

## O que ele faz

- **Puxa os editais do CaptaHub** e mostra os mais alinhados ao perfil da sua OSC.
- **Analisa o edital** e extrai critérios, prazos, exigências e o que pontua.
- **Verifica a elegibilidade** antes de você escrever qualquer linha (CaptaDoc).
- **Escreve a proposta completa** bloco a bloco (CaptaBuilder).
- **Monta o orçamento técnico** por rubrica com memória de cálculo (CaptaBudget).
- **Avalia o projeto** e estima a chance de aprovação antes da submissão (CaptaScore).
- **Exporta a entrega** em Word, PDF e planilha, pronta para submeter.

## A linha de montagem

```
Minerar edital → Analisar → Elegibilidade (CaptaDoc) → Proposta (CaptaBuilder)
   → Orçamento (CaptaBudget) → Avaliação (CaptaScore) → Revisar → Submeter
```

A regra de ouro: o sistema nunca deixa você escrever a proposta antes de checar a elegibilidade. Isso elimina a dor número um do captador, descobrir tarde demais que a OSC nem era elegível.

---

## Como usar

1. Abra a pasta do projeto no Claude Code.
2. Na primeira conversa, o sistema cadastra a sua primeira OSC (`/osc-nova`).
3. Mine editais (`/edital-minerar`) ou cole um edital para analisar (`/edital-analisar`).
4. Rode a elegibilidade (`/projeto-elegibilidade`).
5. Se APTO, escreva a proposta (`/projeto-escrever`), monte o orçamento (`/projeto-orcamento`) e avalie (`/projeto-avaliar`).
6. Exporte pronto para submeter (`/projeto-exportar`).

## Estrutura do projeto

```
CLAUDE.md                  Cérebro do sistema (persona, regras, metodologia)
.claude/
  rules/metodo-captar.md   Referência completa do Método Captar
  commands/                Os comandos (o fluxo do captador)
  agents/                  Os 4 agentes + auxiliares
  skills/                  Bases de conhecimento (editais, proposta, orçamento)
  hooks/                   Guardas de qualidade (acentuação, gate de elegibilidade)
base-editais/              Cache local dos editais puxados do CaptaHub
minhas-oscs/               Dados das suas OSCs (fora do git)
  {slug}/perfil-osc.md     Perfil de cada organização
  {slug}/projetos/{edital}/  Um projeto por edital
scripts/                   Automações (CaptaHub, mineração, exportação)
sala-dos-agentes.html      Sala dos Agentes (escritório ao vivo)
painel/                    Artes da Sala dos Agentes
```

---

## Base de editais

A pasta `base-editais/` traz editais abertos exportados, organizados por escopo. Para atualizar, use `/configurar`.
