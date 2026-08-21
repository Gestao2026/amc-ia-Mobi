# 04 - Renomeação de um arquivo no Drive da dona (Levanta e Brilha)

| Campo | Valor |
|---|---|
| Data | 2026-08-20 |
| Pasta afetada | `_82` no Google Drive da dona, `06 - Clientes\05 - CaptaDrive - Levanta e Brilha\01 - Gestão Documental\03 - Atas e Constituição\3- DOCUMENTOS INSTITUCIONAIS ANTERIORES` |
| Tipo | Renomeação de um único arquivo |
| Situação | Concluída |
| Autorizada por | Rosepaula, escolhendo renomear em vez de excluir |
| Reversível | Sim, renomeando de volta. O nome antigo está registrado abaixo |

---

## 1. Por que foi feito

Era o **único arquivo dos 6.023** da pasta que continuava acima do limite de 260
caracteres mesmo com a solução de unidade virtual. O nome tinha **236
caracteres**, uma frase inteira, e o caminho completo chegava a **478**.

A alternativa considerada era excluir, e foi descartada. O arquivo **não é lixo**:
é o ponteiro para o Google Docs com a lista de presença da Assembleia Geral
Extraordinária do Centro Missionário, de 26/02/2026. Documento constitutivo,
guardado em `Atas e Constituição`, exatamente o tipo de papel que o CaptaDoc
exige na elegibilidade.

Além disso, o arquivo está no Drive **da dona da pasta**, não no da captadora.
Excluir mandaria o Google Docs original para a lixeira da conta dela e sumiria
para todos que têm acesso.

## 2. O que foi decidido

- **Renomear, não excluir.** Resolve o comprimento e preserva o documento.
- **Seguir a convenção que a própria pasta já usa.** Na mesma pasta, `EDITAL DE CONVOCAÇÃO.gdoc` espelha o `EDITAL DE CONVOCAÇÃO.docx` do nível acima. O novo nome espelha o irmão `Lista de presença AGE 26_02_2026 - Centro Missionário.docx`.
- **Avisar a dona**, porque renomear um `.gdoc` renomeia o Google Docs para todos.

## 3. O que mudou

| | Nome | Caracteres | Caminho completo |
|---|---|---|---|
| Antes | `Lista de presença da Assembleia Geral Extraordinária da Associação Centro Missionário de Desenvolvimento Social, realizada no dia 26 02 2026, referente ao Edital de Convocação de Assembleia Geral Extraordinária datado de 16 02 2026.gdoc` | 236 | 478 |
| Depois | `Lista de presença AGE 26_02_2026 - Centro Missionário.gdoc` | 58 | 300 |

## 4. Efeito na pasta inteira

| Medida | Antes | Depois |
|---|---|---|
| Maior caminho relativo do `_82` no Drive | 373 | **249** |
| Arquivos acima de 260, com unidade virtual | 1 | **0** |

Com isso, os **6.023 arquivos** da pasta do Drive passam a ser acessíveis assim
que a unidade virtual for configurada. Antes disso, pelo caminho atual do atalho
(prefixo de 104 caracteres), continuam 2.588 arquivos inacessíveis, porque o
gargalo ali é o prefixo e não este arquivo.

## 5. Verificação feita

- Conferido que não havia arquivo com o nome novo na pasta, antes de renomear.
- Depois da renomeação, o arquivo continua na pasta com os mesmos **198 bytes**.
- O conteúdo do Google Docs não é afetado por renomeação. Só o título muda.

## 6. Como reverter

Renomear de volta para o nome antigo, que está registrado por inteiro na tabela
do item 3.

## 7. O que ficou pendente

- **Avisar a dona da pasta.** O Google Docs aparece com o novo título para todos que têm acesso.
- O outro `.gdoc` da mesma pasta, `EDITAL DE CONVOCAÇÃO.gdoc`, tem 25 caracteres e não precisou de nada.
- Há um terceiro `.gdoc` na pasta, em Ponto Cultural (`Projeto_Elas_no_Esporte_-_Ano_I[1] (1).gdoc`), também dentro do limite.

## 8. Regras que passam a valer

- **Arquivo em pasta de terceiro se renomeia, não se exclui.** Renomear é reversível e não tira nada de ninguém.
- Antes de mexer em qualquer arquivo de pasta compartilhada, verificar se o conteúdo existe em outro lugar e se o arquivo é documento institucional.
- Ao renomear, seguir a convenção que a própria pasta já pratica, não inventar uma nova.
- Toda renomeação em pasta de terceiro fica registrada aqui com o nome antigo por extenso, para permitir a volta.
