# 23 - Auditoria dos documentos de 27/08

| Campo | Valor |
|---|---|
| Data | 2026-08-28 |
| Fonte | `C:\Users\rosep\Desktop\ONDE ESTA TUDO DE 27-08.md` (65 arquivos, 61 pastas com carimbo de 27/08) |
| Tipo | Auditoria (existência, integridade, duplicatas e local na estrutura) |
| Situação | Concluída. Nenhum arquivo ou pasta foi criado, movido, renomeado ou apagado |
| Autorizada por | A captadora, pedindo verificação nas quatro frentes: existência, duplicatas, conteúdo e local correto |
| Reversível | Não se aplica. Auditoria somente leitura, nada foi alterado no disco |

---

## 1. Resumo executivo

- **65 arquivos**: 61 intactos no caminho exato; 3 mudaram de local ou nome desde 27/08 mas existem e abrem normalmente; **1 genuinamente não encontrado**.
- **61 pastas**: todas confirmadas, nenhuma perdida.
- **Nenhum arquivo corrompido** (todos os `.docx`, `.xlsx` e `.pdf` abriram normalmente).
- Um grupo de 4 arquivos idênticos revelou uma pasta duplicada e um possível erro de nomenclatura (edital "MAPFRE" dentro de uma pasta chamada "Essencis").
- Uma planilha de controle de submissão existe em 4 cópias divergentes entre si.
- 3 arquivos de um edital municipal (LMIC) foram encontrados dentro da pasta de outro edital (PNAB Ciclo 2), do mesmo cliente.
- 6 pastas de trabalho seguem soltas na raiz do Desktop, fora do padrão de pasta por cliente.

---

## 2. Existência e integridade

**Pastas (61):** todas confirmadas no caminho exato do documento.

**Arquivos com divergência (4 de 65):**

| Arquivo | Situação |
|---|---|
| `Dossiês Documentais — Editais de Patrocínio 2026.docx` | **Não localizado em lugar nenhum do Desktop.** Buscado por variações do nome em toda a árvore, sem rastro. Único item realmente perdido dos 65. |
| `Multiplos Agentes amcia 27.08.docx` | Movido da raiz do Desktop para `Desktop\Implentações Claude\`. Tamanho bate, abre normalmente. |
| `PERGUNTAS 30.08.docx` | Movido da raiz do Desktop para `Desktop\Implentações Claude\`. Tamanho bate, mas o conteúdo é de 1 parágrafo só (ver seção 4). |
| `ANEXO VII - DECLARAÇÃO PARA GRUPO E COLETIVO SEM CNPJ.docx.docx` (Mededicas 1) | Já foi renomeado, corrigindo a extensão duplicada, para `...docx` (sem repetir). Tamanho bate, abre normalmente. |

Os demais 61 arquivos batem com o caminho, o tamanho (tolerância de 5%) e abrem sem erro.

---

## 3. Duplicatas e inconsistências

### 3.1. "Edital Essencis" vs "Edital Essencis - Copia" (cliente Centro de Arte Almira Lopes)

Os 4 arquivos abaixo (2 nomes × 2 pastas) têm o mesmo hash SHA-256, ou seja, **são idênticos byte a byte**:

- `03 - Edital Essencis\01 - Edital\EDITAL MAPFRE 2026_INFORMAÇÕES_V2.pdf`
- `03 - Edital Essencis\01 - Edital\EDITAL MAPFRE 2026_INFORMAÇÕES_V2 (1).pdf`
- `03 - Edital Essencis - Copia\01 - Edital\EDITAL MAPFRE 2026_INFORMAÇÕES_V2.pdf`
- `03 - Edital Essencis - Copia\01 - Edital\EDITAL MAPFRE 2026_INFORMAÇÕES_V2 (1).pdf`

A pasta "Edital Essencis - Copia" é uma duplicata completa da "Edital Essencis" (ao menos na subpasta 01-Edital; as demais subpastas de ambas estão vazias, o que é normal).

**Ponto para a captadora decidir:** os dois arquivos falam de "MAPFRE", mas a pasta se chama "Edital Essencis". O documento `CALL\Instruções Editais.docx` confirma que Essencis (prazo 11/09) e MAPFRE (prazo 30/09) são **dois editais diferentes**. Isso sugere que o conteúdo do MAPFRE foi colocado, por engano, dentro da pasta do Essencis (ou a pasta tem o nome errado). Vale conferir e, se for o caso, mover o material certo para cada pasta.

### 3.2. Quatro cópias de "Controle de Submissão"

| Local | Tamanho | Abas |
|---|---|---|
| `04 - Controle de Submissão_\01 - Mineração de Editais\01 - Planejamento de Submissões\1 - Controle de Submissão_.xlsx` | 182 KB | GERAL, REPROVADOS, EXCLUIDOS, TABELA DE PROJETOS, Status |
| `06 - Clientes\06 - CaptaDrive - Mededicas\1 - Controle de Submissão.xlsx` | 153 KB | SUBMISSÕES, STATUS PROJETOS, Status |
| `06 - Clientes\08 - CaptaDrive - Núcleo Arte e Música Esperança\1 - Controle de Submissão.xlsx` | 148 KB | SUBMISSÕES, STATUS PROJETOS, Status |
| `Downloads\1 - Controle de Submissão.xlsx` | 88 KB | SUBMISSÕES, ACESSOS SOFTWARE, Status |

As 4 são **todas diferentes entre si** (nenhum hash se repete), e a mestra já usa um modelo de abas diferente das cópias por cliente. Confirma o risco de planilha copiada manualmente por cliente e desatualizada entre si. Como o CaptaHub já é a fonte da verdade do pipeline, é uma oportunidade de consolidar isso lá em vez de manter 4 arquivos divergentes.

Fora esses dois grupos, não apareceu nenhuma outra duplicata de conteúdo entre os 65 arquivos.

---

## 4. Conteúdo dos documentos (verificação de amostra)

| Documento | Situação |
|---|---|
| `Dossiês Documentais — Editais de Patrocínio 2026.docx` | Não pôde ser lido, arquivo ausente |
| `Implentações Claude\Multiplos Agentes amcia 27.08.docx` | Completo: prompt de automação para organizar documentação e habilitação de edital com múltiplos sub-agentes |
| `Implentações Claude\PERGUNTAS 30.08.docx` | **Incompleto**, só 1 parágrafo, parece cabeçalho de comando colado sem o corpo |
| `BANDEJA\Informação Edital 2026.docx` | Completo, 111 parágrafos, categorias e valores do Fomento Anual/PNAB |
| `BANDEJA\Informações Projeto.docx` | Completo, 194 parágrafos, valores solicitáveis e documentação de habilitação |
| `CALL\Instruções Editais.docx` | Completo, confirma que Essencis e MAPFRE são editais distintos (ver 3.1) |
| `NAME\PROJETO CULTURAL name.docx` | Completo, é a proposta "Vozes e Flautas de Esperança" (PNAB Ciclo 2), mesma OSC do cliente Núcleo Arte e Música Esperança, mas solta fora da pasta do cliente |
| `STK\MAPFRE 1.docx` | Completo, análise cruzando critérios Rouanet com os 10 pilares da MAPFRE |
| `STK\Musical de Natal — Patrocínio Shell.docx` | Modelo ainda com campos placeholder (`[INSERIR...]`), não preenchido |
| `STK\SHELL 2.docx` | Versão mais avançada do formulário Shell, já com CNPJ e valores preenchidos |
| `STK\STK OBSERVAÇÃO.docx` | Revisão crítica do material da MAPFRE, com 5 pontos a corrigir |
| `...Energisa Cultural...\Energisa - Informações.docx` | Curto (5 parágrafos) mas completo, ficha-resumo do programa |
| `...PNAB Ciclo 2\04 - Projeto\Organização Projeto.docx` | Lista de escolas/espaços para carta de anuência, mais nota sobre dossiê/clipping. Conteúdo de apoio, não uma proposta em si (ver seção 5) |

---

## 5. Local correto na estrutura

### 5.1. Achado: arquivos do edital errado dentro da pasta do PNAB Ciclo 2

Em `06 - Clientes\08 - CaptaDrive - Núcleo Arte e Música Esperança\02 - Editais\02 - PNAB Ciclo 2\07 - Documentos Específicos\01 - Formulários`, os 3 arquivos abaixo pertencem à **Lei Municipal de Incentivo à Cultura (LMIC)**, um edital diferente do PNAB Ciclo 2 (federal):

- `EDITAL LMIC FORM. INSCRIÇÃO.pdf`
- `EDITAL LMIC PLAN FINANCEIRA.xlsx`
- `INSTRUÇÕES PREENCHIMENTO FORM.pdf`

O mesmo cliente já tem uma pasta própria para isso, `02 - Editais\01 - Edital Multilinguagens`, que é o destino mais provável desses 3 arquivos. Fica como apontamento para a captadora decidir e mover à mão, quando retomar a organização.

### 5.2. Restante da árvore do PNAB Ciclo 2

Todo o resto dos arquivos dessa árvore está na subpasta esperada (edital em 01, anexos em 02, manual em 03, formulário/proposta em 04, orçamento em 05, portfólio e cartas de anuência em 07). O único ponto de atenção secundário é `04 - Projeto\Organização Projeto.docx`, cujo conteúdo (lista de escolas para carta de anuência) se pareceria mais com `07 - Documentos Específicos`, mas pode perfeitamente continuar em 04 se for tratado como nota de trabalho da elaboração.

### 5.3. Pastas soltas na raiz do Desktop

`BANDEJA`, `CALL`, `NAME`, `STK`, `Mededicas 1` e `Credenciais AMC IA` ficam fora da estrutura de `_82 - Rosepaula Aparecida Andrade Rodrigues\06 - Clientes`. Contêm rascunhos, conversas de análise e formulários em andamento de projetos que, em alguns casos (NAME, STK), já têm cliente correspondente dentro de `06 - Clientes`. Registro apenas como observação de estrutura, sem mover nada.

---

## 6. O que ficou pendente

- Confirmar o paradeiro de `Dossiês Documentais — Editais de Patrocínio 2026.docx` (único item realmente perdido).
- Decidir o destino de "Edital Essencis" vs "Edital Essencis - Copia" e o conteúdo MAPFRE dentro delas.
- Decidir se consolida as 4 cópias de "Controle de Submissão" numa fonte única.
- Mover (ou não) os 3 arquivos do LMIC para a pasta do Edital Multilinguagens.
- Decidir se e quando as 6 pastas soltas do Desktop entram na estrutura de `06 - Clientes`.

Nenhuma ação de exclusão, movimentação ou renomeação foi tomada nesta auditoria.
