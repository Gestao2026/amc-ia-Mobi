# 17 - Consolidação do marketing numa pasta única

| Campo | Valor |
|---|---|
| Data | 2026-08-24 |
| Pasta afetada | `Desktop\MOBI\06-MARKETING` (extinta) e `OneDrive E-missão\Documentos\9. MOBILIZANDO MKT LOGO` |
| Tipo | reorganização, deduplicação e exclusão |
| Situação | Concluída. **3 pendências de decisão** |
| Autorizada por | A captadora, em etapas, ao longo da conversa de 24/08 |
| Reversível | Sim para as 80 exclusões, enquanto a Lixeira não for esvaziada. Os 549 movimentos são reversíveis pelo CSV de rastreabilidade |

---

## 1. Por que foi feito

O material de marketing vivia em dois lugares ao mesmo tempo: `Desktop\MOBI\06-MARKETING`, com 987 arquivos e 769 MB, e `Documentos\9. MOBILIZANDO MKT LOGO`, com 891 arquivos e 1,1 GB. Somadas, 1.878 arquivos e 1,85 GB.

Comparando por hash MD5, e não por nome ou data, **775 dos 987 arquivos do Desktop eram cópia byte a byte de algo que já estava em Documentos**. A pasta do Desktop era uma reorganização com nomes novos da mesma coisa: `fotos` era `FOTOS`, `marca-e-logo` era `ARQUIVOS LOGO MOBILIZANDO_V2`, `redes\instagram` era `POSTAGEM INSTAGRAM`, `site-e-landing` era `SITE_PLANO`.

Além da duplicação, a pasta de destino misturava quatro naturezas de arquivo: marketing de verdade, álbum pessoal de família, documentos de cliente e credenciais. Como a pasta passa a ser lida para gerar o perfil de captador, essa mistura contamina a leitura.

## 2. O que foi decidido, e por quem

Decisões da captadora, na ordem em que foram tomadas:

- A pasta que fica é a de Documentos. A do Desktop deixa de existir.
- Nada é excluído em definitivo. Tudo vai para a Lixeira ou é movido.
- Duplicata só sai quando sobra pelo menos uma cópia do mesmo conteúdo.
- **Foto de projeto de cliente é marketing**, não arquivo morto. Ganha uma pasta de portfólio própria.
- Foto pessoal e de família vai para `Documentos\2. PESSOAL`.
- Documento de cliente vai para a pasta dele em `_82\06 - Clientes`.
- O Projeto Egressos é da e-Missão, entra nos editais dela.
- A Mano Down foi vínculo de emprego, não cliente. Vai para o histórico profissional.
- Credencial vai toda para `Desktop\Credenciais AMC IA`.
- `Implentações Claude` fica com os documentos de implementação e as apostilas.

**Descartado, e por quê:**

- **Não apagar os 4 logos repetidos em `APLICAVEIS`.** A repetição é intencional, é uma seleção de uso rápido diante da biblioteca completa. Já registrado na estruturação 16.
- **Não apagar as fotos de `FOTOS ESCOLHIDAS` nem de `Foto - 10 anos casados`.** Apagar da pasta-mãe mutila o acervo, apagar da subpasta destrói a curadoria de quais foram selecionadas.
- **Não apagar as fotos de contexto duplo.** Uma imagem arquivada tanto no evento quanto no cliente perde um caminho de busca se uma cópia sair.
- **Não trazer texto e estratégia para `amc-ia-Mobi\marketing\`.** A regra antiga do `ALFA-AMC.MKT.docx` mandava texto para o projeto e só imagem para a pasta de marketing. Foi substituída: a pasta de Documentos passa a ser a base única de leitura.

## 3. Estado antes

| Medida | Valor |
|---|---|
| Arquivos, nas duas pastas | 1.878 |
| Volume, nas duas pastas | 1,85 GB |
| Conteúdos distintos (por hash) | 1.026 |
| Cópias redundantes entre as duas pastas | 775 |
| Arquivos exclusivos do Desktop | 212 |
| Arquivos exclusivos de Documentos | 39 |
| Duplicatas internas em Documentos | 76 |

## 4. O que foi executado

1. **Inventário por hash MD5** dos 1.878 arquivos, para comparar conteúdo e não nome.
2. **Cópia dos 212 exclusivos do Desktop** para a pasta de Documentos, com conferência de hash em cada um. 212 de 212 confirmados, nenhuma colisão de nome.
3. **Conferência de que os 987 arquivos do Desktop tinham cópia idêntica** em Documentos. Resultado: zero pendências.
4. **A pasta `Desktop\MOBI\06-MARKETING` foi para a Lixeira**, com seus 987 arquivos e 769 MB.
5. **Deduplicação nível 1: 23 arquivos** para a Lixeira. 18 `.DS_Store` (lixo de janela do Finder do Mac, que veio junto com a entrega da agência) e 5 cópias que o próprio Windows já marcara com `- Copia`, `(1)`, `(2)` e `(3)`.
6. **Deduplicação nível 2: 57 arquivos** para a Lixeira, por quatro regras, cada uma exigindo sobrevivente:
   - **R1, 22 arquivos.** A pasta `E-MISSÃO\FOTOS\MOÇAMBIQUE 5` tinha 22 arquivos e todos os 22 já estavam em `E-MISSÃO\MOÇAMBIQUE`, que tem 29. Eram as mesmas fotos reencaminhadas por WhatsApp em datas diferentes, por isso os nomes não batiam. A pasta inteira saiu. Sozinha respondeu por 33 dos 40 MB.
   - **R2, 11 arquivos.** Duas cópias na mesma pasta. Ficou a de nome mais descritivo: ficou `Evento Minas Summit_2.2025.jpg`, saiu `IMG-20250607-WA0018.jpg`.
   - **R3, 12 arquivos.** Cópia solta na raiz de `ROSEDER` com gêmea no arquivo organizado `ROSEDER\Foto\FOTOS ROSE`.
   - **R4, 12 arquivos.** Cópia na pasta genérica `FOTOS 1.2\OUTRAS FOTOS` com gêmea em pasta que nomeia o cliente ou o evento.
7. **Verificação de integridade** contra o conjunto original: dos 1.026 conteúdos distintos, restaram 1.009. Os 17 que sumiram são exatamente os 17 conteúdos de `.DS_Store`. Nenhum conteúdo próprio foi perdido.
8. **Criação do portfólio de clientes: 156 arquivos movidos** para `FOTOS\PROJETOS DE CLIENTES\`, organizados por cliente e por ação: e-Missão (Moçambique, Brumadinho, ENATS, Gerando Falcões, Ação Irmã Patrícia, Rede e Parceiros), Gerando Falcões, Mario Penna (AeC e Equipe), Confraria, CRA, FDC e HE.
9. **Mano Down: 22 arquivos movidos** para `10-HISTORICO-PROFISSIONAL\empresas-3o-setor\MANO DOWN\FOTOS`, unificando duas pastas da mesma organização que estavam separadas.
10. **Saída final: 349 arquivos movidos** para quatro destinos, detalhados no item 5.
11. **Entrada: 4 arquivos** em `POSICIONAMENTO E OFERTA`, vindos da pasta `MKT`.
12. **Remoção de 75 pastas que ficaram vazias**, em três rodadas, porque o OneDrive segurava o identificador de algumas durante a sincronização.

### Detalhe da saída final (passo 10)

| Destino | Arq. | O que |
|---|---|---|
| `Documentos\2. PESSOAL\FOTOS ROSE E EDER\` | 257 | Álbum pessoal, com a estrutura interna preservada |
| `_82\06 - Clientes\02 - CaptaDrive - E-Missão\03 - Registros e Comunicacao\` | 22 | Execução e comunicação do cliente |
| `_82\...\02 - Editais\Fundo Brasil - Projeto Egressos\` | 11 | Edital, orçamento, cronograma e relatórios |
| `MOBI\99-A-CLASSIFICAR\arquivos-de-sistema\DS_Store - logo Mobilizando\` | 46 | Lixo do Mac, em 46 subpastas que replicam o caminho de origem |
| `MOBI\07-COMERCIAL\` | 5 | Plano de negócios |
| `MOBI\07-COMERCIAL\contratos-e-aditivos\` | 3 | Contratos das agências |
| `MOBI\09-TECNOLOGIA-IA\` | 2 | HostGator 1 e 2 |
| `Desktop\Credenciais AMC IA\a-confirmar\` | 3 | `ACESSOS AGÊNCIA CASUS.docx` e as duas planilhas de senha |

Os 46 `.DS_Store` foram para subpastas que replicam o caminho original porque todos têm o mesmo nome: numa pasta só, 45 seriam sobrescritos.

Os contratos ganharam o sufixo "agência logo Mobilizando" para não virarem um `CONTRATO.pdf` genérico no meio dos 31 que já existiam ali.

As duas versões do `📘 PLANO DE NEGÓCIOS_V8.docx` vinham de pastas diferentes e **não são idênticas**. As duas foram mantidas, a segunda marcada como "versão HISTORIA".

## 5. Estado depois

| Medida | Antes | Depois |
|---|---|---|
| Lugares onde há marketing | 2 | 1 |
| Arquivos | 1.878 | 658 |
| Volume | 1,85 GB | 0,96 GB |
| Pastas | — | 146 |
| Pastas vazias | 75 | 0 |
| Caminho mais longo | — | 251 caracteres |
| Conteúdos distintos preservados | 1.026 | 1.009 (os 17 que faltam são `.DS_Store`) |

**Atenção:** medindo a pasta hoje, aparecem 696 arquivos e 1,01 GB, não 658. A diferença são 38 arquivos restaurados da Lixeira às 08h45 por alguém que não a máquina, numa pasta `_RECUPERADO-DA-LIXEIRA-2026-08-24`. Ver o item 9.

### O que ficou na base de marketing

Marca completa (logo em JPG, PDF, PNG e SVG, nas três cores e duas versões, com e sem fundo), Manual da Marca, papel timbrado, cartão, assinatura de e-mail, apresentações institucional e comercial, metodologia, textos e história do site, `POSTAGEM INSTAGRAM`, `POSTAGEM LINKEDIN`, `DESTAQUES`, `DEPOIMENTOS`, `APLICAVEIS`, `GOOGLE ADS`, `PITCH`, `BUZZE MKT`, `FOTOS LAND PAGE`, `EDITAIS IA`, o portfólio de 156 fotos de projeto por cliente, o book profissional e a nova pasta `POSICIONAMENTO E OFERTA`.

## 6. Onde está a rastreabilidade

| Arquivo | O que registra |
|---|---|
| `_detalhado\2026-08-24-17-movimentacao.csv` | As 824 linhas de todas as etapas: origem, destino, ação e motivo de cada arquivo |
| Este registro | A decisão, o critério e os números |

O CSV tem oito etapas: consolidação (212), exclusão da pasta antiga (1), dedup nível 1 (23), dedup nível 2 (57), portfólio (156), Mano Down (22), saída final (349) e entrada (4).

## 7. Backup feito antes

| Origem | Destino | Conferido |
|---|---|---|
| Nenhum backup específico foi feito para esta estruturação | — | **Não** |

Isto contraria a regra permanente do índice, que exige backup antes de qualquer estruturação com exclusão. O que substituiu o backup, na prática, foi outra proteção: **nenhum arquivo foi excluído em definitivo**, tudo foi para a Lixeira, e cada exclusão só ocorreu depois de confirmar por hash que existia uma cópia sobrevivente do mesmo conteúdo. A tarefa diária de backup das 12h30 continua rodando normalmente.

## 8. Como reverter

**As 80 exclusões.** Abrir a Lixeira, localizar os arquivos pela data de 24/08/2026 e usar "Restaurar". Enquanto a Lixeira não for esvaziada, a reversão é completa. A pasta `Desktop\MOBI\06-MARKETING` inteira também está lá, com seus 987 arquivos.

**Os 549 movimentos.** Não há script de desfazer. O caminho é abrir o CSV de rastreabilidade, filtrar pela etapa desejada e mover de volta, usando as colunas origem e destino. Cada linha tem os dois caminhos completos.

**Os 4 arquivos que entraram.** São cópia, os originais continuam na pasta `MKT`. Basta apagar os quatro da pasta `POSICIONAMENTO E OFERTA`.

## 9. O que ficou pendente

As três pendências de arquivo foram para a pasta de triagem `_VERIFICAR-EXCLUIR-ANALISAR`, criada na própria base de marketing, com um `LEIA-ME.md` que descreve cada grupo. Nada foi excluído, e a triagem fica fora da leitura que gera o perfil de captador.

| Subpasta | Arq. | Decisão que falta |
|---|---|---|
| `EXCLUIR - restaurado da Lixeira 2026-08-24` | 38 | Restaurados às 08h45 de 24/08 por alguém que não a máquina. Conferidos por hash: 33 têm gêmeo idêntico na base e 5 não estão mais nela porque foram **movidos**, não excluídos (2 em `07-COMERCIAL\contratos-e-aditivos`, 1 em `07-COMERCIAL`, 1 em `Documentos\2. PESSOAL\FOTOS ROSE E EDER\Foto`, 1 em `MANO DOWN\FOTOS\Mano1.jpg`). Nenhum conteúdo estava perdido. Confirmar a exclusão |
| `EXCLUIR - copia lado a lado` | 1 | O `17.jpg` era idêntico ao `FOTO GF_06.11.jpg`. Antes a repetição tinha função de contexto, depois que o portfólio juntou os dois na mesma pasta, acabou. Confirmar a exclusão |
| `ANALISAR - prints de reuniao sem classificacao` | 4 | `Reunião GF 28.01.2026`, `Reunião SBB 23.01.26` e duas versões da mesma `WhatsApp Image 2025-12-03` em formatos diferentes. Dizer se são registro de trabalho, e vão para a pasta do cliente, ou prova de articulação com potencial de virar conteúdo, e voltam para a base |

Pendências que não são de arquivo:

- **O `ESTADO-ATUAL.md` está de 21/08** e não reflete esta estruturação nem as de números 15 e 16.
- **O `LEIA-ME.md` da pasta de credenciais** afirma que não existe outra cópia de senha na máquina. Era falso até hoje: duas planilhas estavam em `Documentos\2. PESSOAL`. Voltou a ser verdade, mas o texto não menciona a entrada de 24/08.
- **O `ESTADO-ATUAL.md` está de 21/08** e não reflete esta estruturação nem as de números 15 e 16.
- **O `LEIA-ME.md` da pasta de credenciais** afirma que não existe outra cópia de senha na máquina. Era falso até hoje: duas planilhas estavam em `Documentos\2. PESSOAL`. Voltou a ser verdade, mas o texto não menciona a entrada de 24/08.

## 10. Regras que passam a valer

**Sobre o marketing**

- A pasta única de marketing é `OneDrive E-missão\Documentos\9. MOBILIZANDO MKT LOGO`. Não existe segunda pasta de marketing.
- Ela é lida para gerar o perfil de captador. Só entra ali o que é marketing da Mobilizando.
- Foto de projeto de cliente é portfólio e mora em `FOTOS\PROJETOS DE CLIENTES\{cliente}\{ação}\`.
- Copy, oferta, pacotes, preço e estratégia de conteúdo moram em `POSICIONAMENTO E OFERTA\`.
- A regra antiga do `ALFA-AMC.MKT.docx`, que mandava texto e estratégia para `amc-ia-Mobi\marketing\`, está revogada.

**Sobre o que não é marketing**

- Foto pessoal e de família vai para `Documentos\2. PESSOAL`.
- Documento de cliente vai para `_82\06 - Clientes\{cliente}`.
- Credencial vai para `Desktop\Credenciais AMC IA`, sem exceção, nem quando está dentro de um `.docx` que parece de marketing.
- O resto vai para `Desktop\MOBI`, pela numeração dela.

**Sobre deduplicação**

- Comparar sempre por hash de conteúdo, nunca por nome, tamanho ou data.
- Nenhuma exclusão sem confirmar que sobra pelo menos uma cópia do mesmo conteúdo.
- Repetição com função (seleção curada, contexto duplo, atalho de uso rápido) não é duplicata. Só sai a repetição sem função.
- Antes de apagar uma pasta inteira, verificar se ela está contida em outra: foi assim que a `MOÇAMBIQUE 5` saiu sem perda.
- Ao mover arquivos para uma pasta comum, checar se a mudança criou duplicata que antes não existia.

**Sobre extração de documento com segredo**

- Documento que mistura conteúdo útil com token não entra na base de leitura. Extrair a parte útil para um arquivo novo, conferir que nenhuma cadeia longa sobrou e deixar o original onde está.
