# Portal do Cliente Mobilizando. Mapa Operacional v1.0

> **Fonte da verdade da operação do portal.** Proposto pela captadora em 14/09/2026, conferido contra o documento-base e contra a arquitetura de 13/09, e corrigido com as decisões dela em duas rodadas no mesmo dia (seção 23).
>
> **Hierarquia das fontes**
> 1. `marketing/entregas/comercial/como-trabalhamos-juntos.md`: jornada, responsabilidades e prazos. Manda sobre tudo.
> 2. **Este mapa:** a lógica operacional do portal sobre essa jornada, incluindo o Farol.
> 3. `docs/portal-clientes-arquitetura.md`: como o mapa vira telas, dados, segurança e pacotes.
> 4. `docs/portal-clientes-pacote-*.md` e afins: a instrução de cada pacote enviado ao Lovable.
>
> **Este mapa não é prompt de implementação.** Ele não vai inteiro ao Lovable. Cada pacote leva só a parte necessária.

## Decisões da captadora

**Primeira rodada, 14/09/2026**
1. O portal e o documento mantêm **7 etapas**.
2. **Ideia do Projeto:** forma A com 5 perguntas curtas; forma B, "já tenho um esboço", com os 8 itens do roteiro. **Substituída pela decisão 18:** a forma B passa a ter os 11 itens do esboço do projeto.
3. **Andamento:** etapa da jornada mais entregas paralelas. Não é fila única.
4. **Os e-mails automáticos ficam na v1.0**, no fim (pacotes 12 e 13).

**Segunda rodada, 14/09/2026**

5. **Forma C, "Já tenho um documento", faz parte da Ideia do Projeto desde o início.** A infraestrutura segura de armazenamento ainda será definida, no pacote correspondente. Nada de armazenamento provisório.
6. **Complementação da ideia: sim.** Pedir informação complementar não é rejeitar a ideia.
7. **Entregas paralelas sem fila rígida.**
   - A ideia não depende da documentação.
   - A documentação não depende da ideia nem do OK.
   - A elaboração continua com documentação pendente, quando operacionalmente possível.
8. **Registro da submissão: bloqueio com confirmação**, só quando há documento obrigatório pendente.
9. **Documento obrigatório ou facultativo.** Pendente é: não enviado, enviado e ainda não conferido, ou recusado.
10. **Etapa da jornada:** nunca pela "última entrega feita". São as 7 etapas oficiais, sem pulo artificial.
11. **Farol:** lê o processo real. Para o cliente, responde "O que é seu agora?" ou "Agora é com a Mobilizando", com a situação e a data real da próxima referência.
12. **Prioridade do Farol** em 6 níveis, com empate pela data mais próxima.
13. **Cores:**
    - verde para feito;
    - dourado para perto do prazo;
    - vermelho para atrasado e para prazo perdido;
    - "em N dias" neutro;
    - "a calcular" sem cor.
14. **"Como trabalhamos juntos" é atualizado antes de a nova tela da Ideia do Projeto chegar ao cliente.**

**Terceira rodada, 14/09/2026**

15. **Regra da etapa da jornada aprovada** (seção 5.2): a etapa atual é a primeira etapa ainda não concluída, com um marco de conclusão definido para cada uma, sem pular artificialmente etapas. Encerra a pendência 9.
16. **Registro da Ideia do Projeto:** alteração gera registro **somente quando há mudança real de conteúdo ou de escolha ou estado**. Salvamento idêntico não gera registro novo (seção 7.3).
17. **"Cliente visualizou"** deixa de ser decisão necessária antes do pacote 3. Se for adotado, o evento é criado no pacote que implementar esse dado (regra "cada pacote cria o gatilho do seu dado", arquitetura 2.10).

**Quarta rodada, 14/09/2026, noite**

18. **Esboço do projeto em 11 itens.** Os 8 itens do roteiro antigo (o quê, para quem, onde, quando, como, com quem, quanto, o que já existe) **não são o esboço** e saem do portal e do documento. Entra o roteiro da captadora, com 11 itens (seção 7.2, forma B).
19. **Nomes das três formas:**
    - A: "Ainda estou começando";
    - B: "Vou preencher o esboço aqui";
    - C: "Já tenho o esboço em arquivo".
    
    Cada opção leva uma explicação curta embaixo.
20. **Obrigatórios do esboço:** os 11 itens, **menos o 10, Recursos necessários**, que é "se souber". A tela mostra um contador de itens preenchidos.
21. **Porta C:** aceita PDF, Word (DOC e DOCX), imagem (JPG e PNG) e planilha, até 20 MB. **Anexam** a administradora e o cliente; **remove** só a administradora.
22. **Enviar exige resposta**, e ao enviar a entrega vira "feito" sozinha.
23. **Modelo Word "Roteiro do esboço"** com os 11 itens, para baixar na tela, preencher com calma e anexar pela porta C.
24. **Complementação** (seção 7.4) fica para uma etapa seguinte do pacote da Ideia.

**Quinta rodada, 14/09/2026, noite: projeto por versões** (encerra as pendências 5 e 6)

25. **O projeto passa pelo portal, em versões.** A Mobilizando envia V1, V2, V3..., e o portal numera e data cada uma. A etapa 5 se conclui com o envio da versão, **sem "Marcar como feito"**.
26. **A aprovação é presa à versão.** O cliente aprova ou pede ajustes **da versão atual**. A etapa 6 se conclui com "aprovada" na versão atual, **sem "Marcar como feito"**.
27. **Ajustes pedidos voltam a jornada para a etapa 5** (substitui a consequência "Ajustes pedidos mantêm a etapa 6" da seção 5.2): a vez é da Mobilizando, que envia nova versão.
28. **Formato do projeto:** PDF e Word.
29. **O cliente vê e baixa todas as versões**, com o histórico de envio e de resposta.
30. **Nenhuma versão é apagada.** Arquivo errado se corrige com uma versão nova, com observação.
31. **Nova versão enviada depois de uma aprovação faz a aprovação voltar a ficar pendente**, mesmo sem pedido do cliente.
32. **Nome e cargo de quem aprovou não são obrigatórios.**
33. **Submissão:** registra a versão submetida, o protocolo, a data e a hora, quem registrou e o comprovante, que pode ser **arquivo (PDF ou imagem), link ou os dois**. **Registrar a submissão sem a versão atual aprovada não pede confirmação.**

**Sexta rodada, 14/09/2026, noite: a administradora pode tudo** (substitui "o cliente marca as dele" onde houver conflito)

34. **A administradora faz tudo o que o cliente faz, em todas as etapas:** escolher e salvar o OK, marcar documento enviado, enviar a Ideia do Projeto nas três formas (o envio conclui a entrega), aprovar ou pedir ajustes numa versão do projeto e marcar ou desmarcar qualquer entrega.
35. **O registro mostra o nome de quem fez.** Quando a administradora responde pelo cliente, o autor é ela. A entrega conta como feita normalmente.
36. **Aviso na tela para a administradora:** "Você está como administradora: o que marcar ou enviar pelo cliente fica registrado no seu nome."
37. **A administradora pode apagar a resposta do cliente** (OK e Ideia do Projeto) **e apagar uma versão do projeto.** Substitui a decisão 30 para a administradora; o cliente continua sem apagar nada. Ao apagar uma versão, as etapas 5 e 6 voltam a refletir a versão que ficou como atual, e o registro guarda o que foi apagado.
38. **Página da organização:** clicar no nome da organização no painel abre a página dela, com o nome editável, os editais em andamento (em cartões iguais aos do cliente), os finalizados, as pessoas e os convites pendentes (só consulta).

**Sétima rodada, 14/09/2026, noite: convite por e-mail e por WhatsApp**

39. **O convite sai pela conta da captadora, não pelo portal.** Ela registra o convite (e-mail e organização) e o portal monta a mensagem pronta, com o link de acesso, o que é o portal, como entrar pela primeira vez e como usar. Três botões: "Enviar por e-mail" (abre o Gmail com a mensagem escrita), "Enviar pelo WhatsApp" (abre o WhatsApp com a mesma mensagem) e "Copiar mensagem". Os botões aparecem logo depois de registrar e em cada convite pendente da página da organização.
40. **A pessoa cria a conta com o mesmo e-mail do convite** em "Primeiro acesso, criar conta" e já entra na organização. Sem serviço de envio, sem link individual e sem regra nova no banco. O envio automático pelo portal continua no pacote 13, depois do domínio verificado.
41. **Quem já tinha conta sem organização entra pela do convite** ao fazer login, desde que exista convite pendente para o e-mail dela.

**Oitava rodada, 15/09/2026: o link do convite abre direto o cadastro** (ajusta a 40)

42. **Cada convite tem o próprio link** (`portal.mobilizando.org/convite/…`), e é ele que vai no e-mail e no WhatsApp. O link abre a tela "Criar meu acesso" com a organização e o e-mail do convite já preenchido e travado. A pessoa informa nome e senha e entra no painel na hora, **sem e-mail de confirmação**: o link enviado pela captadora serve como a confirmação. Convite já usado ou e-mail que já tem conta levam para a tela de entrada.

43. **Aviso de edital novo, provisório até o pacote 8.** Na página do edital, só a administradora vê o bloco "Avisar o cliente", que monta a mensagem pronta com o nome do edital, o órgão, o último dia das inscrições, o link direto do edital e o que o cliente faz primeiro. Ela envia pelo Gmail ou pelo WhatsApp, como no convite. O aviso automático pelo sino continua no pacote 8 e o e-mail na hora, no pacote 13.

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

**Mobilizando.** Encontra o edital, lê e analisa, produz o Dossiê do Edital, confere a documentação, analisa a ideia e pede complemento quando falta informação, elabora proposta e orçamento, faz a revisão final, submete no portal do financiador, registra a submissão, envia o comprovante e registra o resultado.

**Organização cliente.** Tem quatro momentos, segundo o documento-base:
1. OK para seguir.
2. Documentos extras.
3. Esboço, objeto ou ideia.
4. Aprovação ou ajustes.

"Nos outros momentos, o trabalho é nosso." A resposta a um pedido de complemento (seção 7.4) faz parte do momento 3.

**Portal.** Calcula os prazos, mostra de quem é a vez, controla as entregas, registra as ações, sinaliza atraso e risco, guarda o histórico, organiza os documentos, avisa os dois lados e impede o que cada papel não pode fazer.

---

## 4. O Farol

### 4.1 O que é

O Farol é a **camada de leitura operacional** do portal. Ele não aparece no documento-base: materializa a jornada do documento. Acompanha todas as etapas.

### 4.2 O que o Farol não é

- **Não é etapa.**
- **Não cria estado paralelo.** Ele lê a etapa da jornada, as entregas e a situação do edital (seção 5).
- **Não é um segundo motor de prazos.** Usa o motor único previsto na arquitetura (`src/lib/alertas.ts`, sobre `prazos.ts` e `agenda.ts`). Nenhuma data gravada, nenhuma lista nova de feriados.
- **Não cria níveis de prazo nem de risco** além dos da arquitetura (seção 4.6).
- **Não cria cores** além das da seção 4.6.

### 4.3 O que o Farol lê

- Etapa da jornada.
- Entregas abertas.
- Responsável por cada entrega.
- Prazo e nível de cada entrega.
- Documentos: obrigatórios e facultativos, e suas situações.
- Complementos pedidos e respondidos.
- Situação do edital (em andamento ou encerrado).
- Riscos e atrasos: atraso de qualquer lado, decisão aberta, prazo perdido.

### 4.4 O que o Farol responde ao cliente

A pergunta principal é **"O que é seu agora?"**. A resposta é uma de duas:

- **Há algo do cliente:** o item que vem primeiro pela prioridade (seção 4.7), com o prazo e o nível.
- **Não há nada do cliente: "Agora é com a Mobilizando"**, sempre com **a situação e a data real da próxima referência**. Exemplo: "Agora é com a Mobilizando. Projeto previsto para ter, 29/09, atrasado há 2 dias."

**Pendente (pendência 1):** as frases exatas de cada leitura. Na primeira versão do mapa, as propostas eram "Sua vez" e "Precisamos de você", para complemento e documento recusado.

### 4.5 Nenhum prazo mascarado (regra de 13/09, vale para o Farol)

- Todo prazo, de qualquer lado, aparece para os dois lados com a data e a situação reais.
- Atraso da Mobilizando aparece para o cliente como atraso, na mesma cor dos atrasos dele.
- Prazo recalculado mostra as duas datas e o motivo.
- **Nenhum filtro, texto, estado ou prioridade esconde atraso ou prazo perdido.** A prioridade só decide o que aparece primeiro; o resto continua visível.

### 4.6 Níveis e cores

Os níveis vêm da arquitetura (2.4). As cores vêm da especificação original (`docs/portal-clientes-especificacao.md`) e da decisão 13.

| Nível | Cor |
|---|---|
| Feito | verde |
| A calcular | sem cor |
| Em N dias | neutro |
| Em 3 dias | dourado |
| Em 2 dias | dourado |
| Vence amanhã | dourado |
| Vence hoje | dourado |
| Atrasado há N dias | vermelho |
| Prazo perdido | vermelho |

**Situações sem nível próprio não têm cor própria.** São elas:
- decisão aberta;
- registro de submissão com pendência;
- complemento pedido;
- documento recusado.

Cada uma mostra a cor do nível do prazo do item a que se refere. Sem prazo, fica sem cor.

### 4.7 Prioridade do Farol (decisão 12)

Quando há mais de uma situação ao mesmo tempo, o Farol mostra primeiro, nesta ordem:

1. Bloqueio ou risco crítico que exige decisão.
2. Pendência do cliente que exige ação.
3. Pendência recusada ou complemento solicitado.
4. Prazo mais próximo.
5. Próxima ação normal.
6. Nenhuma ação do cliente: "Agora é com a Mobilizando".

**Empate na mesma prioridade:** prevalece a data mais próxima.

A prioridade usa só os níveis e as situações que já existem. Ela não cria nível novo de risco.

**A fechar no pacote do Farol (pacotes 8 e 9), sem mudar a ordem decidida:**
- o que separa, na prática, a prioridade 2 ("pendência que exige ação") da prioridade 5 ("próxima ação normal");
- quais situações entram na prioridade 1;
- se a mesma ordem vale dentro dos blocos da tela "Prazos da carteira" da administradora.

### 4.8 Sinais do Farol

| Situação lida | Cliente vê | Administradora vê | Prioridade |
|---|---|---|---|
| Decisão aberta por atraso que compromete a submissão | "Vamos decidir juntos" | "Decidir: seguir ou encerrar" | 1 |
| Resposta "Não vamos entrar neste edital" | a resposta registrada | "Decidir: encerrar edital" | 1 |
| Entrega do cliente aberta | O item, com prazo e nível | De quem: cliente, com o nível | 2, 4 ou 5 |
| Documento recusado | O documento e o motivo | Aguardando cliente: documento recusado | 3 |
| Complemento solicitado | O que falta, exatamente | Aguardando informações do cliente | 3 |
| Nenhuma entrega do cliente aberta | "Agora é com a Mobilizando", com a situação e a data real da próxima referência | De quem: Mobilizando, com o nível | 6 |
| Atrasado, de qualquer lado | Atrasado há N dias, em vermelho, dizendo de quem | Idem, e entra em "Atrasados" | pela situação de origem |
| Dia D sem submissão | Prazo perdido | Prazo perdido, com de quem eram as pendências | 1 |
| Encerrado | Resultado ou motivo do encerramento | Idem, e sai da carteira ativa | não se aplica |

As prioridades desta tabela aplicam a ordem da seção 4.7 às situações conhecidas. Elas são conferidas no pacote do Farol.

---

## 5. O modelo de andamento (decisões 3, 7 e 10)

Três camadas, lidas juntas pelo Farol.

### 5.1 Situação do edital

Da arquitetura (2.6):
- em andamento;
- submetido, aguardando resultado;
- aprovado, com data;
- reprovado, com data;
- não submetido, com motivo obrigatório;
- apagado (só erro de cadastro).

### 5.2 Etapa da jornada

As 7 etapas oficiais do documento-base. **A etapa informa onde está a jornada. As entregas informam o que está pendente, de quem é e até quando.**

**Regra:** a etapa atual é **a primeira etapa, na ordem de 1 a 7, que ainda não foi concluída**. Não se usa "a última entrega feita".

| Etapa | Concluída quando |
|---|---|
| 1. Encontramos o edital | o edital é aberto no portal (no portal, o edital só existe depois de encontrado, então a etapa 1 se conclui na abertura) |
| 2. Dossiê do Edital | o dossiê é enviado, marcado pela data do dossiê informada |
| 3. OK e documentos extras | o cliente responde "Quero seguir com este edital" |
| 4. Esboço, objeto ou ideia | o cliente envia a Ideia do Projeto, por A, B ou C |
| 5. Elaboramos o projeto | há uma versão do projeto enviada que não recebeu pedido de ajustes (decisão 25) |
| 6. Aprovação ou ajustes | o cliente aprovou **a versão atual** (decisão 26) |
| 7. Submissão | a submissão é registrada |

**Consequências da regra**
- **Sem pulo artificial.** Uma entrega adiantada não empurra a jornada. Exemplo: se a ideia chega antes do OK, a jornada continua na etapa 3 e a entrega da ideia aparece como feita. Quando o OK vem, a etapa 4 já está concluída e a jornada vai para a 5.
- **Documentos extras não seguram a jornada.** A etapa 3 se conclui com o OK; os documentos continuam como entrega paralela, com prazo e situação próprios.
- **Complemento não reabre a etapa 4.** Ele abre uma pendência do cliente (seção 7.4).
- **Ajustes pedidos voltam a jornada para a etapa 5** (decisão 27, que substituiu "ajustes pedidos mantêm a etapa 6"). A Mobilizando revisa e envia nova versão; a etapa 6 volta a ser a da resposta a essa versão.
- **"Tenho dúvidas" e "Não vamos entrar" não concluem a etapa 3.**

**Aprovada pela captadora em 14/09/2026 (decisão 15).** A pendência 9 está encerrada. Um ponto técnico para o pacote correspondente: hoje o portal pede a data do dossiê na abertura do edital. Se ela puder ser uma data futura, o marco de "dossiê enviado" precisa ser separado da data prevista.

### 5.3 Entregas paralelas

Cada entrega tem prazo, situação e responsável próprios. **Não há fila rígida entre elas.**

| Entrega | Responsável | Pode ser feita |
|---|---|---|
| OK para seguir | cliente | depois do dossiê enviado, porque o prazo conta a partir dele (documento-base) |
| Documentos extras | lista pela Mobilizando; envio pelo cliente | a qualquer momento em que a lista tiver linhas. **Não depende do OK nem da ideia** |
| Esboço, objeto ou ideia | cliente | a qualquer momento. **Não depende da documentação** |
| Resposta ao complemento | cliente | depois que a Mobilizando pede. Não depende da documentação |
| Projeto enviado para aprovação | Mobilizando | a elaboração **continua com documentação pendente**, quando operacionalmente possível. Mostra "com pendência do cliente" sem tirar da tela o atraso da Mobilizando (arquitetura 2.4) |
| Aprovação ou ajustes | cliente | depois do projeto enviado |
| Registro da submissão | administradora | mostra "aguardando aprovação" se ela não veio (arquitetura 2.4). Com documento obrigatório pendente, **bloqueio com confirmação** (seção 9.2) |

**Decisões futuras registradas, sem regra criada:**
- se a ideia pode ser enviada antes do OK (a regra atual não impede);
- ~~se registrar a submissão sem aprovação também pede confirmação~~: **decidido, não pede** (decisão 33).

---

## 6. A jornada, etapa por etapa

### Etapa 1. Encontramos o edital

- **Nós:** buscamos editais que combinam com a área de atuação, o território, o valor e o tipo de proponente aceito.
- **Você:** nada ainda.
- **Portal:** a administradora abre o edital: nome, órgão, link, dia D, data do dossiê e ritmo. Registro: "Abriu o edital".
- **Farol:** cliente, "Agora é com a Mobilizando", com a data do dossiê; administradora, dossiê a enviar.
- **Hoje:** existe.

### Etapa 2. Você recebe o Dossiê do Edital

- **Nós:** lemos o edital e os anexos e enviamos o dossiê: o que financia, quem pode participar, prazos, critérios, riscos e documentos exigidos.
- **Você:** lê o dossiê e decide se quer entrar.
- **Portal:** a data do dossiê dispara o prazo do OK.
- **Farol:** cliente, o OK como item dele, com prazo e nível.
- **Hoje:** existe a data; o dossiê sai fora do portal.
- **Pendente (pendência 4):** o dossiê dentro do portal, como arquivo, link ou fora.

### Etapa 3. Você dá o OK e providencia os documentos extras

**OK para seguir.** Três respostas, como já existe no portal:
1. "Quero seguir com este edital." Conclui a etapa 3.
2. "Não vamos entrar neste edital."
3. "Tenho dúvidas antes de decidir."

Com observações. O banco registra quem respondeu e quando.

- **"Não vamos entrar":**
  - os lembretes do cliente param;
  - a administradora recebe "Decidir: encerrar edital";
  - ela encerra como "Não submetido: desistência do cliente";
  - **o portal não encerra sozinho** (arquitetura 2.6).
- **"Tenho dúvidas":**
  - a resposta e a observação ficam registradas;
  - a etapa 3 não se conclui;
  - o prazo do OK continua visível, com a situação real;
  - **decisão futura:** quem responde a dúvida, por onde, e de quem é a vez enquanto isso. A versão anterior do mapa dizia que a vez passava à Mobilizando; isso era inferência, sem base, e foi retirado.

**Documentos extras**
- **Nós:** conferimos a lista do edital com a documentação base da pasta do cliente (estatuto, ata, cartão CNPJ, certidões) e apontamos só o que falta. A leitura é feita pela AMC IA, fora do portal, só lendo (arquitetura 2.9). Cada linha traz o item do edital de onde vem e **se é obrigatório ou facultativo**.
- **Você:** providencia o que falta: documentos específicos, declarações para assinar e certidões vencidas. **Não precisa ter dado o OK nem enviado a ideia.**
- **Portal:** lista por linha, e cada linha com uma situação: pendente, enviado, conferido ou recusado com motivo (seção 14). Dois caminhos de envio: anexar no portal ou pela pasta do Drive (link manual).
- **Farol:** cliente, os documentos pendentes; recusado aparece com o motivo (prioridade 3).
- **Hoje:** existem a lista e a marcação de enviado. Obrigatório ou facultativo, conferência, recusa, anexo e Drive entram no pacote de documentos.

### Etapa 4. Você envia o esboço, o objeto ou a ideia

Ver seção 7.

### Etapa 5. Elaboramos o projeto

- **Nós:** escrevemos a proposta e montamos o orçamento, ancorados nos critérios do edital, conferimos tudo e enviamos para aprovação até D-6 no padrão (D-10 na folga maior, D-4 no apertado).
- **Você:** fica disponível para alguma dúvida pontual, e responde a complemento, se houver.
- **Portal:** perguntas e respostas no edital; a administradora **envia a versão do projeto** (PDF ou Word, com observação opcional), e a etapa se conclui com o envio (decisões 25 e 28).
- **Farol:** cliente, "Agora é com a Mobilizando", com a data do projeto e a situação real; complemento aberto aparece como item do cliente.
- **Documentação pendente não impede a elaboração**, quando operacionalmente possível.
- **Hoje:** existe, menos o complemento.

### Etapa 6. Você aprova ou pede ajustes

Ver seção 8.

### Etapa 7. Submetemos o projeto

Ver seção 9.

---

## 7. Ideia do Projeto (decisões 2, 5, 6 e 14)

Nome no portal: **Ideia do Projeto**. Nome no documento-base: "esboço, objeto ou ideia". Prazo: D-12 no padrão, D-20 na folga maior, D-8 no apertado.

### 7.1 Mensagem fixa

> **Sua ideia é o ponto de partida, não o projeto final.** A Mobilizando desenvolve e adapta às regras e aos critérios do edital. O projeto pode mudar de formato, público ou valor para caber nas regras e pontuar melhor.

(Adaptado do destaque da etapa 4 do documento-base.)

### 7.2 As três formas, todas parte da experiência desde o início

**A. "Ainda estou começando": 5 perguntas curtas.** Explicação da opção: "Tenho só a ideia. Respondo 5 perguntas curtas."
1. O que você quer fazer?
2. Para quem?
3. Onde?
4. Por que isso é importante?
5. O que você espera alcançar?

**B. "Vou preencher o esboço aqui": o esboço do projeto, 11 itens** (decisão 18). Explicação da opção: "Escrevo o esboço seguindo 11 itens, um de cada vez."
1. **Nome ou ideia do projeto:** mesmo que provisório.
2. **Quem é o proponente:** pessoa, empresa, associação, coletivo, instituição etc.
3. **Problema ou necessidade:** o que o projeto pretende enfrentar ou transformar.
4. **Público-alvo:** quem será beneficiado e, se possível, quantidade estimada.
5. **Local de execução:** cidade ou território e, se já souber, os locais específicos.
6. **Objetivo principal:** o que você quer alcançar.
7. **Atividades previstas:** o que será feito na prática.
8. **Resultados esperados:** quais mudanças ou entregas pretende gerar.
9. **Duração aproximada:** por exemplo, 6, 12 ou 18 meses.
10. **Recursos necessários:** uma estimativa de quanto imagina precisar, se souber. **Único item não obrigatório.**
11. **Diferencial da ideia:** por que esse projeto merece ser realizado e o que o torna diferente.

Os 8 itens antigos (o quê, para quem, onde, quando, como, com quem, quanto, o que já existe) **saíram por decisão da captadora em 14/09**: não são o esboço.

**C. "Já tenho o esboço em arquivo"** (nome anterior: "Já tenho um documento"). Explicação da opção: "Tenho o esboço ou o projeto pronto. Anexo o documento."
- Faz parte da experiência da Ideia do Projeto **desde o início**. Não fica escondida à espera de um pacote.
- Finalidade: permitir anexar projeto, PDF, Word ou outro material existente.
- **A infraestrutura segura de armazenamento ainda precisa ser definida.** O portal não tem hoje nenhum espaço de arquivos (conferido em 14/09: 0 espaços, 0 arquivos), e a página de Privacidade diz que ele não guarda arquivo.
- **Não se cria armazenamento provisório.**
- A decisão técnica (onde guardar, quem vê, tipos, tamanho, versões, atualização da Privacidade) é tratada no pacote correspondente.
- **Decisão futura, desse mesmo pacote:** o que a forma C oferece ao cliente enquanto o anexo não estiver disponível.

**Preenchimento.** "Responda o que souber; o que faltar, construímos juntos." (documento-base) **Decisão futura, do pacote da Ideia:** o mínimo exigido para o botão de envio funcionar. A versão anterior do mapa dizia "ao menos uma resposta"; isso não tinha base e foi retirado.

### 7.3 Ao enviar a ideia

1. Grava as respostas, ou a indicação da forma C.
2. O banco registra quem enviou e quando; autor e hora não vêm da tela.
3. A entrega "Esboço, objeto ou ideia" fica feita, e a situação da ideia passa a **"Ideia recebida"**.
4. A etapa 4 fica concluída. A jornada vai para a primeira etapa ainda não concluída (seção 5.2).
5. Entra no histórico.
   - **Regra do registro (decisão 16):** só gera linha quando há mudança real.
     - Conta como mudança: a escolha da forma, o conteúdo de algum campo ou o estado da entrega.
     - Não conta: salvar de novo o mesmo conteúdo, ou mudar só espaços nas pontas de um campo.
     - Campo vazio e campo em branco valem o mesmo.
   - A primeira gravação com conteúdo registra "Enviou o esboço, objeto ou ideia". As seguintes, com mudança real, registram "Atualizou o esboço, objeto ou ideia", dizendo quais campos mudaram.
6. Aparece para a administradora como novidade: "Nova ideia recebida".
7. O Farol do cliente segue a prioridade; sem outro item dele, "Agora é com a Mobilizando", com a data do projeto.
8. Aviso na hora para a administradora (evento 2 da arquitetura), quando os e-mails estiverem ligados.

### 7.4 Análise e complementação da ideia (decisão 6)

**Pedir complemento não é rejeitar a ideia.**

```text
Cliente envia a ideia
        ↓
Ideia recebida
        ↓
Mobilizando analisa
        ↓
Falta informação?
   não → a elaboração segue
   sim ↓
Aguardando informações do cliente
Mobilizando informa exatamente o que falta
        ↓
Cliente responde
        ↓
Mobilizando recebe
        ↓
A elaboração continua
```

**Regras**
- O pedido é escrito como pergunta específica, por exemplo "Qual será a duração aproximada das atividades?". Nunca "favor complementar".
- A ideia continua recebida e a entrega continua feita. O complemento é uma pendência nova do cliente (prioridade 3 do Farol).
- A etapa 4 não reabre.
- Enquanto o pedido está aberto, a situação é **"Aguardando informações do cliente"**.
- A resposta do cliente fecha o pedido, entra no histórico e avisa a administradora.
- **O prazo do projeto da Mobilizando não para nem é recalculado em silêncio.** Se a resposta demorar e isso afetar o projeto, o recálculo mostra as duas datas e o motivo (regra 2.5).
- **Decisões futuras, do pacote correspondente:**
  - se o pedido de complemento tem prazo próprio, e qual;
  - se pode haver mais de um pedido aberto ao mesmo tempo.

### 7.5 Documento "Como trabalhamos juntos" (decisão 14)

- Até 14/09 o documento trazia só o roteiro antigo de 8 itens.
- **Ele é atualizado antes de a nova tela da Ideia do Projeto chegar ao cliente**, com os caminhos:
  - ideia inicial, com 5 perguntas;
  - esboço do projeto, com 11 itens (decisão 18);
  - esboço em arquivo, anexado no portal.
- O `.md` foi atualizado em 14/09. As versões `.docx`, `.pdf` e `.html` do mesmo documento ainda trazem o roteiro antigo.
- A menção à forma C entra de acordo com o que o cliente de fato puder fazer naquele momento.
- A linguagem continua a de comunicação com o cliente, sem termos do portal nem da operação interna.

---

## 8. Aprovação e ajustes

- **Prazo:**
  - padrão: até 2 dias úteis depois de receber o projeto;
  - folga maior: D-7;
  - apertado: 1 dia útil.
- **Projeto atrasado:** o prazo de aprovação é recalculado com as duas datas visíveis e nunca passa da véspera da submissão.
- **Respostas** (já existem):
  - "Aprovado, pode submeter";
  - "Precisa de ajustes antes de submeter", com "O que precisa mudar";
  - em ambas, "Nome e cargo de quem aprovou".
- **Ajustes pedidos:** a vez volta para a Mobilizando e a jornada volta para a etapa 5, que se conclui de novo com o envio da versão seguinte (decisão 27).
- **Versões (decisões 25 a 31, encerram a pendência 5):**
  - o projeto passa pelo portal em versões numeradas (V1, V2...), com data, arquivo e observação;
  - a resposta do cliente fica presa à versão: "Versão atual: V2";
  - nova versão enviada faz a aprovação anterior deixar de valer, mesmo sem pedido do cliente;
  - o cliente vê e baixa todas as versões; nenhuma versão é apagada;
  - nome e cargo de quem aprovou são opcionais (decisão 32).
- **Registro:** quem enviou cada versão e quando; quem respondeu, quando, a escolha, a versão, o texto dos ajustes e o nome e o cargo informados.
- **Decisão pendente:** se o prazo da aprovação conta a partir de cada versão enviada (recomendado, com as duas datas visíveis) ou só da primeira.

## 9. Submissão (decisão 8)

### 9.1 O que o portal registra

- **A submissão real acontece no portal externo do financiador.** O Portal Mobilizando **registra** a submissão realizada.
- **Nós:** submetemos no portal do edital, antes do último dia, e enviamos o comprovante.
- **Você:** recebe o comprovante, "a prova de que o projeto foi entregue no prazo".
- **Registro pela administradora:** protocolo e data e hora da submissão, com a hora certa (defeito 9). Data informada e data da marcação ficam separadas.
- **Farol do cliente:** "Projeto submetido em {data}, protocolo {número}".

### 9.2 Bloqueio com confirmação

**Quando vale:** ao tentar **registrar** a submissão, se existir **documento obrigatório com situação diferente de "conferido"**, ou seja, não enviado, enviado e ainda não conferido, ou recusado.

**O que o portal faz:**
1. Mostra os documentos obrigatórios pendentes, cada um com a situação.
2. Explica o motivo: há documento obrigatório que ainda não está conferido.
3. Permite **confirmação explícita da administradora** para registrar a submissão mesmo assim.
4. Pede a justificativa e a preserva.
5. Registra no histórico:
   - que havia pendências, e quais;
   - quem confirmou;
   - data e hora;
   - a justificativa.

**Sem documento obrigatório pendente:** o registro segue sem confirmação extra.

**O bloqueio vale só para o registro da submissão.** Ele não bloqueia:
- o envio da ideia;
- a complementação;
- a elaboração do projeto;
- a aprovação;
- as outras entregas paralelas.

**Documento facultativo pendente não aciona este bloqueio.**

**Decisões futuras, do pacote correspondente:**
- se a justificativa é obrigatória para a confirmação valer;
- ~~se registrar a submissão sem aprovação também pede confirmação~~: **decidido, não pede** (decisão 33).

### 9.3 Versão submetida e comprovante (decisão 33, encerra a pendência 6)

- A submissão registra **a versão do projeto submetida**, o protocolo, a data e a hora, e quem registrou.
- **Comprovante:** arquivo (PDF ou imagem), link, ou os dois.
- O cliente vê: "Projeto submetido: V2 · Protocolo 123456 · 16/09/2026, 14h32", com o comprovante para abrir.

## 10. Depois da submissão

Já detalhado na arquitetura (2.6 e 2.8), e vale como está:
- **Situações:** aguardando resultado; aprovado com data; reprovado com data; não submetido com motivo.
- **Motivos de não submissão:**
  - desistência do cliente;
  - não recomendado pela Mobilizando;
  - inelegível;
  - prazo perdido, com de quem eram as pendências.
- **Datas informadas pela administradora:**
  - data prevista do resultado;
  - prazo de recurso, se reprovado;
  - prazo e descrição da pós-aprovação, se aprovado.
- **Resultado registrado** avisa o cliente na hora (evento 9).
- **Painel de resultados** para a organização e para a carteira, sem valores em reais (os valores ficam no CaptaHub).

---

## 11. Prazos

### 11.1 Calendário (documento-base)

- D é o último dia das inscrições.
- D-15 são 15 dias corridos antes.
- Data que cai em sábado, domingo ou feriado nacional vai para o dia útil anterior, e a tela diz o motivo.

| Entrega | Quem | Padrão (15 dias) | Folga maior (30 dias) | Apertado (10 dias) |
|---|---|---|---|---|
| Dossiê do Edital | Mobilizando | assim que o edital é encontrado | idem | idem |
| OK para seguir | cliente | 2 dias úteis após o dossiê | 3 dias úteis | 1 dia útil |
| Documentos extras | cliente | D-15 | D-25 | D-10 |
| Esboço, objeto ou ideia | cliente | D-12 | D-20 | D-8 |
| **Projeto enviado para aprovação** | **Mobilizando** | **D-6** | **D-10** | **D-4** |
| Aprovação ou ajustes | cliente | 2 dias úteis após o projeto | D-7 | 1 dia útil após o projeto |
| Submissão | Mobilizando | D-2 | D-3 | D-1 |

- O ritmo sugerido é o mais folgado que cabe, testando folga maior, padrão e apertado, nessa ordem.
- Teste obrigatório do motor: D em 05/10/2026, dossiê em 11/09/2026, ritmo padrão.
- Os prazos valem para cada entrega de forma independente. Uma entrega adiantada ou atrasada não muda o prazo das outras, salvo o recálculo da aprovação (seção 8).

### 11.2 Regra de ouro

> A submissão nunca fica para o último dia. Os portais costumam ficar lentos ou sair do ar perto do encerramento. (documento-base)

### 11.3 Atraso gera decisão, não só cor

Documento-base: "Avisamos na hora o que o atraso muda. Às vezes dá para compensar reorganizando o calendário. Às vezes não sobra tempo para fazer um projeto com a qualidade que a banca exige, e então decidimos com você se seguimos ou se deixamos para o próximo edital."

No portal:
1. O atraso aparece real para os dois lados, dizendo de quem é.
2. Quando o atraso compromete a submissão:
   - o Farol da administradora abre "Decidir: seguir ou encerrar";
   - o do cliente mostra "Vamos decidir juntos";
   - é prioridade 1.
3. **Seguir:** o recálculo mostra as duas datas e o motivo.
4. **Deixar para o próximo:** a administradora encerra como "Não submetido", com o motivo.
5. **Dia D sem submissão:** "Prazo perdido" para os dois, até o encerramento.

**Pendente (pendência 2):** o critério exato de "compromete a submissão". Proposta ainda não aprovada:
- o prazo do projeto da Mobilizando recalculado para depois da véspera da submissão; ou
- qualquer entrega do cliente atrasada a 3 dias ou menos da submissão.

---

## 12. O que cada lado vê

### 12.1 Cliente (celular primeiro)

Início **"O que é seu agora?"**, uma leitura por edital:

| Pergunta | Exemplo |
|---|---|
| Onde estamos? | Etapa 5. Elaboramos o projeto |
| De quem é a vez? | Agora é com a Mobilizando |
| O que preciso fazer? | Nada neste momento |
| Qual a próxima referência? | O projeto chega para a sua aprovação até ter, 29/09, dentro do prazo |
| Prazo crítico | Submissão até sex, 02/10 (D-3) |

Com item do cliente aberto: um cartão grande com **o item que vem primeiro pela prioridade do Farol (seção 4.7)**, com o botão **Fazer agora**, que abre a etapa já expandida. Os demais itens do cliente aparecem logo abaixo, sem esconder nenhum. Detalhe da tela na arquitetura 2.3.

### 12.2 Administradora

Tela inicial "Prazos da carteira": **o que precisa da minha atenção hoje**. Cada linha com organização, edital, etapa da jornada, de quem é a vez, item, data, D-n e nível do Farol.

Blocos:
- atrasados dos dois lados;
- vence hoje;
- vence amanhã;
- próximos 7 dias;
- prazo perdido;
- decisões abertas: encerrar, seguir ou encerrar, responder dúvida do OK;
- ideias recebidas e complementos respondidos;
- documentos aguardando conferência;
- resultado previsto não registrado;
- recurso e pós-aprovação.

Detalhe na arquitetura 2.2.

## 13. Histórico

O histórico é a memória operacional. É **escrito só pelo banco** (pacote 3), sem como forjar, e **nunca editado nem apagado** (em vigor desde o pacote 2).

Eventos que ficam registrados:
- edital aberto, editado, movido, apagado, restaurado ou apagado de vez;
- dossiê informado;
- OK respondido, e mudança de resposta;
- documento acrescentado, marcado como obrigatório ou facultativo, enviado, conferido ou recusado;
- ideia enviada, com a forma usada;
- complemento pedido e respondido;
- pergunta e resposta;
- projeto enviado;
- aprovação ou pedido de ajustes;
- revisão enviada;
- **submissão registrada e, quando houver, a confirmação com pendências**: quais eram, quem confirmou, data e hora, e a justificativa;
- protocolo;
- encerramento com motivo;
- resultado, prazos de recurso e pós-aprovação;
- nome da organização corrigido (em vigor desde 14/09);
- e-mails enviados, quando ligados.

**Regra geral do registro:** nenhuma ação sem mudança real gera linha (decisão 16, estendida a todos os eventos pela especificação do pacote 3).

**Pendente (pendência 7):** "cliente visualizou", a abertura do dossiê ou do projeto. É escopo novo e exige guardar leitura por pessoa. **Não é necessária antes do pacote 3** (decisão 17): se for adotado, o evento é criado no pacote que implementar esse dado.

## 14. Documentos (decisão 9)

**Cada linha da lista tem:**
- documento;
- onde o edital pede;
- **obrigatório ou facultativo**, conforme a letra do edital;
- situação.

**Situações:** pendente, enviado, conferido e recusado com motivo. São as da arquitetura 2.9, sem situação nova.

**Pendente, para todo efeito deste mapa, é:**
- não enviado;
- enviado e ainda não conferido;
- recusado.

Qualquer outra situação é decisão futura, registrada antes de existir.

**Efeitos**
- Só **documento obrigatório pendente** aciona o bloqueio com confirmação do registro da submissão (seção 9.2).
- Documento pendente de qualquer tipo continua visível para os dois lados, com a situação real.
- **Decisões futuras, do pacote de documentos:**
  - se documento facultativo pendente aparece como item do cliente no Farol;
  - se a entrega "Documentos extras" fica em dia com todas as linhas conferidas (como diz a arquitetura 2.5) ou só com as obrigatórias.

**Como já está na arquitetura 2.9:**
- dois caminhos de envio: anexo privado no portal, com versões, e pasta do Drive por link manual;
- conferência com recusa e motivo;
- "Baixar tudo deste edital";
- o cliente nunca apaga arquivo;
- a leitura do que falta é feita pela AMC IA fora do portal, só lendo a pasta do cliente.

A infraestrutura de armazenamento é a mesma questão aberta da forma C (seção 7.2), tratada no pacote correspondente.

## 15. Notificações

- Nascem de **eventos operacionais**, nunca de mensagem solta.
- No portal, pelo sino e pela central de alertas.
- Por e-mail, nos pacotes 12 e 13 (decisão 4), começando desligado e passando por modo teste.
- Quadro "Quem recebe o quê" na arquitetura 2.4.

Eventos novos trazidos por este mapa:
- complemento solicitado, para o cliente;
- complemento respondido, para a administradora;
- decisão de atraso aberta, para os dois;
- submissão registrada com pendências confirmadas, para a administradora, no histórico.

## 16. Simplicidade

- O cliente não vê arquitetura técnica, agentes, ferramentas de IA, metodologia interna nem operação da Mobilizando.
- Recebe **o que aconteceu, o que precisa fazer, o prazo e o resultado**.
- Vê o prazo real da Mobilizando (seção 4.5). Simplicidade não é esconder atraso.

## 17. Cruzamento com o documento-base

| Documento "Como trabalhamos juntos" | Portal |
|---|---|
| Etapa 1. Encontramos o edital | Edital aberto pela administradora |
| Etapa 2. Dossiê do Edital | Data do dossiê; dossiê no portal pendente |
| Etapa 3. OK e documentos extras | OK com três respostas; lista com obrigatório e facultativo e conferência, em paralelo |
| Etapa 4. Esboço, objeto ou ideia | Ideia do Projeto, formas A, B e C, com complementação |
| Etapa 5. Elaboramos o projeto | Projeto em elaboração, com prazo real, mesmo com documento pendente |
| Etapa 6. Aprovação ou ajustes | Aprovação com nome e cargo; ajustes e revisão |
| Etapa 7. Submissão | Registro da submissão com bloqueio com confirmação; comprovante pendente |
| Os quatro momentos do cliente | "O que é seu agora?" e o Farol |
| Calendário e três ritmos | Cálculo automático, nada digitado |
| Se uma entrega atrasar | Farol mais decisão (seção 11.3) |
| Datas deste edital | Linha do tempo do edital |
| Roteiro do esboço | Forma B da Ideia do Projeto; forma A entra no documento (seção 7.5) |

## 18. Escopo da v1.0

**Dentro:** pacotes 3 a 13 da arquitetura, com o Farol e o escopo novo aprovado (seção 19) encaixados neles na revisão da arquitetura.

**Fora (integrações futuras, pacote 14 ou decisão nova):**
- integração automática com o CaptaHub;
- a AMC IA gravando direto no portal;
- WhatsApp;
- cópia automática dos anexos para o `G:` (esbarra na regra "nada roda sozinho");
- inteligência artificial dentro do portal;
- papel de equipe;
- armazenamento provisório de arquivos (decisão 5).

## 19. Escopo novo trazido por este mapa

Nada disto está nos pacotes da arquitetura de 13/09. O encaixe em pacote e a conta de crédito saem da revisão da arquitetura.

| Item | Situação |
|---|---|
| Farol: leitura, prioridade, níveis e cores (seção 4) | decidido; frases pendentes (pendência 1) |
| Etapa da jornada pela primeira etapa não concluída (seção 5.2) | aprovado (decisão 15) |
| Entregas paralelas sem fila rígida (seção 5.3) | decidido |
| Ideia do Projeto, formas A e B | decidido |
| Ideia do Projeto, forma C desde o início | decidido; armazenamento no pacote correspondente |
| Complementação da ideia (seção 7.4) | decidido |
| Obrigatório ou facultativo por documento (seção 14) | decidido |
| Registro da submissão com bloqueio com confirmação (seção 9.2) | decidido |
| Decisão de atraso (seção 11.3) | critério pendente (pendência 2) |
| Dossiê no portal | pendente (pendência 4) |
| Versões do projeto e versão aprovada | decidido em 14/09 (decisões 25 a 32) |
| Comprovante anexado | decidido em 14/09: arquivo, link ou os dois (decisão 33) |
| "Cliente visualizou" | pendente (pendência 7) |

## 20. Critérios de aceite do mapa

| Pergunta | Situação |
|---|---|
| Sabemos todas as etapas? | Sim: 7, do documento-base |
| Quem é responsável por cada ação? | Sim: seções 3, 5.3 e 6 |
| Quando a responsabilidade passa de um lado para o outro? | Sim: seções 5.3, 7.4 e o Farol |
| Quais são os estados? | Sim: situação, etapa e entregas (seção 5) |
| O que o cliente vê? | Sim: seção 12.1 e arquitetura 2.3 |
| O que a administradora vê? | Sim: seção 12.2 e arquitetura 2.2 |
| Quais ações ficam registradas? | Sim, menos "cliente visualizou" |
| Como os prazos são calculados? | Sim: seção 11.1, motor já conferido |
| O que acontece quando há atraso? | Em parte: falta o critério de "compromete a submissão" |
| Como funciona a Ideia do Projeto? | Sim, incluindo a complementação; o armazenamento da forma C fica no pacote |
| Como o Farol acompanha o processo? | Sim, menos as frases |
| Quais documentos entram? | Em parte: faltam dossiê, projeto e comprovante |
| Como funciona a aprovação? | Sim, menos as versões |
| Como funciona a submissão? | Sim, com bloqueio com confirmação; comprovante pendente |
| O que acontece depois da submissão? | Sim: seção 10 |
| O que é automático e o que é manual? | Sim. Automáticos: cálculo, etapa, Farol e registro. Manuais: decisões, conferência, complemento, confirmação, encerramento e resultado |
| O que já existe no portal? | Sim: arquitetura, diagnóstico, e pacotes 1 e 2 |
| O que precisa ser alterado? | Sim: os 17 defeitos e as seções 5 a 9 e 14 |
| O que será novo? | Sim: seção 19 |
| Temos critérios de teste? | Sim, por pacote na arquitetura; os itens da seção 19 ganham os deles na revisão |

## 21. Caminho até a implementação

```text
MAPA OPERACIONAL v1.0 (este documento, fonte da verdade)
        ↓
REVISÃO DA ARQUITETURA (docs/portal-clientes-arquitetura.md)
absorve a seção 2.11 no corpo do plano, encaixa o escopo novo
em pacotes e refaz a conta de créditos
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

**Quem faz o quê:**
- o Lovable implementa;
- a AMC IA escreve o pacote, confere o resultado e registra;
- a captadora aprova cada envio e faz o teste na tela.

## 22. Pendências

### 22.1 Decidir antes do pacote 7 e da conta final de créditos

Nenhuma pendência do mapa é necessária antes do pacote 3.

| Pendência | Por que antes do pacote 7 |
|---|---|
| 4. Dossiê no portal: arquivo, link ou fora | define o tamanho do pacote de documentos |
| ~~5. Versões do projeto: no portal ou só o registro~~ | **encerrada em 14/09:** no portal, em versões (decisões 25 a 32) |
| ~~6. Comprovante: arquivo, link ou só o protocolo~~ | **encerrada em 14/09:** arquivo, link ou os dois (decisão 33) |

### 22.2 Decidir durante os pacotes respectivos

| Pendência | Quando |
|---|---|
| 1. Frases do Farol | pacotes 8 e 9 |
| 2. Critério de "atraso que compromete a submissão" | pacote de encerramentos e prazo |
| 7. "Cliente visualizou" no histórico | no pacote que implementar esse dado, se for adotado (decisão 17) |
| 8. Atualizar "Como trabalhamos juntos" | antes de a nova tela da Ideia do Projeto chegar ao cliente (decisão 14) |

### Encerradas

| Pendência | Como |
|---|---|
| 3. Complementação da ideia | decisão 6: sim |
| 9. Tabela de conclusão das etapas | decisão 15: aprovada |

### 22.3 Decisões futuras registradas nesta revisão, cada uma no seu pacote

| Decisão futura | Seção | Pacote |
|---|---|---|
| Armazenamento seguro de arquivos (onde, quem vê, tipos, tamanho, versões, Privacidade) | 7.2 e 14 | documentos |
| O que a forma C oferece enquanto o anexo não existe | 7.2 | Ideia do Projeto |
| Mínimo exigido para enviar a ideia | 7.2 | Ideia do Projeto |
| Prazo próprio do complemento, e se pode haver mais de um aberto | 7.4 | Ideia do Projeto |
| "Tenho dúvidas": quem responde, por onde, e de quem é a vez | 6, etapa 3 | Ideia ou pessoas e convites |
| Ideia enviada antes do OK: permitir ou não | 5.3 | Ideia do Projeto |
| Registro da submissão sem aprovação: pedir confirmação ou não | 5.3 e 9.2 | encerramentos e prazo |
| Justificativa obrigatória na confirmação | 9.2 | encerramentos e prazo |
| Facultativo pendente como item do cliente no Farol | 14 | documentos |
| Entrega de documentos em dia com todas as linhas ou só as obrigatórias | 14 | documentos |
| Diferença prática entre as prioridades 2 e 5, conteúdo da prioridade 1, e ordem dentro dos blocos da administradora | 4.7 | Farol (8 e 9) |
| Marco de "dossiê enviado" separado da data prevista | 5.2 | a definir na revisão |

## 23. Histórico de revisões do mapa

| Data | O que mudou |
|---|---|
| 14/09/2026 | Criação, com as decisões 1 a 4 |
| 14/09/2026, revisão | Decisões 5 a 14. Correções A a K da revisão da AMC IA: A, "Tenho dúvidas" sem inferência de vez; B, forma C desde o início; C, sem "ao menos uma resposta"; D, cores de "em N dias" e "a calcular"; E e F, prioridade do Farol; G, situação sem cor própria; H, I e J, bloqueio com confirmação só para documento obrigatório pendente e só no registro da submissão; K, etapa pela primeira etapa não concluída, sem a contradição entre 4 e 5 e sem a exigência de OK antes dos documentos. Também saiu a exigência de aprovação como condição dura para registrar a submissão, que não tinha base (arquitetura 2.4 só mostra "aguardando aprovação") |
| 14/09/2026, terceira rodada | Decisões 15 a 17: regra da etapa aprovada (pendência 9 encerrada); registro da Ideia só com mudança real; "cliente visualizou" fora da lista de antes do pacote 3. A seção 22 foi reorganizada |
