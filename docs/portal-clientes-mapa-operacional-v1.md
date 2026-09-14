# Portal do Cliente Mobilizando. Mapa Operacional v1.0

> **Fonte da verdade da operação do portal.** Proposto pela captadora em 14/09/2026, conferido contra o documento-base e contra a arquitetura de 13/09, e corrigido com as quatro decisões dela no mesmo dia.
>
> **Hierarquia das fontes**
> 1. `marketing/entregas/comercial/como-trabalhamos-juntos.md`: jornada, responsabilidades e prazos. Manda sobre tudo.
> 2. **Este mapa:** a lógica operacional do portal sobre essa jornada, incluindo o Farol.
> 3. `docs/portal-clientes-arquitetura.md`: como o mapa vira telas, dados, segurança e pacotes.
> 4. `docs/portal-clientes-pacote-*.md` e afins: a instrução de cada pacote enviado ao Lovable.
>
> **Este mapa não é prompt de implementação.** Ele não vai inteiro ao Lovable. Cada pacote leva só a parte necessária.
>
> **Decisões da captadora em 14/09/2026**
> 1. O portal e o documento mantêm **7 etapas**. OK e documentos seguem juntos na etapa 3.
> 2. **Ideia do Projeto:** a opção A tem 5 perguntas curtas; a opção B, "já tenho um esboço", tem os 8 itens do roteiro.
> 3. **Andamento:** etapa principal mais entregas paralelas, cada uma com prazo e situação próprios. Não é fila única.
> 4. **Os e-mails automáticos ficam na v1.0**, no fim (pacotes 12 e 13).

---

## 1. Propósito

O portal organiza a relação **Mobilizando, organização cliente e edital**.

> Um projeto aprovado depende do trabalho técnico da Mobilizando e das informações, documentos, decisões e aprovações que só a organização tem. (documento-base, "Para que serve este documento")

A finalidade, também do documento-base, é que nenhum edital se perca por falta de tempo. O portal não é só painel de acompanhamento: é o sistema operacional dessa jornada.

## 2. As cinco perguntas

A qualquer momento, para qualquer edital, o portal responde:

1. Em que etapa estamos?
2. De quem é a vez?
3. O que precisa ser feito?
4. Qual é o prazo?
5. Existe risco ou impedimento?

Quem responde é o **Farol** (seção 4).

## 3. Os três atores

**Mobilizando.** Encontra o edital, lê e analisa, produz o Dossiê do Edital, confere a documentação, elabora proposta e orçamento, faz a revisão final, submete, envia o comprovante e registra o resultado.

**Organização cliente.** Tem quatro momentos, e só quatro, segundo o documento-base:
1. OK para seguir.
2. Documentos extras.
3. Esboço, objeto ou ideia.
4. Aprovação ou ajustes.

"Nos outros momentos, o trabalho é nosso."

**Portal.** Calcula os prazos, mostra de quem é a vez, controla as entregas, registra as ações, sinaliza atraso e risco, guarda o histórico, organiza os documentos, avisa os dois lados e impede o que cada papel não pode fazer.

---

## 4. O Farol

### 4.1 O que é

O Farol é a **camada de leitura operacional** do portal. Não é etapa e não aparece no documento-base: ele materializa a jornada do documento. Acompanha todas as etapas e responde, em linguagem simples:

> **Quem precisa fazer alguma coisa agora, o quê, e até quando?**

### 4.2 O que o Farol não é

- **Não cria estado paralelo.** Ele interpreta a etapa, as entregas e a situação do edital (seção 5).
- **Não é um segundo motor de prazos.** Ele usa o motor único previsto na arquitetura (`src/lib/alertas.ts`, sobre `prazos.ts` e `agenda.ts`). Nenhuma data gravada, nenhuma lista nova de feriados.
- **Não inventa níveis de prazo.** Usa os já decididos em 13/09: a calcular; em N dias; em 3 dias; em 2 dias; vence amanhã; vence hoje; atrasado há N dias; prazo perdido. Cores: verde para feito, dourado para perto do prazo, vermelho para atrasado e prazo perdido.

### 4.3 O que o Farol lê

Etapa principal, entregas com prazo e situação, de quem é cada entrega, documentos pendentes ou recusados, pedido de complemento aberto, situação do edital (em andamento ou encerrado) e o nível de prazo de cada item.

### 4.4 Regra central

O Farol mostra primeiro **de quem é a vez**, e não "projeto em andamento".

Para o cliente, isso vira uma de três leituras:
- **Sua vez:** há entrega do cliente aberta.
- **Precisamos de você:** a Mobilizando pediu um complemento ou recusou um documento.
- **Agora é com a Mobilizando:** nenhuma entrega do cliente aberta.

### 4.5 Nenhum prazo mascarado (regra de 13/09, vale para o Farol)

"Agora é com a Mobilizando" **sempre vem com o prazo e a situação reais da Mobilizando.** Exemplo: "Agora é com a Mobilizando. Projeto previsto para ter, 29/09, atrasado há 2 dias", na mesma cor dos atrasos do cliente. Nenhum filtro, texto ou estado esconde atraso ou prazo perdido de nenhum lado. Prazo recalculado mostra as duas datas e o motivo.

### 4.6 Os sinais do Farol

| Situação lida | Cliente vê | Administradora vê |
|---|---|---|
| Entrega do cliente aberta, dentro do prazo | Sua vez, com o nível do prazo | De quem: cliente, com o nível |
| Complemento pedido ou documento recusado | Precisamos de você, com o que falta | Aguardando cliente: complemento |
| Nenhuma entrega do cliente aberta | Agora é com a Mobilizando, com o prazo e a situação dela | De quem: Mobilizando, com o nível |
| Prazo em 3 dias, 2 dias, amanhã ou hoje | O nível, em dourado | O nível, em dourado |
| Atrasado, de qualquer lado | Atrasado há N dias, em vermelho, dizendo de quem | Idem, e entra em "Atrasados" |
| Atraso que ameaça a submissão | Vamos decidir juntos (seção 11.3) | Decidir: seguir ou encerrar |
| Dia D passou sem submissão | Prazo perdido | Prazo perdido, com de quem eram as pendências |
| Encerrado | Resultado ou motivo do encerramento | Idem, e sai da carteira ativa |

**Pendente de OK da captadora:** as frases exatas de cada sinal. Os níveis e as cores já estão decididos.

---

## 5. O modelo de andamento (decisão 3)

O portal não usa fila única. Três camadas, lidas juntas pelo Farol.

### 5.1 Situação do edital

Da arquitetura (2.6): em andamento; submetido, aguardando resultado; aprovado, com data; reprovado, com data; não submetido, com motivo obrigatório; apagado (só erro de cadastro).

### 5.2 Etapa principal

Uma das 7 etapas do documento-base. **Proposta:** calculada na leitura, pela entrega mais avançada já feita, e não digitada:

| Etapa principal | Quando |
|---|---|
| 1. Encontramos o edital | edital aberto, sem dossiê informado |
| 2. Dossiê do Edital | dossiê informado, OK ainda não dado |
| 3. OK e documentos extras | OK dado, esboço ainda não enviado |
| 4. Esboço, objeto ou ideia | esboço enviado, projeto ainda não enviado |
| 5. Elaboramos o projeto | a partir do esboço enviado, até o projeto sair |
| 6. Aprovação ou ajustes | projeto enviado, aprovação ainda não dada |
| 7. Submissão | aprovado, até a submissão marcada |

A etapa diz **onde a jornada está**. Ela não bloqueia nenhuma entrega.

### 5.3 Entregas paralelas

As seis entregas do documento-base correm ao mesmo tempo, cada uma com prazo, situação e dono:

| Entrega | Dono | Pode ser feita quando |
|---|---|---|
| OK para seguir | cliente | dossiê informado |
| Documentos extras | cliente | a qualquer momento depois do OK; linha a linha |
| Esboço, objeto ou ideia | cliente | a qualquer momento, **mesmo com documento pendente** |
| Projeto enviado para aprovação | Mobilizando | a elaboração corre mesmo com documento pendente; mostra "com pendência do cliente" sem tirar o atraso da Mobilizando da tela |
| Aprovação ou ajustes | cliente | projeto enviado |
| Submissão | Mobilizando | aprovação dada; **sem documentação completa, a submissão fica impedida** e o Farol mostra por quê |

---

## 6. A jornada, etapa por etapa

Para cada etapa: o que diz o documento-base, o que o portal faz, o que o Farol mostra e o que já existe.

### Etapa 1. Encontramos o edital

- **Nós:** buscamos editais que combinam com a área de atuação, o território, o valor e o tipo de proponente aceito.
- **Você:** nada ainda.
- **Portal:** a administradora abre o edital (nome, órgão, link, dia D, data do dossiê, ritmo). Registro: "Abriu o edital".
- **Farol:** cliente, "Agora é com a Mobilizando"; administradora, dossiê a enviar.
- **Hoje:** existe.

### Etapa 2. Você recebe o Dossiê do Edital

- **Nós:** lemos o edital e os anexos e enviamos o dossiê: o que financia, quem pode participar, prazos, critérios, riscos e documentos exigidos.
- **Você:** lê o dossiê e decide se quer entrar.
- **Portal:** a data do dossiê dispara o prazo do OK. **Escopo novo, pendente de decisão:** o dossiê dentro do portal, como arquivo anexado ou como link.
- **Farol:** cliente, "Sua vez: leia o Dossiê do Edital e diga se quer seguir", com o prazo do OK.
- **Hoje:** existe a data; o dossiê sai fora do portal.

### Etapa 3. Você dá o OK e providencia os documentos extras

**OK para seguir.** Três respostas, como já existe no portal:
1. "Quero seguir com este edital."
2. "Não vamos entrar neste edital."
3. "Tenho dúvidas antes de decidir."

Com observações. O banco registra quem respondeu e quando.

- **Se "não vamos entrar":** os lembretes do cliente param; a administradora recebe "Decidir: encerrar edital"; ela encerra como "Não submetido: desistência do cliente". **O portal não encerra sozinho.**
- **Se "tenho dúvidas":** a vez passa para a Mobilizando responder, e o prazo do OK continua visível.

**Documentos extras.**
- **Nós:** conferimos a lista do edital com a documentação base da pasta do cliente (estatuto, ata, cartão CNPJ, certidões) e apontamos só o que falta. A leitura é feita pela AMC IA, fora do portal, só lendo (arquitetura 2.9).
- **Você:** providencia o que falta: documentos específicos, declarações para assinar, certidões vencidas.
- **Portal:** lista por linha (documento e onde o edital pede), cada linha com pendente, enviado, conferido ou recusado com motivo. Dois caminhos de envio: anexar no portal ou pela pasta do Drive (link manual). Recusado volta a pendente e avisa o cliente.
- **Farol:** cliente, "Sua vez: N documentos pendentes" ou "Precisamos de você: documento recusado, motivo". A entrega só fica em dia com todas as linhas conferidas.
- **Hoje:** a lista e a marcação de enviado existem. Conferência, recusa, anexo e Drive entram no pacote 7.

### Etapa 4. Você envia o esboço, o objeto ou a ideia

Ver seção 7, Ideia do Projeto.

### Etapa 5. Elaboramos o projeto

- **Nós:** escrevemos a proposta e montamos o orçamento, ancorados nos critérios do edital, conferimos tudo e enviamos para aprovação até D-6 no padrão (D-10 na folga maior, D-4 no apertado).
- **Você:** fica disponível para alguma dúvida pontual.
- **Portal:** perguntas e respostas no edital; a administradora marca "projeto enviado".
- **Farol:** cliente, "Agora é com a Mobilizando. Projeto previsto para {data}", com a situação real.
- **Hoje:** existe.

### Etapa 6. Você aprova ou pede ajustes

Ver seção 8.

### Etapa 7. Submetemos o projeto

Ver seção 9.

---

## 7. Ideia do Projeto (decisão 2)

Nome no portal: **Ideia do Projeto**. Nome no documento-base: "esboço, objeto ou ideia". Prazo: D-12 no padrão, D-20 na folga maior, D-8 no apertado.

### 7.1 Mensagem fixa

> **Sua ideia é o ponto de partida, não o projeto final.** A Mobilizando desenvolve e adapta às regras e aos critérios do edital. O projeto pode mudar de formato, público ou valor para caber nas regras e pontuar melhor.

(Adaptado do destaque da etapa 4 do documento-base.)

### 7.2 As três formas de enviar

**A. Ainda estou começando: 5 perguntas curtas**
1. O que você quer fazer?
2. Para quem?
3. Onde?
4. Por que isso é importante?
5. O que você espera alcançar?

**B. Já tenho um esboço: os 8 itens do roteiro**
1. **O quê:** em uma ou duas frases, o que o projeto vai fazer.
2. **Para quem:** o público, a faixa etária e quantas pessoas, mais ou menos.
3. **Onde:** bairro, cidade e o espaço das atividades.
4. **Quando:** o período e a duração.
5. **Como:** as principais atividades e a frequência.
6. **Com quem:** a equipe e os parceiros.
7. **Quanto:** o valor aproximado, se já tiver.
8. **O que já existe:** fotos, vídeos, relatórios, matérias e projetos anteriores parecidos.

**C. Já tenho um documento**
Anexar o material existente. **Depende do armazenamento de arquivos do pacote 7.** Até lá, a opção C não aparece.

Nenhum campo é obrigatório além de a pessoa escolher A, B ou C e escrever ao menos uma resposta. "Responda o que souber; o que faltar, construímos juntos." (documento-base)

**Pendência de consistência:** o documento "Como trabalhamos juntos" hoje só traz o roteiro de 8 itens. Com a decisão 2, ele ganha as 5 perguntas curtas na próxima versão.

### 7.3 Ao clicar em "Enviar minha ideia"

1. Grava as respostas.
2. O banco registra quem enviou e quando (autor e hora não vêm da tela).
3. Marca a entrega "Esboço, objeto ou ideia" como feita.
4. A etapa principal passa para 4 ou 5, pela regra da seção 5.2.
5. Entra no histórico.
6. Aparece para a administradora como novidade ("Nova ideia recebida").
7. O Farol do cliente passa a "Agora é com a Mobilizando", com o prazo do projeto.
8. Aviso na hora para a administradora (evento 2 da arquitetura), quando os e-mails estiverem ligados.

### 7.4 Análise da ideia e pedido de complemento (escopo novo)

Operação da Mobilizando, sem prazo próprio no documento-base.

- **Informação suficiente:** a elaboração segue; nada muda para o cliente.
- **Informação insuficiente:** a administradora abre um **pedido de complemento**, escrito como pergunta específica ("Qual será a duração aproximada das atividades?"), nunca "favor complementar".

Com pedido aberto:
- O Farol do cliente mostra "Precisamos de você", com a pergunta.
- **O prazo do projeto da Mobilizando não para nem é recalculado em silêncio.** Se a resposta atrasar e isso afetar o D-6, o recálculo mostra as duas datas e o motivo (regra 2.5).
- A resposta do cliente fecha o pedido, entra no histórico e avisa a administradora.

**Pendente de decisão:** se o pedido de complemento entra na v1.0.

---

## 8. Aprovação e ajustes

- **Prazo:** até 2 dias úteis depois de receber o projeto no padrão; D-7 na folga maior; 1 dia útil no apertado. Com o projeto atrasado, o prazo de aprovação é recalculado com as duas datas visíveis e nunca passa da véspera da submissão.
- **Respostas:** "Aprovado, pode submeter" ou "Precisa de ajustes antes de submeter", com "O que precisa mudar" e "Nome e cargo de quem aprovou". Já existem.
- **Ajustes pedidos:** a vez volta para a Mobilizando, que faz a revisão final, como diz o documento-base. Se a revisão pedir nova aprovação, a entrega de aprovação reabre com registro.
- **Registro:** quem respondeu, quando, a escolha, o texto dos ajustes e o nome e cargo informados.
- **Escopo novo, pendente de decisão:** versões do projeto dentro do portal e a "versão aprovada". Hoje o projeto circula fora do portal; o registro guarda a aprovação, não o arquivo.

## 9. Submissão e comprovante

- **Nós:** submetemos no portal do edital, antes do último dia, e enviamos o comprovante.
- **Você:** recebe o comprovante, "a prova de que o projeto foi entregue no prazo".
- **Portal:** a administradora informa protocolo e data e hora da submissão, com a hora certa (defeito 9, pacote 4). Data informada e data da marcação ficam separadas.
- **Escopo novo, pendente de decisão:** o comprovante anexado, depois do pacote 7, ou por link.
- **Farol:** cliente, "Projeto submetido em {data}, protocolo {número}".

## 10. Depois da submissão

Já detalhado na arquitetura (2.6 e 2.8), e vale como está:
- **Situações:** aguardando resultado; aprovado com data; reprovado com data; não submetido com motivo.
- **Motivos de não submissão:** desistência do cliente; não recomendado pela Mobilizando; inelegível; prazo perdido, com de quem eram as pendências.
- **Datas informadas pela administradora:** data prevista do resultado, prazo de recurso (se reprovado), prazo e descrição da pós-aprovação (se aprovado).
- **Resultado registrado** avisa o cliente na hora (evento 9).
- **Painel de resultados** para a organização e para a carteira, sem valores em reais (valores ficam no CaptaHub).

---

## 11. Prazos

### 11.1 Calendário (documento-base)

D é o último dia das inscrições. D-15 são 15 dias corridos antes. Se cair em sábado, domingo ou feriado nacional, vale o dia útil anterior, e a tela diz o motivo.

| Entrega | Quem | Padrão (15 dias) | Folga maior (30 dias) | Apertado (10 dias) |
|---|---|---|---|---|
| Dossiê do Edital | Mobilizando | assim que o edital é encontrado | idem | idem |
| OK para seguir | cliente | 2 dias úteis após o dossiê | 3 dias úteis | 1 dia útil |
| Documentos extras | cliente | D-15 | D-25 | D-10 |
| Esboço, objeto ou ideia | cliente | D-12 | D-20 | D-8 |
| **Projeto enviado para aprovação** | **Mobilizando** | **D-6** | **D-10** | **D-4** |
| Aprovação ou ajustes | cliente | 2 dias úteis após o projeto | D-7 | 1 dia útil após o projeto |
| Submissão | Mobilizando | D-2 | D-3 | D-1 |

O ritmo sugerido é o mais folgado que cabe no tempo que falta, testando folga maior, padrão e apertado, nessa ordem. Teste obrigatório do motor: D em 05/10/2026, dossiê em 11/09/2026, ritmo padrão.

### 11.2 Regra de ouro

> A submissão nunca fica para o último dia. Os portais costumam ficar lentos ou sair do ar perto do encerramento. (documento-base)

### 11.3 Atraso gera decisão, não só cor

Documento-base: "Avisamos na hora o que o atraso muda. Às vezes dá para compensar reorganizando o calendário. Às vezes não sobra tempo para fazer um projeto com a qualidade que a banca exige, e então decidimos com você se seguimos ou se deixamos para o próximo edital."

No portal:
1. O atraso aparece real para os dois lados, dizendo de quem é.
2. Quando o atraso compromete a submissão, o Farol da administradora abre "Decidir: seguir ou encerrar", e o do cliente mostra "Vamos decidir juntos".
3. **Seguir:** o recálculo mostra as duas datas e o motivo.
4. **Deixar para o próximo:** a administradora encerra como "Não submetido", com o motivo.
5. **Dia D sem submissão:** "Prazo perdido" para os dois, até o encerramento.

**Pendente de OK:** o critério exato de "compromete a submissão". Proposta: prazo do projeto da Mobilizando recalculado para depois da véspera da submissão, ou qualquer entrega do cliente atrasada a 3 dias ou menos da submissão.

---

## 12. O que cada lado vê

### 12.1 Cliente (celular primeiro)

Início "O que é seu agora", uma leitura por edital:

| Pergunta | Exemplo |
|---|---|
| Onde estamos? | Etapa 5. Elaboramos o projeto |
| De quem é a vez? | Agora é com a Mobilizando |
| O que preciso fazer? | Nada neste momento |
| Qual o próximo passo? | O projeto chega para a sua aprovação até ter, 29/09 |
| Prazo crítico | Submissão até sex, 02/10 (D-3) |
| Farol | Agora é com a Mobilizando, dentro do prazo |

Com entrega aberta: cartão grande com a entrega mais urgente e o botão **Fazer agora**, que abre a etapa já expandida. Detalhe da tela na arquitetura 2.3.

### 12.2 Administradora

Tela inicial "Prazos da carteira": **o que precisa da minha atenção hoje**. Cada linha com organização, edital, etapa, de quem é a vez, item, data, D-n e nível do Farol.

Blocos:
- atrasados dos dois lados;
- vence hoje;
- vence amanhã;
- próximos 7 dias;
- prazo perdido;
- decisões abertas (encerrar, seguir ou encerrar, responder dúvida do OK);
- ideias recebidas e complementos respondidos;
- documentos aguardando conferência;
- resultado previsto não registrado;
- recurso e pós-aprovação.

Detalhe na arquitetura 2.2.

## 13. Histórico

O histórico é a memória operacional. **Escrito só pelo banco** (pacote 3), sem como forjar, e **nunca editado nem apagado** (em vigor desde o pacote 2).

Eventos que ficam registrados:
- edital aberto, editado, movido, apagado, restaurado ou apagado de vez;
- dossiê informado;
- OK respondido, e mudança de resposta;
- documento acrescentado, enviado, conferido ou recusado;
- ideia enviada;
- complemento pedido e respondido;
- pergunta e resposta;
- projeto enviado;
- aprovação ou pedido de ajustes;
- revisão enviada;
- submissão e protocolo;
- encerramento com motivo;
- resultado, prazos de recurso e pós-aprovação;
- nome da organização corrigido (em vigor desde 14/09);
- e-mails enviados, quando ligados.

**Pendente de decisão:** "cliente visualizou" (abertura do dossiê ou do projeto). É escopo novo e exige guardar leitura por pessoa.

## 14. Documentos

Como na arquitetura 2.9: lista por linha, dois caminhos de envio (anexo privado no portal com versões, ou pasta do Drive por link manual), conferência com recusa e motivo, "Baixar tudo deste edital", e o cliente nunca apaga arquivo. A leitura do que falta é feita pela AMC IA fora do portal, só lendo a pasta do cliente.

## 15. Notificações

Nascem de **eventos operacionais**, nunca de mensagem solta. No portal, sino e central de alertas; por e-mail, nos pacotes 12 e 13 (decisão 4), começando desligado e passando por modo teste. Quadro "Quem recebe o quê" na arquitetura 2.4.

Eventos novos trazidos por este mapa, se entrarem na v1.0:
- complemento pedido, para o cliente;
- complemento respondido, para a administradora;
- decisão de atraso aberta, para os dois.

## 16. Simplicidade

O cliente não vê arquitetura técnica, agentes, ferramentas de IA, metodologia interna nem operação da Mobilizando. Recebe **o que aconteceu, o que precisa fazer, o prazo e o resultado**, e vê o prazo real da Mobilizando (seção 4.5). Simplicidade não é esconder atraso.

## 17. Cruzamento com o documento-base

| Documento "Como trabalhamos juntos" | Portal |
|---|---|
| Etapa 1. Encontramos o edital | Edital aberto pela administradora |
| Etapa 2. Dossiê do Edital | Data do dossiê; dossiê no portal pendente de decisão |
| Etapa 3. OK e documentos extras | OK com três respostas; lista de documentos com conferência |
| Etapa 4. Esboço, objeto ou ideia | Ideia do Projeto, formas A, B e C |
| Etapa 5. Elaboramos o projeto | Projeto em elaboração, com prazo real |
| Etapa 6. Aprovação ou ajustes | Aprovação com nome e cargo; ajustes e revisão |
| Etapa 7. Submissão | Protocolo, data e hora; comprovante pendente de decisão |
| Os quatro momentos do cliente | "O que é seu agora" e o Farol |
| Calendário e três ritmos | Cálculo automático, nada digitado |
| Se uma entrega atrasar | Farol mais decisão (seção 11.3) |
| Datas deste edital | Linha do tempo do edital |
| Roteiro do esboço | Forma B da Ideia do Projeto |

## 18. Escopo da v1.0

**Dentro:** pacotes 3 a 13 da arquitetura, com o Farol e o escopo novo aprovado da seção 19 encaixados neles.

**Fora (integrações futuras, pacote 14 ou decisão nova):**
- integração automática com o CaptaHub;
- a AMC IA gravando direto no portal;
- WhatsApp;
- cópia automática dos anexos para o `G:` (esbarra na regra "nada roda sozinho");
- inteligência artificial dentro do portal;
- papel de equipe.

## 19. Escopo novo trazido por este mapa

Nada disto está na arquitetura de 13/09. Cada item precisa de decisão, de pacote e de conta de crédito antes de implementar.

| Item | Situação | Encaixe provável |
|---|---|---|
| Farol: nome, três leituras e sinais (seção 4) | aprovado como conceito; frases pendentes | pacotes 8 e 9, sem crédito extra relevante |
| Etapa principal calculada (seção 5.2) | proposta | pacote 8 |
| Ideia do Projeto, formas A e B (seção 7.2) | decidido | pacote 4 ou 9 |
| Ideia do Projeto, forma C | decidido, depende de arquivos | pacote 7 |
| Pedido de complemento (seção 7.4) | pendente | pacote 6 ou 9 |
| Decisão de atraso (seção 11.3) | critério pendente | pacote 6 |
| Dossiê no portal | pendente: arquivo ou link | pacote 7 |
| Versões do projeto e versão aprovada | pendente | pacote 7 |
| Comprovante anexado | pendente: arquivo ou link | pacote 7 |
| "Cliente visualizou" | pendente | pacote 9 |

## 20. Critérios de aceite do mapa

| Pergunta | Situação em 14/09 |
|---|---|
| Sabemos todas as etapas? | Sim: 7, do documento-base |
| Quem é responsável por cada ação? | Sim: seções 3, 5.3 e 6 |
| Quando a responsabilidade passa de um lado para o outro? | Sim: seção 5.3 e o Farol |
| Quais são os estados? | Sim: situação, etapa e entregas (seção 5) |
| O que o cliente vê? | Sim: seção 12.1 e arquitetura 2.3 |
| O que a administradora vê? | Sim: seção 12.2 e arquitetura 2.2 |
| Quais ações ficam registradas? | Sim, menos "cliente visualizou" |
| Como os prazos são calculados? | Sim: seção 11.1, motor já conferido |
| O que acontece quando há atraso? | Em parte: falta o critério de "compromete a submissão" |
| Como funciona a Ideia do Projeto? | Sim, menos o complemento na v1.0 |
| Como o Farol acompanha o processo? | Em parte: faltam as frases |
| Quais documentos entram? | Em parte: faltam dossiê, projeto e comprovante |
| Como funciona a aprovação? | Sim, menos as versões |
| Como funciona a submissão? | Sim, menos o comprovante |
| O que acontece depois da submissão? | Sim: seção 10 |
| O que é automático e o que é manual? | Sim: cálculo, Farol e registro automáticos; decisões, conferência, encerramento e resultado manuais |
| O que já existe no portal? | Sim: arquitetura, diagnóstico, e pacotes 1 e 2 |
| O que precisa ser alterado? | Sim: os 17 defeitos e as seções 6 a 9 |
| O que será novo? | Sim: seção 19 |
| Temos critérios de teste? | Sim, por pacote na arquitetura; os itens da seção 19 ganham os deles na revisão |

**Resultado:** 13 sim, 4 sim com ressalva ("menos...") e 3 em parte. O mapa fecha como v1.0 com as pendências da seção 22 anotadas.

## 21. Caminho até a implementação

```text
MAPA OPERACIONAL v1.0 (este documento, fonte da verdade)
        ↓
REVISÃO DA ARQUITETURA (docs/portal-clientes-arquitetura.md)
absorve o Farol, o modelo de andamento e o escopo novo aprovado,
e refaz a conta de créditos
        ↓
PACOTE 3, 4, 5... (a numeração continua; os pacotes 1 e 2 já estão aplicados)
um arquivo em docs/ por pacote, enviado ao Lovable só com o OK da captadora
        ↓
CONFERÊNCIA SEM CRÉDITO (banco e código) E TESTE DE COMPORTAMENTO COM OK
        ↓
TESTE NA TELA PELA CAPTADORA
        ↓
PRÓXIMO PACOTE
        ↓
HOMOLOGAÇÃO FINAL
```

**O que cada pacote leva ao Lovable:**
- objetivo;
- contexto mínimo;
- arquivos envolvidos;
- comportamento esperado;
- regras;
- segurança;
- critérios de aceite;
- testes obrigatórios;
- a frase "não altere regras de linha, permissões nem gatilhos fora do que foi pedido", e o que mais não pode mudar.

**Quem faz o quê:** o Lovable implementa; a AMC IA escreve o pacote, confere o resultado e registra; a captadora aprova cada envio e faz o teste na tela.

## 22. Pendências abertas

1. Frases exatas dos sinais do Farol (seção 4.6).
2. Critério de "atraso que compromete a submissão" (seção 11.3).
3. Pedido de complemento da ideia na v1.0: sim ou não (seção 7.4).
4. Dossiê no portal: arquivo, link ou fora (etapa 2).
5. Versões do projeto e versão aprovada no portal: sim ou só o registro (seção 8).
6. Comprovante de submissão: arquivo, link ou só o protocolo (seção 9).
7. "Cliente visualizou" no histórico: sim ou não (seção 13).
8. Atualizar o documento "Como trabalhamos juntos" com as 5 perguntas curtas da Ideia do Projeto (decisão 2).
9. Confirmar a regra da etapa principal calculada (seção 5.2).
