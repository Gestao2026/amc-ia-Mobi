# Plano de operação do MAPA CLIENTES

> ⛔ **DESLIGADO EM 31/08/2026.** A captadora encerrou o projeto MAPA e o Airtable saiu de cena.
> A base continua existindo com os dados intactos, mas **não é mais o painel operacional e ninguém a
> mantém**. Este documento vira registro histórico: não seguir nada aqui como processo vivo. Os
> scripts que falavam com a base estão em `scripts/desativados/`.

> Base **MAPA CLIENTES | EDITAIS E PROJETOS** (`appKWLTFSCcWucXfQ`).
> Escrito em 31/08/2026, a partir da leitura ao vivo da base.
> As regras de estrutura estão em `docs/regras-de-negocio-airtable.md`. Este documento
> responde a outra pergunta: **o que a captadora digita, o que a base faz sozinha e em
> que ritmo.**

---

## 1. A dinâmica em uma frase

O mapa não se atualiza por revisão geral. Ele se atualiza em **três batidas**:

| Batida | Quando | O que se toca |
|---|---|---|
| **Triagem** | Todo dia, 10 minutos | O campo Triagem dos editais que chegaram |
| **Evento** | Na hora em que o fato acontece | Dois campos do projeto que andou |
| **Fechamento** | Segunda e sábado, pelo e-mail | Nada se digita, se decide a semana |

Todo o resto (semáforo, contagem de dias, situação do edital, funil, valor por projeto,
valor captado, taxas do painel) **se calcula sozinho** a partir desses toques. Campo de
cálculo nunca se digita: digitar nele quebra a conta.

A regra de ouro do mapa é esta: **um fato, um campo, na hora em que acontece.**
Quem submete hoje e anota na sexta perde o alerta e distorce a métrica.

---

## 2. O que a base já faz sozinha (verificado em 31/08/2026)

### 2.1 As cinco automações, todas publicadas e válidas

| Hora | Automação | O que faz |
|---|---|---|
| 7h, todo dia | Enviar para Não Submetidos | Varre editais com prazo vencido e zero propostas enviadas e cria a ficha na tabela Não Submetidos, já vinculada. Não duplica |
| 8h, todo dia | Alerta diário de prazo e marcos | Três blocos: marcos do calendário em até 30 dias, editais Interessa com prazo em até 30 dias, projetos não submetidos com prazo em até 30 dias |
| 8h, todo dia | Alerta de data do resultado | Resultados previstos para os próximos 7 dias e os que passaram da data sem resposta |
| Segunda, 9h | Consulta semanal de resultado | Projetos submetidos, aguardando, sem nenhuma data de retorno prevista. É a lista de para quem ligar |
| Sábado, 9h | Relatório de fim de semana | Pipeline inteiro, aguardando resultado e editais com prazo em até 30 dias |

Todos os e-mails vão para gestao.mobilizando@gmail.com.

### 2.2 Os campos que se calculam (não digitar em nenhum deles)

- **Editais:** Alerta de prazo, Alerta de próxima ação, Alerta de próxima edição, Alerta de resultado, Situação do edital, Valor por projeto, Propostas enviadas, Não submetido e os três contadores de dias.
- **Projetos:** Alerta de prazo, Alerta de resultado, Status CaptaHub, Grupo (auto), Não submetido, Prazo do edital, Resultado previsto no edital, Aprovado (1 ou 0), Situação para o cliente, Valor captado, A captar e os dois contadores de dias.
- **Clientes:** Valor captado total.
- **Financiadores:** Valor captado.
- **Não Submetidos:** Situação, Tipo e Próxima edição provável, que chegam por vínculo.

### 2.3 A sincronização de clientes

`scripts/sincronizar-clientes-airtable.py` atualiza os clientes que **já existem** no
Airtable, casando pelo ID CaptaHub. Nunca cria cliente, e nunca escreve Situação,
CaptaDrive, Observações estratégicas, Pendências documentais, Pasta local e Responsável.

Roda sob demanda. **Ainda não está no Agendador de Tarefas**, e essa é a única automação
prevista que falta ligar.

---

## 3. O que só a captadora pode fazer

A lista abaixo é curta de propósito. Se um campo não está aqui e não é cálculo, é
cadastro que vem do CaptaHub pela sincronização.

| Tabela | Campos manuais | Quando se toca |
|---|---|---|
| **Editais** | Triagem, Categoria, Tipo, Subtipo, Proponente aceito, Prazo de submissão, Próxima data, URL, Teto informado, Projetos contemplados, Ciclo, Recorrência | Na entrada do edital e na triagem |
| **Projetos** | Projeto, OSC, Edital, Status, Elegibilidade, Documentação, Valor solicitado, Nota técnica, Chance de aprovação, Data de submissão, Resultado, Valor aprovado | A cada etapa que o projeto anda |
| **Clientes** | Situação comercial, Contato, E-mail, Telefone, CaptaDrive, Observações estratégicas | Quando a relação com o cliente muda |
| **Captações** | Todos. Um registro por aporte | Quando o dinheiro entra |
| **Não Submetidos** | Motivo da não submissão, O que fazer diferente, Retomar no próximo ciclo | Depois que a automação das 7h criar a ficha |

---

## 4. O ciclo de vida, passo a passo

### Passo 1. O edital entra

**Você faz:** confere se o registro existe; se for achado seu (web, e-mail, indicação),
cria com Título, URL, Prazo de submissão e Financiador.
**A base faz:** calcula o Alerta de prazo e a Situação do edital na hora.

> Regra 9 das fontes: o prazo se confirma **na URL oficial** antes de qualquer
> elaboração, e ganha o "lido em DD/MM" nas Observações.

### Passo 2. A triagem (o campo mais barato e mais caro da base)

**Você faz:** troca **A triar** por **Interessa** ou **Descartado**, e preenche a
**Categoria**.
**A base faz:** só o que está em Interessa entra no alerta diário. O que fica em A triar
é invisível, e quando o prazo passa vira `⚪ Encerrou sem ser triado`, a pior das perdas,
porque acontece antes de qualquer trabalho.

### Passo 3. Nasce o projeto

**Você faz:** cria o registro em Projetos com o nome no padrão `OSC — Edital`, vincula a
**OSC** e o **Edital**, e põe o Status inicial (Mapeado ou Selecionado).
**A base faz:** puxa o prazo do edital, liga o semáforo do projeto e o conta no funil.

> Sem projeto vinculado, o edital continua contando como oportunidade que ninguém pegou.

### Passo 4. Portão 1, a elegibilidade

**Você faz:** roda `/projeto-elegibilidade` e grava o veredito no campo **Elegibilidade**;
Status vai para Elegível ou Inelegível.
**A base faz:** nada muda sozinho aqui. Este portão é humano, e é o que impede escrever
projeto para quem nunca poderia ganhar.

### Passo 5. Elaboração e documentos

**Você faz:** Status andando (Checklist, Separar Documentos, Documentação Pendente,
Elaborar o projeto, Pronto para Submissão), **Documentação** (Completa, Parcial, Pendente,
Não iniciada) e **Valor solicitado** assim que o orçamento fechar.
**A base faz:** traduz o Status para o CaptaHub, classifica em Grupo (auto) e mantém a
contagem regressiva viva no e-mail das 8h.

### Passo 6. Portão 3, a submissão. **São dois campos, e só dois**

**Você faz, no dia em que enviar:**

1. **Status = Submetido**
2. **Data de submissão = a data real do envio**

**A base faz, sozinha, a partir desses dois campos:**

- o Alerta de prazo do projeto vira `✅ Submetido em DD/MM/AAAA` e para de cobrar;
- o Alerta de resultado liga, com a data que vem do edital;
- **Propostas enviadas** do edital passa de 0 para 1;
- a Situação do edital deixa de ser `⛔ Não submetido` e vira `📤 Encerrado. Proposta enviada`;
- a varredura das 7h para de criar ficha em Não Submetidos para aquele edital;
- o projeto sai do bloco de não submetidos do alerta diário e entra no de aguardando resultado;
- Situação para o cliente vira "Enviada, aguardando resultado".

> É por isso que a Data de submissão é o campo mais importante da base inteira. Sem ela,
> um projeto enviado aparece como oportunidade perdida em todos os relatórios.
> Se o edital não tinha data prevista de resultado, preencha também **Data prevista do
> resultado** no projeto, ou ele cai na consulta de segunda-feira toda semana.

### Passo 7. O resultado

**Você faz:** **Resultado** (Aprovado ou Reprovado), Status correspondente e, se aprovado,
**Valor aprovado**.
**A base faz:** o semáforo vira 🟢 ou 🔴, a taxa de aprovação do painel se recalcula, e
"A captar" nasce igual ao valor aprovado.

### Passo 8. Aprovado não é captado

**Você faz:** um registro em **Captações** por aporte que entra, com Projeto, Financiador,
Valor e Data.
**A base faz:** soma o Valor captado no projeto, no financiador e no cliente, e desconta
o "A captar" até zerar. Em lei de incentivo é assim que se enxerga o que ainda falta
patrocinar.

### Passo 9. Quando o prazo passa sem envio

**A base faz:** às 7h cria a ficha em Não Submetidos, vinculada ao edital, com prazo e
valor que passaram.
**Você faz:** preenche o **Motivo da não submissão** e **O que fazer diferente**. É o
único lugar onde fica registrado por que a oportunidade morreu, e é o que separa problema
de capacidade de problema de leitura.

> O Status do projeto perdido **não vira Descartado**. Ele fica parado onde morreu, e é
> isso que mostra qual etapa é o gargalo.

---

## 5. As rotinas

### Diária, 10 minutos, de manhã

1. Abrir o e-mail das 8h.
2. Abrir a tabela Editais e triar tudo que está em **A triar** com prazo aberto: Interessa
   ou Descartado, mais a Categoria.
3. Olhar os 🔴 e 🟠 do e-mail: para cada um, ou existe projeto aberto, ou existe a decisão
   de não concorrer.
4. Mover o Status dos projetos que andaram ontem.

### Na hora do evento (não deixar para depois)

| Aconteceu | Você digita |
|---|---|
| Submeteu | Status = Submetido **e** Data de submissão |
| Saiu o resultado | Resultado, Status e, se aprovado, Valor aprovado |
| Entrou dinheiro | Um registro em Captações |
| Perdeu o prazo | Motivo da não submissão na ficha que a base criou |

### Segunda-feira

Ler o e-mail da **consulta semanal**. Cada projeto listado ali é um telefonema ou um
e-mail para o financiador. Ao descobrir a data, gravar em Data prevista do resultado e o
projeto sai da lista.

### Sábado

Ler o **relatório de fim de semana** e decidir a semana: quais editais viram projeto,
quais projetos entram em elaboração, quais documentos precisam ser cobrados do cliente.

### Mensal

Rodar a sincronização de clientes, conferir a Situação comercial de cada cliente e o
vencimento das certidões.

---

## 6. Diagnóstico da base hoje (31/08/2026)

Leitura ao vivo, não estimativa, feita na manhã de 31/08/2026.

> **O que mudou ainda no mesmo dia.** Os pontos 1 e 3 abaixo foram resolvidos na
> tarde de 31/08. Não submetidos caiu de 36 para **27**, editais com proposta
> enviada subiu de 2 para **12**, e os dois editais que venceram sem decisão
> foram triados como Descartado. O registro completo está em
> `docs/estruturacoes/2026-08-31-25-correcao-da-contagem-de-propostas-enviadas.md`.
> Os números da tabela abaixo ficam como a fotografia de antes.

| Medida | Número |
|---|---|
| Clientes | 21, todos marcados como Ativa |
| Editais | 79 |
| Editais com prazo aberto | 15 |
| Editais em A triar | 37 |
| Editais encerrados sem proposta | 36 (32 ⛔ que interessavam, 4 ⚪ nunca lidos) |
| Editais com proposta enviada | 2 |
| Projetos | 14 (3 submetidos aguardando, 9 reprovados, 2 Sem Tempo Hábil) |
| Fichas em Não Submetidos | 36, nenhuma com motivo preenchido |
| Projetos em elaboração hoje | nenhum |

### 6.1 Sete pontos que precisam de decisão antes de operar

**1. Nove fichas indevidas em Não Submetidos. RESOLVIDO em 31/08.** Os 9 projetos
reprovados estavam sem **Data de submissão**, então a base entendia que aquelas propostas
nunca foram enviadas, e a varredura das 7h criou ficha de "não submetido" para os 9
editais deles. O número real de oportunidades perdidas era **27, não 36**.

A correção não foi achar as datas, que não existem em sistema nenhum: foi trocar o
critério. O campo **Foi enviado** marca como enviado quem tem data **ou** está no grupo
Submetido, que já inclui Reprovado, e o rollup **Propostas enviadas (real)** passou a
alimentar a Situação do edital e a varredura das 7h. *As 9 fichas antigas foram
apagadas na mesma noite, e a tabela Não Submetidos fechou com 27.*

**2. Categoria vazia em 78 dos 79 editais.** É a Categoria que cruza com a área temática
do cliente para responder "para quem serve este edital". Sem ela, a triagem é memória, e
memória é o que fez perder 6 editais em 7.

**3. Três editais vencem hoje** e nenhum tem projeto aberto: Edital 49º Amazônia Legal,
EDP e PNAB BH Fomento 2026 (Ciclo 2), este último já marcado como Interessa. O FSA/BRDE
Núcleos Criativos vence em 04/09.

**4. Trinta e sete editais em A triar,** e quatro já morreram sem nunca terem sido lidos.

**5. Elegibilidade e Documentação vazias nos 14 projetos.** Os dois portões existem no
desenho e não estão preenchidos em lugar nenhum, então nenhum dos dois bloqueia nada hoje.

**6. Não existe campo de prontidão documental no cliente.** A regra de bloqueio prevê
"Documentos em dia" com 13 itens e cinco datas de certidão. Nenhum desses campos existe
na tabela Clientes hoje. Enquanto não existirem, o Portão 2 é decisão de cabeça, e não há
como alertar certidão vencendo.

**7. Só existe "Grid view" nas três tabelas principais.** As cinco visões de trabalho
(Agora, Por cliente, Apto para submeter, Aguardando resultado, Perdidos e reprovados)
nunca foram criadas. Visão não é exposta pela API: é trabalho de tela, e é o que faz a
diferença entre uma grade de 79 linhas e uma lista de cinco coisas para fazer hoje.

---

## 7. O plano, em três semanas

### Semana 1. Fazer o número dizer a verdade

1. ~~Preencher a Data de submissão dos 9 reprovados.~~ **Feito em 31/08**, pelo critério
   novo, com as 9 fichas indevidas apagadas em seguida.
2. ~~Decidir os 3 editais que vencem hoje.~~ **Feito em 31/08:** PNAB BH Fomento foi
   submetido e ganhou projeto, Amazônia Legal e EDP foram marcados Descartado.
3. Acrescentar a coluna **DATA DE ENVIO** na planilha mestra, ao lado de STATUS. É o
   buraco que originou o problema do item 1.
4. Triar os 35 editais que continuam em "A triar", preenchendo a Categoria.
5. Preencher o **Motivo da não submissão** nas 27 fichas legítimas. É a matéria-prima do
   argumento de venda da assessoria.

### Semana 2. Ligar a tela

5. Criar as cinco visões de Projetos e as três de Editais (seção 8.5 das regras).
6. Criar o campo de prontidão documental do cliente e as cinco datas de certidão.
7. Agendar a sincronização de clientes no Agendador de Tarefas.

### Semana 3. Operar

8. Rodar a rotina diária de 10 minutos por cinco dias seguidos, sem exceção.
9. No sábado, comparar o relatório com o da semana anterior. Se o número de A triar caiu e
   nenhum edital venceu sem decisão, a rotina pegou.

---

## 8. As três frases para lembrar

1. **Um fato, um campo, na hora.** Submeteu, digita. O resto a base faz.
2. **Não digitar em campo de cálculo.** Se tem círculo colorido ou a palavra "auto", é
   leitura, não digitação.
3. **A Data de submissão é o campo mais importante da base.** Sem ela, trabalho entregue
   vira oportunidade perdida no relatório.
