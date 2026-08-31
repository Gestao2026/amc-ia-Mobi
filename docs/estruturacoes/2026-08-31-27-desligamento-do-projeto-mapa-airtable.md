# 27 - Desligamento do projeto MAPA e saída do Airtable

| Campo | Valor |
|---|---|
| Data | 2026-08-31 |
| Pasta afetada | `scripts/`, `scripts/desativados/`, `docs/`, memória persistente |
| Tipo | Desligamento de sistema, com preservação do dado |
| Situação | Concluída. **1 ponta solta**, no item 5 |
| Autorizada por | A captadora, que comunicou o encerramento do projeto MAPA e confirmou o alcance: o projeto inteiro, o Airtable sai de cena |
| Reversível | Sim. Nada foi apagado. A base continua íntegra e os scripts saem da trava renomeando e removendo o bloco do topo |

---

## 1. O que foi decidido

A captadora encerrou o **projeto MAPA**, a base Airtable `appKWLTFSCcWucXfQ`
("MAPA CLIENTES | EDITAIS E PROJETOS"), montada em 24 e 25/08/2026. O alcance foi
confirmado por ela: não são só as automações nem só a sincronização, é **o projeto
inteiro**. O Airtable sai de cena.

O motivo não foi registrado aqui porque não foi dito, e não se inventa razão em
registro.

## 2. O dado não foi tocado

Antes de qualquer coisa, a base foi lida ao vivo. As 6 tabelas respondem e têm
registro: Clientes, Editais, Projetos, Financiadores e Não Submetidos com dados,
Captações vazia (nunca chegou a receber aporte).

**Nada foi apagado.** O que terminou foi o papel da base, não o conteúdo. Ela
passa a ser registro histórico do período de 24/08 a 31/08/2026.

## 3. O que foi desativado

Três scripts falavam com a base e podiam ser chamados por engano. Foram para
`scripts/desativados/` pelo procedimento que já existia na pasta: extensão trocada
para `.desativado` e trava interna no topo, testada, que interrompe com saída 1 e
aponta o LEIA-ME.

| Script | O que fazia |
|---|---|
| `sincronizar-clientes-airtable.py` | Puxava a carteira do CaptaHub e atualizava o Airtable |
| `sincronizar-clientes.bat` | Atalho do Agendador do Windows para o anterior. Nunca chegou a ser agendado |
| `ler-planilha-submissao.py` | Lia a planilha mestra e comparava com o Airtable, gravando Status e Data de submissão com `--aplicar` |

O terceiro merece atenção: **a parte que lê a planilha continua boa**. Se um dia a
comparação passar a ser com o CaptaHub, é dali que se parte, não do zero.

## 4. O que foi marcado como histórico

- `docs/plano-operacao-mapa-airtable.md` e `docs/regras-de-negocio-airtable.md`, com aviso no topo.
- Memórias `painel-airtable-mapa-clientes`, `sincronizacao-captahub-airtable` e `regras-de-fonte-airtable`, com o mesmo aviso, e as três linhas do índice reescritas.
- Memória nova `projeto-mapa-airtable-desligado`, que é o ponto de entrada do assunto.
- `docs/reconciliacao-pipeline-captahub.md`, onde o Airtable aparecia como risco de id quebrado. Deixou de ser risco.

O `CLAUDE.md` não citava o Airtable em nenhum ponto, então não precisou de ajuste.

## 5. Onde ficou a triagem (resolvido no mesmo dia)

A pergunta era onde passa a viver o "isto interessa, aquilo não", já que o campo
`Triagem` do Airtable morreu com o MAPA. A captadora respondeu: **fica na planilha
mesmo.**

Ao abrir a planilha mestra, a triagem já estava lá, e sempre esteve. **Triar é mover
a linha de aba**, e é assim que funcionava antes de o Airtable existir:

| Aba | O que significa | Linhas em 31/08 |
|---|---|---|
| `GERAL` | Em jogo, é o que se trabalha | 52 |
| `EXCLUIDOS` | Descartado por decisão | 100 |
| `REPROVADOS` | Foi submetido e não passou | 102 |
| `TABELA DE PROJETOS` | vazia | 0 |
| `Status` | dicionário com os 25 status válidos | 25 |

O campo `Triagem` do Airtable era uma reimplementação disso. Não se recria em outro
lugar sem ela pedir.

**Duas lacunas ficam registradas, as duas para ela decidir:**

1. **Não existe estado "a triar".** Edital novo cai direto na `GERAL` e ou fica, ou
   vai para `EXCLUIDOS`. Quem nunca foi olhado não se distingue de quem foi olhado e
   aprovado. O Airtable tinha esse estado e ele se perde aqui.
2. **Não existe coluna DATA DE ENVIO.** Já era a pendência 3 do registro 25, e agora
   pesa mais: com o Airtable fora, a planilha virou o único lugar onde essa data
   poderia viver.

## 6. Rastreabilidade

`scripts/desativados/LEIA-ME.md`, memória `projeto-mapa-airtable-desligado`, e os
registros anteriores do MAPA: `2026-08-25-18`, `2026-08-26-19` e `2026-08-31-25`.
