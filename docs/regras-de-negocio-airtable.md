# Regras de negócio do painel no Airtable

> Base: **MAPA CLIENTES | EDITAIS E PROJETOS** (`appKWLTFSCcWucXfQ`).
> Nome anterior: Mineração de Editais, trocado em 24/08/2026.
> Escrito em 24/08/2026. A leitura é sempre **a partir do cliente**.

---

## 0. O princípio que organiza tudo

O cliente é a entidade raiz. Edital não é trabalho, é oportunidade. Trabalho só existe quando um cliente encontra um edital, e esse encontro se chama **projeto**.

```
CLIENTE (a OSC)
   └── PROJETO (o cliente cruzado com um edital)
            └── EDITAL (a oportunidade)
                     └── FINANCIADOR (quem paga)
```

Três consequências práticas:

1. Nenhum projeto existe sem cliente vinculado. Projeto sem cliente é edital em triagem, não projeto.
2. Nenhum edital vira projeto sem antes passar pela triagem e por um cliente elegível.
3. Toda pergunta de gestão começa com "para qual cliente". Prazo, resultado e dinheiro se leem por cliente.

---

## 1. O cliente

### 1.1 Cadastro mínimo

Sem estes campos o cliente não entra na carteira operacional: OSC, CNPJ, Natureza jurídica, Data de fundação, Município, UF, Áreas temáticas, Situação.

A **Data de fundação** não é enfeite. É ela que responde à exigência de tempo mínimo de existência, presente na maioria dos editais.

### 1.2 Situação, e quem entra na carteira

**Regra de carga, definida em 24/08/2026: só sobem para o Airtable os clientes ativos,
os em negociação e os negociados. Cliente inativo não entra, e se já estiver na base,
sai.** Removidos por essa regra: ABA, Paixão por BH e GAMT.

Como a API do CaptaHub não devolve a situação comercial, quem identifica o inativo é o
captador. O script ajuda de um jeito indireto: ao rodar, ele lista quem está no CaptaHub
e fora do Airtable. Essa lista é a memória de quem ficou de fora por decisão.

| Situação | O que significa | O que pode acontecer |
|---|---|---|
| Ativa | Cliente com contrato vigente | Pode abrir projeto novo |
| Inativa | Sem contrato no momento | Não abre projeto novo. Projetos antigos seguem até o encerramento |

O campo hoje só tem esses dois valores. **Em negociação** e **Negociado** ainda precisam
ser acrescentados à lista, e opção de lista de seleção não é exposta pela API.

Este dado não vem pela API do CaptaHub, só aparece na tela web. Ou seja: quem mantém a
Situação em dia é o captador, na mão.

### 1.3 Prontidão documental (regra de bloqueio)

O campo **Documentos em dia** tem 13 itens. Oito deles formam o kit básico cobrado em praticamente todo edital:

CNPJ ativo, Estatuto social registrado, Ata de eleição da diretoria, Certidão federal (RFB/PGFN), Certidão estadual, Certidão municipal, FGTS (CRF), Trabalhista (CNDT).

| Prontidão | Condição | Regra |
|---|---|---|
| Verde | Kit básico completo | Pode submeter |
| Amarelo | Falta 1 ou 2 do kit | Pode elaborar, **não pode submeter** |
| Vermelho | Faltam 3 ou mais | Não abre projeto novo. Primeiro regulariza |

Os outros cinco itens (CEBAS, CNAS, conta bancária de projetos, Transferegov, SALIC) são condicionais: viram obrigatórios quando o edital pede.

### 1.4 Lacuna conhecida

Certidão tem validade, e o campo atual é uma caixa de seleção que não guarda data. Marcada hoje, continua marcada quando a certidão vencer, e o painel mente.

Correção necessária: cinco campos de data, um para cada certidão com validade (federal, estadual, municipal, FGTS, CNDT). Só com data existe alerta de certidão vencendo, e só assim a regra de bloqueio acima é confiável.

---

## 2. O edital

### 2.1 Triagem

| Triagem | Significado | Consequência |
|---|---|---|
| A triar | Chegou e ninguém leu | Fora dos alertas |
| Interessa | Serve para pelo menos um cliente | Entra nos alertas de prazo |
| Descartado | Não serve | Sai de tudo |

Regra: o edital só entra no alerta diário quando está marcado como **Interessa**. Edital em "A triar" com prazo curto é risco silencioso, então a triagem é tarefa de rotina, não de quando sobrar tempo.

### 2.2 Origem

CaptaHub significa espelho da fonte da verdade, com ID CaptaHub preenchido. Fora do CaptaHub significa achado próprio (web, e-mail, indicação), sem ID.

### 2.3 Quem pode propor

O campo **Proponente aceito**, na tabela Editais, diz o que o edital permite: sem fins
lucrativos, com fins lucrativos, ambos, ou não informado.

É o **primeiro corte de elegibilidade**, anterior a qualquer outro. Cruza com o campo
Natureza jurídica da tabela Clientes:

| Natureza jurídica do cliente | Vale como |
|---|---|
| Associação, Fundação, OSCIP, Organização Religiosa, Cooperativa Social | Sem fins lucrativos |
| Empresa | Com fins lucrativos |

Se não bate, nada mais importa: nem prazo, nem valor, nem qualidade da proposta.
Na dúvida, deixar em "Não informado" e confirmar na fonte antes de elaborar.

### 2.4 As duas datas do edital

Todo edital tem duas datas, e elas medem coisas diferentes:

| Data | O que é | Campo |
|---|---|---|
| **Data limite** | Prazo para enviar o projeto | Prazo de submissão |
| **Data final** | Retorno sobre aprovação ou reprovação | Data prevista do resultado |

Quatro regras, definidas pelo captador em 24/08/2026:

1. **Edital sem data limite é contínuo.** Não existe edital sem prazo por esquecimento.
   Se o campo está vazio, o alerta lê "Fluxo contínuo", com ou sem a caixa marcada.
2. **A data do resultado pertence ao edital, não ao projeto.** É a mesma para todo mundo
   que concorre. No projeto ela chega pelo campo **Resultado previsto no edital**, que
   puxa do edital vinculado. O campo Data prevista do resultado, no projeto, só se
   preenche quando aquele projeto tiver data diferente da do edital.
3. **Edital contínuo também tem data de retorno.** Não ter prazo de envio não significa
   não ter resposta.
4. **Edital sem data de retorno gera consulta ativa.** Projeto submetido, aguardando, e
   sem nenhuma data de resultado entra no alerta quinzenal por e-mail. Ninguém vai
   avisar, então a consulta é do captador.

---

## 3. O projeto

### 3.1 Os 27 status

Definidos pelo captador em 24/08/2026, substituindo as 15 etapas anteriores.

| Grupo do funil | Status |
|---|---|
| **Não submetido** | Mapeado, Selecionado, Encontrar OSC, Em Análise, Elegível, Checklist, Contrato, Enviado para OSC, Separar Documentos, Documentação Pendente, Elaborar o projeto, Pronto para Submissão, Sem Tempo Hábil |
| **Submetido** | Submetido, Recurso, Aprovado Resultado Preliminar, Aprovado, Reprovado, Em Execução, Pagamento Pendente, Prestação de Contas, Pagamento Recebido, Finalizado, Encerrado |
| **Descartado** | Inelegível, Desistiu do Edital, Encerrado Proponente |

A lógica das cores, herdada da planilha: verde escuro encerra bem, vermelho encerra mal,
laranja e amarelo estão em andamento, azul caminha para a submissão, cinza saiu.

**Sem Tempo Hábil fica em Não submetido, não em Descartado.** Perder prazo não é escolha,
e não deve se esconder entre os descartes. É a mesma razão pela qual o status de um
projeto perdido não vira Descartado (item 9.2).

### 3.2 Os três portões

**Portão 1. Elegibilidade.** Nada de elaboração antes do parecer. Projeto não sai da etapa 3 sem Elegibilidade preenchida. INAPTO NO MOMENTO manda para a etapa 4.

**Portão 2. Documentos.** Projeto não chega a "Pronto para submeter" com o cliente em prontidão vermelha ou amarela. Passa por "Documentação pendente" antes.

**Portão 3. Submissão.** Projeto não vira Submetido sem Data de submissão. É essa data que desliga o alerta de prazo e liga o alerta de resultado.

### 3.3 Campos obrigatórios por etapa

| A partir de | Passa a ser obrigatório |
|---|---|
| Elegível | Elegibilidade |
| Em elaboração | Valor solicitado |
| Pronto para submeter | Nota técnica e Chance de aprovação |
| Submetido | Data de submissão e Data prevista do resultado |
| Aprovado | Valor aprovado |

### 3.4 Tradução automática

O CaptaHub só entende 11 nomes de estágio e a operação do captador tem 15. O campo **Status CaptaHub** faz a conversão sozinho, e é esse valor que sobe na sincronização. Nunca preencher à mão.

Os campos foram renomeados em 24/08/2026: Estágio virou **Status**, e Estágio no CaptaHub virou **Status CaptaHub**.

**Grupo (auto)** classifica em Submetido, Não submetido ou Descartado. É a base das taxas do funil.

---

## 4. Cores

### 4.1 O que já tem cor

O campo **Status** já tem uma cor por etapa, do cinza (início) ao verde escuro (encerrado), com vermelho nas saídas negativas. Não precisa mexer.

### 4.2 Colorir por condição é recurso pago

O botão Cor do Airtable só oferece coloração por condição no plano Team. No plano
atual ele deixa colorir apenas por um campo de seleção único.

Solução adotada em 24/08/2026: o **círculo colorido entra dentro do texto da fórmula**.
Funciona em qualquer plano, aparece na grade, nos agrupamentos e também dentro dos
e-mails de alerta, que a regra de cor da visão nunca alcançaria.

### 4.3 Semáforo do prazo

| Sinal | Quando |
|---|---|
| 🔵 Fluxo contínuo | Sem data limite, ou caixa de fluxo contínuo marcada |
| ⛔ Prazo encerrado | A data passou |
| 🔴 Urgente | Faltam 7 dias ou menos |
| 🟠 Atenção | Faltam de 8 a 30 dias |
| 🟢 No prazo | Faltam mais de 30 dias |
| ✅ Submetido em DD/MM/AAAA | Já foi enviado, o prazo não cobra mais |

### 4.4 Semáforo do resultado

| Sinal | Quando |
|---|---|
| 🟢 Aprovado | Resultado divulgado e favorável |
| 🔴 Reprovado | Resultado divulgado e desfavorável |
| 🟠 Resultado atrasado há N dias | Passou da data prevista e ninguém respondeu |
| 🟡 Resultado sai hoje | É o dia |
| 🔵 Resultado em N dias | Contagem normal |
| 🟣 Sem data de retorno. Consulta semanal | Submetido, sem data nenhuma. Entra na consulta semanal (era quinzenal até 26/08/2026) |
| ⚪ Sem data de resultado | Ainda não submetido e sem data |

### 4.5 O que continua sendo cor de verdade

O campo **Status** tem cor por opção, e isso funciona em qualquer plano. É a única
coloração nativa da base. Se um dia houver upgrade para o plano Team, as regras de cor
por condição podem substituir os círculos, ou conviver com eles.

## 5. Alertas

| Alerta | Quando | Recorte |
|---|---|---|
| Prazo e marcos | Todo dia às 8h | Três blocos: marcos do calendário do edital em até 30 dias, editais Interessa com prazo final em até 30 dias, projetos não submetidos com prazo em até 30 dias |
| Data do resultado | Todo dia às 8h | Resultado previsto em até 7 dias, e os que passaram da data sem resposta |
| Relatório de fim de semana | Sábado às 9h | Pipeline inteiro, aguardando resultado, editais com prazo em até 30 dias |
| Consulta semanal de resultado | Toda segunda às 9h (era quinzenal; mudou em 26/08/2026) | Projetos submetidos, aguardando, sem nenhuma data de retorno prevista |

**Situação em 26/08/2026: as cinco estão PUBLICADAS e rodando.** Os e-mails vão
para gestao.mobilizando@gmail.com. Na publicação, o Relatório de fim de semana
estava inválido porque o texto do e-mail referenciava três campos já excluídos
(o Estágio antigo, Origem e um segundo campo de limpezas anteriores); a
configuração foi corrigida trocando pelos campos atuais (Status, Categoria,
Valor por projeto) antes de ligar.

Falta ainda: alerta de certidão vencendo, que depende dos campos de data do item 1.4.

---

## 6. Pendências de decisão

1. **Quem é a fonte da verdade da carteira.** Hoje a mesma informação vive em três lugares: CaptaHub, este Airtable e as pastas locais. Enquanto isso não for decidido, os três divergem em silêncio.
2. **Publicar as três automações.**
3. **Criar os cinco campos de data das certidões.**
4. **Aplicar as regras de cor dos itens 4.3 e 4.4.**
5. ~~Excluir o campo velho e a opção Contrato.~~ **Feito em 24/08/2026.** O campo
   Status ficou com exatamente as 15 etapas da planilha, e o campo órfão não existe mais.

---

## 7. Conferência com a planilha PAINEL SUBMISSÃO

Fonte: `Área de Trabalho\PAINEL SUBMISSÃO.xlsx`, sete abas, atualizada em 21/08/2026.

### 7.1 Status: conferência fechada em 15

Os 15 status da planilha estão todos no Airtable, na mesma ordem e com a mesma
classificação de grupo (Submetido, Não submetido, Descartado). A conferência bateu.

O Airtable tinha uma etapa a mais, **Contrato**, acrescentada por mim entre
"Não elegível" e "Em elaboração". O captador decidiu retirar em 24/08/2026, e o
Airtable volta a espelhar a planilha exatamente.

### 7.2 O que a planilha tinha e o Airtable não tinha (já corrigido)

| Campo criado | Onde | Por que importa |
|---|---|---|
| Tipo de edital | Editais | Lei de incentivo, emenda parlamentar, prêmio e chamada de fundação seguem regras completamente diferentes. Não se confunde com Escopo nem com Categoria |
| Valor disponível e Valor por projeto | Editais | Antes havia um campo só, com descrição ambígua. No exemplo real da planilha o edital tinha R$ 10 milhões disponíveis e teto de R$ 200 mil por projeto. Misturar os dois corrompe toda métrica financeira |
| Próxima data e Dias para a próxima ação | Editais | O marco intermediário. No exemplo, prazo final em 13/10 mas inscrições no SALIC abrindo em 15/08. Sem esse campo o painel fica calmo enquanto a ação real já venceu |
| Documentação | Projetos | Completa, Parcial, Pendente, Não iniciada, por projeto. Diferente de Documentos em dia, que é o cadastro geral do cliente |
| Perdeu o prazo | Editais e Projetos | A métrica que a planilha revelou: 6 dos 7 editais mapeados foram perdidos por prazo, nenhum por reprovação |

### 7.3 Faixas de prazo: resolvido em 7 e 30

O Airtable usava 3 e 15. A planilha usava 7 e 30. Venceram as da planilha, por decisão
do captador em 24/08/2026.

| Faltam | Passou a dizer |
|---|---|
| Até 7 dias | Urgente |
| 8 a 30 dias | Atenção |
| Acima de 30 | No prazo |

O motivo: elaborar um projeto do zero, com proposta, orçamento e documentação da OSC,
leva mais de 20 dias. Um painel que só começa a avisar aos 15 avisa quando já não dá
tempo de fazer bem feito, e isso conversa direto com o número do item 7.2, seis de sete
editais perdidos por prazo.

Alterado: as duas fórmulas de semáforo (Editais e Projetos) e o recorte do alerta
diário, que passou de 15 para 30 dias.

### 7.4 As taxas do funil que a planilha calcula

Taxa de submissão, taxa de não submissão por prazo perdido, taxa de descarte, taxa de
aprovação sobre decididos, sobre submetidos e sobre o total mapeado, e conversão
financeira (R$ aprovado dividido por R$ submetido).

Todas se reproduzem no Airtable a partir de **Grupo (auto)**, **Perdeu o prazo**,
**Resultado**, **Valor solicitado** e **Valor aprovado**. Falta montar a interface que
as mostra.

### 7.5 A regra da lista "Apto para Submissão"

Da própria planilha: editais elegíveis e dentro do prazo. Um dia após a data limite o
edital sai da lista automaticamente e passa para não submetidos por prazo perdido.
Reprovados só mudam por instrução do captador.

No Airtable isso vira uma visão filtrada de Projetos: Elegibilidade diferente de
INAPTO, Perdeu o prazo vazio, Data de submissão vazia, ordenada por Dias até o prazo.


---

## 8. O que fica visível na tela

> Nada é excluído. Ocultar campo é por visão, e o campo continua no registro: ao abrir
> um registro, o botão "mostrar campos ocultos" traz todos de volta. Nenhuma informação
> se perde, nenhuma fórmula para de funcionar.

Regra do captador, 24/08/2026: **prazo se vê, cálculo de prazo não.** Os campos
"Dias até o prazo", "Dias até o resultado" e "Dias para a próxima ação" existem para
alimentar os semáforos e os filtros, não para serem lidos. A contagem já aparece dentro
do texto do alerta, junto com o círculo colorido.

Os três cálculos têm agora um semáforo correspondente. O **Alerta de próxima ação** foi
criado em 24/08/2026 justamente para fechar essa lacuna: ele mostra círculo, contagem e
a data do marco, então tanto o cálculo quanto a Próxima data podem ficar ocultos.

> Revisão aplicada na tela em 26/08/2026, regra da captadora: só os campos-chave
> do processo ficam visíveis; todo o resto oculto, com a leitura vinda dos alertas.
> **Clientes: 9 visíveis** (Cliente, CNPJ/CPF, UF, Situação, Área temática,
> E-mail, Telefone, Contato, CaptaDrive). **Projetos: 11 visíveis** (Projeto, OSC,
> Edital, Status, Elegibilidade, Alerta de prazo, Alerta de resultado,
> Documentação, Valor solicitado, Valor captado, A captar). **Editais: 10
> visíveis** (ver 8.2). As listas antigas abaixo ficam como histórico do desenho.

### 8.1 Projetos: 10 visíveis de 25

| Visível | Por quê |
|---|---|
| Projeto | Nome do registro |
| OSC | Para qual cliente |
| Edital | Contra qual oportunidade |
| Status | Em que etapa está |
| Elegibilidade | O portão que libera a elaboração |
| Alerta de prazo | 🔴 🟠 🟢 e a contagem em texto |
| Prazo do edital | A data em si |
| Documentação | O que falta para submeter |
| Alerta de resultado | Depois do envio, é o que importa |
| Valor solicitado | Quanto está em jogo |

Ocultos: Dias até o prazo, Dias até o resultado, Status CaptaHub, Grupo (auto),
Nota técnica, Chance de aprovação, Valor aprovado, Data de submissão, Data prevista do
resultado, Resultado previsto no edital, Resultado, Perdeu o prazo, ID CaptaHub projeto,
Pasta local, Observações.

Quatro deles não somem de fato, porque já estão dentro dos alertas: Data de submissão
aparece como "✅ Submetido em DD/MM/AAAA", Resultado aparece como 🟢 Aprovado ou
🔴 Reprovado, e as duas datas de resultado viram a contagem do semáforo.

### 8.2 Editais: 9 visíveis, 4 excluídos (revisão de 26/08/2026)

Visíveis (aplicado na tela em 26/08/2026): Título, Prazo de submissão, Triagem,
URL, Alerta de prazo, Alerta de próxima ação, Valor por projeto, Categoria,
Situação do edital e **Alerta de próxima edição**.

O Alerta de próxima edição foi criado em 26/08/2026 a pedido da captadora: é o
radar do próximo ciclo em uma linha só (📅, data provável e contagem), para que
Recorrência e Próxima edição provável possam ficar ocultos. Não é prazo de
submissão e não entra nos alertas diários.

**Excluídos de vez, por decisão da captadora em 26/08/2026 (redundantes):**
Escopo (o Subtipo diz o mesmo), Instituição (repetia o vínculo Financiador),
Origem (ID CaptaHub preenchido já diz a origem) e Data de publicação (nunca
alimentou alerta nem decisão). A exclusão é feita na tela; nenhuma fórmula
dependia deles.

Todo o resto fica oculto: insumos de cálculo (Valor disponível, Teto informado,
Projetos contemplados, Próxima data, Fluxo contínuo, Data prevista do resultado),
cálculos de dias e alerta de resultado, radar (Ciclo, Recorrência, Próxima edição
provável), medidores do painel (Propostas enviadas, Não submetido), fiação
(Financiador, Projetos, Não Submetidos), consulta e chave (Descrição, Observações,
ID CaptaHub), classificação fina (Tipo de edital, Subtipo, UF, Município,
Proponente aceito).

### 8.3 Clientes: 8 visíveis de 28

OSC, Sigla, CNPJ, Situação, UF, Áreas temáticas, Documentos em dia, CaptaDrive.

Todo o resto é cadastro de consulta, que se lê abrindo o registro na hora da
elegibilidade.

### 8.4 Financiadores: 5 visíveis de 9

Financiador, Tipo, Prioritário, Pessoa de contato, Site.

### 8.5 O tamanho não se resolve só ocultando

Uma grade só, por mais enxuta, continua servindo a perguntas diferentes ao mesmo tempo.
O caminho é ter poucas visões curtas, cada uma respondendo a uma pergunta.

**Em Projetos**

| Visão | Pergunta que responde | Filtro |
|---|---|---|
| Agora | O que fazer hoje | Perdeu o prazo vazio, Resultado igual a Aguardando, ordenado pelo prazo mais curto |
| Por cliente | Como está a carteira | Agrupado por OSC |
| Apto para submeter | O que dá para enviar | Elegibilidade diferente de INAPTO, sem data de submissão, prazo aberto |
| Aguardando resultado | O que já foi e não voltou | Data de submissão preenchida, Resultado igual a Aguardando |
| Perdidos e reprovados | O que deu errado e por quê | Perdeu o prazo preenchido, ou Resultado igual a Reprovado |

**Em Editais**

| Visão | Filtro |
|---|---|
| A triar | Triagem igual a A triar |
| Interessa, prazo aberto | Triagem igual a Interessa, prazo não encerrado |
| Perdidos | Perdeu o prazo preenchido |

As cinco visões de Projetos reproduzem as abas da planilha `PAINEL SUBMISSÃO`, que já
separava Painel, Apto para Submissão, Visão Cliente e Reprovados e Não Submetidos.

### 8.6 Também é trabalho de tela

Ocultar campo e criar visão não são expostos pela API do Airtable. Só a estrutura
(campos, fórmulas, automações) é. A organização da tela é sempre manual.


---

## 9. Editais perdidos e o radar do próximo ciclo

Decidido em 24/08/2026.

### 9.1 O destino é um campo, não uma pasta

Edital com prazo vencido e sem submissão **fica na base**. Sai da lista de trabalho por
filtro, nunca por exclusão. Apagar esses registros apagaria a prova do maior problema da
operação, que é perder por prazo e não por reprovação.

O lugar para onde ele vai é o campo **Situação do edital**, que se calcula sozinho e põe
todo edital em exatamente uma destas seis situações, sem sobreposição:

| Situação | Quando |
|---|---|
| 🔵 Fluxo contínuo. Sempre aberto | Sem data limite, ou caixa marcada |
| 🟢 Aberto. Em prazo | A data ainda não chegou |
| 📤 Encerrado. Proposta enviada | Prazo passou e pelo menos um projeto foi submetido |
| ⛔ Perdeu o prazo. Interessava e não foi enviado | Prazo passou, Triagem Interessa, nenhuma proposta |
| ⚫ Encerrado. Descartado na triagem | Prazo passou e a decisão tinha sido não seguir |
| ⚪ Encerrado sem triagem. Morreu sem ser lido | Prazo passou e ninguém chegou a triar |

As três últimas parecem a mesma coisa e não são. Uma é falha de execução, outra é decisão
consciente, a terceira é falha de leitura. Só separadas elas viram diagnóstico:

- Muitos ⛔ significa que a assessoria pega mais do que dá conta de escrever.
- Muitos ⚪ significa que os editais chegam e ninguém abre. É o pior dos três, porque a
  perda acontece antes de qualquer trabalho.

O campo **Propostas enviadas (real)** conta, por edital, quantos projetos chegaram a ser
submetidos. É ele que separa o 📤 do ⛔.

> **Corrigido em 31/08/2026.** Até então quem fazia essa conta era o campo
> Propostas enviadas, um rollup que contava **datas de submissão preenchidas**.
> Nove projetos reprovados estavam sem data, a base concluiu que aquelas
> propostas nunca saíram, e o painel mostrou 36 oportunidades perdidas quando o
> número real era 27.
>
> A pergunta certa não é "tem data?", é "saiu?". O campo **Foi enviado**, em
> Projetos, responde isso: vale 1 quando existe Data de submissão **ou** quando
> Grupo (auto) diz Submetido, que já inclui Reprovado. O rollup
> **Propostas enviadas (real)** soma esse campo, e é ele que alimenta a Situação
> do edital, o campo Não submetido e a varredura das 7h.
>
> A razão de fundo: a data de submissão **não existe em nenhum sistema de
> registro**. Não está na planilha mestra, nem nas planilhas por cliente, e o
> campo `data_submissao` da API do CaptaHub repete a data de criação do registro.
> Ela só vive no comprovante do portal, salvo na pasta do cliente. Amarrar uma
> métrica a um dado que sistematicamente falta é o que quebrou a conta.

### 9.2 Não mude o Status deles

A tentação é marcar tudo como Descartado. Não. **Descartado significa "eu escolhi não
fazer", e perder prazo não é escolha.** O Status fica parado onde o projeto morreu, e
isso vira diagnóstico:

| Se a maioria morreu em | O gargalo é |
|---|---|
| Identificado | Triagem. Mapeia e não decide |
| Em análise de elegibilidade | Falta perfil de cliente pronto |
| Em elaboração | Capacidade. Pega mais do que escreve |
| Documentação pendente | O cliente, não a assessoria |

### 9.3 A regra que impede a mistura de ciclos

> **Um registro é uma edição. Edição encerrada nunca se reescreve.**

Quando a próxima edição abrir, **duplique** o registro, mude o Ciclo e as datas. O
registro antigo fica congelado com o ⛔ dele. Dois registros com o mesmo título e ciclos
diferentes são obviamente coisas diferentes, e nunca dividem a mesma lista.

| Campo | Como se preenche |
|---|---|
| Ciclo | À mão. O ano da edição |
| Recorrência | À mão. Anual, Bienal, Edição única, A verificar |
| Próxima edição provável | Automático. Prazo mais um ano (Anual) ou dois (Bienal) |

### 9.4 Prazo e radar são vocabulários separados

| Trabalho de hoje | Radar do próximo ciclo |
|---|---|
| Prazo de submissão | Próxima edição provável |
| Alerta de prazo | Visão Radar |
| Visão Agora | Visão Radar |

**Próxima edição provável não alimenta nenhum alerta de prazo nem semáforo.** Um edital
perdido em 2026 não tem como reaparecer como "vence em X dias".

Garantia mecânica, verificada em 24/08/2026: os três blocos do alerta diário filtram por
"prazo dentro dos próximos 30 dias", e data passada nunca cai nessa janela. O bloco de
marcos ainda exclui explicitamente quem tem ⛔.


---

## 10. O Painel de Captação

Criado e publicado em 24/08/2026. Não é tabela nem visão: é uma **Interface**, que é a
ferramenta de painel do Airtable. Duas páginas.

Endereço: https://airtable.com/appKWLTFSCcWucXfQ/pbdt9jTMZSU3faziO

### 10.1 Cinco páginas, uma por assunto

Decidido em 24/08/2026: em vez de uma página longa com cinco faixas, cada faixa virou uma
**aba própria** dentro da interface. Cada uma responde a uma pergunta e cabe numa tela.

| Aba | Pergunta que responde |
|---|---|
| 1. Os editais | Quanto foi mapeado e quanto vale |
| 2. Visão Atualizada | O que fecha de hoje até 30 dias |
| 3. Projetos x Clientes | Onde está o trabalho e quanto dinheiro está em jogo |
| 4. Funil de Projetos | O método está funcionando |
| 5. Não submetidos | Quanto custou não ter assessoria |

Nomes definidos pelo captador em 24/08/2026.

Cada número e cada gráfico carrega um subtítulo em cinza explicando o que mede, para não
depender de documentação externa na hora de ler.

### 10.2 As duas taxas de não submissão

Existem duas, com o mesmo nome e denominadores diferentes, por decisão do captador:

- **Taxa de não submissão** na aba 1: dos editais mapeados, quantos interessavam e se
  encerraram sem proposta.
- **Taxa de não submissão** na aba 4: dos projetos abertos, quantos passaram do prazo sem
  envio.

Um edital pode nunca virar projeto, então os dois números divergem por natureza. A
divergência é esperada, não é erro. O subtítulo de cada um diz qual é qual.

### 10.3 O valor por projeto se calcula sozinho

Definido em 24/08/2026. Três campos trabalham juntos:

| Campo | Como se preenche |
|---|---|
| Teto informado no edital | À mão, **só quando** o edital declara o teto por proposta |
| Projetos contemplados | À mão, quantas propostas o edital vai selecionar |
| **Valor por projeto** | Automático. Usa o teto informado quando existe; senão divide o valor total pelos projetos contemplados |

É o **Valor por projeto** que aparece no painel, limita o orçamento do CaptaBudget e é
copiado para a tabela Não Submetidos. Os outros dois são insumo.

A regra vale para os dois jeitos que um edital se apresenta: o que diz "teto de R$ 200 mil
por proposta" e o que diz "R$ 10 milhões, no mínimo 50 propostas selecionadas".

### 10.4 Classificação do edital

Definida em 24/08/2026, em três dimensões independentes:

| Campo | Opções |
|---|---|
| **Tipo de edital** | Lei de incentivo, Edital público, Fundo público, Transferegov, Fundo privado, Empresa privada, Internacional, Outro |
| **Subtipo** | Municipal, Estadual, Federal (para os três primeiros tipos) e Prêmio, Patrocínio, Doação (para fundo privado) |
| **Categoria** | A área de atuação: assistência social, esporte, cultura, meio ambiente e as demais |

O antigo campo Escopo fica redundante com Subtipo e pode ser ocultado. A lista antiga de
Tipo de edital foi renomeada para "APAGAR. Tipo de edital antigo" e pode ser excluída
na tela.

### 10.3 As taxas

O painel do Airtable soma e conta, mas não divide um número por outro. Duas saídas foram
usadas:

- **percentFilled**, para taxa de submissão e taxa de prazo perdido. Não exigiu campo novo.
- **Aprovado (1 ou 0)**, campo técnico em Projetos que devolve 1 para aprovado, 0 para
  reprovado e vazio para quem aguarda. A média dele é a taxa de aprovação sobre os
  decididos. Manter oculto na grade.

A conversão financeira (valor aprovado dividido por valor submetido) não tem equivalente
direto. O painel mostra os dois valores lado a lado.


---

## 11. A tabela Não Submetidos

Criada em 24/08/2026 por decisão do captador, que não quis os editais vencidos misturados
na mesma tabela dos vivos.

### 11.1 Como ela evita a divergência

Cada registro guarda apenas o essencial copiado (título, prazo que passou, valor que
passou, ciclo) e **aponta para a ficha do edital** pelo campo Ficha do edital. Situação,
Tipo e Próxima edição provável chegam por vínculo, não por cópia, então nunca divergem do
original nem envelhecem.

O edital continua existindo em Editais, com os vínculos de Financiador e Projetos
intactos. Sem isso a Situação do edital pararia de se calcular, porque ela precisa de
prazo e triagem.

### 11.2 Vocabulário: não submetido, nunca "perdeu o prazo"

Decidido em 24/08/2026. Os campos e rótulos dizem **Não submetido**, não "Perdeu o prazo".
O primeiro é fato, o segundo é acusação, e quem lê o painel é a assessoria e o cliente.
O número existe para mostrar o custo de não ter assessoria, não para atribuir culpa.

### 11.3 Os campos que só existem depois da perda

| Campo | Para quê |
|---|---|
| Motivo da não submissão | Sete opções, de "não houve tempo de elaborar" a "não foi lido a tempo" |
| O que fazer diferente | A lição, escrita enquanto está fresca |
| Retomar no próximo ciclo | Bandeira verde que põe o edital no radar da próxima edição |

O **Motivo** é o campo mais valioso da base. É o único lugar onde fica registrado por que
a oportunidade morreu, e é o que separa problema de capacidade de problema de leitura.

### 11.4 O preenchimento é automático

A automação **Enviar para Não Submetidos** roda todo dia às 7h, uma hora antes do alerta
diário, varre os editais com prazo vencido e zero propostas enviadas, e cria a ficha já
vinculada. Resta ao captador preencher o motivo e a lição.

Ela filtra também por "ainda sem ficha em Não Submetidos", e é esse filtro que impede
registro duplicado. Rodar duas vezes no mesmo dia não cria nada a mais.

**Alterada em 31/08/2026:** o filtro de "zero propostas" passou a usar
**Propostas enviadas (real)**, e não mais a contagem de datas preenchidas. A
versão anterior criou nove fichas indevidas em 27/08, para editais que tiveram
proposta reprovada. Atenção ao publicar: alteração feita pela API entra como
rascunho, e só passa a valer quando alguém abre a automação e clica em Update.

A primeira versão usava o gatilho "quando o registro entra na condição". Foi trocada em
24/08/2026 por varredura diária, porque a condição depende de um campo que muda sozinho
com a virada da data, e o recálculo desse tipo de campo no Airtable é irregular. Um
gatilho que às vezes não dispara é pior que nenhum, porque cria confiança falsa.

### 11.5 O registro não some de Editais

O edital continua existindo em Editais, e isso é necessário: sem ele, a Situação do edital
para de se calcular e os vínculos com Financiador e Projetos morrem. O que muda é que ele
deixa de aparecer no trabalho do dia:

- Os alertas por e-mail já o excluem, porque filtram por prazo dentro dos próximos 30 dias.
- O painel o separa em página própria.
- A lista que se abre para trabalhar passa a ser a tabela Não Submetidos.

Para ele sumir também da grade de Editais, basta a visão de trabalho filtrar por
Situação do edital diferente de encerrada. Isso é ajuste de tela.

---

## 12. Sincronização com o CaptaHub

Definida em 24/08/2026.

### 12.1 O que a API do CaptaHub devolve, e o que não devolve

Sondado em 24/08/2026. As rotas existentes são `/v1/me`, `/v1/clientes`,
`/v1/editais`, `/v1/projetos` e `/v1/estagios`.

**Não existem** rotas para o Checkpoint: `/v1/checkpoint`, `/v1/contratos`,
`/v1/reunioes` e `/v1/instituicoes` devolvem 404.

Consequência: a tela de Checkpoint do CaptaHub mostra reuniões, contratos,
selecionados e submissões, mas **nada disso chega pela API**. O payload de cliente
traz apenas identificação, perfil, situação documental e histórico de aprovações.
Não traz a situação comercial (ativo, em negociação, negociado).

### 12.2 A regra que resolve isso

> **O script nunca cria cliente no Airtable. Só atualiza quem já está lá.**

Como a API devolve a carteira inteira sem distinguir a situação comercial, criar
registro automaticamente subiria cliente que o captador decidiu deixar de fora.
Quem entra na carteira do Airtable é decisão humana. O script só mantém em dia o
que já foi decidido, casando pelo campo **ID CaptaHub**.

### 12.3 Campos que a sincronização nunca escreve

| Campo | Por quê |
|---|---|
| Situação | Ativo, em negociação, negociado. Não vem da API |
| CaptaDrive | Link da pasta no Drive |
| Observações estratégicas | Leitura do captador sobre o cliente |
| Pendências documentais | Texto do captador |
| Pasta local | Caminho em minhas-oscs/ |
| Responsável | Quem cuida do cliente na assessoria |

Sem essa exclusão, cada rodada apagaria o trabalho feito no Airtable.

### 12.4 Como rodar

| Arquivo | O que é |
|---|---|
| `scripts/sincronizar-clientes-airtable.py` | O script. `--simular` mostra sem gravar |
| `scripts/sincronizar-clientes.bat` | O envelope para o Agendador de Tarefas do Windows |

Registra o log junto com o do backup, em `Backups\_historico-sincronizacao.log`.

Depende de duas chaves no `.env`: `AIRTABLE_BASE_ID`, já preenchida, e
`AIRTABLE_TOKEN`, gerada em airtable.com/create/tokens com os escopos
`data.records:read` e `data.records:write` nesta base.

---

## 13. Fontes de informação (regras de origem)

Definidas pela captadora em 26/08/2026, depois que a auditoria mostrou dado
misturado de fonte não declarada. Substituem qualquer versão anterior destas regras.

### Regra 1. Dados cadastrais vêm do Cartão CNPJ do Drive

Os seis campos cadastrais da tabela Clientes (**Cliente** com a razão social,
**CNPJ/CPF**, **Natureza jurídica**, **Data de fundação**, **Município** e **UF**)
são retirados do **Cartão CNPJ que está na pasta do cliente no Google Drive**:

```
{pasta do cliente no CaptaDrive} → 01 - Gestão Documental → 03 - Atas e Constituição
```

O link da pasta de cada cliente já está gravado na coluna CaptaDrive do Airtable.
Cliente pessoa física usa o documento de CPF da mesma pasta. O nome do arquivo
varia ("CNPJ - X.pdf", "CNPJ X.pdf"), o local não.

**O circuito de correção é sempre: Cartão CNPJ → CaptaHub → Airtable.**
O cartão é a fonte; a correção se digita no CaptaHub; a sincronização espelha no
Airtable. Corrigir um desses campos direto no Airtable é trabalho perdido, porque
a próxima rodada da sincronização sobrescreve. Os três lugares ficam iguais, e o
cartão manda nos três.

Cartão digitalizado como imagem não tem camada de texto e não é legível pelo
conector: reemitir em `solucoes.receita.fazenda.gov.br/servicos/cnpjreva`.

### Regra 2. Todo campo vazio tem um de dois nomes

"Não Informado" não se digita. O campo fica **vazio** nos dois casos abaixo, e a
diferença vive em Observações, sempre com o prefixo em caixa alta. O teste é uma
pergunta só: **a fonte já foi lida?**

| Situação | Prefixo | Exemplo | Significa |
|---|---|---|---|
| Fonte lida, dado não está lá | **NÃO CONSTA** | `NÃO CONSTA: teto por projeto (edital lido em 26/08/2026)` | Não é pendência; só nova versão da fonte muda |
| Dado existe e não foi buscado | **BUSCAR** | `BUSCAR: data de fundação → Cartão CNPJ na pasta do cliente` | É pendência, já com o endereço da busca |

Buscar por "BUSCAR:" lista todas as pendências da base; "NÃO CONSTA" nunca vira
tarefa. Texto dentro de campo de valor ou data corrompe soma e filtro.

### Regra 3. Fonte de busca por tabela

Em conflito, a fonte de cima ganha, e divergência nunca se corrige em silêncio.

**Clientes.** Duas fontes: a **pasta individual do cliente no CaptaDrive** (com as
documentações) e o **CaptaHub**. O cadastro (6 campos) segue a Regra 1, Cartão
CNPJ. Só depois de o cliente estar preenchido é que as tabelas que dependem dele
(Projetos, Captações) se preenchem.

**Editais.** Duas fontes: o **CaptaHub** e a **planilha de submissões da captadora**,
`1 - Controle de Submissão_.xlsx`, em
`Desktop\_82 - Rosepaula Aparecida Andrade Rodrigues\04 - Controle de Submissão_\01 - Mineração de Editais\01 - Planejamento de Submissões`
(sempre atualizada; a cópia solta na Área de Trabalho não é a mestra). A palavra
final sobre prazo, valor e regra é sempre o **edital publicado na URL oficial**.

**Financiadores.** O **CaptaHub** e as pastas da `_82` em
`04 - Controle de Submissão_\01 - Mineração de Editais\`:
`02 - Editais Abertos` (organizada por tipo: contínuos, lei de incentivo, empresa
privada, internacionais, Transferegov, editais e fundos públicos, fundos privados),
`05 - Histórico Editais _ Enviados` e `06 - Histórico de Editais _ Não Submetidos`.

**Cliente de cada edital.** A planilha de submissões traz o nome do cliente na
linha do edital: é por ela que se descobre para quem o edital foi mapeado. Na
sequência vem a elegibilidade, e o veredito sobe para o registro do projeto.

**Demais dados:** contato do cliente vem da tela do CaptaHub (Instituições);
situação comercial é da captadora, à mão; resultado vem da publicação oficial ou
do portal de submissão; aporte de captação só entra com contrato ou comprovante.

### Regra 4. Vazio é melhor que deduzido. Na dúvida, consulte o Cartão CNPJ

Dedução nunca entra em campo oficial. Se valer registrar, vai em Observações como
`DEDUZIDO: UF=MG, a partir do município (confirmar)`, e a confirmação de dado
cadastral se faz sempre no Cartão CNPJ da pasta do cliente.

### Regra 5. Todo dado carrega fonte e data

"Cartão CNPJ emitido em 25/08/2026", "edital lido em 26/08/2026". Atenção no
Cartão CNPJ: a **Data de fundação é o campo DATA DE ABERTURA da instituição**,
impresso no cartão. A data de emissão do cartão marca só a idade da leitura, e as
duas não se confundem.

### Regra 6. Antes de afirmar, consultar

Nada de responder de memória sobre o estado de um campo ou registro: lê-se na hora.

### Regra 7. O que a API não devolve fica escrito como manual, nunca assumido

Situação comercial, nome do contato e o Checkpoint só existem na tela do CaptaHub.
Quando mudarem lá, a réplica no Airtable é gesto declarado, nunca automático.

### Regra 8. Tradução é interpretação, não fonte

Todo mapeamento (área temática a partir de texto livre, natureza jurídica a partir
de descrição) precisa do aval da captadora, e o texto original fica guardado ao
lado da tradução.

### Regra 9. Prazo se confirma na fonte antes de elaborar

Nenhum projeto entra em elaboração com prazo vindo só de índice (CaptaHub,
planilha, e-mail). A data é conferida na URL oficial e ganha o "lido em DD/MM".
É a regra que ataca a perda histórica de seis editais em sete por calendário.

---

## 14. Aprovado não é captado (a tabela Captações)

Definido pela captadora em 26/08/2026. Em lei de incentivo, o projeto aprovado
ganha **autorização para captar**, não dinheiro: o recurso só existe quando as
empresas patrocinadoras aportam. O modelo respeita essa diferença.

### 14.1 A tabela Captações

**Uma linha por aporte** que entra em projeto aprovado: Captação (nome curto),
Projeto (vínculo), Financiador (vínculo, quem aportou: em lei de incentivo é a
empresa patrocinadora, não o órgão que aprovou), Valor, Data, Observação.
Preenchida à mão, um registro por aporte.

### 14.2 Os resumos que se calculam sozinhos a partir dela

| Pergunta | Campo | Onde |
|---|---|---|
| Quanto este projeto já captou | Valor captado | Projetos |
| Quanto falta captar | A captar (aprovado menos captado) | Projetos |
| Quanto veio de cada financiador | Valor captado | Financiadores |
| Total geral do cliente | Valor captado total | Clientes |

Nenhum dos quatro se digita. **Cliente é resumo, nunca depósito de fato:** o
detalhe vive em Captações; o "por financiador" vive em Financiadores.

Projeto com status Aprovado e "A captar" maior que zero é a lei de incentivo
autorizada que ainda precisa de patrocínio, e é seção própria do relatório do
cliente.

### 14.3 Situação para o cliente (o que a OSC lê)

O que a captadora lê e o que o cliente lê não são a mesma tabela. Nota técnica,
chance de aprovação e observações estratégicas nunca saem do painel interno. O
campo **Situação para o cliente** (Projetos, oculto na grade) traduz sozinho os
27 status em 6 frases:

`Em análise` · `Em elaboração` · `Enviada, aguardando resultado` ·
`Aprovada` · `Aprovada, em captação de patrocínio` · `Não selecionada`
(e `Encerrada sem envio` para o que não avançou: Sem Tempo Hábil, Desistiu,
Inelegível, Encerrado Proponente).

### 14.4 Histórico do CaptaHub não vira número

Os campos Histórico de aprovações e Valor já aprovado (Clientes) vêm do CaptaHub
como registro do passado, sem estrutura por aporte. Servem de prova de capacidade
técnica na elegibilidade e ficam ocultos, como consulta. Não alimentam soma nem
relatório: número somável só nasce da tabela Captações.
