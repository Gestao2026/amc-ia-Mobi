# Modelo do CaptaDrive por instituição

> Reconstruído em 05/09/2026 a partir da pasta viva
> `G:\Meu Drive\_82 - Rosepaula Aparecida Andrade Rodrigues\06 - Clientes\02 - CaptaDrive - E-Missão`,
> cruzada com o esqueleto em branco da mentoria (`18 - Outros Modelos`) e com
> `docs/estrutura-padrao-82.md`. A e-Missão é o exemplo porque é o cliente mais
> completo: 21 pastas de cliente seguem o mesmo desenho.
>
> Três termos, e só três, para falar do modelo:
>
> - `[INSTITUIÇÃO]` é o cliente. Uma pasta por cliente.
> - `[PASTA]` é cada subpasta numerada dentro do cliente. Tem nome fixo e finalidade fixa.
> - `[EDITAL]` é o edital trabalhado. Uma pasta por edital, com as mesmas subpastas sempre.

---

## `[INSTITUIÇÃO]`. A pasta do cliente

```
06 - Clientes\
└── NN - CaptaDrive - [INSTITUIÇÃO]\
    ├── 01 - Gestão Documental\        ← seção 1, as [PASTA]
    ├── 02 - Editais\                  ← seção 2, os [EDITAL]
    └── 1 - Controle de Submissão.xlsx
```

**O que é.** Tudo o que existe de um cliente na assessoria fica dentro de uma única
pasta, chamada `NN - CaptaDrive - [INSTITUIÇÃO]`. O `NN` é a ordem de entrada na
carteira (a e-Missão é a `02`), e `[INSTITUIÇÃO]` é o nome pelo qual o cliente é
conhecido, não a razão social.

**Por que só três coisas na raiz.** A raiz do cliente tem exatamente duas pastas e
uma planilha. Nada de arquivo solto. Se um documento não cabe em nenhuma
`[PASTA]` nem em nenhum `[EDITAL]`, o lugar dele ainda não foi decidido, e ele
espera fora da raiz, nunca dentro dela.

**A planilha.** `1 - Controle de Submissão.xlsx` é a memória de tudo o que foi
tentado para aquela `[INSTITUIÇÃO]`. A aba `SUBMISSÕES` tem uma linha por edital,
com número, nome, descrição, recurso disponível, recurso por projeto, data limite,
link, prazo, status e observação de andamento. A aba `Status` é a lista dos
estados possíveis. É a única gestão de carteira que vive na pasta; o resto está no
CaptaHub.

**As duas variantes.** O desenho de `01 - Gestão Documental` depende da natureza
jurídica, nunca de quem organiza:

| Natureza da `[INSTITUIÇÃO]` | `01 - Gestão Documental` recebe |
|---|---|
| OSC (associação, fundação, instituto) | as sete `[PASTA]` da seção 1 |
| Produtora, empresa, MEI, pessoa física | duas: `01 - Documentos` e `02 - Portfolio` |

`02 - Editais` é igual nas duas variantes.

---

## 1. `[PASTA]`. As sete pastas da Gestão Documental

```
01 - Gestão Documental\
├── 01 - Declarações
├── 02 - Informações Institucionais
├── 03 - Atas e Constituição
├── 04 - Certidões Negativas
├── 05 - Alvarás e Licenças
├── 06 - Dados Bancários
└── 07 - Serviços
```

**O que é.** A Gestão Documental é o dossiê permanente da `[INSTITUIÇÃO]`: o que
serve para todo edital, independentemente de qual. Cada `[PASTA]` guarda um tipo
de documento, e o tipo não muda de cliente para cliente. Quando o CaptaDoc monta o
checklist de um edital, é daqui que ele tira os documentos.

**A regra da `[PASTA]`.** Toda `[PASTA]` é criada no dia em que o cliente entra,
mesmo sem documento. Pasta vazia é estrutura, não sobra: ela diz onde o documento
vai cair quando chegar. Nunca se apaga, nunca se relata como pendência.

**O que vai em cada uma, com o exemplo da e-Missão:**

| `[PASTA]` | O que guarda | Como está na e-Missão |
|---|---|---|
| `01 - Declarações` | Declarações emitidas por conselhos e órgãos que atestam a inscrição ou o funcionamento da `[INSTITUIÇÃO]` | Declaração do CMAS e declaração do CMDCA |
| `02 - Informações Institucionais` | O que apresenta a organização: portfólio, dossiê do proponente, missão, visão, valores, logo, fotos | Portfólio institucional e dossiê do proponente |
| `03 - Atas e Constituição` | O que prova que a `[INSTITUIÇÃO]` existe e quem responde por ela. Três subpastas: `01 - Procuração e Contrato` (procuração para a assessoria, contrato de prestação de serviço, nota técnica da presidência), `02 - Ata e Estatuto` (estatuto vigente, alterações registradas, atas de eleição e assembleia por ano) e `03 - Outros Documentos` (cartão CNPJ, comodato da sede, documento e comprovante de endereço do dirigente) | Estatuto antigo e alteração registrada, atas de 2023 a 2026, procuração assinada, contrato, CNPJ, comodato |
| `04 - Certidões Negativas` | As certidões que todo edital pede, mais um arquivo com os links para renová-las | CND federal, estadual, municipal, FGTS, taxa de fiscalização e o documento `LINK DAS CERTIDÕES` |
| `05 - Alvarás e Licenças` | O que autoriza a sede a funcionar | Alvará de localização e funcionamento, dispensa sanitária, laudo dos bombeiros, ART do laudo de segurança, viabilidade |
| `06 - Dados Bancários` | Conta da `[INSTITUIÇÃO]` e a prova de saúde financeira: balanço, DRE, relatório financeiro | Balanços de 2024 e 2025, DRE de 2024, relatório financeiro |
| `07 - Serviços` | As habilitações: cada registro ou inscrição que mantém a `[INSTITUIÇÃO]` apta a captar, uma subpasta por órgão, organizada por ano dentro dela | `01 - CMAS`, `02 - CMDCA`, `03 - CEBAS`, `04 - OSCIP`, `05 - Ministério da Cultura`, `06 - Ministério do Esporte`, `07 - Diagnóstico Escola` |

**Habilitação não é `[EDITAL]`.** A `07 - Serviços` é a `[PASTA]` que mais cresce e
a que mais confunde. CMAS, CMDCA, CEBAS, OSCIP e as certificações dos ministérios
não são editais: são registros que mantêm a organização elegível. Sem eles, o
CaptaDoc reprova antes de olhar o mérito. Por isso ficam na Gestão Documental e não
em `02 - Editais`. Dentro de cada órgão, a organização é por ano (`2024`, `2025`,
`2026`), com uma pasta de orientações e modelos ao lado.

---

## 2. `[EDITAL]`. Uma pasta por edital, sempre com as mesmas subpastas

```
02 - Editais\
├── 00 - Projeto Base [NOME]\          ← projeto reaproveitável, não é edital
└── NN - Edital [EDITAL] - [RESULTADO]\
    ├── 01 - Edital
    ├── 02 - Anexos
    ├── 03 - Manuais
    ├── 04 - Projeto
    ├── 05 - Orçamento
    ├── 06 - Resultados
    └── 07 - Documentos Específicos
```

**O que é.** Cada edital em que a `[INSTITUIÇÃO]` entrou, ou avaliou entrar, ganha
uma pasta própria, `NN - Edital [EDITAL]`. O `NN` é a ordem em que os editais foram
trabalhados, e `[EDITAL]` é o nome curto do edital ou do financiador (MROSC, TJMG
VEC, Fundo Brasil, SNJ, CESE, Paps Arena, Multilinguagens). A pasta é por edital,
nunca por ano nem por órgão.

**O resultado entra no nome.** Quando o edital termina, o nome da pasta ganha o
sufixo: `- Aprovado`, `- Reprovado`. Assim a lista de `02 - Editais` já é o
histórico da `[INSTITUIÇÃO]`, sem abrir nada. Na e-Missão: MROSC reprovado, TJMG
VEC reprovado, SNJ aprovado, CESE reprovado, Paps Arena reprovado, Fundo Brasil e
Multilinguagens ainda sem resultado.

**Projeto base não é `[EDITAL]`.** Um projeto que a organização reaproveita em
vários editais fica em `00 - Projeto Base [NOME]`, no início da lista. Ele guarda a
versão-mãe do texto, as fotos e os documentos do parceiro. Quando um edital abre,
o projeto base é copiado para o `04 - Projeto` daquele `[EDITAL]` e adaptado lá. Na
e-Missão são três: Afegãos, Capacitar PPP e GF ConectAI.

**As sete subpastas, sempre as mesmas, criadas no dia em que o `[EDITAL]` é aberto:**

| Subpasta | O que guarda | Como está na e-Missão |
|---|---|---|
| `01 - Edital` | O edital oficial em PDF, erratas, retificações, lista de aprovados publicada e o print da tela de inscrição | SNJ: o edital e a convocação; TJMG VEC: o edital, a nova data do resultado e a lista de aprovados |
| `02 - Anexos` | Os anexos que o edital fornece e a `[INSTITUIÇÃO]` preenche: ficha de inscrição, modelo de proposta, plano de trabalho, cartas de anuência, procuração específica | Multilinguagens: as cartas de anuência e os e-mails que as pediram; MROSC: ficha de inscrição assinada e modelo de proposta |
| `03 - Manuais` | Tudo o que ensina a responder: cartilha, manual da plataforma, checklist do edital, passo a passo, orientações de execução | SNJ: doze manuais numerados, do cadastro na plataforma ao repasse financeiro |
| `04 - Projeto` | O texto do projeto em todas as versões, o formulário preenchido, as declarações que acompanham e o comprovante de submissão | SNJ: `01 - Execução` (plano de curso, cronograma) e `02 - Projeto Modelo`; TJMG VEC: o projeto, a matriz de vinculação financeira e o comprovante |
| `05 - Orçamento` | A planilha de orçamento no modelo do edital, com cronograma de desembolso e justificativa | MROSC: cronograma de execução e orçamento no Anexo III; Fundo Brasil: modelo de planilha do financiador |
| `06 - Resultados` | O que o financiador respondeu: e-mail de resultado, lista de habilitados e inabilitados, comunicado oficial, e depois os relatórios de execução | TJMG VEC: comunicado oficial e relação de inabilitadas; Afegãos: relatório descritivo e fotos |
| `07 - Documentos Específicos` | Documento que só este `[EDITAL]` pediu e que não pertence ao dossiê permanente: certidão extra, atestado de capacidade técnica para aquele objeto, termo específico | Nenhum edital da e-Missão tem esta pasta ainda; é a sétima do padrão da mentoria e a que mais falta nas pastas vivas |

**Por que sempre as sete, mesmo vazias.** O `[EDITAL]` começa com as sete no dia
zero. Quem abre a pasta de um edital sabe, sem perguntar, onde está o edital, onde
está o projeto e onde está a resposta. Uma pasta vazia em `06 - Resultados` diz
"ainda não saiu"; a ausência da pasta não diz nada.

---

## As regras de nome, que valem para `[INSTITUIÇÃO]`, `[PASTA]` e `[EDITAL]`

1. **Dois dígitos, traço com espaço dos dois lados:** `01 - Nome`. É o formato
   que mais diverge nas pastas vivas (`01- Edital`, `07- Serviços`), e a
   divergência quebra a ordenação.
2. **A contagem recomeça em 01 dentro de cada pasta-mãe.** Nunca é contínua.
3. **`00` é reservado para projeto base**, dentro de `02 - Editais`.
4. **`[EDITAL]` leva o resultado no nome** quando ele sai. `[PASTA]` nunca muda
   de nome.
5. **Pasta vazia não se apaga, não se renomeia e não se relata como problema.**
   Vale para as sete `[PASTA]`, para as sete subpastas do `[EDITAL]` e para tudo
   dentro da `_82`.
6. **Certidão leva a validade no nome** quando entra em `04 - Certidões Negativas`,
   para avisar o vencimento sem abrir o arquivo.

---

## Onde a e-Missão diverge do modelo hoje

Registro de leitura, sem pedido de correção. Ela está estruturando à mão.

- `02 - Informações` está sem o complemento `Institucionais`.
- `03 - Edital Fundo Brasil` usa `01- Edital`, `02- Anexos` e assim por diante,
  com o traço colado no número.
- `02 - Edital TJMG VEC - Peprovado` tem o sufixo grafado com P.
- Nenhum `[EDITAL]` tem a `07 - Documentos Específicos`.
- `07 - Serviços` mistura duas numerações: `01 - CMAS` e `1 - Orientações` dentro
  dela; `02 - CMDCA` tem `1 - Escopo do Projeto` e `03 - FazDeNovo CMDCA` com o
  mesmo conteúdo.
- `04 - OSCIP` tem pares duplicados por grafia: `DOC` e `Documentos`, `PROTOCOLO`
  e `Protocolos`, `RENUNCIA UTILIDADE PÚBLICA` e `Renúncia Utilidade Pública`.
