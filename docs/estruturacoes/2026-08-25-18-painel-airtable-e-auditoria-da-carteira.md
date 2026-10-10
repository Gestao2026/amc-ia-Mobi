# 18 - Painel no Airtable e auditoria documental da carteira

| Campo | Valor |
|---|---|
| Data | 2026-08-24 e 2026-08-25 |
| Pasta afetada | Base Airtable `appKWLTFSCcWucXfQ`, CaptaHub, e `Meu Drive\CaptaDrive` (pasta `1Ye6_gYooAg0SFpE6L2TOQvSVIbvlr8lT`) |
| Tipo | Configuração, carga de dados e auditoria |
| Situação | Concluída, com pendências de tela listadas no item 9 |
| Autorizada por | A captadora, comando a comando, ao longo das duas sessões |
| Reversível | Parcialmente. Ver item 8 |

---

## 1. Por que foi feito

A planilha `PAINEL SUBMISSÃO.xlsx` mostrou o número que motivou tudo: dos 7 editais
mapeados, **6 se encerraram sem nenhuma proposta enviada**. Taxa de não submissão de
85,7%, R$ 29 milhões em oportunidade que passou. Nenhum foi reprovado.

Ou seja, o gargalo da operação não era texto fraco nem orçamento furado. Era calendário
e triagem. A planilha registrava o problema mas não avisava a tempo, porque planilha não
manda e-mail nem calcula prazo sozinha.

O segundo problema: a carteira de clientes vivia em três lugares (CaptaHub, planilhas e
pastas do Drive) sem nenhum cruzamento, e o cadastro tinha erro que só apareceria no dia
da submissão.

## 2. O que foi decidido, e por quem

Decisões da captadora, na ordem em que foram tomadas:

- O Airtable é o **painel operacional**; o CaptaHub continua sendo o **cadastro**.
- A sincronização é **de mão única**: CaptaHub manda, Airtable recebe.
- **Cliente inativo não entra** na carteira do Airtable, e se estiver, sai.
- Editais vencidos e não submetidos ganham **tabela própria**, não ficam junto dos vivos.
- O vocabulário é **"não submetido"**, nunca "perdeu o prazo". Fato, não acusação.
- As faixas de alerta são **7 e 30 dias**, não 3 e 15.
- **Sem Tempo Hábil** fica no grupo Não submetido, não em Descartado.
- O campo de documento passa a se chamar **CNPJ/CPF**, porque nem todo cliente é OSC.
- O nome do cliente segue a **razão social**, não o nome de projeto.

Descartado: pipeline e CRM dentro da AMC IA, que continuam sendo do CaptaHub.

## 3. Estado antes

| Medida | Valor |
|---|---|
| Base Airtable | 1 tabela vazia de exemplo, 3 registros em branco |
| Clientes no Airtable | 1 (STK Produções) |
| Editais no Airtable | 1 registro em branco |
| Painel | não existia |
| Automações | 3 montadas, nenhuma publicada |
| Sincronização CaptaHub e Airtable | não existia |

## 4. O que foi executado

1. Excluída a tabela de exemplo e desenhadas as 4 tabelas reais: Clientes, Editais,
   Projetos e Financiadores.
2. Criada a 5ª tabela, **Não Submetidos**, ligada a Editais por vínculo, sem cópia.
3. Conferida a planilha `PAINEL SUBMISSÃO.xlsx`: os 15 status batiam, e faltavam no
   Airtable o Tipo de edital, a separação entre valor total e teto por projeto, a Próxima
   data e a Documentação por projeto.
4. Trocados os 15 status pelos **27 definidos pela captadora**, com as cores da planilha,
   e religadas as duas fórmulas, o painel e o alerta.
5. Criado o **Painel de Captação**, interface com 5 abas, cada número com o significado
   escrito em cinza embaixo.
6. Resolvida a coloração por círculo dentro da fórmula, porque colorir por condição é
   recurso do plano pago.
7. Criadas 5 automações de alerta por e-mail, todas ainda desligadas.
8. Escrito `scripts/sincronizar-clientes-airtable.py` e o `.bat` do Agendador.
9. Carregados os clientes do CaptaHub, e retirados por decisão ABA, Paixão por BH e GAMT.
10. Mapeadas as 18 pastas do CaptaDrive e gravado o link em cada cliente.
11. Cadastradas 3 OSCs novas nos dois sistemas: Santa Casa de Itabuna, Mãos Unidas pelo
    Autismo e Núcleo Espírita Maria Dolores, a partir dos documentos do Drive.
12. Auditados os **19 Cartões CNPJ**, depois que a captadora reemitiu os digitalizados.
13. Renomeada a Quintal Eh para **Cinestratégico** nos três lugares.

## 5. Estado depois

| Medida | Antes | Depois |
|---|---|---|
| Tabelas | 1 de exemplo | 5 em uso |
| Clientes no Airtable | 1 | 21 |
| Campos com regra escrita | 0 | mais de 90 |
| Painel | não existia | 5 abas publicadas |
| Automações | 3, desligadas | 5, desligadas |
| Sincronização | não existia | script testado, rodando sob demanda |
| Erros de cadastro corrigidos | 0 | 9 |

## 6. Onde está a rastreabilidade

| Arquivo | O que registra |
|---|---|
| `docs/regras-de-negocio-airtable.md` | Todas as regras de negócio, campo a campo |
| `scripts/sincronizar-clientes-airtable.py` | A sincronização e os 7 campos protegidos |
| `scripts/sincronizar-clientes.bat` | O envelope do Agendador |
| Campo Natureza jurídica detalhada, no Airtable | O texto que o CaptaHub achatou |
| Campo Observações estratégicas, no Airtable | O que cada Cartão CNPJ revelou |
| `Backups\_historico-sincronizacao.log` | Cada rodada da sincronização |

## 7. Backup feito antes

| Origem | Destino | Conferido |
|---|---|---|
| Nenhum | Nenhum | A base estava vazia; não havia dado a perder |

O backup diário das 12h30 continua cobrindo o projeto. A base do Airtable **não** entra
nele: ela vive na nuvem da Airtable e não tem cópia local.

## 8. Como reverter

**Os clientes.** Basta apagar os registros no Airtable e rodar a carga de novo. O
CaptaHub é a fonte e não foi destruído em nenhum momento.

**As correções de cadastro.** As 9 datas e a natureza jurídica do NEMD foram corrigidas
no CaptaHub. Os valores antigos estão na tabela do item 10 deste registro e no histórico
desta conversa. Para desfazer, é digitar de volta.

**O painel e as tabelas.** Não há reversão automática. Cada exclusão de campo ou tabela
feita pela API devolveu um identificador de desfazer, mas eles expiram quando o esquema
muda. Na prática, refazer é o caminho.

**A pasta do Drive renomeada.** É só renomear de volta para `08 - CaptaDrive - Quintal Eh`.

## 9. O que ficou pendente

Tudo que depende da tela, porque a API do Airtable não expõe:

- Publicar as 5 automações. Enquanto não forem ligadas, nenhum e-mail sai.
- Aplicar as regras de cor por condição, se houver upgrade para o plano Team.
- Acrescentar **Em negociação** e **Negociado** na lista Situação.
- Acrescentar **Reciclagem** em Áreas temáticas, na tabela Clientes.
- Ocultar os campos da seção 8 do documento de regras e criar as visões.
- Renomear a área de trabalho, hoje "My First Workspace", e trocar o ícone da base.

Do lado do CaptaHub:

- A aba **Geral** tem Status, Nome do Contato, Endereço e Link da Pasta, e a aba
  **Perfil completo** tem Tempo de existência e Experiência prévia. **Nada disso vem pela
  API.** Só se lê na tela.
- O contrato da Mobilizando com o NAME traz CNPJ 60.346.136/0001-80, e o Cartão CNPJ diz
  64.302.549/0001-13. **Corrigir o contrato.**

## 10. Regras que passam a valer

**O Cartão CNPJ é a fonte da verdade do cadastro.** Não o que está digitado no CaptaHub.
A auditoria de 19 cartões achou erro em 9:

| Cliente | Estava | Cartão CNPJ diz |
|---|---|---|
| Ponto Cultural | 27/08/1998 | 22/03/2001 |
| Instituto Kuyper | 23/11/2020 | 18/05/2021 |
| Inter São Gotardo | 04/10/2001 | 21/03/2002 |
| Levanta e Brilha | 16/04/2016 | 22/08/2016 |
| Rede Amor e Compaixão | 29/04/2011 | 27/06/2011 |
| Luzeiros da Glória | 18/12/2025 | 13/02/2026 |
| NAME | 19/12/2025 | 18/12/2025 |
| MUPA | em branco | 01/06/2012 |
| NEMD | Associação | **Organização Religiosa, 322-0** |

**Cadastro se corrige no CaptaHub, gestão se faz no Airtable.** Corrigir CNPJ ou data
direto no Airtable é trabalho perdido: a próxima sincronização sobrescreve.

**Sete campos são só do Airtable** e a sincronização nunca os toca: Situação, CaptaDrive,
Observações estratégicas, Pendências documentais, Pasta local, Responsável e Natureza
jurídica detalhada.

**O script nunca cria cliente.** Quem entra na carteira é decisão humana. Rodar a
sincronização não traz de volta quem saiu.

**Um registro é uma edição de edital.** Edição encerrada nunca se reescreve; quando a
próxima abrir, duplica-se o registro e muda-se o Ciclo.

**Perder prazo não é escolha.** Por isso "Sem Tempo Hábil" não se esconde entre os
descartes, e o status de um projeto perdido não vira Descartado. O cemitério é
diagnóstico, não arquivo morto.
