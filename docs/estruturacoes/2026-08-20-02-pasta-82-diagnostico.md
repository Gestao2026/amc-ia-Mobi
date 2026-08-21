# 02 - Diagnóstico da pasta _82 (dos mentores)

| Campo | Valor |
|---|---|
| Data | 2026-08-20 |
| Pasta afetada | `C:\Users\rosep\Desktop\_82 - Rosepaula Aparecida Andrade Rodrigues` e a original no Drive |
| Tipo | Diagnóstico. **Nenhum arquivo foi movido, renomeado ou apagado** |
| Situação | Diagnóstico concluído. Execução aguardando decisões |
| Autorizada por | Rosepaula. O dona da pasta autorizou apenas o acesso como Editora |
| Reversível | Não se aplica. Nada foi alterado |

---

## 1. Por que foi feito

A pasta é o ambiente de trabalho da assessoria, com os documentos de 23 clientes.
O caminho mais longo tinha **316 caracteres** e **629 arquivos não abriam** pelo
Explorer nem pelo Office. Tentativas de subir a pasta para o Google Drive
falharam pela metade.

## 2. O que foi decidido, e por quem

- **Nenhum nome de pasta pode mudar.** A estrutura foi criada pelos mentores e é padrão da mentoria. Isso inclui nome de cliente e nome de edital.
- **Nome de arquivo pode ser encurtado.**
- **A propriedade não será transferida.** A pasta continua da dona e Rosepaula é Editora.
- **A pasta continua sendo espelho do que a dona mantém.**
- Os 772 `desktop.ini` devem ser separados, mas só depois de resolvida a questão da propriedade.

## 3. Estado antes (e ainda hoje)

### Cópia local, na Área de Trabalho

| Medida | Valor |
|---|---|
| Arquivos | 3.490 |
| Volume | 5,40 GB |
| Pastas | 1.112 (90 vazias) |
| Caminho mais longo | 316 caracteres |
| Acima de 260 | 629 arquivos |
| Prefixo da raiz | 66 caracteres |

### Pasta original, no Drive da dona

| Medida | Valor |
|---|---|
| Arquivos | 6.023 |
| Volume | 10,43 GB |
| Caminho mais longo | 478 caracteres |
| Acima de 260 | 2.588 arquivos |
| Prefixo do atalho | 104 caracteres |

## 4. O que foi apurado

### 4.1. O padrão dos mentores não cabe no limite do Windows

A cadeia mais profunda consome **179 caracteres só em nome de pasta**:

| Trecho | Caracteres |
|---|---|
| `06 - Clientes` | 13 |
| `01 - OSC-Organizações da Sociedade Civil` | 40 |
| `08 - CaptaDrive - Núcleo Arte e Música Esperança` | 48 |
| `02 - Editais` | 12 |
| `01 - Edital Multilinguagens - Name` | 34 |
| `07 - Documentos Específicos` | 27 |

Com o prefixo de 66 caracteres da Área de Trabalho, sobram **3 caracteres para o
nome do arquivo**. Simulação: encurtar apenas nomes de arquivo derruba o máximo
de 316 para 314. Praticamente nada. **O gargalo são os nomes de pasta, que são
intocáveis.**

### 4.2. A solução é encurtar o prefixo, não os nomes

Uma unidade virtual do Windows (`subst`) aponta uma letra de unidade para a
pasta, reduzindo o prefixo para 2 caracteres. Testado:

| | Acima de 260 hoje | Com unidade virtual |
|---|---|---|
| Pasta do Drive | 2.588 de 6.023 | **1** |
| Cópia local | 629 de 3.490 | **0** |

Zero renomeação, zero mudança de estrutura.

### 4.3. As cópias soltas não são modelos, são uma arrumação inacabada

No Drive, cada cliente aparece duas vezes: solto em `06 - Clientes` com a
numeração antiga e de novo dentro de `01 - OSC`, `02 - Empresa Privada` ou
`03 - Outros Modelos` com a numeração nova. As datas de criação provam a origem:

| Cliente | Cópia solta | Cópia categorizada |
|---|---|---|
| Kuyper | 15/04/2026 22:08 | 18/08/2026 14:02 |
| Bandeja Films | 18/05/2026 00:26 | 18/08/2026 14:01 |
| Luzeiros | 23/06/2026 18:54 | 18/08/2026 14:01 |

Todas as categorizadas foram criadas em **18/08/2026, entre 14h01 e 14h02**, numa
cópia em lote que nunca removeu os originais. São **2.551 arquivos e 5,04 GB**.

Três clientes têm cópias divergentes e exigem conferência antes de qualquer
remoção: **E-Missão** (517 solta contra 609 categorizada), **Levanta e Brilha**
(84 contra 77) e **Ponto Cultural** (193 contra 189).

### 4.4. Os modelos de verdade

Ficam em `06 - Clientes\03 - Outros Modelos`: as pastas `X7`, `X8`, `X9` e
`X10 - CaptaDrive - Cliente X`, cada uma só com
`01 - Atendimento da Burocracia\DOCUMENTOS OSC.pdf`, mais os dois arquivos
`Y -` e `Z - CaptaDrive - Cliente X-20250423T233823Z-001.zip`.

`X - CaptaDrive - Clientes Standby` **não é modelo**: guarda três prospects
reais, Instituto Boreal (550 arquivos), COMPEG (24) e ABST (12).

### 4.5. Conformidade com o padrão

- **Gestão Documental:** 7 dos 23 CaptaDrives seguem as 7 subpastas do documento. Oito usam outro padrão (`01 - Documentos` + `02 - Portfolio`), que faz sentido para produtora e pessoa física. Cinco não têm a pasta.
- **Pastas de edital:** 37 das 51 seguem o padrão `01 - Edital` a `07 - Documentos Específicos`. As 14 restantes divergem por hífen sem espaço ou por `07 - Documentos` no lugar de `07 - Documentos Específicos`.
- **Erros de digitação:** `05 - Alvaras e Licenças` sem acento, `07- Serviços` sem espaço, `01 - Declaração` no singular, `02 - Documentos Institucionais` em vez de `02 - Informações Institucionais`, e três grafias de portfólio.

### 4.6. Problemas de sincronização com o Google Drive

- **772 arquivos `desktop.ini`**, em 772 das 1.112 pastas. 1.226 deles já estão no Drive da dona.
- **4 arquivos com emoji 🔥** em `E-Missão\02 - Editais\02 - Edital TJMG VEC\04 - Projeto`.
- **3 pares de arquivos com o acento em codificação de Mac** (caractere combinante) convivendo com a versão do Windows. Mesmo tamanho, mesmo nome na tela, dois arquivos distintos.

O Google Drive em si **não tem limite de caminho**: a pasta da dona já tem
caminhos de 478 caracteres funcionando. Quem falha é o Explorer do Windows ao
copiar. Por isso **não se deve encurtar nome de arquivo**: criaria divergência
com a pasta da dona, que é justamente o que se quer evitar.

### 4.7. Divergências entre a cópia local e a do Drive

Comparação por conteúdo, ignorando a renumeração: **2.716 dos 2.718** arquivos
locais já estão no Drive.

| Onde só existe | Quais |
|---|---|
| Só no computador | 2 planilhas de controle, **em versão mais nova** (179 KB contra 180 KB, e 166 KB contra 163 KB) |
| Só no Drive | `CNH-Germano - representante legal.pdf` e `Comprovante residencia.pdf`, ambos em Levanta e Brilha |

### 4.8. Sobreposição com o Projeto AMC IA

**902 dos 1.045 arquivos de `minhas-oscs` são o mesmo documento que já existe no
`_82`**, ou seja 1,42 GB dos 1,56 GB. Só 143 arquivos são exclusivos, e são o
trabalho técnico: 68 `.md` dos agentes e 65 PDFs.

## 5. Backup feito

| Origem | Destino | Conferido |
|---|---|---|
| Cópia local do `_82` | `C:\Users\rosep\Backups\pasta-82\2026-08-20` | Sim: 3.490 arquivos e 5,40 GB, batendo com o original |

**A pasta do Drive ainda não tem backup sob controle da Rosepaula.** Os dois PDFs
de identidade do Levanta e Brilha, que só existem lá, seguem desprotegidos.

## 6. O que ficou pendente

| Pendência | Depende de |
|---|---|
| Unidade virtual permanente | Decisão da Rosepaula |
| Backup diário da pasta do Drive | Decisão sobre a primeira carga de 10,43 GB |
| Higiene de arquivo: seis planilhas `backup antes de...`, 4 nomes com emoji, 3 pares com acento de Mac, 772 `desktop.ini` | Decisão da Rosepaula |
| Reconciliar as 2 planilhas mais novas e trazer os 2 PDFs do Levanta e Brilha | Decisão da Rosepaula |
| Remover as 2.551 cópias soltas | **Aval da dona da pasta** |
| Quatro tarefas agendadas órfãs apontando para `C:\amc-ia`, pasta que não existe mais | Decisão da Rosepaula |

## 7. Regras que passam a valer

- **Nome de pasta no `_82` não muda.** Nunca. É padrão da mentoria.
- **Nome de arquivo no `_82` também não muda**, enquanto a pasta for espelho da da dona.
- Caminho longo se resolve com unidade virtual, não com renomeação.
- Documento pessoal de dirigente de cliente (CNH, CPF, RG, comprovante de residência) exige decisão consciente antes de qualquer compartilhamento.
