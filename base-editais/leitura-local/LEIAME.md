# Leitura Local dos Editais Abertos

> Leitura feita em 20/08/2026 sobre os arquivos da pasta `02 - Editais Abertos`, no Desktop do captador. São 36 editais, lidos a partir do conteúdo real dos PDF, DOCX e XLSX, não do nome do arquivo.

Esta pasta NÃO substitui o cache do CaptaHub (`base-editais/editais-abertos.json`). É a leitura da carteira local de editais que o captador já garimpou, organizada para permitir, na etapa seguinte, o cruzamento com o perfil de cada OSC.

## Arquivos

| Arquivo | Uso |
|---|---|
| `editais-locais.json` | Índice estruturado dos 36 editais, com natureza jurídica aceita, território, prazo, valor e leis aceitas |
| `fichas/*.md` | Uma ficha por edital, com objeto, elegibilidade, vedações, documentos, critérios e o bloco "o que checar na OSC" |

## Como usar na análise de compatibilidade

Cada ficha tem uma seção **"O que checar na OSC para compatibilidade"**. É por ali que a análise começa. A ordem de checagem que menos desperdiça tempo é:

1. **Natureza jurídica.** Alguns editais só aceitam associação e fundação; outros excluem fundação (ISPN); outros só aceitam produtora registrada na ANCINE (BRDE); outros só pessoa jurídica sem fins lucrativos (Usiminas, Minasligas).
2. **Território.** É o corte que mais elimina. Vários editais têm lista fechada de municípios: CBMM (Araxá), Essencis (7 cidades), Energisa (Anexo 1), EDP (Anexo I), Minasligas (14 municípios), Floresta Viva (C4 e C5 do Recaatingar), Rouanet nas Favelas (8 localidades), PNAB BH (Belo Horizonte), ISPN (MA, TO, MT), Banco do Nordeste (Nordeste, Norte do ES e Norte de MG).
3. **Tempo de existência.** Impactarte e MDA exigem 3 anos; IBAMA exige 3 anos e 2 projetos concluídos; Floresta Viva e ISPN exigem 2 anos; PNAB bianual exige 5 anos.
4. **Projeto já aprovado em lei de incentivo.** Metade dos editais privados só recebe projeto aprovado e com captação vigente. Sem PRONAC ativo ou equivalente, esses canais estão fechados.
5. **Documentação e conformidade.** Certidões federais, FGTS, CEIS, CEPIM, CNEP, CADIN e ausência de agente público na diretoria aparecem como eliminatórios em Usiminas, Rumo, Banco do Nordeste e IBAMA.

## Os cortes menos óbvios (que costumam derrubar boa proposta)

- **Ambev** não aceita Rouanet, só leis estaduais, e exige sede no mesmo estado da lei.
- **EDP** também não aceita Rouanet nesta chamada.
- **Brasilseg** não aceita PROAC, ICMS nem projeto sem incentivo fiscal.
- **Shell** não apoia espetáculo teatral nem produção audiovisual, mesmo com Rouanet aprovada.
- **ISPN** exclui fundações, igrejas e empresas; só associação, sindicato rural ou cooperativa da agricultura familiar.
- **Impactarte** exclui organização religiosa e organização puramente assistencialista.
- **PNAB BH, linha continuada**, exclui iniciativa com vínculo com poder público, fundação, instituto de empresa ou Sistema S.
- **MDA** exige três cláusulas específicas no estatuto (finalidade pública, destinação do patrimônio na dissolução e escrituração contábil) e habilitação prévia no Transferegov.
- **Minasligas** veda pagamento de comissionamento de captação.
- **BRDE** exige pelo menos uma roteirista mulher cis ou trans no núcleo.

## Prazos mais próximos (a partir de 20/08/2026)

| Edital | Encerra |
|---|---|
| PNAB Ciclo 2, Belo Horizonte | 31/08/2026 |
| ISPN Fundo Ecos 49, TAIPAS | 31/08/2026 |
| Instituto EDP, Projetos Incentivados | 31/08/2026 |
| BRDE FSA, Núcleos Criativos | 04/09/2026 |
| Essencis Minas, Verbas Incentivadas | 11/09/2026 |
| Minasligas | setembro de 2026 |
| Mapfre (cultura, esporte, FIA, idoso) | 30/09/2026 |
| Ambev Brasilidades | 30/09/2026 |
| Embratur | 03/10/2026 |
| Rouanet nas Favelas 2 | 13/10/2026 |
| Shell Patrocínios Incentivados | 31/10/2026 |
| Brasilprev | último dia útil de outubro |
| Floresta Viva, ciclo 2 | 14/12/2026 |
| Mapfre (PRONAS e PRONON) | 15/12/2026 |

Prazos já encerrados na data da leitura, mantidos por serem editais com ciclos futuros ou reabertura prevista: MDA SFDT 02/2026 (encerrou em 09/08/2026) e Floresta Viva ciclo 1 (encerrou em 10/08/2026).

Os demais são de fluxo contínuo ou de credenciamento permanente.

## Pendências de material

Quatro documentos da pasta são digitalizações sem camada de texto e não puderam ser lidos. Vale baixar de novo a versão em texto na fonte antes de trabalhar esses canais:

- Santander, Política de Patrocínios 2025 (regulamento).
- Petrobras, Diretrizes de Patrocínio.
- Petrobras, Diretrizes do Programa Petrobras Cultural.
- Petrobras, FAQ.

Também está incompleto o material da Mapfre, que traz apenas o cronograma, sem as regras de elegibilidade. E o checklist do PNAB Ciclo 2 está em formato .doc antigo, que não foi lido.

## Inconsistência registrada

No edital do PNAB Ciclo 2 de Belo Horizonte, a Linha 4 (Eventos Artístico-Culturais Continuados) aparece exigindo no mínimo 5 edições do evento no item 2 e no mínimo 3 edições no item 3.2. Confirmar na versão vigente antes de inscrever.
