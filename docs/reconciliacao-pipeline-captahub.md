# Reconciliação do pipeline do CaptaHub. Os 43 projetos sem edital ligado

> Levantado em 31/08/2026. **O `PATCH /v1/projetos/{id}` recusa o campo `edital_id`** com erro 422,
> "Nenhum campo válido para atualizar". O `edital_id` só é aceito na criação.
>
> Existe um caminho pela API: como o `POST` aceita `edital_id` e o `DELETE /v1/projetos/{id}` funciona,
> dá para recriar a ficha já ligada e apagar a antiga. **Mas o id do projeto muda**, e ele está gravado no
> Airtable (`ID CaptaHub projeto`) e nos `estado.md` locais; a data de criação vira a de hoje; e o
> Checkpoint do CaptaHub, que não existe na API, se perde em silêncio. Por isso esse caminho só se usa em
> ficha vazia, em `encontrar_cliente`, sem OSC, valor ou nota. **As demais se ligam na tela do CaptaHub**,
> e é para isso que serve esta folha.
>
> **Já resolvidos em 31/08 por recriação:** FAVORECICLE 2025 e ArcelorMittal Investe 2027. Restam 41.
>
> **O BIP tem um edital por trilha**, conferido em 31/08: BIP Cultura (`db38b8ac`), BIP Esporte (`1ff18f09`),
> BIP Reciclagem (`f3244082`), BIP Fundo da Pessoa Idosa (`63ab1471`) e BIP FIA (`c3347702`), todos do PROSAS
> e contínuos. A ficha genérica "Banco de Incentivados da Prosas – BIP" (`c2282489`) é a guarda-chuva antiga,
> com prazo vencido em 31/12/2025, e **não deve ser usada**.

Confiança: **alta** significa título idêntico ou quase, pode ligar direto. **Média** significa
candidato plausível que precisa do seu olho antes. **Sem candidato** significa que não existe
edital correspondente na base, quase sempre porque a ficha é de financiador ou banco de projetos,
e não de um edital com prazo.


## Confiança alta. Pode ligar direto

| Projeto | Estágio | OSC | Edital no CaptaHub | id | Prazo | Como casou |
|---|---|---|---|---|---|---|
| Edital Social Lei de Incentivo à Reciclagem FAVORECICLE 20 | `encontrar_cliente` | sem OSC | EDITAL SOCIAL LEI DE INCENTIVO À RECICLAGEM - FAVORE | `88978971` | 2027-10-30 | **feito em 31/08** |
| Edital ArcelorMittal Investe 2027 | `encontrar_cliente` | sem OSC | Edital ArcelorMittal Investe 2027 | `945ff1d5` | 2026-08-16 | **feito em 31/08** |
| CHAMADA FAPEMIG/SEDE - 011/2026 - COMPETE MINAS | `submetido` | Quintal Eh | CHAMADA FAPEMIG/SEDE - 011/2026 - COMPETE MINAS | `b7ffe660` | 2026-07-30 | título idêntico |
| Edital Ambev Brasilidades 2026 | `elaborar_projeto` | Associação Ponto Cultural | Edital Ambev Brasilidades 2026 | `d698d1a3` | 2026-09-30 | título idêntico |
| EDITAL DE CHAMAMENTO PÚBLICO Nº 01/2026 - FOMENTO À EXECUÇ | `submetido` | sem OSC | Edital De Chamamento Público PNAB Nº 01/2026 Fomento | `5bf0865b` | 2026-06-01 | título 97% igual |
| Edital de Chamamento Público SNSA/MCID nº 01/2026 APOIO À  | `reprovado` | sem OSC |  Chamamento Público SNSA/MCID nº 01/2026 - APOIOÀ IN | `68e1d14c` | 2026-07-31 | título 96% igual |
| Programa Shell de Patrocinios Incentivados 2026 | `checklist` | STK Produções Ltda | Edital de Patrocínio Shell Cultural 2026 | `83e81534` | 2026-10-31 | confirmado por você hoje |
| BIP Esporte - Banco de Incentivados Prosas | `encontrar_cliente` | sem OSC | BIP: Esporte | `1ff18f09` | contínuo | trilha própria, conferido em 31/08 |
| BIP Cultura - Banco de Incentivados Prosas | `selecionado` | Berê Xikrin | BIP: Cultura | `db38b8ac` | contínuo | trilha própria, conferido em 31/08 |

## Confiança média. Confira antes de ligar

| Projeto | Estágio | OSC | Candidato a edital | id | Prazo | Ressalva |
|---|---|---|---|---|---|---|
| Instituto John Deere - Banco de Projetos | `encontrar_cliente` | sem OSC | Instituto John Deere - Banco de Projetos 2025 | `63cc1f75` | 2025-11-12 | o do CaptaHub é da edição **2025** |
| APC - Assistência para Projetos Comunitários e de Seguranç | `encontrar_cliente` | sem OSC | Programa de Assistência para Projetos Comunitários e | `64a0d361` | sem prazo | título 91% igual |
| Edital Social Grupo Porto 2026 | `encontrar_cliente` | sem OSC | Edital Social Porto 2026 | `499c3da2` | 2026-07-31 | título 89% igual |
| Programa Energisa Cultural | `encontrar_cliente` | sem OSC | Energisa Cultural | `de9a0766` | sem prazo | título 79% igual |
| Edital de Chamamento Público SMSP nº 01/2026 - Juventude e | `selecionado` | SEMEAR | Edital de Chamamento Público nº 01/2026 - SECLIMAS J | `50c2c60b` | 2026-09-04 | o candidato é da **SECLIMAS**, órgão diferente |
| PNAB 2026 SECULT-MG SELEÇÃO DE PROJETOS PARA FIRMAR TERMO  | `aprovado` | sem OSC | EDITAL DE CHAMAMENTO PÚBLICO Nº 003/2026 SELEÇÃO DE  | `0ca6ed0c` | 2026-05-15 | título 79% igual |
| PNAB 2026 SECULT-MG SELEÇÃO DE PROJETOS PARA FIRMAR TERMO  | `reprovado` | sem OSC | EDITAL DE CHAMAMENTO PÚBLICO Nº 003/2026 SELEÇÃO DE  | `0ca6ed0c` | 2026-05-15 | título 79% igual |
| PNAB 2026 SECULT-MG EDITAL DE CHAMAMENTO PÚBLICO Nº 01/202 | `reprovado` | sem OSC | EDITAL DE CHAMAMENTO PÚBLICO Nº 003/2026 SELEÇÃO DE  | `0ca6ed0c` | 2026-05-15 | título 77% igual |
| EDITAL LEI MUNICIPAL DE INCENTIVO À CULTURA 2026 – FUNDO M | `submetido` | sem OSC | Edital da Lei Municipal de Incentivo à Cultura 2026 | `44444e81` | 2026-06-03 | título 76% igual |
| EDITAL LEI MUNICIPAL DE INCENTIVO À CULTURA 2026 – FUNDO M | `submetido` | sem OSC | Edital da Lei Municipal de Incentivo à Cultura 2026 | `44444e81` | 2026-06-03 | título 76% igual |
| Programa Energisa Cultural. Eles Sabem (Bandeja Films) | `checklist` | sem OSC | Energisa Cultural | `de9a0766` | sem prazo | achado pela busca, não pelo título |
| Usiminas - Patrocínios e Doações (Investimento Direto) | `encontrar_cliente` | sem OSC | DOAÇÕES USIMINAS | `1bd9ebc8` | 2025-10-09 | achado pela busca, não pelo título |
| Lojas Renner - Patrocínio Cultural Contínuo | `encontrar_cliente` | sem OSC | Edital Instituto Lojas Renner 2026 | `db9edc67` | sem prazo | achado pela busca, não pelo título |
| Edital Minasligas 2026-2027 - Projetos Sociais via Incenti | `selecionado` | Levanta e Brilha | Edital de Apresentação de Projetos Sociais através d | `d07ec882` | 2026-09-30 | achado pela busca, não pelo título |
| Impactarte - Instituto de Impacto Social | `encontrar_cliente` | sem OSC | Edital Contínuo de Apoio a Projetos Sociais – Ciclo  | `31f5c4ae` | sem prazo | achado pela busca, não pelo título |
| FUNDO OSC MROSC | `reprovado` | sem OSC | Plataforma MROSC lança edital que apoia projetos de  | `b25732ce` | 2026-05-31 | achado pela busca, não pelo título |

## Sem candidato na base de editais

Estas fichas não têm edital correspondente no CaptaHub. Na maioria são **financiador ou banco de
projetos**, não edital com prazo, e por isso talvez nunca devam ter edital ligado.

| Projeto | Estágio | OSC |
|---|---|---|
| CHAMAMENTO PÚBLICO Nº 04/2026 EDITAL BH FOMENTO A PROJETOS ANUAIS E AÇ | `submetido` | sem OSC |
| Wadhwani Charitable Foundation Grant Fund | `encontrar_cliente` | sem OSC |
| Diretrizes de Patrocínio Petrobras | `encontrar_cliente` | sem OSC |
| EMS Farmacêutica - Patrocínios e Doações | `encontrar_cliente` | sem OSC |
| Edital de Seleção Pública 001/2026 - Florestas Produtivas com Barragin | `encontrar_cliente` | sem OSC |
| STIHL - Solicitação de Patrocínio (Cultural, Ambiental e Esportivo) | `encontrar_cliente` | sem OSC |
| Santander - Projetos e Patrocínios (Educação, Esporte e Cultura) | `encontrar_cliente` | sem OSC |
| Rumo S.A. - Doações e Patrocínios | `encontrar_cliente` | sem OSC |
| Fazcultura - Programa Estadual de Incentivo ao Patrocínio Cultural (Ba | `encontrar_cliente` | sem OSC |
| Brasilprev - Doações a Projetos Incentivados de Impacto Social | `encontrar_cliente` | sem OSC |
| Bem Brasil - Projetos Sociais e Leis de Incentivo | `encontrar_cliente` | sem OSC |
| BB Seguros - Patrocínios Socioculturais (Leis de Incentivo) | `encontrar_cliente` | sem OSC |
| Patrocínio Ambipar Group - Projetos Socioambientais, Culturais e Espor | `encontrar_cliente` | sem OSC |
| Diretrizes para Investimento Social Privado do Grupo HDI: Foco em Patr | `encontrar_cliente` | sem OSC |
| Espaço Jovens Transformadores (PAPS 2027) | `reprovado` | Organização Multidisciplinar de voluntariado e-Missão |
| EDITAL Nº 01/2026 VARA DE EXECUÇÕES CRIMINAIS - VEC/BH | `reprovado` | sem OSC |
| Fundo Marielle Franco – Cultura nos Territórios | `reprovado` | sem OSC |
| BOLSA FUNARTE DE MOBILIDADE ARTÍSTICA INTERNACIONAL | `reprovado` | sem OSC |
