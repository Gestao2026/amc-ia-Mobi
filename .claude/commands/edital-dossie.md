---
description: Produzir o Dossiê do Edital, documento completo em Word e PDF para enviar ao cliente, com categorias, anexos, documentos por etapa, território, critérios e riscos.
---

# /edital-dossie

Transforma um edital e seus anexos em **um documento único, pronto para enviar ao cliente**. É o entregável que mostra domínio do edital antes de qualquer proposta ser escrita, e serve tanto para o captador trabalhar quanto para a OSC entender no que está entrando.

Diferença para o `/edital-analisar`: aquele faz a primeira leitura e grava o `edital.md` com os 11 blocos do modelo. **Este não relê o edital: ele formata o que já está lido** e acrescenta a parte que só existe na entrega, o cruzamento com a carteira.

## Passo 0. Contexto

Leia `minhas-oscs/.ativa` e o `perfil-osc.md` da OSC ativa, se houver. O dossiê funciona sem OSC ativa (é um documento sobre o edital), mas com ela é possível preencher a parte de cruzamento com a carteira.

## Passo 1. Localizar a primeira leitura

Leia `projetos/{edital-slug}/edital.md`. **Se ele não existir, pare e rode `/edital-analisar` primeiro.** O dossiê não é o lugar de ler edital.

Confira antes de formatar:

1. Os 11 blocos estão preenchidos? Liste os que estão vazios ou marcados como não encontrado, e pergunte se ela quer completar a leitura antes de gerar o documento.
2. Os anexos que o edital cita estão todos na pasta? O que faltar vai marcado no documento com alerta de bloqueio, separando **o que impede a inscrição** do que só é usado depois.

## Passo 2. Anúncio

```
🔍 Próximo passo: montar o dossiê a partir da primeira leitura e gerar o Word e o PDF. Tempo estimado: 2 a 4 minutos.
```

## Passo 3. Montagem

O dossiê é o `edital.md` formatado para entrega, na mesma ordem dos 11 blocos, mais três partes que só existem aqui.

| Parte do dossiê | De onde vem |
|---|---|
| O que é urgente | Bloco 1, o semáforo, mais as **decisões já tomadas** para não reabrir discussão |
| O edital em uma tela | Bloco 2 |
| Quem pode e quem não pode | Bloco 3, com as vedações, as exceções e as cotas |
| As categorias | Bloco 4 |
| As regras do dinheiro | Bloco 5 |
| Ficha de controle documental | Bloco 6, com as colunas Enviado e Data **em branco** |
| Os anexos, como preencher | Bloco 7 |
| Os critérios, um a um | Bloco 8 |
| Os riscos e o que derruba | Bloco 9 |
| Território e leitura estratégica | Bloco 10 |
| Divergências | Bloco 11 |
| **Cronograma completo** | Novo aqui. Da inscrição à prestação de contas, com as trilhas paralelas quando houver |
| **A carteira** | Novo aqui. Quais clientes são elegíveis, quais estão fora e por quê. Só com OSCs cadastradas |
| **Ficha de autoavaliação** | Nova aqui. Cada critério do bloco 8 com a pergunta de verificação e campo para a nota estimada |

Omita parte que não se aplique ao edital. **Não invente seção nova e não acrescente informação que não esteja no `edital.md`.** Se faltar algo importante, volte ao `/edital-analisar` e complete a leitura lá, para que o arquivo e o dossiê nunca divirjam.

## Passo 4. Aprovação

Mostre a estrutura montada e pergunte:

```
1. Aprovar e gerar o Word e o PDF
2. Quero ajustar algo
```

## Passo 5. Geração e entrega

Escreva o dossiê em markdown num arquivo temporário e converta:

```
python3 scripts/dossie-para-word.py <dossie.md> "<pasta do edital>/DOSSIE DO EDITAL - {edital}.docx"
```

O script gera o `.docx` e, se o Word estiver instalado, o `.pdf` junto.

**Entregue os dois formatos** e explique por quê: o Word para preencher as fichas de controle, o PDF para ler e enviar ao cliente.

Salve na **pasta do edital**, junto com o edital e os anexos. Informe o caminho completo.

Se o arquivo estiver aberto no Word, a gravação falha. Avise e peça para fechar, em vez de criar um arquivo com outro nome.

## Passo 6. Próximo passo

Sugira `/projeto-elegibilidade` (CaptaDoc) para cada cliente candidato, lembrando que o dossiê já fez o primeiro filtro (natureza jurídica e território) mas não leu os estatutos.

## Regras

- **Não invente exigência que não esteja no edital.** Se algo estiver ambíguo, marque como divergência e registre a pergunta ao canal de dúvidas.
- **Verifique antes de afirmar.** Se o captador disser que algo pontua, confira no texto. Se não houver regra, diga onde aquilo pesa de fato, em vez de simplesmente concordar ou negar.
- **Toda tabela de controle sai com as colunas de marcação em branco.**
- **Um documento só.** Nunca espalhe o dossiê em vários arquivos: o cliente recebe um Word e um PDF.
- Português correto, acentuação conferida, **sem travessão**.
- O dossiê é material de entrega ao cliente: linguagem de consultor, sem jargão técnico de programação e sem detalhe de implementação.
