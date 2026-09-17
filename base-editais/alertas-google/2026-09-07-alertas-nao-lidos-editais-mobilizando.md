# Alertas não lidos da editais.mobilizando (leitura de 07/09/2026)

Leitura feita pelo conector do Gmail, que aponta para `editais.mobilizando@gmail.com`. Foram lidos os 9 e-mails de Alerta do Google de 05 e 06/09/2026, todos da lista de editais públicos cadastrada nessa conta. Nenhum e-mail foi alterado, movido ou marcado como lido.

## O que os alertas trouxeram

Cinco editais de verdade e dois falsos positivos.

### Dentro do território dos clientes

| Edital | Onde | O que é | Prazo | Fonte |
|---|---|---|---|---|
| Festival Mosaico, Parada da Pessoa com Deficiência | Nova Lima, MG | Chamamento público para selecionar OSC que vai realizar o evento, voltado a inclusão, acessibilidade e cidadania | não informado na notícia | Jornal Panorama Minas |
| Programa para periferias do Amazonas | Manaus, AM | Apoio a projetos ambientais, sociais, culturais e tecnológicos, além de produção de conhecimento | inscrições prorrogadas até o dia 20 | D24AM |

### Fora do território dos clientes

| Edital | Onde | O que é | Prazo | Fonte |
|---|---|---|---|---|
| Lei Aldir Blanc, PNAB, R$ 129 mil para iniciativas culturais | Fernandópolis, SP | Pontos de Cultura, OSCs sem fins lucrativos e coletivos culturais informais | não informado na notícia | Jornal CidadãoNET e Região Noroeste |
| Gestão da UPA 24h e do PA da Cohab | Ourinhos, SP | Chamamento público para selecionar OSC gestora | edital a publicar no Diário Oficial do Município | Passando a Régua |
| ATER Bem Viver Pampa II | Rio Grande do Sul | Inclusão produtiva e geração de renda | oficina virtual em 22/09; propostas de 22/09 a 23/10, pelo SGA | Minuto MT |

### Falsos positivos

| Alerta | O que veio | Por que não serve |
|---|---|---|
| edital chamamento publico Minas Gerais assistencia social | Notícia sobre Unidade Móvel do Centro Estadual de Referência em Álcool e Drogas, em Divinópolis | Notícia institucional. O alerta disparou porque a página da prefeitura tem um menu "Editais de Chamamento Público" |
| edital Minas Gerais meio ambiente sociedade civil | Notícia sobre tentativa de homicídio durante fiscalização de mineração | Casou "sociedade civil" e "meio ambiente" em texto jornalístico, sem edital nenhum |

O alerta `edital chamamento publico estado do Para sociedade civil` trouxe três resultados, e nenhum deles é do Pará: vieram Fernandópolis, Ourinhos e Nova Lima. A palavra "Para" está pegando a preposição, apesar do "estado do" na frente. É candidato a ajuste ou exclusão na revisão de 30 dias.

## Por que ninguém leu

Levantamento da caixa em 07/09/2026:

| Pasta | Mensagens | Não lidas |
|---|---|---|
| Caixa de entrada | 0 | 0 |
| Lixeira | 26 | 26 |
| Enviados | 1 | 0 |
| Marcadores criados por ela | nenhum | |

**Nenhum e-mail chega à Caixa de entrada.** Todos os 26 alertas, inclusive os de 05 e 06/09, estão na Lixeira sem terem sido abertos. Fora eles, a conta tem apenas um e-mail enviado, de junho.

As 106 conversas que existiam nessa caixa em 30/08, registradas em `docs/estruturacoes/2026-08-30-24-desligamento-do-encaminhamento-editais-para-gestao.md`, não estão mais nem na Lixeira. Foram excluídas em definitivo.

**Causa confirmada pela captadora em 07/09/2026: a exclusão foi manual, feita por ela.** Não há filtro nem automação envolvida. A hipótese do filtro com ação Excluir, levantada antes de perguntar, fica descartada.

**Regra definida na mesma conversa:** e-mail de alerta só vai para a Lixeira **depois de lido e triado**. Enquanto não passou pela triagem, fica na Caixa de entrada.

## O que está em risco

A Lixeira do Gmail apaga sozinha o que tem mais de 30 dias. Cada alerta não lido tem esse prazo, contado da chegada. Os de 05/09 somem por volta de 05/10.

## Restauração dos 26

**Feita em 07/09/2026.** Os 26 alertas saíram da Lixeira e voltaram para a Caixa de entrada, ainda não lidos. Confirmado das duas formas: a Lixeira mostra "Não há conversas na lixeira", e o conector do Gmail passou a ler Caixa de entrada com 26 e Lixeira com 0.

Como foi feito, para repetir quando precisar:

1. A conta editais.mobilizando é a **`u/1`** no Chrome chamado "Trabalho" (a `u/0` desse mesmo Chrome é a gestao.mobilizando). Endereço direto da Lixeira dela: `https://mail.google.com/mail/u/1/#trash`.
2. Marcar a caixa de seleção do topo, que pega as 26 de uma vez.
3. Botão **Mover para**, na barra de ferramentas, e escolher **Caixa de entrada**.

Duas armadilhas encontradas no caminho:

- O conector do Gmail desta sessão **só lê, não escreve**. `untrash_message`, `untrash_thread` e `update_message_labels` respondem "The caller does not have permission", e `get_thread` também falha. Por isso a restauração teve de ser feita pelo navegador.
- A leitura do navegador **mentiu uma vez**: logo depois da primeira tentativa, a busca `in:inbox` devolveu 26 linhas que eram tela velha, e a movimentação não tinha acontecido. Quem apontou o erro foi o conector, que continuava vendo 26 na Lixeira. Ao conferir uma ação no Gmail, confirmar pelas duas fontes antes de dar por feita.

## Sobre a tarefa agendada

Não existe tarefa agendada neste ambiente. Verificado em 07/09/2026, nas duas formas possíveis, e as duas voltaram vazias. Isso está de acordo com a regra NADA RODA SOZINHO do `CLAUDE.md`, que proíbe agendamento por horário. Criar uma é decisão da captadora, e exige abrir exceção à regra.
