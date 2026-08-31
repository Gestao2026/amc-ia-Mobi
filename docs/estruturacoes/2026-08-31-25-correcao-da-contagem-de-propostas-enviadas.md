# 25 - Correção da contagem de propostas enviadas e a ponte com a planilha

| Campo | Valor |
|---|---|
| Data | 2026-08-31 |
| Pasta afetada | Base Airtable `appKWLTFSCcWucXfQ` (tabelas Projetos e Editais, uma automação), `scripts/`, `docs/` |
| Tipo | Correção de regra de negócio, criação de campo, ajuste de fórmula e script novo |
| Situação | Concluída. **2 pendências com a captadora**, listadas no item 6 |
| Autorizada por | A captadora, passo a passo: confirmou que os nove projetos foram submetidos e reprovados, autorizou a correção, o `--aplicar` e a criação do projeto do PNAB BH Fomento |
| Reversível | Sim. Campos novos podem ser excluídos, fórmulas têm a versão anterior transcrita no item 5, e a automação tem `revert_action` pelo actionId |

---

## 1. Por que foi feito

A pergunta da captadora era outra: como manter o mapa em dia, o que é manual e o
que é automático. Ao ler a base ao vivo para responder, apareceu um erro que
tornava a resposta inútil.

**O painel dizia 36 oportunidades perdidas por prazo. O número real era 27.**

A causa: a coluna **Propostas enviadas** era um rollup que contava quantos
projetos ligados ao edital tinham a **Data de submissão** preenchida. Nove
projetos reprovados estavam sem essa data, então a base concluía que aquelas
propostas nunca saíram. Como consequência:

- a **Situação do edital** desses nove marcava `⛔ Não submetido`, e não `📤 Proposta enviada`;
- a varredura das 7h criou, em 27/08, nove fichas indevidas em Não Submetidos;
- a métrica mais importante da operação, a que mostra ao cliente o custo de não
  ter assessoria, estava inflada em um terço.

O erro não era de digitação. Era de premissa: a base perguntava "tem data?"
quando a pergunta certa é "saiu?".

## 2. O que se descobriu sobre a data de submissão

Antes de gravar qualquer coisa, procurou-se a data real em cinco lugares. **Ela
não existe em nenhum sistema de registro.**

| Fonte | Resultado |
|---|---|
| Planilha mestra `1 - Controle de Submissão_.xlsx` | Não tem coluna de data de envio. Só DATA LIMITE e PRÓXIMA ETAPA |
| Planilhas por cliente no CaptaDrive | Idem. Conferido na do Coletivo Medêdicas, que sozinha cobre 4 dos 9 |
| Gmail (conector) | Aponta para editais.mobilizando, que não recebe confirmação de portal. Busca voltou vazia |
| API do CaptaHub | **Armadilha:** o campo `data_submissao` repete o `created_at` na maioria dos registros (dezenas de projetos em `encontrar_cliente` com 06/08, o dia da carga). Não serve de fonte |
| Pastas do CaptaDrive | Onde a data realmente está, nos comprovantes. Encontrados três |

Comprovantes localizados, todos em `{cliente}/{NN - Edital X}/04 - Projeto/`:

| Projeto | Arquivo | Data |
|---|---|---|
| e-Missão × VEC/BH | `COMPROVANTE DE SUBMISSÃO.png`, print do formulário do TJMG com "Sua resposta foi registrada" | 15/05/2026, 18h48 |
| e-Missão × PAPS 2027 | `ENTREGA EDITAL PAPS.jpg`, print da Fundação Salvador Arena com "recebemos o Resumo da Proposta" | 13/07/2026, 18h |
| e-Missão × FUNDO OSC MROSC | `INSCRIÇÃO EDITAL MROSC 2026.png` | print salvo 01/06 às 00h10, prazo 31/05. Ambíguo, não gravado |

O print costuma não trazer a data impressa: quem data é o `modifiedTime` do
arquivo. Por isso só duas datas foram gravadas.

## 3. O que foi executado

1. **Campo novo em Projetos: `Foi enviado`** (fórmula). Devolve 1 quando existe
   Data de submissão **ou** quando `Grupo (auto)` diz Submetido, que já inclui
   Reprovado, Aprovado, Recurso e Em Execução.
2. **Campo novo em Editais: `Propostas enviadas (real)`** (rollup). Soma o
   `Foi enviado` dos projetos ligados, em vez de contar datas.
3. **Três fórmulas religadas** ao campo novo: `Situação do edital` e
   `Não submetido` (Editais), e `Não submetido` (Projetos).
4. **`Alerta de prazo` (Projetos)** ganhou um degrau: projeto enviado sem data
   agora lê `✅ Enviado. Data a confirmar`, em vez de `⛔ Prazo encerrado`.
5. **Automação das 7h** teve o filtro trocado de `Propostas enviadas` para
   `Propostas enviadas (real)`.
6. **Duas datas gravadas** (VEC/BH e PAPS) com a fonte escrita nas Observações,
   e **sete Observações com `BUSCAR: data de submissão`** e o endereço exato de
   onde buscar. Nenhuma data foi deduzida.
7. **Dois editais triados** a pedido da captadora, no dia do prazo: Edital 49º
   Amazônia Legal e EDP passaram a **Descartado**. Descartado é decisão
   consciente e fica separado de "encerrou sem ser triado", que é falha de leitura.
8. **Script novo `scripts/ler-planilha-submissao.py`**: lê a planilha mestra,
   compara com o Airtable e mostra as diferenças. Não grava nada por padrão.
9. **Status do SNSA/MCID corrigido** para Reprovado (pelo script) e **Resultado**
   para Reprovado, fechando a incoerência entre os dois campos.
10. **Projeto criado:** Coletivo Medêdicas × PNAB BH Fomento 2026 (Ciclo 2),
    submetido em 31/08, R$ 80.000, com o id do CaptaHub gravado.

## 4. Estado antes e depois

| Medida | Antes | Depois |
|---|---|---|
| Editais não submetidos | 36 | **27** |
| Editais com proposta enviada | 2 | **12** |
| Projetos no Airtable | 14 | 15 |
| Projetos com Data de submissão | 3 | 5 |
| Projetos marcados como enviados | 3 | **12** |
| Editais em "A triar" | 37 | 35 |
| Fichas em Não Submetidos | 36 | **27** (as 9 indevidas foram apagadas) |

O script de leitura da planilha, na primeira execução, encontrou: 84 linhas com
edital preenchido, **0 editais faltando no Airtable**, **0 prazos divergentes**,
7 projetos que existem na planilha e não no Airtable, e 1 status divergente.

## 5. Como reverter

Os dois campos novos (`Foi enviado`, `Propostas enviadas (real)`) podem ser
excluídos na tela. As fórmulas anteriores, para copiar de volta:

- **Situação do edital:** idêntica à atual, trocando `{Propostas enviadas (real)}` por `{Propostas enviadas}`.
- **Não submetido (Editais):** a condição `{Propostas enviadas (real)} = 0` era ausente.
- **Não submetido (Projetos):** a condição `{Grupo (auto)} != "Submetido"` era ausente.
- **Alerta de prazo (Projetos):** o degrau `IF({Foi enviado} = 1, "✅ Enviado. Data a confirmar", ...)` era ausente.

A automação tem `actionId` `actfaNBhrrwFRTbhV`, revertível por `revert_action`.
A coluna antiga **Propostas enviadas** não foi excluída: continua na tabela, sem
alimentar nada, e pode ser ocultada.

## 6. Pendências com a captadora

1. ~~Publicar a automação.~~ **Feito na mesma noite.** Ver o item 8 abaixo: não
   existia botão a apertar, e a mudança já estava valendo.
2. ~~Apagar as nove fichas indevidas.~~ **Feito na mesma noite.** A tabela Não
   Submetidos ficou com 27 registros.
3. **Acrescentar a coluna DATA DE ENVIO** na planilha mestra, ao lado de STATUS.
   É o buraco que originou tudo, e o script avisa toda vez até ela existir.
4. **Sete projetos** existem na planilha e não no Airtable: Almira Lopes ×
   Essencis e × MAPFRE, STK × Shell, Ponto Cultural × Ambev e × Usiminas,
   e-Missão × Prefeitura de BH. O oitavo, PNAB BH Fomento, já foi criado.

Ainda em aberto, de sessões anteriores e reconfirmado hoje: a data do MROSC, o
prazo real dos dois PNAB SECULT (a Secult prorrogou os editais do Ciclo 2), a
Categoria vazia em 78 dos 79 editais, a ausência de campo de prontidão
documental na tabela Clientes e as cinco visões de trabalho que nunca foram
criadas.

## 7. Achados de passagem

- **A carteira e o funil de editais não conversam.** Dos 41 editais vivos, cerca
  de 24 são patrocínio incentivado, que exige projeto **já aprovado** em lei de
  incentivo. Só três clientes têm isso: STK, Bandeja Films e Berê Xikrin. Outros
  seis clientes são Empresa ou "Outra" e são cortados por todo edital que exige
  OSC sem fins lucrativos.
- **Encaixes parados sem ninguém pegar:** Banco Nordeste/FAVORECICLE com os
  Catadores de Itabuna, Consulado do Japão com a Santa Casa e a Mãos Unidas,
  Fundos da Infância e da Adolescência (prazo 13/09) com e-Missão, Levanta e
  Brilha e Rede Amor e Compaixão.
- **O CaptaHub tem 58 projetos e o Airtable 15.** A reconciliação segue pendente.
- **VEC/BH:** a planilha marca Reprovado e a observação da mesma linha diz
  "Aprovado, 30 dias para abertura da conta". As duas coisas não podem ser
  verdade, e isso não foi resolvido hoje.

## 8. O botão de publicar que não existe

Ao alterar uma automação pela API, a ferramenta avisa que a mudança fica como
rascunho e só passa a valer quando alguém clica em **Update** na tela do
Airtable. Esse aviso levou a captadora a procurar, sem sucesso, um botão em
quatro telas diferentes.

**O botão não existe.** Verificado ao vivo em 31/08/2026, pelo navegador: a tela
da automação tem apenas "História" e "Automação de testes". Ao abrir a automação
no editor e rodar o teste do passo, a consulta `get_automation` passou a devolver
`deployedVersion: null`, ou seja, o que roda e o rascunho voltaram a ser a mesma
coisa. A alteração feita pela API entrou em vigor sozinha.

Regra para as próximas vezes: **depois de alterar uma automação pela API,
conferir com `get_automation` e `includeDeployedVersion: true`.** Se
`deployedVersion` vier `null`, está publicado. Não mandar ninguém procurar botão.

O teste do passo "Encontre registros" é leitura pura e não cria nada. Já testar a
**automação inteira** cria registro de verdade, e não deve ser usado para
conferência.

**Sujeira gerada e removida:** durante essa navegação foi criado um registro em
branco na tabela Não Submetidos, às 19h32, sem edital e sem vínculo. Foi apagado
na sequência. A tabela fechou com 27.

## 9. Rastreabilidade

`docs/plano-operacao-mapa-airtable.md` (o plano de operação escrito hoje),
`scripts/ler-planilha-submissao.py`, memória
`data-submissao-nao-existe-nos-sistemas`, e a página publicada com o plano:
https://claude.ai/code/artifact/ca7d7f47-2b5b-4a9f-bfc1-22554339eacf
