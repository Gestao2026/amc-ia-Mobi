# 22 - Limpeza das cópias divergentes da _82 e exceção do Meu Drive local

| Campo | Valor |
|---|---|
| Data | 2026-08-28 |
| Pasta afetada | `C:\amc-ia-Mobi-backup-piloto-2026-08-20`, `_82` do Drive (`12 - Backup Clientes - Atividade Jurídica`), `Backups\pasta-82\atual\06 - Clientes`, `_credenciais-nao-sincronizar\` (dois arquivos de senha), `C:\Users\rosep\Meu Drive\_82 - ...` |
| Tipo | Exclusão de duplicata e de cópia obsoleta |
| Situação | Concluída |
| Autorizada por | A captadora, item por item, ao longo da mesma sessão. A exclusão do `Meu Drive local` teve autorização específica de exceção à regra de nunca apagar pasta `_82` |
| Reversível | Parcial. Ver item 9: a exclusão do `Meu Drive local` não foi para a Lixeira, foi definitiva |

---

## 1. Por que foi feito

Na mesma sessão em que se investigou o susto de arquivo "sumido" da Área de Trabalho
(registro 21), a captadora pediu para seguir limpando a bagunça de cópias divergentes
que vinha sendo mapeada havia várias trocas de mensagem: duplicatas dentro do próprio
Drive, pastas fantasma dentro do backup, arquivos com senha exposta, e uma quarta cópia
inteira (`Meu Drive local`) que não sincronizava mais com nada.

Cada exclusão só foi proposta depois de uma varredura que comparava **conteúdo**, não só
nome de pasta, para não repetir o erro cometido mais cedo na mesma sessão (uma pasta de
modelo em branco foi inicialmente confundida com conteúdo perdido).

## 2. O que foi decidido, e por quem

- Excluir `C:\amc-ia-Mobi-backup-piloto-2026-08-20` (1,76 GB), depois de uma varredura
  cliente por cliente que achou zero perda real.
- Excluir `12 - Backup Clientes - Atividade Jurídica` dentro do Drive (4,88 GB),
  duplicata da `06 - Clientes` com nomes anteriores à correção de 25/08.
- Excluir 16 pastas e arquivos fantasma dentro de `Backups\pasta-82\atual\06 - Clientes`
  (nomes antigos de cliente, categorias pré-numeração, cópia extra do modelo).
- Excluir dois arquivos `Senha_ 123456.docx` (MUPA) que expunham senha no nome, dentro
  de `_credenciais-nao-sincronizar\`. Executado em dois momentos: o comando foi
  preparado primeiro e só rodado de fato mais tarde, depois de a captadora perguntar
  por que ainda não tinha sido feito. Confirmado nos dois lados, foram para a Lixeira
  normalmente.
- **Abrir uma exceção pontual** à regra "pasta `_82` nunca se apaga" (ver
  [[pasta-82-nao-se-apaga]]) para excluir `C:\Users\rosep\Meu Drive\_82 - ...` por
  inteiro (5,75 GB), só depois de a análise confirmar, item por item, que nada ali era
  exclusivo.

Descartado por ora: excluir o `.pfx` do certificado das Mãos Unidas Pelo Autismo (achado
na mesma varredura, com a senha no nome do próprio certificado) e os quatro documentos de
acesso da mesma pasta. A captadora disse "não precisa" quando isso foi oferecido; fica
como pendência de segurança, não como limpeza concluída.

## 3. Estado antes

| Medida | Valor |
|---|---|
| Cópias inteiras da `_82` no computador | 4 (Drive, Área de Trabalho, Meu Drive local, mais o cofre de backup) |
| Volume do Drive | 9,75 GB, incluindo 4,88 GB de duplicata interna (`12 - Backup Clientes`) |
| Volume do backup do Drive (`pasta-82\atual`) | 19,78 GB, quase o dobro do Drive real |
| Volume do Meu Drive local | 5,75 GB |
| Arquivos com senha exposta no nome, achados | 3 (dois da MUPA, um das Mãos Unidas Pelo Autismo) |

## 4. O que foi executado

1. Confirmada a exclusão de `amc-ia-Mobi-backup-piloto-2026-08-20`, feita pela própria
   captadora.
2. Verificado no Drive o conteúdo de `12 - Backup Clientes - Atividade Jurídica`: 18
   pastas de cliente com nomes anteriores à correção, incluindo a cópia do arquivo de
   senha da MUPA. Excluída pela captadora.
3. Levantada a lista exata de 16 itens fantasma dentro de `Backups\pasta-82\atual\06 -
   Clientes`, cada um com o nome certo já presente ao lado. Excluídos pela captadora.
4. Localizado o caminho dos dois `Senha_ 123456.docx` (MUPA) dentro de
   `_credenciais-nao-sincronizar\` e preparado o comando de exclusão.
5. Feita a varredura fina do `Meu Drive local`: comparados os quatro clientes que não
   batiam por nome contra o Drive e a Área de Trabalho. Três eram certidão vencida ou
   duplicata de duplicata. O quarto, `01 - Grupo Faz de Novo`, foi identificado por
   conteúdo (mesma equipe, mesmo edital PNAB 2026 Contagem) como uma versão antiga do
   cliente hoje chamado `17 - Faz de Conta`, já mais avançada no Drive (tem resultado e
   recurso de edital que a cópia antiga não tinha).
6. Apresentada a análise à captadora, que autorizou a exceção específica e excluiu a
   pasta inteira.
7. Confirmada a exclusão de `Meu Drive local`. **Ao checar se ela tinha ido para a
   Lixeira, como as exclusões anteriores, não foi encontrada nem no painel da Lixeira
   nem na pasta crua `C:\$Recycle.Bin\` no disco.** A exclusão foi definitiva, não
   reversível. Hipótese mais provável: caminhos internos longos (dentro de
   `CLIENTES Adapte\NEMD\CECA - APROVADO\...`) impediram o Windows de preservar o item
   na Lixeira.
8. A captadora pediu conferência byte a byte do conteúdo excluído contra o que restou.
   **Não foi possível**, porque a fonte para comparar não existe mais em lugar nenhum
   (nem Lixeira, nem cópia de sombra, nem ponto de restauração, já descartados no
   registro 21). A garantia que existe é a varredura por nome, tamanho e amostra de
   conteúdo feita **antes** da exclusão (passo 5), não uma comparação byte a byte
   posterior.
9. A captadora perguntou por que os dois `Senha_ 123456.docx` ainda não tinham sido
   excluídos. O comando do passo 4 nunca tinha sido executado, só preparado. Rodado
   agora, e desta vez confirmado que os dois foram para a Lixeira normalmente (arquivo
   pequeno, sem o problema de caminho longo do passo 7).
10. Atualizado o `CLAUDE.md` e a memória [[pasta-82-nao-se-apaga]] para refletir a
    exceção e reduzir a lista de instâncias protegidas de quatro para três.

## 5. Estado depois

| Medida | Antes | Depois |
|---|---|---|
| Cópias inteiras da `_82` | 4 | 3 |
| Duplicata interna no Drive | 4,88 GB | 0 |
| Itens fantasma no backup do Drive | 16 | 0 |
| Arquivos com senha da MUPA expostos no projeto | 2 | 0 |
| Volume do Meu Drive local | 5,75 GB | pasta não existe mais |

## 6. Onde está a rastreabilidade

| Arquivo | O que registra |
|---|---|
| `CLAUDE.md`, seção "A pasta `_82` inteira é intocável" | A exceção aberta e o motivo |
| `memory/pasta-82-nao-se-apaga.md` | A mesma exceção, com o padrão de prova exigido para futuras exceções |
| Este arquivo | O raciocínio completo e a lista do que foi excluído |

## 7. Backup feito antes

| Origem | Destino | Conferido |
|---|---|---|
| Nenhum backup adicional | — | A maioria das exclusões foi para a Lixeira do Windows, conferido item a item. A exclusão do `Meu Drive local` foi definitiva, sem backup prévio dedicado (ver item 9) |

## 8. Como reverter

**A maioria dos itens**: abrir a Lixeira do Windows e usar Restaurar.

**`Meu Drive local`**: não há como reverter. Não foi para a Lixeira, não há cópia de
sombra nem ponto de restauração neste computador. A única forma de recuperar qualquer
arquivo específico dali seria reconstruir manualmente a partir do que existe na Drive
ou na Área de Trabalho, usando a mesma comparação por nome feita no passo 5 do item 4.

## 9. O que ficou pendente

- **A exclusão do `Meu Drive local` foi definitiva, não reversível**, ao contrário do
  que foi dito à captadora antes de ela rodar o comando. Isso só foi descoberto quando
  ela pediu a conferência byte a byte, depois da exclusão já feita.
- **A conferência byte a byte pedida pela captadora não pôde ser feita**, porque a fonte
  já não existe em lugar nenhum. A garantia que existe é a varredura por nome, tamanho e
  amostra de conteúdo, feita antes da exclusão, não uma comparação posterior.
- ~~O certificado `.pfx` das Mãos Unidas Pelo Autismo~~ **Resolvido, ver item 11.**
- ~~Os quatro documentos de acesso não abertos~~ **Resolvido, ver item 11.**
- ~~A senha real do certificado da MUPA~~ **Encerrado por decisão da captadora, ver
  item 11: não vamos mais perseguir a troca com o emissor.**
- **Item #2** (`amc-ia-original`) e a numeração duplicada da `_82` na Área de Trabalho
  ainda não foram tratados.
- **A duplicata `12 - Backup Clientes - Atividade Jurídica` dentro do backup do Drive**,
  ~~pendência~~ **excluída, ver item 11.**

## 10. Regras que passam a valer

- **Comparação por conteúdo, não por nome, é obrigatória antes de qualquer exclusão de
  pasta `_82` ou de suas cópias.** Foi assim que se evitou apagar o `Grupo Faz de Novo`
  achando que era perda, quando na verdade era o mesmo trabalho, só desatualizado.
- **Abrir exceção a uma regra de "nunca apagar" exige prova específica daquela pasta,
  não uma avaliação geral.** A exceção do Meu Drive local só foi concedida depois de
  descartar, um por um, todos os itens que pareciam exclusivos dela.
- **Nunca afirmar que uma exclusão "vai para a Lixeira, não é definitiva" sem conferir
  depois.** Estrutura de pasta funda, com caminho interno longo, pode fazer o Windows
  apagar em definitivo mesmo usando o comando normal de excluir. A partir de agora,
  toda exclusão de pasta grande ou funda se confere na Lixeira logo depois de rodar,
  antes de dizer à captadora que está reversível.
- **Achado de segurança durante uma limpeza de arquivo vira pendência registrada, não
  vira decisão automática.** O certificado das Mãos Unidas ficou de fora da exclusão
  porque a captadora não pediu, e isso fica escrito, não broadcast.

## 11. Continuação, tarde de 28/08/2026

Mais tarde no mesmo dia, a captadora retomou as pendências 3, 4, 5 e 6 do quadro
apresentado a ela.

**Pendências 3 e 4 (arquivos de credencial soltos no projeto).** Antes de mover, cada
arquivo foi comparado por hash SHA256 contra o que já existia em
`Desktop\Credenciais AMC IA`. De sete arquivos candidatos, cinco já eram idênticos byte
a byte ao que já estava na pasta de destino (não precisou mover, mover teria só
duplicado). Dois eram genuinamente novos ou diferentes:
- `MAOS_UNIDAS_PELO_AUTISMO_157040370000178 SENHA 123456.pfx`, movido para a raiz de
  `Credenciais AMC IA` (não existia lá).
- `ACESSOS.docx`, que tinha tamanho diferente do já existente no destino (14.675 contra
  16.207 bytes). Não foi sobrescrito: movido com o nome
  `ACESSOS (versão do projeto, conferir).docx`, para a captadora comparar os dois e
  decidir qual fica.

**Pendência 5 (senha real do certificado da MUPA).** A captadora decidiu não perseguir a
troca da senha com o emissor. Pendência encerrada por decisão dela, não por execução.

**Pendência 6 (duplicata `12 - Backup Clientes - Atividade Jurídica` dentro do backup do
Drive).** Comparação em três rodadas, corrigindo o método a cada uma:
1. Por caminho exato: 1.845 arquivos, 1.534 idênticos, 311 sem correspondência.
2. Por nome de arquivo em qualquer lugar da pasta do cliente certo: subiu para 1.712
   batendo, 133 sem correspondência, concentrados em três clientes que tiveram o nome
   trocado (Cinestratégico, AACRRI_Adapte, Bandeja Filmes).
3. Corrigido o mapeamento do grupo Adapte, que tinha virado quatro clientes
   independentes (`18-AACRRI_Adapte`, `19-Mupa_Adapte`, `20-NEMD_Adapte`,
   `21-SCMI_Adapte`) e só estava sendo comparado contra um. Por nome **e** tamanho,
   contra os destinos certos: de 336 arquivos nos três grupos, só 11 ficaram sem
   nenhuma correspondência.

Dos 11, quatro tinham valor real e foram copiados para as pastas atuais certas antes da
exclusão: `cianotipia.jpeg` e `IMG_20231014_233934.jpg` (fotos do Cinestratégico) e
`CNPJ - MUPA (versão janeiro, conferir).pdf` e `MUPA.jpeg` (documentos da Mupa_Adapte,
o CNPJ renomeado de propósito para sinalizar que é uma versão a conferir, não a atual).
Os outros sete eram CNPJ antigo já substituído, documento de acesso que não deveria
estar ali, e mais uma cópia do arquivo de senha exposta da MUPA. Ficaram de fora do
resgate.

Depois do resgate, `12 - Backup Clientes - Atividade Jurídica` foi excluída do backup do
Drive. **Mesmo padrão do `Meu Drive local`: não foi para a Lixeira**, confirmado nos dois
lados (sumiu do caminho original, não apareceu na Lixeira). Pasta funda, com muitos
arquivos de caminho longo, mesma causa provável. O risco de perda é considerado baixo
porque a comparação foi feita por nome e tamanho contra os destinos certos antes de
excluir, e o que tinha valor genuíno já foi copiado para o lugar certo.

**Pendência 7 (segunda camada de nuvem para o backup da Área de Trabalho).** Adicionado
um bloco novo ao `scripts/backup-diario.bat`, copiando `Backups\desktop-82\atual` para
`G:\Meu Drive\AMC-IA-Backup\desktop-82`. A origem escolhida foi o backup local, não a
pasta viva da Área de Trabalho, para não recriar um processo tocando naquela pasta
depois do isolamento do registro 21. Esse bloco só roda quando a tarefa agendada for
religada, hoje ela continua desativada.
