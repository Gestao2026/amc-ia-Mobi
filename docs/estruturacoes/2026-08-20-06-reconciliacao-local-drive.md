# 06 - Reconciliação entre a cópia local e o Drive da dona

| Campo | Valor |
|---|---|
| Data | 2026-08-20 |
| Pasta afetada | `_82` na Área de Trabalho e `_82` no Google Drive da dona |
| Tipo | Reconciliação de divergências |
| Situação | Concluída |
| Autorizada por | Rosepaula: "faça o 4" |
| Reversível | Sim, as versões anteriores dos dois lados estão guardadas |

---

## 1. Contexto: a pasta local mudou de arranjo no meio do caminho

Entre o inventário das 15h25 e a execução, a captadora reorganizou
`06 - Clientes` na cópia local. O que mudou:

| Pasta | Antes | Depois |
|---|---|---|
| `01 - OSC-Organizações da Sociedade Civil` | 12 clientes dentro | removida |
| `02 - Empresa Privada` | 6 clientes dentro | existe, vazia |
| `03 - Outros Modelos` | 5 itens | intacta |
| Os 18 clientes | dentro das categorias | soltos na raiz de `06 - Clientes` |

Contagem antes e depois: **3.490 arquivos e 5,40 GB nos dois casos.** Nada foi
perdido, só o arranjo mudou. Confirmado com a captadora que a mudança foi
deliberada, e o arranjo atual passou a ser o válido. O inventário foi refeito
antes de qualquer operação.

## 2. Por que a reconciliação era necessária

Comparando por conteúdo, 2.716 dos 2.718 arquivos locais já existiam no Drive.
Sobravam quatro pontos de divergência, todos com risco de perda:

- **Duas planilhas de controle** estavam mais novas no computador que no Drive. Uma sincronização descuidada sobrescreveria o trabalho mais recente.
- **Dois documentos de identidade** existiam só no Drive e não tinham cópia nenhuma sob controle da captadora.

## 3. O que foi executado

**Passo 1. Guardar os dois lados antes de mexer.** Cinco arquivos copiados para
`C:\Users\rosep\Backups\pasta-82\reconciliacao-2026-08-20\`, separados em
`drive-antes\` e `local-antes\`.

**Passo 2. Subir as versões mais novas do local para o Drive.**

| Planilha | Local (subiu) | Drive (era) |
|---|---|---|
| `04 - Controle de Submissão_\...\1 - Controle de Submissão_.xlsx` | 183.376 bytes, 19/08 23h09 | 184.107 bytes, 18/08 00h02 |
| `06 - Clientes\07 - CaptaDrive - Ponto Cultural\1 - Controle de Submissão.xlsx` | 169.472 bytes, 19/08 21h53 | 166.785 bytes, 12/08 01h09 |

A planilha do Ponto Cultural existe em **dois lugares no Drive**, na cópia solta e
na cópia dentro de `01 - OSC-...`. As duas foram atualizadas, para não deixar
versões diferentes convivendo.

**Passo 3. Trazer do Drive o que faltava no computador.**

| Arquivo | Tamanho |
|---|---|
| `06 - Clientes\05 - CaptaDrive - Levanta e Brilha\01 - Gestão Documental\Identidade representante legal\CNH-Germano - representante legalpdf.pdf` | 288.670 bytes |
| a mesma pasta, `Comprovante residencia.pdf` | 29.580 bytes |

A pasta `Identidade representante legal` não existia na cópia local e foi criada
para receber os dois arquivos, reproduzindo o que já existe no Drive.

## 4. Onde está a rastreabilidade

| Arquivo | O que registra |
|---|---|
| `C:\Users\rosep\Backups\pasta-82\reconciliacao-2026-08-20\reconciliacao.csv` | As 10 cópias feitas, com origem, destino e tamanho |
| `...\drive-antes\` | As versões que estavam no Drive antes de serem sobrescritas |
| `...\local-antes\` | As versões que estavam no computador |

## 5. Como reverter

Copiar de volta os arquivos de `drive-antes\` para os caminhos originais no
Drive, listados na coluna `Para` do `reconciliacao.csv`. Para desfazer a descida
dos dois PDFs, basta apagá-los da cópia local, já que o original continua no
Drive.

O Google Drive também guarda histórico de versões dos arquivos sobrescritos, o
que dá uma segunda via de recuperação pelo próprio site.

## 6. O que ficou pendente

- Avisar a dona da pasta que duas planilhas foram atualizadas no Drive dela.
- Os dois PDFs de identidade só existem na cópia **solta** de Levanta e Brilha no Drive. A cópia categorizada não os tem. Isso reforça que as cópias soltas não são duplicatas puras e exigem conferência antes de qualquer remoção.

## 7. Regras que passam a valer

- Antes de sobrescrever arquivo em pasta de terceiro, guardar as duas versões, e não só a que vai ser substituída.
- Comparar por **data de modificação**, não por tamanho. Tamanho diferente não diz qual é mais novo.
- Quando o mesmo arquivo existe em dois caminhos no Drive, atualizar os dois. Deixar um desatualizado cria a próxima divergência.
- Inventário tem validade curta. Se a pasta pode ter mudado, refazer antes de operar.
