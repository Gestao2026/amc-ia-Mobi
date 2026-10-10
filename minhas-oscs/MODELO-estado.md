# Estado da elaboração. Modelo

> Este é o modelo do `estado.md`, o arquivo que diz **em que ponto o projeto está**. Fica em `minhas-oscs/{slug}/projetos/{edital-slug}/estado.md`, ao lado dos entregáveis.
>
> **Para que serve.** É o que o orquestrador lê para dizer o próximo passo, e o que qualquer conversa nova lê para retomar o trabalho sem perguntar de novo. Todo agente da linha de montagem atualiza este arquivo ao terminar a sua estação.
>
> **Regra de preenchimento.** Marque `[x]` apenas o que existe como arquivo na pasta. Etapa sem arquivo é etapa não feita, mesmo que já se tenha conversado sobre ela. Campo sem resposta fica escrito **a confirmar**, nunca em branco e nunca deduzido.
>
> **Este modelo não migra o que já existe.** Os `estado.md` já gravados nas pastas de cliente continuam como estão. A captadora move cada um quando quiser, à mão. Nenhum comando reescreve `estado.md` antigo para encaixá-lo neste formato.

---

## Estado da elaboração. {nome do projeto ou do edital}

| Campo | Valor |
|---|---|
| OSC | |
| Edital | número, nome e órgão |
| Prazo de inscrição | data e hora, com o item do edital |
| Dias restantes | contados da última atualização, com a data dessa contagem |
| Etapa atual | uma das etapas da linha de montagem abaixo |
| Veredito de elegibilidade | APTO, APTO COM PENDÊNCIAS, INAPTO NO MOMENTO, ou ainda não verificado |
| Semáforo da estratégia | 🟢, 🟡, 🟠, 🔴, ou ainda não avaliado |
| Última atualização | data |

## Linha de montagem

- [ ] **Edital analisado.** Ver `edital.md` (11 blocos, modelo em `minhas-oscs/MODELO-edital.md`)
- [ ] **Elegibilidade (CaptaDoc).** Ver `elegibilidade.md`. Veredito: {veredito}
- [ ] **Estratégia de entrada (CaptaEstrategista).** Ver `estrategia.md` (modelo em `minhas-oscs/MODELO-estrategia.md`). Semáforo: {semáforo}
- [ ] **Proposta (CaptaBuilder).** Ver `proposta.md`
- [ ] **Orçamento (CaptaBudget).** Ver `orcamento.md`. Valor solicitado: {valor}
- [ ] **Avaliação (CaptaScore).** Ver `score.md`. Nota: {nota ou "o edital não tem escala"}
- [ ] **Revisão final.** `/projeto-revisar`
- [ ] **Exportação e submissão.** Pasta `entrega-final/`

> **A ordem tem duas travas de natureza diferente.** A elegibilidade é o único Gate duro: com INAPTO NO MOMENTO, a proposta não se escreve. A estratégia **não é Gate**: se ela faltar, ou se sair 🟠 ou 🔴, o trabalho segue com a confirmação da captadora, e essa confirmação fica registrada no `estrategia.md` com a data.

## Sincronização CaptaHub

- **ID CaptaHub projeto:** {id} ou "pendente"
- **O que já subiu:** liste o que foi gravado na carteira e quando
- **O que está só local:** liste o que ainda não subiu

> Toda gravação na carteira é oferecida e espera o OK da captadora, salvo quando subir é a finalidade do comando (ver a classificação de chamadas no `CLAUDE.md`).

## Onde estão as coisas

> Seção opcional, e útil quando o projeto tem material fora do padrão: anexos, documentos originais, publicação em diário oficial, comprovações que vivem no dossiê da OSC. Diga o caminho e por que o arquivo está ali.

## Próximos passos

1. {a próxima ação concreta, com o comando que a executa}
2. {o que depende de terceiro, com quem e desde quando}

## Observações

> Só o que muda a decisão ou a próxima ação. Prazo alterado, retificação publicada, certidão que vence antes do resultado, dependência que leva semanas. O que não muda nada fica fora.

---

## Variantes previstas

Nem todo projeto está em elaboração, e o modelo acima é para os que estão. Duas variantes legítimas convivem com ele e **não são erro**:

1. **Projeto já aprovado ou em execução.** Troque a linha de montagem por situação, valor aprovado, prazo de captação ou de execução, e o que falta prestar. O cabeçalho e as seções de sincronização, "onde estão as coisas" e próximos passos permanecem.
2. **Habilitação, que não é projeto.** Fica em `habilitacoes/{orgao}/estado.md`, com órgão no lugar de edital e sem linha de montagem, porque não passa pelos cinco agentes.
