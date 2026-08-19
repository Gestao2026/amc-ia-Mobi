# Triagem de editais. Minas Gerais, perfil ponto de cultura

> Recorte de 19/08/2026, feito a partir do cache local `base-editais/editais-abertos.json` (publicação mais recente do cache: 29/06/2026). Base: 46 editais de MG, sendo 27 de Cultura e 15 com prazo vigente.
>
> Este é um recorte por território e área, não é parecer de elegibilidade. O veredito APTO, APTO COM PENDÊNCIAS ou INAPTO só sai do CaptaDoc (`/projeto-elegibilidade`), com o perfil da OSC em mãos.

## Aviso sobre os prazos

A data 31/12/2026 aparece 54 vezes na base inteira, o que indica preenchimento genérico de fim de ano, não prazo real. **Todo edital marcado com 31/12 abaixo precisa ter o prazo confirmado na fonte oficial antes de qualquer decisão.** Os prazos com data específica (08/09, 30/09, 12/11, 15/11) são confiáveis.

---

## Onde estão os editais municipais de MG

Os 15 editais vigentes de Cultura em MG se concentram em pouquíssimas cidades:

| Município | Editais vigentes |
|---|---|
| Uberlândia | 9 |
| Contagem | 3 |
| Muriaé | 1 |
| Uberaba | 1 |
| Estadual (vale para MG inteiro) | 1 |

Ou seja, **o município da Associação Ponto Cultural decide quase tudo**. Se ela estiver em Uberlândia ou Contagem, há caminho farto e imediato. Se estiver em Belo Horizonte, Juiz de Fora, Montes Claros ou qualquer outra cidade, o cache não traz edital municipal e a jogada muda de figura (ver "Se a OSC não for de Uberlândia nem Contagem").

---

## Cenário 1. Se a OSC for de Uberlândia

Este é o cenário mais forte da base inteira para um ponto de cultura. A Secretaria Municipal de Cultura e Turismo abriu o Ciclo 2 da PNAB com uma trilha inteira dedicada a Pontos de Cultura.

| Prioridade | Edital | Prazo | Valor |
|---|---|---|---|
| 1 | SMCT nº 04/2026, Fomento a Projetos Continuados de Pontos de Cultura (Cultura Viva) | 31/12, confirmar | R$ 630.000 |
| 2 | SMCT nº 08/2026, Premiação de Pontos e Pontões de Cultura (PNCV, recursos PNAB) | 31/12, confirmar | R$ 451.840 |
| 3 | SMCT nº 03/2026, Territorialidades, produção cultural em áreas vulneráveis e rurais | **30/09** | R$ 645.000 |
| 4 | SMCT nº 10/2026, Subsídio para Espaços Culturais, PNAB Ciclo 2 | **12/11** | R$ 288.000 |
| 5 | SMCT nº 06/2026, Fomento a Manifestações Culturais Tradicionais e Populares | 31/12, confirmar | R$ 200.000 |
| 6 | SMCT nº 11/2026, Espaços e Iniciativas Culturais Emergentes, PNAB Ciclo 2 | **12/11** | R$ 60.000 |

Complementares, de menor porte ou natureza diferente: Feira da Cultura (SMCT nº 01/2026, prazo 15/11), uso do Teatro Municipal (SMCT nº 16/2026) e exposições nas Galerias de Arte (SMCT nº 02/2026, para artistas de artes visuais).

**Leitura estratégica.** Os itens 1 e 2 são a mesma política (Cultura Viva) em dois formatos: fomento a projeto continuado e premiação por trajetória. A premiação costuma exigir menos elaboração e comprovar histórico, enquanto o fomento exige projeto completo. Se a OSC tem trajetória documentada como ponto de cultura, dá para ir aos dois. O item 4 (subsídio a espaço cultural) é o que sustenta custo de manutenção da sede, que é justamente o que ponto de cultura mais sofre para financiar.

## Cenário 2. Se a OSC for de Contagem

| Prioridade | Edital | Prazo | Valor |
|---|---|---|---|
| 1 | Chamamento PNAB nº 06/2026, Premiação a Pontos de Cultura (15 agentes culturais) | **12/11** | R$ 340.000 |
| 2 | Premiação Cultural Contagem PNAB nº 02/2026 (100 agentes culturais) | 31/12, confirmar | R$ 450.000 |
| 3 | Chamamento PNAB nº 03/2026, bolsas de promoção, difusão, circulação e residência (18 projetos) | 31/12, confirmar | R$ 360.000 |

**Leitura estratégica.** Os dois primeiros são premiação com natureza jurídica de doação sem encargo, ou seja, pagamento direto ao contemplado sem prestação de contas de execução. Para a OSC isso significa recurso livre e risco baixíssimo de glosa. É o tipo de edital com melhor relação entre esforço de elaboração e retorno, e o que se apresenta é trajetória, não projeto futuro.

## Cenário 3. Se a OSC não for de Uberlândia nem de Contagem

O cache não traz edital municipal para o resto de MG, mas isso **não** significa que não exista. O Ciclo 2 da PNAB está correndo em praticamente todo município mineiro nesta janela, e o cache está sete semanas atrasado. O caminho é:

1. Checar o site da secretaria de cultura ou da fundação cultural do município e o Diário Oficial municipal, procurando "PNAB Ciclo 2" e "Cultura Viva".
2. Rodar `/captahub-conectar` e `/edital-minerar` na sua máquina, para trazer o que entrou no CaptaHub depois de 29/06.

Enquanto isso, valem os de alcance estadual e nacional abaixo.

---

## Estadual. Vale para MG inteiro

**Chamamento Público nº 003/2025, Restauro do Patrimônio Mineiro Cemig 2026.** Prazo **08/09/2026**, ou seja, 20 dias. R$ 15.000.000. Foco em preservação e restauração do patrimônio material mineiro.

Atenção à condição de entrada: o edital seleciona **projetos já aprovados pela Lei Estadual de Incentivo à Cultura**. Se a Ponto Cultural ainda não tem projeto aprovado na LEIC, ela não entra neste ciclo, e o movimento correto é preparar a inscrição na LEIC para disputar o próximo. Se já tem, e o objeto for patrimônio material, este é o edital de maior valor disponível para MG.

## Nacionais. Independem do município

Do bloco nacional já levantado, os que conversam com perfil de ponto de cultura:

| Edital | Prazo | Valor |
|---|---|---|
| Ambev Brasilidades 2026, cultura e esporte | 30/09 | R$ 67.000.000 no total |
| II Edital Escolas Livres de Formação em Arte e Cultura (MinC) | 30/09 | não informado |
| Edital MAPFRE 2026, projetos incentivados | 30/09 | não informado |
| Cadastro de Projetos da Lei Federal de Incentivo à Cultura (Rouanet) | 30/10 | não informado |
| Patrocínio Shell Cultural 2026 | 31/10 | não informado |
| Programa Funarte Aberta 2026, Complexo Funarte MG | 30/04/2027 | não informado |

O **II Edital Escolas Livres de Formação em Arte e Cultura** é o mais aderente ao DNA de ponto de cultura, porque trabalha formação artística comunitária, que é exatamente o que a maioria dos pontos já faz. O **Funarte Aberta Complexo MG** é ocupação de espaço, não repasse de recurso, mas gera contrapartida de visibilidade e circulação dentro do estado.

---

## Fora do escopo da OSC, mas de interesse do captador

Dois editais de MG são credenciamento de pareceristas, ou seja, remuneram profissionais para avaliar projetos, não financiam a OSC:

- Credenciamento de Pareceristas, 2º Ciclo PNAB, Muriaé.
- Edital de Credenciamento de Pareceristas nº 001/2026, Uberaba (exige MEI).

Não servem para a Associação Ponto Cultural captar, mas servem como fonte de receita e de repertório de banca para você, captador. Quem senta na cadeira de parecerista aprende exatamente o que derruba projeto.

---

## Próximo passo recomendado

1. Me diga o município da Associação Ponto Cultural, para eu fechar em 3 ou 4 candidatos.
2. Cole o `perfil-osc.md` (CNPJ, natureza jurídica, tempo de existência, certidões, se é reconhecida como Ponto de Cultura pela Cultura Viva, histórico de projetos).
3. Com isso rodamos `/projeto-elegibilidade` no edital escolhido. Nenhuma linha de proposta antes do parecer do CaptaDoc.
