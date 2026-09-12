# Portal do Cliente. Especificação

> Documento da Fase 1 do planejamento de 11/09/2026. Descreve o portal que a Mobilizando vai construir no Lovable para acompanhar, junto com cada cliente, a elaboração de um projeto para edital.
>
> **Origem.** O conteúdo, os prazos e os textos vêm da página já aprovada pela captadora em `marketing/entregas/comercial/como-trabalhamos-juntos.html` e do documento impresso de mesmo nome. Nada aqui é invenção nova: o que muda é o lugar onde a página vive, para que a captadora e o cliente vejam sempre a mesma versão.
>
> **Estado:** aguardando aprovação da captadora. Nenhuma mensagem foi enviada ao Lovable.

---

## 1. Para que serve, e o que ele não é

O portal é o lugar onde a captadora e a organização cliente acompanham **um edital de cada vez, do dossiê à submissão**, com as datas calculadas e o registro do que cada lado entregou.

**Ele não é**, e isso é decisão de projeto:

1. Não tem funil, kanban, valores nem status de carteira. A gestão da carteira continua no CaptaHub.
2. Não dispara nada por conta própria, com uma única exceção, pedida pela captadora em 12/09/2026: os e-mails do item 5. Fora deles, tudo acontece porque alguém clicou.
3. Não recebe arquivos. Os documentos continuam no Drive do cliente. O portal guarda o nome de cada documento e se ele já foi enviado.
4. Não fala com o CaptaHub nem com a AMC IA. Nenhuma integração nesta primeira versão.

## 2. Quem usa

| Papel | Quem é | O que enxerga |
|---|---|---|
| Administradora | Rosepaula, e quem ela convidar para a equipe | Todas as organizações e todos os editais |
| Cliente | As pessoas da organização cliente | Apenas a própria organização |

A administradora cadastra a organização, convida a pessoa do cliente por e-mail e abre cada edital. O cliente entra com e-mail e senha, define a senha no primeiro acesso e recupera por e-mail quando esquecer.

**O que o cliente pode escrever:**

- o OK para seguir, com a observação;
- marcar cada documento como enviado, com a data;
- o roteiro do esboço inteiro;
- a aprovação do projeto, o que precisa mudar e o nome de quem aprovou;
- marcar como feitas as quatro entregas dele: OK, documentos, esboço e aprovação.

**O que só a administradora pode mudar:** o nome do edital, o órgão, o link, o dia D, a data do dossiê, o ritmo, a lista de documentos (nome e onde o edital pede), as entregas da Mobilizando (projeto enviado e submissão), o protocolo, a data da submissão e a finalização do edital.

## 3. As telas

### 3.1. Como trabalhamos juntos (aberta, sem login)

Endereço fixo, para a captadora mandar a qualquer OSC. Traz as sete etapas, os três ritmos, o roteiro do esboço e as três notas do fim (como contamos os dias, nunca no último dia, se uma entrega atrasar). É a versão em página do documento impresso. Sem nome de cliente e sem dado nenhum.

### 3.2. Entrar

E-mail e senha. Link para recuperar a senha. Nada mais.

### 3.3. Painel da administradora

Lista das organizações. Em cada linha: o nome, quantos editais em andamento, a próxima entrega com data e a situação em cor. As organizações com entrega atrasada aparecem primeiro. Botões: **Nova organização**, **Convidar pessoa**, **Novo edital**.

### 3.4. Painel do cliente

O nome da organização e duas seções:

- **Em andamento.** Um cartão por edital: nome, órgão, o contador grande (D-24), a próxima entrega com data e a situação em cor.
- **Finalizados.** Lista simples, com nome, data da submissão e um botão para abrir. Nada some daqui.

### 3.5. Página do edital

É o coração do portal, e repete a estrutura da página aprovada, nesta ordem:

1. **Cabeçalho:** nome do edital, órgão, link para o edital e o botão de baixar em PDF.
2. **Este edital:** organização, dia D, data do dossiê e ritmo. Para o cliente, esses campos aparecem preenchidos e travados.
3. **Contador:** "Hoje é D-24", com a frase "Hoje, sexta-feira, 11/09/2026. Faltam 24 dias para o fim das inscrições, em 05/10/2026".
4. **O que depende de você:** as quatro entregas do cliente, cada uma com data, rótulo D-n e situação. Clicar leva à etapa.
5. **A régua do prazo:** linha do tempo até o dia D. Acima da linha, as entregas do cliente; abaixo, as da Mobilizando. Marcas de D-7 em D-7 e uma linha tracejada no dia de hoje.
6. **As sete etapas**, que abrem e fecham com um clique, cada uma com o lado "Nós", o lado "Você", o prazo, a situação e os campos de resposta.
7. **Os três ritmos**, em tabela, com a coluna do ritmo escolhido em destaque e as datas já calculadas.
8. **As três notas** do fim.

### 3.6. Novo edital (só administradora)

Nome, órgão, link, dia D, data do dossiê e ritmo (ou deixar o ritmo sugerido). Ao salvar, o edital nasce com a lista de documentos vazia, pronta para a captadora preencher a partir do dossiê.

### 3.7. Finalizar edital (só administradora)

Botão na página do edital. Pede confirmação, grava a data e passa o edital para Finalizados. A partir daí ele fica **só para leitura, para os dois lados**.

### 3.8. Apagar e restaurar (só administradora)

Erro acontece: edital criado em duplicidade, dia D digitado errado, documento repetido. Por isso existe apagar, e ele é só da administradora.

- **Apagar um edital** pede confirmação e passa o edital para **Apagados**, onde ele continua inteiro, com tudo o que foi escrito. Ele some das listas do cliente na hora.
- **Restaurar** devolve o edital ao estado em que estava, em andamento ou finalizado.
- **Apagar de vez** existe, pede uma segunda confirmação e é definitivo. Só a administradora chega nele.
- **Nada sai de Apagados por tempo.** O que está lá fica lá até ela decidir. Não há limpeza automática.
- **Linha de documento:** a administradora remove a linha errada. O cliente não remove nenhuma.
- **O cliente nunca apaga nada**, nem edital, nem documento, nem resposta.
- O registro guarda quem apagou, o que apagou e quando. **O registro não se apaga.**

## 4. As regras de prazo

### 4.1. Os três ritmos

D é o último dia das inscrições.

| Entrega | Quem | Padrão (15 dias) | Folga maior (30 dias) | Apertado (10 dias) |
|---|---|---|---|---|
| Dossiê do Edital | Mobilizando | data informada | data informada | data informada |
| OK para seguir | Cliente | 2 dias úteis depois do dossiê | 3 dias úteis depois do dossiê | 1 dia útil depois do dossiê |
| Documentos extras | Cliente | D-15 | D-25 | D-10 |
| Esboço, objeto ou ideia | Cliente | D-12 | D-20 | D-8 |
| Projeto enviado para aprovação | Mobilizando | D-6 | D-10 | D-4 |
| Aprovação ou ajustes | Cliente | 2 dias úteis depois do projeto | D-7 | 1 dia útil depois do projeto |
| Submissão | Mobilizando | D-2 | D-3 | D-1 |

### 4.2. Dias úteis e feriados

Dia útil é de segunda a sexta, fora os feriados nacionais. Os feriados são calculados pelo ano, sem tabela fixa que precise ser atualizada à mão:

- 1 de janeiro, Confraternização Universal
- Sexta-feira da Paixão, dois dias antes da Páscoa (cálculo pelo algoritmo gregoriano)
- 21 de abril, Tiradentes
- 1 de maio, Dia do Trabalho
- 7 de setembro, Independência do Brasil
- 12 de outubro, Nossa Senhora Aparecida
- 2 de novembro, Finados
- 15 de novembro, Proclamação da República
- 20 de novembro, Dia Nacional de Zumbi e da Consciência Negra
- 25 de dezembro, Natal

Feriados estaduais e municipais não entram na conta, e a página diz isso ao usuário.

### 4.3. Antecipação

Toda data contada em D menos alguma coisa que caia em sábado, domingo ou feriado nacional **passa para o dia útil anterior**. A página mostra o motivo: "antecipado porque o D-15 caía em um domingo".

### 4.4. Ritmo sugerido

Ao abrir um edital sem ritmo escolhido, o portal sugere **o mais folgado que cabe no tempo que falta**, testando nesta ordem: folga maior, padrão, apertado. Um ritmo só cabe se o prazo do OK não passar do prazo dos documentos e se a aprovação não passar da submissão. Se nenhum couber, a página avisa: "Nem o ritmo apertado cabe nesse tempo. Converse com a Mobilizando antes de seguir". A administradora pode escolher outro ritmo a qualquer momento, e volta ao sugerido com um clique.

### 4.5. As situações

| Situação | Quando | Cor |
|---|---|---|
| Feito | a entrega foi marcada como feita | verde |
| Atrasado | a data já passou e ninguém marcou | vermelho |
| Vence hoje, vence amanhã, em 2 ou 3 dias | falta pouco | dourado |
| Em N dias | falta mais | neutra |
| A calcular | falta informar o dia D | neutra |

O rótulo D-n acompanha toda data: D-15, D, D+3 depois do encerramento.

### 4.6. O exemplo que serve de teste

Dia D em 05/10/2026, segunda. Dossiê enviado em 11/09/2026, sexta. Ritmo padrão. O portal tem que chegar exatamente a:

| Entrega | Data | Observação |
|---|---|---|
| OK para seguir | ter, 15/09 (D-20) | 2 dias úteis depois do dossiê |
| Documentos extras | sex, 18/09 (D-17) | o D-15 caía num domingo |
| Esboço, objeto ou ideia | qua, 23/09 (D-12) | |
| Projeto para aprovação | ter, 29/09 (D-6) | |
| Aprovação | qui, 01/10 (D-4) | 2 dias úteis depois do projeto |
| Submissão | sex, 02/10 (D-3) | o D-2 caía num sábado |

## 5. Os e-mails do portal

> Exceção autorizada pela captadora em 12/09/2026 à regra "nada roda sozinho" do `CLAUDE.md`. A rotina vive dentro do portal, não no ambiente da AMC IA. Quando o portal entrar no ar, a exceção é registrada no `CLAUDE.md` e em `docs/automacoes-desligadas.md`, com a data.

O portal manda **três tipos de e-mail, e nenhum além destes**: o lembrete de prazo, o aviso de atividade que exige ação do outro lado, e o resumo diário da captadora. Dentro do portal, os dois lados veem tudo pelo registro do edital, independentemente de e-mail.

### 5.1. Lembretes de prazo

**Quem recebe.** A pessoa da organização cliente, com cópia para a captadora em toda mensagem.

**Sobre o que.** Só as quatro entregas do cliente: OK para seguir, documentos extras, esboço e aprovação. As entregas da Mobilizando nunca geram e-mail ao cliente.

**Quando sai:**

- 3 dias corridos antes do prazo da entrega;
- no dia do prazo;
- depois do prazo, a cada 2 dias, enquanto a entrega não for marcada como feita.

**Os limites, que impedem o lembrete de virar spam:**

- No máximo **uma mensagem por dia por edital**. Se duas entregas vencem no mesmo dia, vão juntas, na mesma mensagem.
- No máximo **5 avisos de atraso** por entrega.
- Nada é enviado depois do dia D, nem em edital finalizado, apagado, ou com a entrega já marcada como feita.
- A rotina roda **uma vez por dia útil, às 8h de Brasília**. Em sábado, domingo e feriado nacional não sai nada.

**O texto da mensagem.** Assunto: "{Edital}: {entrega} vence em {data}". Corpo curto, em português: o que falta, a data com o dia da semana, o link para a página do edital e a frase "Se você já enviou, marque no portal para o lembrete parar".

### 5.2. Avisos de atividade, na hora

Só oito eventos geram e-mail na hora, porque só eles pedem uma ação do outro lado.

**Do cliente para a captadora:**

1. deu o OK para seguir, inclusive quando a resposta é "não vamos entrar" ou "tenho dúvidas";
2. marcou o esboço ou a ideia como enviado;
3. marcou os documentos extras como enviados;
4. respondeu a aprovação, aprovando ou pedindo ajustes.

**Da captadora para o cliente:**

5. um edital novo foi aberto para a organização dele;
6. documentos foram acrescentados à lista;
7. o projeto foi enviado para aprovação;
8. o projeto foi submetido, com o número do protocolo.

Cada aviso diz o que aconteceu, em qual edital, e traz o link da página. **Nenhum outro evento gera e-mail na hora:** um documento marcado no meio de vários, um campo do roteiro preenchido, uma observação escrita, uma troca de ritmo ou de data entram no resumo do dia.

### 5.3. O resumo diário da captadora

Um e-mail por dia útil, às 18h de Brasília, **só para a captadora**, com o que os clientes mexeram no dia, agrupado por organização e por edital. **Em dia sem atividade, o e-mail não sai.** O cliente nunca recebe este resumo.

### 5.4. Regras comuns aos três

**Nada se repete.** O que já foi contado por um aviso na hora não volta no resumo do dia.

**Como desligar:**

- A captadora desliga cada um dos três tipos separadamente, e desliga por edital, por organização ou tudo de uma vez, num interruptor no painel dela.
- O cliente pode parar de receber, por um link no rodapé do e-mail. Quando ele para, a captadora vê isso no portal.
- Enquanto o portal estiver em teste, nenhum lembrete é enviado a ninguém.

**Registro e falhas.** Todo e-mail enviado entra no registro do edital: para quem foi, quando saiu e o que dizia. Se o envio falhar, o portal mostra o erro para a captadora e não fica tentando para sempre.

**O que isso exige, e é tarefa da captadora.** O envio depende de um serviço de e-mail ligado ao portal e da verificação do domínio `mobilizando.org` no DNS da HostGator, para as mensagens saírem em nome da Mobilizando e não caírem na caixa de spam do cliente. Enquanto o domínio não estiver verificado, o remetente é um endereço do próprio serviço de envio.

## 6. Os dados

**organizacoes:** id, nome, criada_em.

**pessoas:** id (do login), nome, email, papel (administradora ou cliente), organizacao_id (vazio para administradora), criada_em.

**editais:** id, organizacao_id, nome, orgao, link, dia_d, data_dossie, ritmo (padrao, folga, apertado ou vazio para sugerido), situacao (andamento ou finalizado), finalizado_em, criado_em, atualizado_em. Guarda também as respostas: ok_resposta, ok_observacoes, esboco_tipo, esboco_oque, esboco_paraquem, esboco_onde, esboco_quando, esboco_como, esboco_comquem, esboco_quanto, esboco_jaexiste, duvidas, aprovacao_resposta, aprovacao_quem, aprovacao_ajustes, protocolo, submetido_em.

**entregas:** id, edital_id, chave (ok, docs, esboco, projeto, aprovacao, submissao), feito, feito_em.

**documentos:** id, edital_id, nome, onde_pede, enviado, enviado_em, ordem.

**registro:** id, edital_id, pessoa_id, o_que (texto curto, por exemplo "marcou os documentos como enviados"), quando. Serve para os dois lados saberem quem fez o quê, e nunca é apagado.

Nenhuma data é gravada calculada: o portal guarda o dia D, a data do dossiê e o ritmo, e calcula o resto na hora. Assim, mudar uma regra corrige todos os editais de uma vez.

## 7. Segurança e privacidade

1. **Isolamento por organização.** O cliente só lê e escreve linhas da organização dele. A regra vale no banco de dados, não só na tela.
2. **Campos travados.** O que é da administradora não muda pela conta do cliente, mesmo por caminho indireto.
3. **Dado mínimo.** Só nome e e-mail das pessoas. Nada de CPF, documento pessoal, senha de portal de edital ou chave de acesso.
4. **Nenhum segredo no código.** Toda chave fica na configuração do próprio Lovable, nunca escrita no projeto.
5. **Apagar é decisão da captadora, e só dela.** O cliente não apaga nada. Apagar manda para Apagados, de onde dá para restaurar; apagar de vez pede uma segunda confirmação. Nada é removido por tempo nem por rotina automática.
6. **Registro de quem fez.** Toda marcação guarda quem marcou e quando.

## 8. Aparência

A identidade já existe no site da Mobilizando e se repete aqui: verde #1d624d como cor principal, dourado #d1b484 para destaque, roxo #7f126f e azul-marinho #070552 como apoio, fontes Poppins nos títulos e Inter no texto. Feito em verde, atrasado em vermelho #B42318, próximo do prazo em dourado. Papel de cada lado com cor própria: Mobilizando em verde, cliente em roxo.

Pensado primeiro para o celular, porque é dali que o cliente responde. Texto em português do Brasil, com acentuação correta e sem travessão.

## 9. Critérios de aceite (a conferência da Fase 3)

1. Um cliente de teste não enxerga, de jeito nenhum, o edital de outra organização.
2. Sem login, nenhuma página mostra dado de cliente. Só a página "Como trabalhamos juntos" abre.
3. O cliente não consegue mudar dia D, ritmo, datas nem a lista de documentos.
4. O exemplo do item 4.6 confere, data por data, inclusive as duas antecipações.
5. Marcar uma entrega como feita muda a situação na hora para os dois lados.
6. O edital finalizado fica só para leitura e continua visível na lista.
7. O PDF do edital sai com tudo o que está na tela.
8. A página funciona no celular, com o polegar, sem zoom.
9. Nenhum e-mail sai fora das regras do item 5: em teste não sai nenhum, no mesmo dia nunca sai mais de uma mensagem por edital, e depois do dia D não sai nada.
10. O interruptor da captadora desliga os lembretes na hora, por edital e no geral, e o link do rodapé desliga os do cliente.
11. O edital apagado some das listas do cliente na hora, continua inteiro em Apagados, volta ao mesmo estado quando restaurado e não sai de lá por tempo.
12. O cliente não consegue apagar nada, por nenhum caminho.
13. O aviso na hora sai nos oito eventos do item 5.2, e em nenhum outro.
14. O resumo diário não sai em dia sem atividade e não repete o que já foi avisado na hora.

## 10. O que fica para depois

Lembrete por WhatsApp, envio de arquivo pelo portal, endereço próprio em mobilizando.org, relatório de desempenho por cliente e qualquer conversa com o CaptaHub. Cada um desses é uma decisão nova da captadora.
