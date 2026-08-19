# Triagem de editais. Belo Horizonte, perfil ponto de cultura

> Recorte de 19/08/2026. **Origem dos dados: varredura web**, não o cache local nem o CaptaHub. O cache de `base-editais/` não tem nenhum edital de Cultura para Belo Horizonte, e o CaptaHub não está conectado neste ambiente.
>
> Limitação importante: a rede deste ambiente bloqueia o acesso direto aos sites da PBH e da imprensa mineira. As informações abaixo vieram de resultados de busca, não da leitura da página oficial. **Todo prazo, valor e requisito precisa ser conferido no Mapa Cultural BH e no Portal PBH antes de qualquer inscrição.**

---

## O achado principal. Um único edital aberto, e fecha em 12 dias

**Chamamento Público nº 04/2026. BH Fomento, PNAB Ciclo 2. Seleção de projetos culturais e ações continuadas.**

| Item | Informação |
|---|---|
| Valor total | R$ 6.300.000 |
| Projetos selecionados | 78 |
| Teto por projeto | R$ 100.000 |
| Inscrições | **14 a 31 de agosto de 2026** |
| Plataforma | Mapa Cultural BH |
| Modalidade A, projetos anuais | execução em até 12 meses, cerca de R$ 4,3 milhões |
| Modalidade B, ações continuadas | atividades em dois anos consecutivos, cerca de R$ 2 milhões |
| Categorias da modalidade anual | Circulação, Difusão, Criação e Produção, Formação, Memória e Preservação |

**Requisitos de entrada divulgados:** pessoa jurídica com ou sem fins lucrativos, **no mínimo 5 anos de existência**, trajetória comprovada e **sede em Belo Horizonte**.

Esses três requisitos são o filtro que decide tudo. Se a Associação Ponto Cultural tem CNPJ com 5 anos ou mais, sede em BH e portfólio documentado, ela está na disputa. Se tem menos de 5 anos, está fora deste edital e o esforço precisa ir para outro lugar.

## A regra que pode eliminar a OSC antes de começar

Segundo o material divulgado, **um mesmo agente cultural, individual ou coletivo, não pode ser aprovado em mais de um edital do Ciclo 2 da PNAB lançado em Belo Horizonte.**

Isso vira a primeira pergunta do parecer de elegibilidade: **a Ponto Cultural já foi aprovada em algum edital do Ciclo 2 da PNAB de BH em 2026?** Se sim, o Chamamento 04/2026 está bloqueado para ela e não vale gastar um dia de trabalho. Se não, o caminho está livre.

---

## O que já fechou em 2026 (para não perder tempo procurando)

Estes editais de BH já encerraram inscrições. Registro aqui porque são o calendário que se repete, e é por ele que se planeja 2027.

| Edital | Prazo encerrado | Valor |
|---|---|---|
| Chamamento nº 01/2026, Premiação Agentes Culturais, PNAB Ciclo 2 | 02/03/2026 | parte dos R$ 5 milhões de premiação |
| Chamamento nº 02/2026, Premiação Cultura Viva, Rede Municipal de Pontos e Pontões | 03/03/2026 | R$ 1.830.000, 124 pontos premiados, R$ 40.000 por entidade com CNPJ |
| Chamamento nº 03/2026, Fomento a Projetos Continuados de Pontos de Cultura | 19/06/2026 (prorrogado) | até R$ 90.000 por projeto |
| Multilinguagens 2026, Fundo Municipal de Cultura | 17/08/2026 | R$ 9.600.000 |
| BH nas Telas 2026, audiovisual | 10/08/2026 | R$ 2.000.000 |
| Chamamento FMC nº 001/2026, execução da Virada Cultural (termo de colaboração) | 25/02/2026 | R$ 5.216.900 |

Repare no padrão: **as duas premiações voltadas a Pontos de Cultura abriram em fevereiro e fecharam no começo de março.** É a janela mais importante do ano para um ponto de cultura em BH, e ela passou. Em 2027 essa data entra no calendário com dois meses de antecedência.

## O que ainda vai abrir

| Edital | Previsão | Observação |
|---|---|---|
| Descentra 2026 | agosto de 2026 | projetos em regiões descentralizadas da cidade, ligado à Lei Municipal de Incentivo à Cultura |
| Zona Cultural Praça da Estação 2026 | setembro de 2026 | projetos, eventos e ações naquele território específico |
| Lei Municipal de Incentivo à Cultura (LMIC) | ciclo próprio | mecanismo de renúncia fiscal do município, exige captação junto a patrocinador |

Vale monitorar a plataforma Mapa Cultural BH semanalmente até setembro.

---

## Recomendação

**Alvo único e imediato: Chamamento nº 04/2026, BH Fomento.** É o único edital aberto para a Ponto Cultural em BH, fecha em 31/08 e paga até R$ 100.000 por projeto.

Sequência sugerida, com o prazo que sobra:

1. **Hoje.** Confirmar no Mapa Cultural BH os três requisitos: 5 anos de CNPJ, sede em BH e a regra de não ter sido aprovada em outro edital do Ciclo 2. Baixar o edital completo e os anexos.
2. **Em seguida.** Rodar `/edital-analisar` com o PDF do edital, para extrair critérios de pontuação, documentos obrigatórios e o que derruba.
3. **Depois.** Rodar `/projeto-elegibilidade` (CaptaDoc) para o veredito formal antes de escrever qualquer linha.
4. **Só então.** `/projeto-escrever` e `/projeto-orcamento`, com `/projeto-avaliar` antes de submeter.

Doze dias é apertado, porém suficiente para um projeto de R$ 100.000 bem amarrado, desde que a elegibilidade seja confirmada nas próximas horas. O que não dá é escrever primeiro e conferir depois.

**Escolha de modalidade.** Se a OSC já mantém atividade regular na comunidade, a modalidade de ações continuadas (dois anos) costuma casar melhor com o DNA de ponto de cultura e traz previsibilidade de caixa. Se o que existe é um projeto novo e delimitado, a modalidade anual é mais defensável perante a banca.

## Fontes consultadas

- Prefeitura de Belo Horizonte, Licitações e Editais da FMC: https://prefeitura.pbh.gov.br/licitacoes/fmc
- Mapa Cultural BH, Chamamento nº 04/2026 BH Fomento: https://mapaculturalbh.pbh.gov.br/projeto/1995/
- Mapa Cultural BH, Chamamento nº 02/2026 Pontos e Pontões: https://mapaculturalbh-dsv.pbh.gov.br/projeto/1927/
- Mapa Cultural BH, Chamamento nº 01/2026 Premiação Agentes Culturais: https://mapaculturalbh.pbh.gov.br/projeto/1925/
- PBH, Fomento Cultura Viva: https://prefeitura.pbh.gov.br/cultura/fomentoculturaviva
- PBH, notícia do edital de R$ 6,3 milhões: https://prefeitura.pbh.gov.br/noticias/pbh-lanca-edital-de-r-63-milhoes-para-projetos-culturais-e-acoes-continuadas
