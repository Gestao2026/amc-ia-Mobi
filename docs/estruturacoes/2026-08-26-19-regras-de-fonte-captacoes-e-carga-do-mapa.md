# 19 - Regras de fonte, tabela Captações, automações ligadas e a primeira carga do mapa

| Campo | Valor |
|---|---|
| Data | 2026-08-26 |
| Pasta afetada | Base Airtable `appKWLTFSCcWucXfQ`, `docs/regras-de-negocio-airtable.md`, memórias do projeto |
| Tipo | Regras de negócio, estrutura, publicação de automações e carga de dados |
| Situação | Concluída, com as correções listadas no item 6 a cargo da captadora |
| Autorizada por | A captadora, decisão a decisão, ao longo da sessão |
| Reversível | Registros criados podem ser apagados; automações podem ser desligadas na tela |

## 1. O que foi feito, na ordem

1. **Contato dos 21 clientes preenchido** a partir da tela de Instituições do CaptaHub
   (o dado não vem pela API). Achados de passagem: Semear está "Pendente" no CaptaHub
   e "Ativa" no Airtable; o e-mail da STK está grafado `gamil.com` nos dois sistemas.
2. **Regra 1 formalizada:** cadastro vem do Cartão CNPJ, circuito Cartão → CaptaHub → Airtable.
3. **Tabela Captações criada** (aprovado não é captado): uma linha por aporte, com os
   quatro resumos automáticos (Valor captado em Projetos, A captar, Valor captado por
   Financiador, Valor captado total no Cliente) e o campo Situação para o cliente
   (27 status viram 6 frases, incluindo "Aprovada, em captação de patrocínio").
4. **Limpeza de Editais:** excluídos Origem, Instituição, Escopo e Data de publicação
   (redundantes) e as duas linhas em branco; grades enxugadas (Editais 10 visíveis,
   Clientes 9, Projetos 11) e criado o **Alerta de próxima edição** (radar em uma linha,
   com Recorrência e Próxima edição provável ocultos).
5. **As 5 automações publicadas.** O Relatório de fim de semana estava inválido porque
   o e-mail referenciava três campos já excluídos; corrigido pela API antes de ligar.
   A consulta de resultado **virou semanal** (era quinzenal), a pedido da captadora.
6. **As 9 regras de fonte definidas** (seção 13 do documento de regras): NÃO CONSTA
   versus BUSCAR, fontes por tabela (planilha mestra da `_82`, CaptaHub, pastas de
   históricos), vazio melhor que deduzido, fonte e data em tudo, prazo confirmado na URL.
7. **Primeira carga do mapa**, da planilha mestra `1 - Controle de Submissão_.xlsx`
   (abas GERAL, REPROVADOS, EXCLUIDOS): **40 financiadores, 79 editais, 14 projetos**,
   com prévia aprovada antes (arquivo `previa-carga-airtable.xlsx` enviado à captadora).
   O banco de 2.196 editais do CaptaHub não entra em bloco: é descoberta, não trabalho.

## 2. Estado depois

Semáforos e situações calculando ao vivo: EDP, Fundo Ecos e PNAB BH Fomento urgentes
(5 dias), FSA/BRDE em atenção (9 dias); SNSA/MCID e Multilinguagens marcados
"📤 Proposta enviada"; contínuos em 🔵. E-mails diários passam a sair com conteúdo.

## 3. Rastreabilidade

`docs/regras-de-negocio-airtable.md` (seções 13 e 14, e revisões nas seções 5 e 8),
memórias `regras-de-fonte-airtable`, `painel-airtable-mapa-clientes`,
`cartao-cnpj-e-a-fonte-do-cadastro`, e os scripts da sessão no scratchpad
(`gerar_previa.py`, `gravar_carga.py`).

## 4. Como reverter

Registros criados na carga podem ser apagados em lote (Financiadores, Editais e
Projetos criados em 26/08 às 18h28). Automações se desligam pelo botão da tela.
Campos excluídos de Editais estão na lixeira do Airtable por tempo limitado.

## 5. Pendências que ficaram com a captadora

1. **Data de submissão dos 9 projetos reprovados** (BUSCAR): sem ela, a varredura das
   7h cria fichas indevidas em Não Submetidos para os editais deles; apagar as fichas
   indevidas e preencher as datas quando localizar.
2. **BIP Prosas** entrou como um registro só (eram duas linhas: Lei Esporte e Lei
   Rouanet); separar se forem editais distintos.
3. **PNAB BH Fomento (5 dias):** definir quais clientes concorrem e abrir os projetos.
4. Conferir Semear (Pendente × Ativa) e o e-mail da STK (`gamil.com`).
5. Segunda rodada de carga: conciliar os 66 itens do pipeline do CaptaHub.
6. Ainda da lista antiga: campos de data das certidões, opções "Em negociação" e
   "Negociado" na Situação, agendar a sincronização de clientes no Agendador.
