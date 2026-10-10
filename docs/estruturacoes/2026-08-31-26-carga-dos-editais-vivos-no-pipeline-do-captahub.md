# 26 - Carga dos editais vivos no pipeline do CaptaHub

| Campo | Valor |
|---|---|
| Data | 2026-08-31 |
| Pasta afetada | Pipeline do CaptaHub (3 projetos criados), `docs/`, memória persistente |
| Tipo | Carga de dados em sistema externo, com triagem prévia |
| Situação | Concluída. 3 fichas criadas. **2 pendências**, listadas no item 5 |
| Autorizada por | A captadora, em quatro decisões: o conjunto alvo, a ficha canônica do FIA, a da Ambev e a confirmação do Shell |
| Reversível | Sim. As três fichas podem ser excluídas na tela do CaptaHub pelos ids do item 3 |

---

## 1. O pedido e o que ele produziria

O pedido foi "rodar os editais para o pipeline no CaptaHub". O conjunto natural
eram os **28 editais marcados `Interessa` no funil do Airtable que ainda não
tinham projeto**. A captadora autorizou carregar os que já existissem como
edital no CaptaHub, e apenas listar os demais.

Ao conferir prazo contra a data de hoje, a carga autorizada se revelou inútil:

| Edital que casava com o CaptaHub | Situação em 31/08 |
|---|---|
| BH nas Telas 2026 | vencido há 21 dias |
| Seleção pública de Projetos Comunitários (Fundação BB Rio Doce) | vencido há 70 dias |
| Fundo Valor Local | vencido há 98 dias |
| PNAB Lages 2026 Fomento | vencido há 55 dias |
| Edição BNDES Periferias Mulheres (5º ciclo) | vencido há 80 dias |
| Seleção de Projetos Aprovados via FIA | vencido há 49 dias |
| Programa Incentivar 2026 | vencido há 82 dias |
| BIP Prosas | sem prazo, mas já estava no pipeline como BIP Esporte e BIP Cultura |

Seriam 7 fichas mortas e 1 duplicata. **Nada foi gravado desse conjunto.** A
captadora foi consultada com o achado e redirecionou a carga.

## 2. O achado que inverteu o problema

Dos 28 editais `Interessa` sem projeto, só **4 tinham prazo vivo**, e eles
estavam justamente entre os que o casamento automático não encontrava. Procurados
um a um, **três existiam no CaptaHub com outro título**, e com duplicata.

O gargalo não era carregar o pipeline. Era que a base global de editais do
CaptaHub repete o mesmo edital em várias fichas, e escolher a canônica é decisão
humana: o `edital_id` amarra prazo, valor e critérios do projeto.

Erro de método corrigido no caminho: a primeira tentativa de casamento cortava a
query string da URL, o que colapsou todos os links do Prosas na mesma chave e
gerou 8 casamentos falsos apontando para o mesmo edital de 2023. As chaves que
funcionam são o `edital_id` da URL do Prosas e o id da URL da Plataforma Êxitos.

## 3. O que foi criado

Três fichas, todas em `encontrar_cliente`, sem cliente amarrado, porque o encaixe
com a OSC ainda não está fechado.

| Edital | Prazo | id do projeto | id do edital |
|---|---|---|---|
| Edital FIA Fundos da Infância e Adolescência | 13/09 (13 dias) | `aea932ab-1f4c-4f98-bdb4-08a03ac82b6d` | `cc9fab7b-49d3-49a4-987d-4ef0692a4cd2` |
| Edital Ambev Brasilidades 2026 | 30/09 (30 dias) | `7498eec6-287c-4b80-9adb-c9c922e84db6` | `d698d1a3-a713-48da-8382-c0650601fb16` |
| Edital de Patrocínio Shell Cultural 2026 | 31/10 (61 dias) | `6d129b2c-d16e-4cf7-a02e-e9c67031a8d5` | `83e81534-748b-4352-b533-b28b928b4f95` |

Critério de escolha da ficha canônica, aplicado com o aval da captadora: órgão
preenchido, link apontando para a página do edital e não para notícia, blog ou
PDF em S3 com assinatura vencida, e link batendo com o do funil.

Pipeline do CaptaHub: de 58 para **61 projetos**.

## 4. Estado antes e depois

| Medida | Antes | Depois |
|---|---|---|
| Projetos no pipeline do CaptaHub | 58 | **61** |
| Projetos do pipeline sem edital ligado | 43 | 43 |
| Editais `Interessa` sem projeto, no funil | 28 | 25 |
| Editais vivos do funil sem ficha de pipeline | 4 | **1** (Essencis Minas) |

## 5. Pendências com a captadora

1. **Essencis Minas (prazo 11/09)** não existe na base do CaptaHub. Busca vazia.
   Precisa ser cadastrado na tela do painel, porque o token da AMC IA não tem
   escopo de escrita em editais. Depois disso a ficha de pipeline sai em segundos.
2. **Os 43 projetos do pipeline sem edital ligado** continuam como estavam. É a
   herança da carga de 06/08 e a reconciliação segue pendente, agora com o
   método de casamento por chave estrita já testado e disponível.

Achado de passagem, para conferir: a linha **Prefeitura de BH** no funil do
Airtable tem como URL o link do patrocínio da Shell
(`maisbaluarte.com.br/patrocinioshell`). Título e link não combinam.

## 6. Os 25 que ficaram de fora

Vinte e um estão vencidos, de 18 a 123 dias. Dois são sem prazo (USIMINAS e
Wadhwani). Vários não são edital e sim financiador solto, e por isso nunca vão
casar com nada: PETROBRAS, Prefeitura de BH, SEDESE, Prefeitura de Sabará,
Essencis Minas. A triagem desses é decisão da captadora.

## 7. Rastreabilidade

Registro anterior `docs/estruturacoes/2026-08-31-25-correcao-da-contagem-de-propostas-enviadas.md`,
memórias `captahub-base-de-editais-tem-duplicata` e
`captahub-o-que-o-token-pode-escrever`, script `scripts/captahub-api.py`.
