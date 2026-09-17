# Portal do Cliente Mobilizando. Arquitetura e plano de execução

> **Consolidada em 14/09/2026 com o Mapa Operacional v1.0.**
>
> **Hierarquia das fontes**
> 1. `marketing/entregas/comercial/como-trabalhamos-juntos.md`: jornada, responsabilidades e prazos.
> 2. `docs/portal-clientes-mapa-operacional-v1.md`: **fonte da verdade da operação**. Onde esta arquitetura e o mapa divergirem, vale o mapa.
> 3. **Este plano:** como o mapa vira telas, dados, segurança e pacotes.
> 4. `docs/portal-clientes-pacote-*.md` e afins: a instrução de cada pacote enviado ao Lovable.
>
> **Histórico deste documento**
> - **13/09/2026:** criação, com as 12 decisões da captadora (seção 4), a regra "nenhum prazo mascarado", encerramentos, painel de resultados, alertas do resultado e documentos.
> - **14/09/2026:** pacotes 1 e 2 aplicados; nome da organização editável aplicado.
> - **14/09/2026, consolidação:** entraram as 14 decisões do Mapa Operacional e a aprovação da regra da etapa da jornada (mapa, seção 5.2). Mudaram as seções 1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.9, 2.10, 3, 4, 5, 6 e 7. Foram criadas as seções 2.11, 2.12 e 2.13 e o pacote 7B.
> - **14/09/2026, noite:**
>   - pacotes 3 e 4 concluídos e publicados (o site publicado foi conferido);
>   - PDF do edital aplicado, publicado e testado na tela (`docs/portal-clientes-pdf-do-edital.md`);
>   - painel em branco depois de entrar corrigido, publicado e testado (`docs/portal-clientes-correcao-login.md`).
>
> **Implementado até agora:** pacotes 1 a 4, nome da organização, PDF do edital e correção do login. O resto deste plano não foi implementado.

## Contexto

O portal foi construído no Lovable em três rodadas (12 e 13/09/2026, cerca de 12,6 créditos), a partir de `docs/portal-clientes-especificacao.md`. A conta da captadora é a única administradora. Em 14/09, o banco tinha 8 organizações, 1 convite pendente e nenhum edital.

A captadora pediu uma arquitetura melhor, com:
- visão da administradora e visão do cliente bem separadas;
- funcionalidades próprias para cada lado;
- **alertas de todos os prazos dos dois lados, sem mascarar prazo para ninguém**;
- controle de resultados e dos documentos pendentes.

Em 14/09 ela acrescentou o Mapa Operacional. O portal passa a ser o sistema operacional da jornada, com o **Farol** respondendo, a qualquer momento, em que etapa estamos, de quem é a vez, o que precisa ser feito, qual é o prazo e se há risco ou impedimento.

A auditoria de 13/09 foi feita só com leitura: código pelo `read_file`, banco por SELECT em `pg_policies`, `pg_trigger` e `information_schema`. Ela achou 17 defeitos e confirmou que **`pg_cron` e `pg_net` estão disponíveis** no Lovable Cloud, ainda não instalados.

---

## 1. Diagnóstico

**Funciona e fica como está**
- O motor de prazos (`src/lib/prazos.ts`) foi conferido contra o exemplo de 05/10/2026. Nenhuma data calculada é gravada.
- `src/lib/agenda.ts` cruza prazo com marcação e é a base do motor de alertas e do Farol.
- O isolamento por organização vale no banco, com as travas do cliente e do edital finalizado ou apagado.
- Apagados com Restaurar, a página pública e o PDF pela impressão.
- **Desde o pacote 2:** duas camadas de proteção, autor e datas definidos pelo banco, registro que sobrevive ao "apagar de vez" e convite pelo e-mail exato.

**Ainda frágil**
- **O registro ainda é escrito pela tela.** A chamada `registrar()` fica em `src/lib/dados.ts` e é usada em 15 lugares de três arquivos: 13 em `edital.tsx`, 1 em `painel.tsx` e 1 em `apagados.tsx`. Ela não confere erro: se a gravação falhar, a ação acontece e o registro some em silêncio. E o cliente ainda pode inserir linha no registro.
- **Registro repetido:** cada vez que a resposta é salva, uma linha nova entra no registro.
- **O cliente apaga a marcação** direto na tabela.
- **Buracos de fluxo:** hora da submissão anda 3h a cada salvamento; edital muda de organização com um clique; não há como voltar ao ritmo sugerido.
- **Alertas, Farol e e-mails não existem.** As chaves de notificação são gravadas, mas nada as lê.

**Os 17 defeitos, com a situação em 14/09**

| Nº | Defeito | Situação |
|---|---|---|
| 1 | Autor da pergunta forjável | corrigido no pacote 2 |
| 2 | Registro escrito pela tela e forjável | corrigido no pacote 3 |
| 3 | Datas de feito e de envio forjáveis | corrigido no pacote 2 |
| 4 | "Apagar de vez" apaga o registro e não se registra | corrigido no pacote 2 |
| 5 | Cliente apaga marcação | corrigido no pacote 3 |
| 6 | Convite frágil | parcial: e-mail exato no pacote 2; estado "sem acesso" no pacote 5. **Achado em 14/09:** quem cria conta antes do convite fica cliente sem organização, e o convite feito depois é ignorado |
| 7 | Permissões de tabela totais | corrigido no pacote 2 |
| 8 | Troca de organização com um clique | corrigido no pacote 4 |
| 9 | Hora da submissão +3h | corrigido no pacote 3, etapa 1 (14/09), por decisão da captadora; falta o teste na tela |
| 10 | Sem "voltar ao sugerido" | corrigido no pacote 4 |
| 11 | Finalizados fora do painel | corrigido no pacote 1 (falta o teste na tela) |
| 12 | Atalho não abre a etapa | corrigido no pacote 4 |
| 13 | O outro lado só vê a mudança ao recarregar | pacote 9 |
| 14 | Registro repetido a cada salvamento do esboço | corrigido no pacote 3 |
| 15 | Nome, órgão, link e linha de documento não editáveis | corrigido no pacote 4 (o nome da **organização** ficou editável em 14/09) |
| 16 | Erro técnico cru para quem não tem acesso | corrigido no pacote 4 |
| 17 | Configurações órfãs, sem chave estrangeira | corrigido no pacote 2 |

---

## 2. Arquitetura

### 2.1 Papéis

| Papel | Decisão |
|---|---|
| **Administradora** | Poder total. É a captadora. |
| **Cliente** | Todas as pessoas da organização veem e escrevem igual, e todas recebem e-mail, cada uma podendo se descadastrar. |
| **Sem acesso** (novo) | Criou conta sem convite: vê "Aguardando liberação da Mobilizando" e nenhum dado. |
| **Equipe** | Fica para depois. O banco já aceita o papel, sem tela. |

### 2.2 Visão da administradora

1. **Painel "Prazos da carteira"** (tela inicial): **o que precisa da minha atenção hoje** (mapa, 12.2).
   - Blocos:
     - atrasados, do cliente e da Mobilizando;
     - vence hoje;
     - vence amanhã;
     - próximos 7 dias;
     - prazo perdido;
     - **decisões abertas:** encerrar, seguir ou encerrar, responder dúvida do OK;
     - **ideias recebidas e complementos respondidos;**
     - documentos enviados aguardando conferência;
     - resultado previsto e ainda não registrado;
     - prazos de recurso e pós-aprovação;
     - pendências de cadastro.
   - Cada linha: organização, edital, **etapa da jornada**, **de quem é a vez**, item, data, D-n, nível do Farol e link direto.
   - Filtros: organização, "só minhas entregas" e "só do cliente".
   - A ordem dentro dos blocos é decidida no pacote 8 (mapa, 4.7).
2. **Resultados da carteira:** o painel de resultados (2.7) somando todas as organizações, com a opção de abrir organização por organização.
3. **Organizações:** ficha de cada uma, com nome editável (**em vigor desde 14/09**), pessoas, editais em andamento, painel de resultados da organização e chaves de notificação.
4. **Pessoas**
   - Convites pendentes, com reenviar e cancelar.
   - Pessoas sem acesso, com atribuir organização.
   - Mover pessoa entre organizações e retirar acesso, sempre com registro.
5. **Editais:** abas Em andamento, Encerrados (aguardando resultado primeiro) e Apagados, com busca.
6. **Página do edital: o que só ela faz**
   - Editar nome, órgão, link, dia D, dossiê e ritmo, com "Voltar ao sugerido".
   - Informar o link da pasta do Drive do edital.
   - Colar e editar a lista de documentos, **marcando cada linha como obrigatória ou facultativa**, e conferir ou recusar cada envio.
   - **Analisar a ideia e pedir complemento**, escrito como pergunta específica (2.12).
   - Marcar o projeto com data informável (as duas datas ficam no registro).
   - **Registrar a submissão** com protocolo e a hora certa, com **bloqueio com confirmação** quando há documento obrigatório pendente (2.13).
   - Mover de organização, só quando o cliente ainda não mexeu.
   - Encerrar (2.6), marcar resultado com data e confirmação, e informar data prevista do resultado, prazo de recurso e prazo pós-aprovação.
   - Apagar.
   - Bloco "E-mails deste edital": enviados, falhas e prévia do que sairia amanhã.
7. **Central de alertas** e sino com número no topo, mais "Novidades desde a sua última visita".
8. **Configurações:** chaves por escopo, modo de envio (desligado, teste, ligado), histórico de e-mails e Exportar tudo.
9. **Apagados** como hoje, com o registro protegido.

### 2.3 Visão do cliente (celular primeiro)

1. **Início "O que é seu agora?"** (mapa, 4.4 e 12.1)
   - **Com item do cliente aberto:** um cartão grande com o item que vem primeiro pela **prioridade do Farol** (2.4), com o botão **Fazer agora**, que abre a etapa já expandida. Os demais itens dele aparecem logo abaixo, sem esconder nenhum.
   - **Sem item do cliente: "Agora é com a Mobilizando"**, sempre com a situação e a data real da próxima referência. Exemplo: "Projeto previsto para ter, 29/09, atrasado há 2 dias", na mesma cor dos atrasos do cliente.
   - Para cada edital: onde estamos (etapa da jornada), de quem é a vez, o que preciso fazer, a próxima referência e o prazo crítico.
   - Depois, os editais em andamento e o atalho para Resultados.
2. **Página do edital simplificada**, nesta ordem:
   - contador;
   - o que é seu agora;
   - as entregas dele;
   - **pedido de complemento aberto, com a pergunta e o campo de resposta**;
   - documentos pendentes, com obrigatório ou facultativo e os dois jeitos de enviar;
   - as etapas (as dele abertas, as da Mobilizando resumidas, mas com prazo e situação visíveis);
   - "Falar com a Mobilizando";
   - o registro.

   A tabela de ritmos e as notas ficam num bloco fechado, "Como os prazos foram calculados".
3. **Ideia do Projeto** na etapa 4, com as formas A, B e C (2.12).
4. **Resultados:** o painel de resultados da organização (2.7) e o histórico dos editais encerrados.
5. **Central de alertas** e sino: as entregas dele por nível, documentos recusados, complementos pedidos, prazos de recurso e pós-aprovação, e as novidades da Mobilizando, inclusive o resultado.
6. **Minha conta:** nome editável, preferências de e-mail, contato da Mobilizando e privacidade.
7. **Descadastro** por link do e-mail, aberto e sem login, com token aleatório.
8. **Nunca apaga nada.** "Desfazer marcação" existe, passa pelo banco e fica no registro. Arquivo enviado errado se corrige com um novo envio, que vira nova versão.

### 2.4 Alertas e Farol dos dois lados

**Motor único.** Arquivo novo `src/lib/alertas.ts`, que só usa `prazosDoEdital`, `feitosDoEdital` e `situacaoDoPrazo`. Nenhuma data gravada e nenhuma lista nova de feriados. Funções: `alertasDoEdital()` e `alertasDaCarteira()`.

**Farol** (mapa, seção 4). É a camada de leitura sobre o motor. Não é etapa, não é segundo motor e não cria nível nem cor.

O Farol lê:
- etapa da jornada (2.11);
- entregas abertas;
- responsável;
- prazo e nível;
- documentos obrigatórios e facultativos;
- complementos;
- situação do edital;
- riscos e atrasos.

**Níveis e cores, iguais para os dois lados**

| Nível | Cor |
|---|---|
| Feito | verde |
| A calcular | sem cor |
| Em N dias | neutro |
| Em 3 dias, em 2 dias, vence amanhã, vence hoje | dourado |
| Atrasado há N dias | vermelho |
| Prazo perdido (dia D passou sem submissão) | vermelho |

Situações sem nível próprio (decisão aberta, registro de submissão com pendência, complemento pedido, documento recusado) não têm cor própria: usam a cor do prazo do item a que se referem. Sem prazo, ficam sem cor.

**Prioridade do Farol** (mapa, 4.7). O que aparece primeiro:
1. Bloqueio ou risco crítico que exige decisão.
2. Pendência do cliente que exige ação.
3. Pendência recusada ou complemento solicitado.
4. Prazo mais próximo.
5. Próxima ação normal.
6. Nenhuma ação do cliente: "Agora é com a Mobilizando".

Empate: a data mais próxima. A prioridade só ordena; nada fica escondido (2.5).

**Espera: quando cada alerta começa a valer.** A situação de todos os itens continua visível para os dois lados.

| Item | De quem | Vira alerta quando | Enquanto espera, mostra |
|---|---|---|---|
| OK | cliente | o dossiê foi informado | "a calcular" |
| Documentos extras | cliente | a lista tem linhas; **não depende do OK nem da ideia** | nada |
| Ideia do Projeto | cliente | sempre; **não depende da documentação** | nada |
| Complemento | cliente | a Mobilizando pediu | nada |
| Projeto | Mobilizando | sempre; **a elaboração segue com documentação pendente** | "com pendência do cliente" se a ideia, um complemento ou os documentos estão atrasados, sem tirar o atraso da Mobilizando da tela |
| Aprovação | cliente | o projeto foi marcado | "Aguardando o projeto da Mobilizando", com a data prevista e o atraso dela, se houver |
| Submissão | Mobilizando | sempre | "aguardando aprovação" se ela não veio; no registro, bloqueio com confirmação se há documento obrigatório pendente (2.13) |
| Resultado previsto | administradora | a data foi informada | nada |
| Recurso | os dois | resultado reprovado com prazo informado | nada |
| Pós-aprovação | os dois | resultado aprovado com prazo informado | nada |

**Quem recebe o quê**

| Item | No portal (sem custo e sem DNS) | Por e-mail (pacote 13, autorizado pela captadora) |
|---|---|---|
| 4 entregas do cliente | Cliente: sino e início. Administradora: painel | 3 dias antes, no dia e a cada 2 dias no atraso (máximo 5), cópia para a administradora, um e-mail por dia por edital, nada depois do dia D, dia útil às 8h |
| 2 entregas da Mobilizando | Os dois, com prazo e atraso reais | Administradora, na "Agenda de hoje" às 8h, em dia com vencimento ou atraso |
| Resultado previsto | Os dois veem a data; depois dela, "ainda não registrado" | Administradora, na Agenda de hoje, no dia e a cada 2 dias depois, até registrar |
| Prazo de recurso | Os dois | Organização e administradora: 3 dias antes e no dia |
| Prazo pós-aprovação | Os dois | Organização com cópia para a administradora: 3 dias antes, no dia e a cada 2 dias no atraso (máximo 5) |
| Eventos do cliente: 1 OK dado, 2 ideia enviada, 3 todos os documentos enviados, 4 aprovação respondida, **12 complemento respondido** | Novidades da administradora | Aviso na hora para a administradora |
| Eventos da Mobilizando: 5 edital novo, 6 documentos acrescentados, 7 projeto enviado, 8 submissão, 9 resultado registrado, 10 documento recusado, **11 complemento solicitado** | Novidades do cliente | Aviso na hora para a organização; o evento 6 espera 30 min para juntar |
| Decisão de atraso aberta | Os dois, no Farol | a decidir no pacote 12 |
| Submissão registrada com pendências confirmadas | Histórico e Novidades da administradora | não se aplica |
| Resumo diário | Não se aplica | 18h, dia útil, só para a administradora, pula dia sem atividade e não repete aviso já enviado |

O prazo de recurso e o pós-aprovação acontecem **depois** do dia D e são exceção explícita à regra "nada depois do dia D".

**Guarda e controle de repetição**
- Tabela `envios_email`, que nunca é apagada.
- Único por (edital, dia) para lembrete, e único por dia para o resumo e a agenda.
- Contagem de avisos de atraso.
- `registro.avisado_na_hora`, para o resumo não repetir.
- Tabela `preferencias_email` por pessoa, com token de descadastro.
- `envio_modo` nasce **desligado**. No modo teste, tudo vai só para a captadora, com "[TESTE]" no assunto.

**Agendamento**
- `pg_cron` com `pg_net` chamando uma função do Lovable Cloud: 8h (`0 11 * * 1-5` UTC) e 18h (`0 21 * * 1-5` UTC).
- Os avisos na hora saem por gatilho no banco, sem cron.
- A função confere feriado com uma cópia literal de `prazos.ts`, testada contra o exemplo de 05/10/2026.
- **Nenhum job é criado antes do pacote 13**, do DNS e do modo teste. Até lá, os alertas existem só quando alguém abre a tela.

### 2.5 Nenhum prazo mascarado (regra da captadora, 13/09)

1. Todo prazo, de qualquer lado, aparece **para os dois lados** com a data real e a situação real. Atraso da Mobilizando aparece para o cliente como atraso, na mesma cor dos atrasos dele.
2. Prazo recalculado mostra as duas datas e o motivo. Exemplo da aprovação depois de projeto atrasado: "prevista para 01/10, recalculada para 03/10 porque o projeto saiu em 01/10". O recálculo nunca passa da véspera da submissão.
3. Marcação com data informada mostra as duas datas: "enviado em 13/09, marcado em 14/09".
4. Dia D sem submissão aparece para os dois como **Prazo perdido**, calculado na leitura, até o edital ser encerrado.
5. Documento enviado e depois recusado não conta como cumprido. A entrega de documentos fica em dia quando as linhas estão conferidas, e a data de cumprimento é a do envio aceito. **Se isso vale para todas as linhas ou só para as obrigatórias é decisão do pacote 7** (mapa, 14).
6. Nenhum filtro, estado ou texto esconde atraso ou prazo perdido de nenhum lado.
7. **A prioridade do Farol só ordena** o que aparece primeiro. Ela não esconde nada.
8. **O pedido de complemento não para nem recalcula em silêncio o prazo do projeto.** Se ele afetar o projeto, o recálculo mostra as duas datas e o motivo.

### 2.6 Encerramentos e desistência

**Situações de um edital**

| Situação | Quando | Quem define |
|---|---|---|
| Em andamento | desde a abertura | automático |
| Submetido, aguardando resultado | submissão registrada e edital encerrado | administradora |
| Aprovado, com data | resultado publicado | administradora, com confirmação |
| Reprovado, com data | resultado publicado | administradora, com confirmação |
| Não submetido, com motivo obrigatório | encerrado sem submissão | administradora |
| Apagado | só erro de cadastro; não entra em nenhuma conta | administradora |

**Motivos de não submissão:**
- desistência do cliente;
- não recomendado pela Mobilizando;
- inelegível;
- prazo perdido.

No prazo perdido, o portal grava **de quem eram as pendências atrasadas no dia D** (cliente, Mobilizando ou os dois), calculado pelas entregas, sem campo livre para mascarar.

**Caminho da desistência**
1. O cliente responde "Não vamos entrar neste edital".
2. Os lembretes do cliente naquele edital param na hora.
3. A administradora recebe o alerta "Decidir: encerrar edital", no portal e por e-mail na hora (evento 1). É prioridade 1 do Farol.
4. Ela encerra como "Não submetido: desistência do cliente". **O portal não encerra sozinho.**
5. O edital sai de "Em andamento", vai para o histórico **dos dois lados** e entra na contagem do painel de resultados.

**"Tenho dúvidas antes de decidir":** fica registrado, não conclui a etapa 3 e mantém o prazo do OK visível. Quem responde, por onde e de quem é a vez é **decisão futura** (mapa, 22.3).

**Atraso que compromete a submissão** (mapa, 11.3):
- o Farol abre "Decidir: seguir ou encerrar" para a administradora e "Vamos decidir juntos" para o cliente, com prioridade 1;
- seguir gera recálculo com as duas datas;
- deixar para o próximo encerra como "Não submetido".

O critério de "compromete" é a pendência 2 do mapa, decidida no pacote 6.

### 2.7 Painel de resultados

**Quem vê:** o cliente vê o da organização dele. A administradora vê o de cada organização e o da carteira inteira.

**Números, todos clicáveis para abrir a lista:**
- Propostos: todos os editais abertos, menos apagados.
- Em andamento.
- Submetidos.
- Aguardando resultado.
- Aprovados.
- Reprovados.
- Não submetidos, com a divisão por motivo.
- Prazos perdidos, com a divisão cliente, Mobilizando ou os dois.

**Taxa de aprovação:** aprovados divididos por aprovados mais reprovados, sempre com o número bruto ao lado ("3 de 5, 60%").

**Filtro por ano**, pelo ano do dia D.

**Sem valores em reais:** valor aprovado e carteira continuam no CaptaHub. O portal conta só os editais trabalhados nele, e o painel diz isso numa linha.

### 2.8 Alertas do resultado e do que vem depois

Campos novos no edital, preenchidos pela administradora:
- data prevista do resultado, tirada do cronograma do edital;
- prazo de recurso, quando reprovado;
- prazo e descrição dos documentos pós-aprovação (contratação ou assinatura do termo), quando aprovado.

Os alertas estão na tabela "Quem recebe o quê" (2.4). O resultado registrado vira o evento 9: o cliente sabe na hora, pelo portal e por e-mail.

### 2.9 Documentos: leitura, entrega e conferência

1. **Leitura pela AMC IA, fora do portal.**
   - Com o edital analisado, eu cruzo o que o edital exige com a pasta do cliente no `G:` (CaptaDoc e `/projeto-anexos`), inclusive a validade das certidões.
   - O resultado é a lista de pendentes, cada uma com **o item do edital de onde vem e se é obrigatória ou facultativa, conforme a letra do edital**.
   - **Só leitura:** nada é criado, renomeado ou movido na `06 - Clientes`.
2. **Lista no portal.**
   - A administradora usa "Colar lista": uma linha por documento, no formato `documento; onde o edital pede; obrigatório ou facultativo`.
   - Gravar a lista direto no banco a partir da AMC IA fica como opção futura, sempre com o OK dela a cada vez.
   - **A lista pode ser feita e enviada a qualquer momento: não depende do OK nem da ideia.**
3. **Situações de cada linha** (mapa, 14):
   - pendente, enviado, conferido, e recusado com motivo;
   - nenhuma outra situação sem decisão registrada antes.

   **Pendente, para todo efeito, é:**
   - não enviado;
   - enviado e ainda não conferido;
   - recusado.
4. **Entrega pelo cliente, com os dois caminhos em cada linha:**
   - **Anexar no portal**, em armazenamento privado do Lovable Cloud, visível só para a organização e a administradora. Cada novo envio vira nova versão, e o cliente não apaga versão.
   - **Pasta do Drive:** o edital mostra o link da pasta informado pela administradora. O cliente sobe o arquivo lá e marca "enviado pelo Drive".
5. **Armazenamento seguro** (mapa, decisão 5).
   - A infraestrutura ainda **precisa ser definida no pacote 7**: onde guardar, regra de acesso, tipos, tamanho, versões e atualização da Privacidade.
   - A proposta de 13/09 (PDF, JPG, PNG, DOC ou DOCX, até 10 MB) é ponto de partida, não decisão fechada.
   - **Não existe armazenamento provisório.**
   - Em 14/09 o portal tinha 0 espaços de armazenamento e 0 arquivos.
   - A forma C da Ideia do Projeto usa a mesma infraestrutura (2.12).
6. **Conferência:** cada linha passa por pendente, enviado, e depois conferido ou recusado com motivo (por exemplo, "certidão vencida em 02/09, envie a nova"). Recusado volta a pendente para o cliente, com aviso na hora (evento 10).
7. **Efeito na submissão:** só **documento obrigatório pendente** aciona o bloqueio com confirmação do registro da submissão (2.13).
8. **Levar para o Drive:**
   - os arquivos anexados no portal precisam chegar à pasta do edital;
   - no início, a administradora usa "Baixar tudo deste edital";
   - uma cópia automática da AMC IA para o `G:` fica fora da v1.0 (esbarra na regra "nada roda sozinho").

**Decisões futuras do pacote 7** (mapa, 22.3):
- se documento facultativo pendente aparece como item do cliente no Farol;
- se a entrega de documentos fica em dia com todas as linhas conferidas ou só com as obrigatórias.

**Impactos**
- A página de Privacidade passa a dizer que o portal guarda os arquivos enviados e quem os vê.
- O armazenamento consome a cota mensal de nuvem.
- A regra "só nome e e-mail" continua valendo para dado de pessoa. Os arquivos são documentos da organização.
- "Apagar de vez" um edital remove também os arquivos dele, e o registro guarda a lista do que foi removido.

### 2.10 Dados e segurança

| Mudança | Motivo | Pacote |
|---|---|---|
| ~~Revogar a permissão de `anon`; `authenticated` só com o necessário; sem TRUNCATE~~ | defeito 7 | **2, aplicado** |
| ~~Autor, nome e papel da pergunta definidos pelo banco~~ | defeito 1 | **2, aplicado** |
| ~~Autor e data da marcação definidos pelo banco~~; data informada guardada à parte | defeito 3, decisão 9 | autor e data: **2, aplicado**; data informada: 6 |
| Registro escrito só por gatilhos do banco; `registrar()` sai de `dados.ts`; o `authenticated` perde INSERT em `registro` | defeito 2 | 3 |
| Registro só com mudança real de conteúdo, escolha ou estado; salvamento idêntico não gera linha (mapa, decisão 16, aplicada a todos os eventos) | defeito 14 | 3 |
| ~~Registro sobrevive ao "apagar de vez" (SET NULL, com cópia do nome), travado contra edição e exclusão; "apagar de vez" exige o nome digitado e se registra~~ | defeito 4 | **2, aplicado** |
| Cliente sem DELETE em `marcos`; desfazer pela função `desmarcar_entrega`, com registro, só em andamento | defeito 5, decisão 3 | 3 |
| ~~Convite casa pelo e-mail exato~~; sem convite, sem papel; confirmação de e-mail ligada | defeito 6 | e-mail exato: **2, aplicado**; resto: 5 |
| Trava de mover edital com atividade do cliente, como gatilho `trava_mover_edital_com_atividade` por SQL direto (decisão de 14/09, no lugar da função `mover_edital`) | defeito 8, decisão 8 | 4 |
| ~~FKs em `config_notificacoes`; `editais.atualizado_em`~~ | defeito 17 | **2, aplicado** |
| ~~Nome da organização editável, com registro por gatilho~~ | pedido de 14/09 | **aplicado em 14/09** |
| `editais`: `desfecho`, `motivo_nao_submissao`, `pendencia_no_prazo_perdido`, `resultado_previsto_em`, `recurso_ate`, `pos_aprovacao_ate`, `pos_aprovacao_descricao`, `drive_link` | 2.6, 2.8, 2.9 | 6 e 7 |
| `marcos`: data informada e data da marcação separadas; aprovação com data recalculada visível | 2.5 | 6 |
| `documentos_extras`: `status`, `motivo_recusa`, `conferido_por`, `conferido_em`, `enviado_pelo_drive` e **`obrigatorio`** | 2.9, mapa 14 | 7 |
| Armazenamento privado com regra por organização, sem DELETE para cliente, e tabela de versões | 2.9 | 7 (infraestrutura a definir) |
| **Confirmação do registro da submissão:** quais pendências havia, quem confirmou, quando e a justificativa, gravados pelo banco e mostrados no histórico | 2.13, mapa 9.2 | 7 |
| **Ideia do Projeto:** a forma escolhida (A, B ou C), as 5 respostas da forma A, os 8 itens da forma B, e a referência ao material da forma C | 2.12, mapa 7.2 | 7B |
| **Pedidos de complemento:** a pergunta, quem pediu e quando, a resposta, quem respondeu e quando, e a situação (aberto ou respondido), gravados pelo banco | 2.12, mapa 7.4 | 7B |
| **Etapa da jornada:** nunca gravada; calculada na leitura pelos marcos de conclusão | 2.11 | 8 |
| `perfis.visto_ate`, `preferencias_email`, `envios_email`, `registro.avisado_na_hora` | alertas | 8 e 12 |

**Regras consolidadas**
1. Duas camadas de proteção: permissão mínima e regra de linha, inclusive no armazenamento de arquivos.
2. Autor, data e registro saem do servidor.
3. Registro e histórico de e-mail não se editam nem se apagam.
4. O cliente nunca tem DELETE, em tabela nem em arquivo.
5. Nenhum prazo mascarado (2.5).
6. Segredos do serviço de e-mail só nos segredos do Lovable Cloud.
7. Toda mensagem ao Lovable termina com "não altere regras de linha, permissões nem gatilhos fora do que foi pedido".
8. **Cada pacote que cria dado novo cria também o gatilho de registro desse dado.** O pacote 3 cobre só os eventos que já existem.
9. **Nenhuma entrega bloqueia outra.** O único bloqueio da v1.0 é o do registro da submissão, e ele é com confirmação (2.13).
10. **Etapa da jornada e Farol nunca são gravados:** são sempre calculados na leitura.
11. **Sem armazenamento provisório de arquivos.**

### 2.11 Jornada: etapa e entregas paralelas (mapa, seção 5)

**Três camadas, lidas juntas pelo Farol**
1. **Situação do edital** (2.6).
2. **Etapa da jornada:** uma das 7 etapas oficiais de "Como trabalhamos juntos".
3. **Entregas paralelas:** cada uma com prazo, situação e responsável próprios.

**Regra da etapa, aprovada pela captadora em 14/09/2026:** a etapa atual é a **primeira etapa ainda não concluída**, com um marco de conclusão definido para cada uma, **sem pular artificialmente etapas**. Não se usa "a última entrega feita".

| Etapa | Concluída quando |
|---|---|
| 1. Encontramos o edital | o edital é aberto no portal |
| 2. Dossiê do Edital | o dossiê é enviado, marcado pela data do dossiê informada |
| 3. OK e documentos extras | o cliente responde "Quero seguir com este edital" |
| 4. Esboço, objeto ou ideia | o cliente envia a Ideia do Projeto, por A, B ou C |
| 5. Elaboramos o projeto | a Mobilizando marca o projeto como enviado para aprovação |
| 6. Aprovação ou ajustes | o cliente responde "Aprovado, pode submeter" |
| 7. Submissão | a submissão é registrada |

**Consequências**
- Entrega adiantada não empurra a jornada. Ideia enviada antes do OK: a jornada fica na etapa 3; quando o OK vem, vai para a 5.
- Documentos extras não seguram a jornada; seguem como entrega paralela.
- Complemento não reabre a etapa 4.
- Ajustes pedidos mantêm a etapa 6.
- "Tenho dúvidas" e "Não vamos entrar" não concluem a etapa 3.

**Entregas paralelas, sem fila rígida** (mapa, decisão 7)

| Entrega | Responsável | Depende de |
|---|---|---|
| OK para seguir | cliente | dossiê enviado (o prazo conta dele) |
| Documentos extras | lista pela Mobilizando; envio pelo cliente | só de a lista ter linhas |
| Ideia do Projeto | cliente | nada |
| Resposta ao complemento | cliente | o pedido da Mobilizando |
| Projeto | Mobilizando | nada; segue com documentação pendente, quando operacionalmente possível |
| Aprovação | cliente | projeto enviado |
| Registro da submissão | administradora | nada; bloqueio com confirmação por documento obrigatório pendente |

**Onde fica o cálculo.** Uma função só, junto do motor de alertas, usada pelas duas visões e pelo Farol. O arquivo exato é definido no pacote 8.

**Ponto técnico para o pacote 8:** hoje a data do dossiê é pedida na abertura do edital. Se ela puder ser futura, o marco "dossiê enviado" precisa ser separado da data prevista.

### 2.12 Ideia do Projeto e complementação (mapa, seção 7)

**As três formas**, todas parte da experiência desde o início:
- **A. Ainda estou começando:** 5 perguntas.
  1. O que você quer fazer?
  2. Para quem?
  3. Onde?
  4. Por que isso é importante?
  5. O que você espera alcançar?
- **B. Já tenho um esboço:** os 8 itens do roteiro: o quê, para quem, onde, quando, como, com quem, quanto, o que já existe.
- **C. Já tenho um documento:** anexar projeto, PDF, Word ou outro material existente. Usa a infraestrutura segura de armazenamento do pacote 7 (2.9). Sem armazenamento provisório.

**Registro (decisão 16):**
- só gera linha quando há mudança real de conteúdo, escolha ou estado;
- salvar de novo o mesmo conteúdo não gera linha;
- espaço nas pontas não conta, e vazio vale o mesmo que em branco;
- a primeira gravação com conteúdo registra "Enviou o esboço, objeto ou ideia", e as seguintes, "Atualizou o esboço, objeto ou ideia", com os campos que mudaram;
- aplicado desde o pacote 3, sobre os 8 campos que já existem; as formas A e C entram na mesma regra no pacote 7B.

**O que já existe:** a etapa 4 do portal tem a escolha "Tenho um esboço pronto e vou enviar o arquivo" ou "Tenho só a ideia e respondo abaixo", mais os 8 campos (`src/lib/etapas.ts` e `CamposEsboco` em `edital.tsx`). O botão salva e registra a cada clique (defeito 14). **Não há anexo.**

**Ao enviar:**
- a entrega fica feita e a situação passa a "Ideia recebida";
- o banco registra quem enviou, quando e a forma;
- a etapa 4 fica concluída;
- a administradora vê "Nova ideia recebida" (evento 2).

**Complementação** (mapa, decisão 6)
1. A Mobilizando analisa a ideia.
2. Se falta informação, abre um pedido com **uma pergunta específica**.
3. A situação passa a "Aguardando informações do cliente".
4. O cliente responde.
5. A Mobilizando recebe, e a elaboração continua.

**Não é rejeição:** a ideia continua recebida e a etapa 4 não reabre. O pedido é pendência do cliente com prioridade 3 do Farol, e gera os eventos 11 e 12.

**Decisões futuras do pacote 7B** (mapa, 22.3):
- mínimo exigido para enviar a ideia;
- prazo próprio do complemento, e se pode haver mais de um aberto;
- ideia enviada antes do OK (a regra atual não impede).

**Condição antes de o cliente ver a nova tela:** "Como trabalhamos juntos" atualizado com a forma A e a forma B (mapa, 7.5), no `.md` e no `.html`.

### 2.13 Registro da submissão com bloqueio com confirmação (mapa, seção 9)

**A submissão real acontece no portal do financiador.** O Portal Mobilizando registra a submissão realizada.

**Quando vale:** ao tentar **registrar** a submissão, se existir documento **obrigatório** com situação diferente de "conferido".

**O que acontece:**
1. O portal lista os documentos obrigatórios pendentes, cada um com a situação.
2. Explica o motivo.
3. Permite a **confirmação explícita da administradora**, com justificativa.
4. O banco grava no histórico:
   - as pendências;
   - quem confirmou;
   - data e hora;
   - a justificativa.

**Sem pendência obrigatória:** registra sem confirmação extra.

**Não bloqueia:**
- envio da ideia;
- complementação;
- elaboração;
- aprovação;
- nenhuma outra entrega.

Documento facultativo pendente não aciona o bloqueio.

**Segurança:** só a administradora registra submissão e confirma. A confirmação e a justificativa são gravadas pelo banco, não pela tela.

**Decisões futuras** (mapa, 22.3):
- se a justificativa é obrigatória;
- se registrar a submissão sem aprovação também pede confirmação.

---

## 3. Execução em pacotes

Custo estimado dos pacotes 3 a 13: **44 a 53,5 créditos** pela soma da tabela abaixo (estimativas de 13/09 mais o escopo novo do mapa). **Com folga de cerca de 25%, planejar 55 a 67 créditos**, porque o pacote 1 custou o dobro do previsto e o pacote 2 gastou 1,1 crédito só para ler. Sem o pacote 13, que está bloqueado pelo domínio: 36 a 43,5 pela soma, e 45 a 55 com folga.

Cada pacote é uma mensagem ao Lovable, escrita antes como arquivo em `docs/` e enviada só com o OK da captadora. A conferência é sempre gratuita, por `read_file` e SELECT. Pacote grande é dividido em mensagens de até cerca de 3 créditos, para caber no saldo.

**Contas de teste:** a administradora e um cliente de teste, com o alias `+teste` do Gmail dela e a "Organização Teste". Edital de teste: dia D em 05/10/2026, dossiê em 11/09/2026 e ritmo padrão.

| Pacote | Entra | Depende de | Créditos | Situação |
|---|---|---|---|---|
| **1. Finalizados no painel** | defeito 11 | nada | ~1 | **aplicado 14/09** (2,1) |
| **2. Blindagem do banco** | defeitos 7, 1, 3, 4, 17; convite com e-mail exato; `atualizado_em` | 1 | 2,5 a 3 | **aplicado e testado 14/09** |
| Extra. Nome da organização | nome editável com registro por gatilho | 2 | ~1 | **aplicado 14/09**; falta o teste na tela |
| **3. Registro no servidor** | defeitos 2, 14, 5 e 9; desfazer marcação com registro; gatilhos de registro para os eventos que já existem | 2 | ~3 (custou 8: etapa 1 pelo Lovable; etapa 2 por SQL direto, 0) | **concluído em 14/09**: etapas 1 e 2 aplicadas, conferidas e testadas em transação desfeita; falta o teste na tela (`docs/portal-clientes-pacote-3-registro.md`) |
| **4. Correções de tela** | defeitos 10, 12, 16, 8, 15 (o 9 saiu no pacote 3); inclui `prazosDoEdital` com o ritmo sugerido | 3 | 2,5 a 3 (custou 2,9: banco por SQL direto 0, Lovable 2,9) | **aplicado, conferido e publicado em 14/09**; falta testar na tela no primeiro edital real (`docs/portal-clientes-pacote-4-correcoes-de-tela.md`) |
| **5. Pessoas e convites** | estado "sem acesso", tela Pessoas, convite por e-mail do login | 2 | 3 a 4 | a fazer |
| **6. Encerramentos, resultado e prazo sem máscara** | situações e motivos, desistência, prazo perdido com responsável, resultado com data e confirmação, data prevista, recurso, pós-aprovação, duas datas no recálculo e na data informada, **decisão de atraso** (pendência 2) | 3, 4 | 3 a 4 | a fazer |
| **7. Documentos** | colar lista com **obrigatório ou facultativo**, situações e conferência, link do Drive, **infraestrutura segura de armazenamento**, anexo privado com versões, Baixar tudo, Privacidade atualizada, **registro da submissão com bloqueio com confirmação** | 3 | 5 a 6 | a fazer |
| **7B. Ideia do Projeto e complementação** (novo) | formas A, B e C; "Ideia recebida"; pedido de complemento e resposta; eventos 11 e 12; anexo da forma C sobre o armazenamento do 7 | 3, 7 | 3 a 4 | a fazer; o documento do cliente é atualizado antes |
| **8. Motor de alertas, Farol e painel da administradora** | `alertas.ts` com 2.4; **etapa da jornada** (2.11); **prioridade, níveis e cores do Farol**; Prazos da carteira com etapa e de quem é a vez; sino, central, Novidades, abas de Editais | 6, 7, 7B | 4,5 a 5,5 | a fazer |
| **9. Visão do cliente** | **"O que é seu agora?"** com o Farol e "Agora é com a Mobilizando" com a próxima referência; edital simplificado; documentos com os dois caminhos; complemento aberto; central e sino; atualização ao voltar à aba e a cada 60 s (defeito 13) | 8 | 3,5 a 4,5 | a fazer |
| **10. Painel de resultados** | números clicáveis, taxa com número bruto, filtro por ano, para cliente, organização e carteira | 6 | 2,5 a 3 | a fazer |
| **11. Organização e exportação** | ficha da organização; exportação com pessoas, convites, perguntas, registro, encerramentos, motivos, lista de arquivos, complementos, confirmações de submissão, datas e ids | 5, 10 | ~3 | a fazer |
| **12. Preparação dos e-mails, sem envio** | tabelas de envio e preferências, modo desligado, Configurações, Minha conta, descadastro, prévia do que sairia amanhã, eventos 11 e 12 | 8, 9 | 3 a 3,5 | a fazer |
| **13. Envio dos e-mails** | 13a: eventos 1 a 12 na hora, em modo teste. 13b: lembretes das 8h, Agenda da administradora e resumo das 18h com `pg_cron`, em modo teste | 12, domínio verificado no serviço de envio | 8 a 10 | bloqueado até o domínio |
| 14. Opcionais | Realtime, papel equipe, WhatsApp, gravar a lista de documentos direto pela AMC IA, cópia automática dos anexos para o `G:` | decisão nova | a definir | fora da v1.0 |

**Por que o 7B vem depois do 7.** A forma C precisa do armazenamento seguro, e o mapa proíbe armazenamento provisório. Com o 7B depois do 7, a tela nova da Ideia do Projeto já nasce com as três formas funcionando, e some a decisão futura "o que a forma C oferece enquanto o anexo não existe". **É uma proposta de ordem, que a captadora confirma** antes do pacote 7.

**Conferência por pacote**
1. `read_file` do painel mostra a busca de finalizados. O edital de teste finalizado aparece em "Finalizados" sem mudar o contador de andamento.
2. ~~SELECT sem `anon` nem TRUNCATE; registro com SET NULL; pergunta forjada grava como cliente.~~ **Feito em 14/09, todos passaram.**
3. `dados.ts` sem `registrar()` e nenhum arquivo o importa. `authenticated` sem INSERT em `registro`. Insert direto no registro falha, como cliente e como administradora. Marcar e desmarcar um documento gera 2 linhas com o autor certo. Salvar a mesma resposta 3 vezes não gera linha; mudar a escolha gera 1. O cliente desmarca pela função, com registro, e o DELETE direto em `marcos` falha. As 20 travas e gatilhos atuais continuam intactos.
4. Salvar a submissão 3 vezes não mexe na hora. "Voltar ao sugerido" grava `ritmo` nulo. O atalho abre a etapa. Edital sem acesso mostra mensagem amigável.
5. Cadastro sem convite fica "Aguardando liberação" e sem papel no banco. O convite `+teste` chega e o cadastro cai na organização certa.
6. Encerrar sem motivo é recusado. Com D ontem e sem submissão, o edital aparece "Prazo perdido" para os dois, com o responsável. O projeto marcado com atraso gera a aprovação com as duas datas. Resultado pede confirmação e data.
7. Colar 3 linhas com obrigatório e facultativo cria 3 documentos com a marcação certa. O cliente anexa um PDF; a administradora recusa com motivo e a linha volta a pendente. Um cliente de outra organização não abre o arquivo. "Baixar tudo" traz a versão aceita. Registrar a submissão com um obrigatório "enviado e não conferido" mostra a lista e pede confirmação; confirmar grava pendências, autor, hora e justificativa no histórico; com só facultativo pendente, registra sem confirmação.
7B. Enviar pela forma A, depois pela B e depois pela C, cada vez com o registro da forma. A administradora pede complemento, o cliente vê "Aguardando informações do cliente" com a pergunta, responde, e a administradora vê a resposta. A etapa 4 continua concluída. O prazo do projeto não muda sozinho.
8. `alertas.ts` só importa `prazos.ts` e `agenda.ts`. Com hoje em 13/09, o OK aparece "em 2 dias". Atraso da Mobilizando aparece no painel e na visão do cliente. Ideia enviada antes do OK: a etapa fica 3 e a entrega da ideia aparece feita. "Em N dias" neutro, "a calcular" sem cor, dourado de 3 dias até hoje, vermelho atrasado. Com documento recusado e ideia no prazo ao mesmo tempo, a ordem segue a prioridade.
9. Em tela de celular, "Fazer agora" aparece na primeira dobra. Sem item do cliente, "Agora é com a Mobilizando" mostra a data e a situação reais. O atraso da Mobilizando aparece para o cliente com a mesma cor. Duas abas se atualizam sem recarregar.
10. Os números batem com `select desfecho, motivo_nao_submissao, resultado, count(*) from editais group by 1,2,3`. A taxa mostra o número bruto.
11. O CSV abre no Excel com acentos e todas as colunas novas.
12. `cron.job` sem nenhum job. A prévia bate com as regras de 2.4.
13. SELECT em `envios_email` e `cron.job`. Uma semana em modo teste antes de ligar. Registrar a exceção no `CLAUDE.md` e em `docs/automacoes-desligadas.md`.

**Depois de todo pacote:** repetir as consultas de permissões, regras de linha, gatilhos e armazenamento, porque o Lovable pode reescrever regras sem avisar.

---

## 4. Decisões da captadora

### 4.1 Respondidas em 13/09/2026

1. **E-mail das suas entregas:** sim, só para você, numa "Agenda de hoje" às 8h, em dia com vencimento ou atraso.
2. **Atraso da Mobilizando para o cliente:** **substituída pela regra "nenhum prazo mascarado" (2.5).** O cliente vê o atraso real, com a mesma cor.
3. **Cliente desfaz marcação:** sim, com registro, só em andamento.
4. **Aprovação depois de projeto atrasado:** recalculada a partir do envio real, sem passar da véspera da submissão, **mostrando as duas datas**.
5. **"Não vamos entrar":** para os lembretes do cliente e avisa você para encerrar como desistência (2.6).
6. **Quem recebe e-mail:** todas as pessoas da organização, cada uma podendo se descadastrar.
7. **Mais de um edital em andamento:** permitido, com aviso ao abrir o segundo.
8. **Mover edital de organização:** só sem atividade do cliente.
9. **Data informada nas suas marcações:** sim, com as duas datas visíveis.
10. **E-mail de contato na privacidade:** o Gmail agora, `@mobilizando.org` depois do DNS.
11. **Papel equipe:** depois.
12. **Convite pelo e-mail do login antes do DNS:** sim.

**Também decidido em 13/09**
- **Nenhum prazo mascarado**, para os dois lados.
- **Os quatro alertas do resultado:** resultado registrado, data prevista, prazo de recurso e documentos pós-aprovação.
- **Documentos pelos dois caminhos:** anexo no portal e pasta do Drive, com conferência.
- **Painel de resultados para o cliente**, com propostos, submetidos, prazos perdidos, aprovados e reprovados.

### 4.2 Decididas em 14/09/2026 (Mapa Operacional)

Texto completo no mapa, seção "Decisões da captadora".
1. 7 etapas.
2. Ideia do Projeto: forma A com 5 perguntas e forma B com 8 itens.
3. Etapa da jornada mais entregas paralelas.
4. E-mails ficam na v1.0.
5. Forma C desde o início, sem armazenamento provisório.
6. Complementação da ideia.
7. Entregas paralelas sem fila rígida.
8. Registro da submissão com bloqueio com confirmação.
9. Documento obrigatório ou facultativo, e a definição de pendente.
10. Etapa nunca pela última entrega feita, sem pulo.
11. O que o Farol lê e responde.
12. Prioridade do Farol.
13. Cores do Farol.
14. "Como trabalhamos juntos" atualizado antes da nova tela da Ideia.

**Terceira rodada de 14/09**
15. Regra da etapa atual como a primeira etapa ainda não concluída, com marco de conclusão por etapa, sem pulo artificial (2.11).
16. Registro da Ideia do Projeto só com mudança real de conteúdo, escolha ou estado; salvamento idêntico não gera linha (2.12). A especificação do pacote 3 aplica a mesma regra a todos os eventos.
17. "Cliente visualizou" não é necessário antes do pacote 3; se adotado, nasce no pacote que criar esse dado (regra 8).

### 4.3 Conflitos entre o plano de 13/09 e o mapa, resolvidos na consolidação

| Conflito | Como estava | Como ficou |
|---|---|---|
| Visão do cliente | "entrega mais urgente", sem critério | prioridade do Farol em 6 níveis (2.3, 2.4) |
| Níveis de prazo | sem cor definida | tabela de cores, com "em N dias" neutro e "a calcular" sem cor (2.4) |
| Etapa do edital | não existia | etapa da jornada calculada pela primeira etapa não concluída (2.11) |
| Documentos e OK | a tabela "Espera" não dizia nada; o mapa, na primeira versão, exigia o OK antes | documentos só dependem de a lista ter linhas (2.4, 2.9, 2.11) |
| Obrigatório ou facultativo | não existia | campo por linha e formato do "Colar lista" (2.9, 2.10) |
| Pendente | só "pendente" como situação | pendente = não enviado, enviado não conferido ou recusado (2.9) |
| Submissão | só "aguardando aprovação" | registro com bloqueio com confirmação por documento obrigatório pendente (2.13) |
| Ideia do Projeto | só o roteiro de 8 itens, dentro do pacote 9 | formas A, B e C e complementação, pacote 7B (2.12) |
| Armazenamento | tipos e 10 MB tratados como definidos | infraestrutura a definir no pacote 7; a proposta de 13/09 é ponto de partida (2.9) |
| Eventos | 10 eventos | 12 eventos, com complemento solicitado e respondido (2.4) |
| Evento 2 | "esboço enviado" | "ideia enviada" |
| Pacote 13 | dependia de "DNS" | depende do domínio verificado no serviço de envio |
| Registro de dado novo | tudo no pacote 3 | cada pacote cria o gatilho do dado que cria (regra 8) |

---

## 5. Riscos e fora do escopo

**Riscos e como reduzir cada um**
- **O Lovable reescreve regras.** Conferência por SQL depois de cada pacote.
- **Mensagem grande para no meio.** Mensagens de até cerca de 3 créditos, com "se não couber, pare e liste o que faltou". Enviar só a continuação quando parar.
- **Duas cópias da regra de prazo** (tela e função de e-mail). Cópia literal, com o teste de 05/10/2026 dentro da função.
- **Duas leituras diferentes da etapa ou do Farol.** Uma função só, usada pelas duas visões, com os testes do pacote 8.
- **Arquivos sensíveis no Lovable.** Armazenamento privado, regra por organização, sem link público e teste de acesso cruzado no pacote 7.
- **Dois lugares para procurar documento** (portal e Drive). O portal mostra em cada linha por onde veio o envio, e "Baixar tudo" leva os anexos para o Drive.
- **Confirmação com pendência virar atalho.** Toda confirmação fica no histórico com as pendências, o autor, a hora e a justificativa.
- **Limite baixo do e-mail nativo do login.** Afeta só convite e recuperação de senha.
- **Horário de verão, se voltar.** Ajustar os 2 horários do cron.
- **Dados de teste no banco real.** Só a "Organização Teste", levada para Apagados no fim.

**Fora do escopo da v1.0** (mapa, seção 18):
- carteira, funil e valores (ficam no CaptaHub);
- integração automática com o CaptaHub;
- a AMC IA gravando direto no portal;
- WhatsApp;
- cópia automática dos anexos para o `G:`;
- inteligência artificial dentro do portal;
- papel de equipe;
- relatório financeiro;
- limpeza automática por tempo;
- armazenamento provisório de arquivos;
- dado pessoal além de nome e e-mail.

---

## 6. Arquivos críticos

**No projeto Lovable (532312b5)**
- `src/lib/prazos.ts` e `src/lib/agenda.ts`: reutilizados, sem mudança de regra.
- `src/lib/alertas.ts`: novo, pacote 8, com o Farol e a etapa da jornada (ou em arquivo vizinho, decidido no pacote).
- `src/lib/dados.ts`: sai o `registrar()` (pacote 3).
- `src/lib/etapas.ts`: textos das etapas e opções da Ideia do Projeto (pacote 7B).
- `src/components/portal/edital.tsx`: hoje concentra 13 das 15 chamadas de `registrar()`, a marcação, os documentos, a Ideia e a submissão.
- `src/components/portal/formulario.tsx` e `comum.tsx`.
- `src/routes/_authenticated/painel.tsx`, `apagados.tsx`, `notificacoes.tsx`, e as rotas novas (resultados, pessoas, organizações, alertas, minha conta). A rota `edital.$id.tsx` só repassa para `edital.tsx`.
- `src/lib/perfil.functions.ts`: estado "sem acesso" (pacote 5).
- `src/integrations/supabase/types.ts`: acompanha cada migração.
- `supabase/migrations/`: permissões, regras de linha, gatilhos, funções, tabelas novas e armazenamento.

**Na máquina local**
- `docs/portal-clientes-mapa-operacional-v1.md`: fonte da verdade da operação.
- `marketing/entregas/comercial/como-trabalhamos-juntos.md` e `.html`: atualizar com as formas A e B antes do pacote 7B chegar ao cliente.
- `docs/portal-clientes-especificacao.md`: desatualizada; vale este plano.
- `docs/portal-clientes-pacote-2-blindagem.md` e `docs/portal-clientes-nome-da-organizacao.md`: registros dos envios de 14/09.

---

## 7. Próximos passos

1. ~~Salvar o plano em `docs/` e fazer o commit.~~ Feito em 13/09.
2. ~~Registrar as respostas das 12 decisões.~~ Feito em 13/09.
3. **Fora do plano, em 13/09 à tarde e à noite:** a captadora pediu direto no Lovable a logomarca da Mobilizando no topo do portal. Ficou a versão de fundo claro, e as duas versões foram guardadas na memória do projeto Lovable. O manual de marca não está lá.
4. ~~Pacote 1.~~ Enviado em 14/09, à 1h48, com o OK da captadora; plano aprovado no editor; custo de 2,1 créditos. Só mudou `src/routes/_authenticated/painel.tsx`. **Falta o teste na tela**, quando existir o edital de teste finalizado.
5. ~~Pacote 2.~~ Aplicado em 14/09 às 13h05 e conferido (`docs/portal-clientes-pacote-2-blindagem.md`). O Lovable retirou UPDATE de `organizacoes`, DELETE de `convites` e DELETE de `config_notificacoes` por não estarem no código. Teste de comportamento feito com o OK dela, e todos os itens passaram.
6. ~~Nome da organização editável.~~ Aplicado às 13h28, com a permissão de edição de volta (`docs/portal-clientes-nome-da-organizacao.md`). **Falta o teste na tela, feito por ela.**
7. ~~Mapa Operacional v1.0 e consolidação deste plano.~~ Feitos em 14/09, sem implementação.
8. ~~Atualizar o mapa: pendência 9 aprovada e pendência 7 fora de "antes do pacote 3".~~ Feito em 14/09, com a autorização da captadora (mapa, decisões 15 a 17).
9. ~~Escrever a especificação do pacote 3.~~ Escrita em 14/09: `docs/portal-clientes-pacote-3-registro.md`. **Não enviada.** Aguarda as decisões abertas da seção 12 dela e a autorização da captadora para implementar.
10. Atualizar `docs/portal-clientes-especificacao.md` para refletir este plano, ou marcá-la como histórica.
