# Padrão de organização das pastas por cliente

> Definido em 20/08/2026 e validado no piloto com a Associação Ponto Cultural e a
> e-Missão. Vale para toda OSC, empresa, coletivo ou pessoa física da carteira.

## A estrutura

```
minhas-oscs/{cliente}/
├── perfil-osc.md         ficha viva: natureza jurídica, CNPJ, missão, id CaptaHub
├── assessoria.md         contrato, origem do cliente, remuneração, resultados
│
├── dossie/               o que serve para TODO edital
│   ├── 01-constituicao/    estatuto ou contrato social, atas, CNPJ, comodato da sede
│   ├── 02-certidoes/       certidões, com a validade no nome, mais o _PAINEL.md
│   ├── 03-institucional/   portfólio, logo, fotos, comprovante de endereço
│   ├── 04-equipe/          documentos e currículos dos dirigentes
│   ├── 05-comprovacao/     projetos aprovados, atestados, termos assinados
│   ├── 06-licencas/        alvará, laudo de bombeiros, dispensa sanitária, taxas
│   └── 07-financeiro/      balanço, DRE, relatório financeiro
│
├── habilitacoes/         o que mantém a organização apta a captar
│   └── {orgao}/            CMAS, CMDCA, OSCIP, utilidade pública, por ano
│
├── projetos/             um edital, uma pasta
│   └── {orgao-nome-ano}/
│       ├── estado.md       painel: etapa, prazo, id CaptaHub, pendências
│       ├── edital.md       o edital destrinchado
│       ├── elegibilidade.md   CaptaDoc
│       ├── proposta.md        CaptaBuilder
│       ├── orcamento.md       CaptaBudget
│       ├── score.md           CaptaScore
│       ├── anexos/         formulários e anexos deste edital
│       ├── entrega-final/  o que foi submetido, congelado
│       └── _historico/     versões anteriores, com data no nome
│
├── captacao/             frentes contínuas: emendas, ICMS, prospecção de patrocínio
├── modelos/              modelos reutilizáveis: ofícios, requerimentos, papel timbrado
├── referencias/          normativos e cartilhas do setor
├── operacao/             acessos, pautas de reunião, gastos e recibos
└── _duplicados/          cópias idênticas retiradas do caminho, nunca apagadas
```

## Habilitação não é projeto

Distinção que organiza o resto. **Habilitação** é inscrição ou registro que
mantém a organização apta: CMAS, CMDCA, OSCIP, CEBAS, utilidade pública. Sem ela,
o CaptaDoc reprova antes de olhar o mérito. **Projeto** é a resposta a um edital
específico, e é o que passa pelos quatro agentes.

## As quatro regras de nomeação

1. **Um nome, um arquivo.** O arquivo vivo nunca leva V2, FINAL, REV1 nem
   ATUALIZADO. Ao melhorar, o arquivo vivo é sobrescrito e a versão anterior vai
   para `_historico/` com a data no nome.
2. **O nome diz o que é**, não quando foi baixado.
3. **Certidão leva a validade no nome:** `certidao-federal-val-2026-11-15.pdf`.
   É o que permite avisar o vencimento sem abrir nada.
4. **Pasta de projeto é por edital**, nunca por ano nem por órgão.

## A natureza jurídica muda o checklist, não a pasta

Todos os clientes ficam no mesmo lugar. O que muda conforme a natureza é o que o
dossiê exige:

| Natureza | Dossiê exige |
|---|---|
| OSC (associação, fundação) | Estatuto registrado, ata de eleição, inscrição em conselho, CEBAS |
| Empresa (LTDA, MEI) | Contrato social e alterações, cadastro SALIC ou ANCINE |
| Pessoa física | RG, CPF, comprovante de endereço, certidões da PF |
| Coletivo sem CNPJ | Declaração de representação, documentos do representante |

Com a natureza registrada no perfil, o CaptaDoc elimina automaticamente editais
restritos a organizações sem fins lucrativos quando o proponente é empresa ou
pessoa física.

## Nunca apagar

Cópias idênticas vão para `_duplicados/`, preservando o caminho de origem, e só
são excluídas por ordem expressa da captadora. Antes de reorganizar uma pasta,
tirar cópia de segurança.

## Clientes de parceria

Cliente que vem de uma parceria (a captadora executa e recebe percentual) fica
**junto com os clientes diretos**, em `minhas-oscs/`, porque o trabalho técnico é
idêntico. O que muda é a relação comercial, registrada no `assessoria.md` do
cliente com quatro campos: origem, titular comercial, modelo de remuneração e
vigência.

As regras da parceria em si ficam fora da lista de clientes, em
`parcerias/{parceiro}/`, com contrato, percentuais e repasses.

## Credenciais nunca ficam na pasta do cliente

Certificado digital (`.pfx`, `.p12`), senha e token vão para
`_credenciais-nao-sincronizar/`, na raiz do projeto. Essa pasta está fora do
GitHub e fora do backup em nuvem, de propósito. Senha jamais no nome do arquivo.
