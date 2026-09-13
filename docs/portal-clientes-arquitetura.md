# Portal do Cliente Mobilizando. Nova arquitetura e plano de execução

> **Revisão de 13/09/2026, com a captadora.** Entraram:
> - as respostas das 12 decisões, com a decisão 2 trocada pela regra "nenhum prazo mascarado";
> - os encerramentos, com desistência e prazo perdido;
> - o painel de resultados para os dois lados;
> - os quatro alertas do resultado;
> - os documentos, com leitura pela AMC IA, anexo no portal, link do Drive e conferência.
>
> Os pacotes foram renumerados.

## Contexto

O portal foi construído no Lovable em três rodadas (12 e 13/09/2026, cerca de 12,6 créditos) a partir de `docs/portal-clientes-especificacao.md`. Todas as telas existem, a conta da captadora é a única administradora e o banco tem 8 organizações e nenhum edital.

A captadora pediu uma arquitetura melhor, com:
- visão da administradora e visão do cliente bem separadas;
- funcionalidades próprias para cada lado;
- **alertas de todos os prazos dos dois lados, sem mascarar prazo para ninguém**;
- controle de resultados e dos documentos pendentes.

A auditoria de 13/09 foi feita só com leitura: código pelo `read_file`, banco por SELECT em `pg_policies`, `pg_trigger` e `information_schema`. Ela achou 17 defeitos e confirmou que **`pg_cron` e `pg_net` estão disponíveis** no Lovable Cloud, ainda não instalados. Portanto, os e-mails automáticos são tecnicamente viáveis.

---

## 1. Diagnóstico

**Funciona e fica como está**
- O motor de prazos (`src/lib/prazos.ts`) foi conferido contra o exemplo de 05/10/2026. Nenhuma data calculada é gravada.
- `src/lib/agenda.ts` cruza prazo com marcação e é a base do futuro motor de alertas.
- O isolamento por organização vale no banco, com as travas do cliente e do edital finalizado ou apagado.
- Apagados com Restaurar, a página pública e o PDF pela impressão.

**Frágil**
- **O registro não é confiável.** Quem grava é a tela, depois da ação. O cliente pode inventar linhas, e o "Apagar de vez" apaga o registro junto.
- **Autoria e datas forjáveis:** o autor da pergunta, a data de "feito" e a data de envio do documento.
- **Uma camada só de proteção:** as tabelas têm permissão total para `anon` e `authenticated`.
- **Convite frágil:** quem se cadastra sem convite vira cliente sem organização para sempre. A busca por e-mail usa `ilike`.
- **Buracos de fluxo:** finalizados fora do painel; hora da submissão anda 3h a cada salvamento; edital muda de organização com um clique; não há como voltar ao ritmo sugerido.
- **Alertas e e-mails não existem.** As chaves de notificação são gravadas, mas nada as lê.

**Os 17 defeitos, numerados** (referência nos pacotes)
1. Autor da pergunta forjável.
2. Registro escrito pela tela e forjável.
3. Datas de feito e de envio forjáveis.
4. "Apagar de vez" apaga o registro e não se registra.
5. Cliente apaga marcação.
6. Convite frágil.
7. Permissões de tabela totais.
8. Troca de organização com um clique.
9. Hora da submissão +3h.
10. Sem "voltar ao sugerido".
11. Finalizados fora do painel.
12. Atalho não abre a etapa.
13. O outro lado só vê a mudança ao recarregar.
14. Registro repetido a cada salvamento do esboço.
15. Nome, órgão, link e linha de documento não editáveis.
16. Erro técnico cru para quem não tem acesso.
17. Configurações órfãs, sem chave estrangeira.

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

1. **Painel "Prazos da carteira"** (tela inicial)
   - Blocos: Atrasados (do cliente e da Mobilizando); Vence hoje; Vence amanhã; Próximos 7 dias; Prazo perdido; Resultado previsto e ainda não registrado; Prazos de recurso e pós-aprovação; Documentos enviados aguardando conferência; Pendências de cadastro.
   - Cada linha: organização, edital, item, de quem é, data, D-n, cor do nível e link direto.
   - Filtros: organização, "só minhas entregas" e "só do cliente".
2. **Resultados da carteira:** o painel de resultados (2.7) somando todas as organizações, com a opção de abrir organização por organização.
3. **Organizações:** ficha de cada uma, com nome editável, pessoas, editais em andamento, painel de resultados da organização e chaves de notificação.
4. **Pessoas**
   - Convites pendentes, com reenviar e cancelar.
   - Pessoas sem acesso, com atribuir organização.
   - Mover pessoa entre organizações e retirar acesso, sempre com registro.
5. **Editais:** abas Em andamento, Encerrados (aguardando resultado primeiro) e Apagados, com busca.
6. **Página do edital: o que só ela faz**
   - Editar nome, órgão, link, dia D, dossiê e ritmo, com "Voltar ao sugerido".
   - Informar o link da pasta do Drive do edital.
   - Colar e editar a lista de documentos, e conferir ou recusar cada envio.
   - Marcar projeto e submissão com data informável (as duas datas ficam no registro) e protocolo com a hora certa.
   - Mover de organização, só quando o cliente ainda não mexeu.
   - Encerrar (2.7), marcar resultado com data e confirmação, e informar data prevista do resultado, prazo de recurso e prazo pós-aprovação.
   - Apagar.
   - Bloco "E-mails deste edital": enviados, falhas e prévia do que sairia amanhã.
7. **Central de alertas** e sino com número no topo, mais "Novidades desde a sua última visita".
8. **Configurações:** chaves por escopo, modo de envio (desligado, teste, ligado), histórico de e-mails e Exportar tudo.
9. **Apagados** como hoje, com o registro protegido.

### 2.3 Visão do cliente (celular primeiro)

1. **Início "O que é seu agora"**
   - Um cartão grande com a entrega mais urgente e o botão **Fazer agora**, que abre a etapa já expandida.
   - Logo abaixo, a situação da Mobilizando **sem disfarce**, por exemplo "Projeto da Mobilizando: previsto para qui, 29/09, atrasado há 2 dias", na mesma cor dos atrasos do cliente.
   - Depois, os editais em andamento e o atalho para Resultados.
2. **Página do edital simplificada**
   - Ordem: contador, sua próxima entrega, as 4 entregas, documentos pendentes com os dois jeitos de enviar, as etapas (as dele abertas, as da Mobilizando resumidas mas com prazo e situação visíveis), "Falar com a Mobilizando" e o registro.
   - A tabela de ritmos e as notas ficam num bloco fechado, "Como os prazos foram calculados".
3. **Resultados:** o painel de resultados da organização (2.7) e o histórico dos editais encerrados.
4. **Central de alertas** e sino: as entregas dele por nível, documentos recusados, prazos de recurso e pós-aprovação, e as novidades da Mobilizando, inclusive o resultado.
5. **Minha conta:** nome editável, preferências de e-mail, contato da Mobilizando e privacidade.
6. **Descadastro** por link do e-mail, aberto e sem login, com token aleatório.
7. **Nunca apaga nada.** "Desfazer marcação" existe, passa pelo banco e fica no registro. Arquivo enviado errado se corrige com um novo envio, que vira nova versão.

### 2.4 Alertas dos dois lados

**Motor único.** Arquivo novo `src/lib/alertas.ts`, que só usa `prazosDoEdital`, `feitosDoEdital` e `situacaoDoPrazo`. Nenhuma data gravada e nenhuma lista nova de feriados. Funções: `alertasDoEdital()` e `alertasDaCarteira()`.

**Níveis, iguais para os dois lados:** a calcular; em N dias; em 3 dias; em 2 dias; vence amanhã; vence hoje; atrasado há N dias; prazo perdido (dia D passou sem submissão).

**Espera: quando cada alerta começa a valer.** A situação de todos os itens continua visível para os dois lados.

| Item | De quem | Vira alerta quando | Enquanto espera, mostra |
|---|---|---|---|
| OK | cliente | o dossiê foi informado | "a calcular" |
| Documentos, Esboço | cliente | sempre | nada |
| Projeto | Mobilizando | sempre | "com pendência do cliente" se esboço ou documentos estão atrasados, sem tirar o atraso da Mobilizando da tela |
| Aprovação | cliente | o projeto foi marcado | "Aguardando o projeto da Mobilizando", com a data prevista e o atraso dela, se houver |
| Submissão | Mobilizando | sempre | "aguardando aprovação" se ela não veio |
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
| Eventos do cliente: 1 OK dado, 2 esboço enviado, 3 todos os documentos enviados, 4 aprovação respondida | Novidades da administradora | Aviso na hora para a administradora |
| Eventos da Mobilizando: 5 edital novo, 6 documentos acrescentados, 7 projeto enviado, 8 submissão, **9 resultado registrado**, **10 documento recusado** | Novidades do cliente | Aviso na hora para a organização; o evento 6 espera 30 min para juntar |
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
5. Documento enviado e depois recusado não conta como cumprido. A entrega de documentos só fica em dia quando todas as linhas estão conferidas, e a data de cumprimento é a do envio aceito.
6. Nenhum filtro, estado ou texto esconde atraso ou prazo perdido de nenhum lado.

### 2.6 Encerramentos e desistência

**Situações de um edital**

| Situação | Quando | Quem define |
|---|---|---|
| Em andamento | desde a abertura | automático |
| Submetido, aguardando resultado | submissão marcada e edital encerrado | administradora |
| Aprovado, com data | resultado publicado | administradora, com confirmação |
| Reprovado, com data | resultado publicado | administradora, com confirmação |
| Não submetido, com motivo obrigatório | encerrado sem submissão | administradora |
| Apagado | só erro de cadastro; não entra em nenhuma conta | administradora |

**Motivos de não submissão:** desistência do cliente; não recomendado pela Mobilizando; inelegível; prazo perdido. No prazo perdido, o portal grava **de quem eram as pendências atrasadas no dia D** (cliente, Mobilizando ou os dois), calculado pelas entregas, sem campo livre para mascarar.

**Caminho da desistência**
1. O cliente responde "Não vamos entrar neste edital".
2. Os lembretes do cliente naquele edital param na hora.
3. A administradora recebe o alerta "Decidir: encerrar edital", no portal e por e-mail na hora (evento 1).
4. Ela encerra como "Não submetido: desistência do cliente".
5. O edital sai de "Em andamento", vai para o histórico **dos dois lados** e entra na contagem do painel de resultados.

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

1. **Leitura pela AMC IA, fora do portal.** Com o edital analisado, eu cruzo o que o edital exige com a pasta do cliente no `G:` (CaptaDoc e `/projeto-anexos`), inclusive a validade das certidões. O resultado é a lista de pendentes, cada uma com o item do edital de onde vem. **Só leitura:** nada é criado, renomeado ou movido na `06 - Clientes`.
2. **Lista no portal.** A administradora usa "Colar lista" na etapa 3: uma linha por documento, no formato `documento; onde o edital pede`. Gravar a lista direto no banco a partir da AMC IA fica como opção futura, sempre com o OK dela a cada vez.
3. **Entrega pelo cliente, com os dois caminhos em cada linha:**
   - **Anexar no portal:** PDF, JPG, PNG, DOC ou DOCX, até 10 MB, em armazenamento privado do Lovable Cloud, visível só para a organização e a administradora. Cada novo envio vira nova versão, e o cliente não apaga versão.
   - **Pasta do Drive:** o edital mostra o link da pasta informado pela administradora. O cliente sobe o arquivo lá e marca "enviado pelo Drive".
4. **Conferência:** cada linha passa por pendente, enviado, e depois conferido ou recusado com motivo (por exemplo, "certidão vencida em 02/09, envie a nova"). Recusado volta a pendente para o cliente, com aviso na hora (evento 10).
5. **Levar para o Drive:** os arquivos anexados no portal precisam chegar à pasta do edital. No início, a administradora usa "Baixar tudo deste edital". Uma cópia automática da AMC IA para o `G:` fica como opção futura, dependente de ela liberar a `06 - Clientes`.

**Impactos**
- A página de Privacidade passa a dizer que o portal guarda os arquivos enviados e quem os vê.
- O armazenamento consome a cota mensal de nuvem.
- A regra "só nome e e-mail" continua valendo para dado de pessoa. Os arquivos são documentos da organização.
- "Apagar de vez" um edital remove também os arquivos dele, e o registro guarda a lista do que foi removido.

### 2.10 Dados e segurança

| Mudança | Motivo |
|---|---|
| Revogar a permissão de `anon`; `authenticated` só com o necessário; sem TRUNCATE | defeito 7 |
| Autor, nome e papel da pergunta definidos pelo banco | defeito 1 |
| Autor e data da marcação definidos pelo banco; data informada guardada à parte | defeito 3, decisão 9 |
| Registro escrito só por gatilhos do banco; `registrar()` sai de `dados.ts` | defeito 2 |
| Respostas registradas só quando a escolha muda | defeito 14 |
| Registro sobrevive ao "apagar de vez" (SET NULL, com cópia do nome), travado contra edição e exclusão; "apagar de vez" exige o nome digitado e se registra | defeito 4 |
| Cliente sem DELETE; desfazer pela função `desmarcar_entrega`, com registro | defeito 5, decisão 3 |
| Convite casa pelo e-mail exato; sem convite, sem papel; confirmação de e-mail ligada | defeito 6 |
| `mover_edital` recusa quando há atividade do cliente | defeito 8, decisão 8 |
| FKs em `config_notificacoes`; `editais.atualizado_em` | defeito 17 |
| `editais`: `desfecho`, `motivo_nao_submissao`, `pendencia_no_prazo_perdido`, `resultado_previsto_em`, `recurso_ate`, `pos_aprovacao_ate`, `pos_aprovacao_descricao`, `drive_link` | 2.6, 2.8, 2.9 |
| `marcos`: data informada e data da marcação separadas; aprovação com data recalculada visível | 2.5 |
| `documentos_extras`: `status`, `motivo_recusa`, `conferido_por`, `conferido_em`, `enviado_pelo_drive` | 2.9 |
| Tabela `arquivos_documento` (versões) e armazenamento privado `documentos` com regra por organização, sem DELETE para cliente | 2.9 |
| `perfis.visto_ate`, `preferencias_email`, `envios_email`, `registro.avisado_na_hora` | alertas |

**Regras consolidadas**
1. Duas camadas de proteção: permissão mínima e regra de linha, inclusive no armazenamento de arquivos.
2. Autor, data e registro saem do servidor.
3. Registro e histórico de e-mail não se editam nem se apagam.
4. O cliente nunca tem DELETE, em tabela nem em arquivo.
5. Nenhum prazo mascarado (2.5).
6. Segredos do serviço de e-mail só nos segredos do Lovable Cloud.
7. Toda mensagem ao Lovable termina com "não altere regras de linha, permissões nem gatilhos fora do que foi pedido".

---

## 3. Execução em pacotes

Custo total estimado: **43 a 52 créditos**, cerca de 10 dias no plano gratuito ou um mês de Pro somado aos 5 diários. Cada pacote é uma mensagem ao Lovable, escrita antes como arquivo em `docs/` e enviada só com o OK da captadora. A conferência é sempre gratuita, por `read_file` e SELECT.

**Contas de teste:** a administradora e um cliente de teste, com o alias `+teste` do Gmail dela e a "Organização Teste". Edital de teste: dia D em 05/10/2026, dossiê em 11/09/2026 e ritmo padrão.

| Pacote | Entra | Depende de | Créditos |
|---|---|---|---|
| **1. Finalizados no painel** | `docs/portal-clientes-mensagem-3-pendente.md`, sozinho (defeito 11) | nada | ~1 |
| **2. Blindagem do banco** | Defeitos 7, 1, 3, 4, 17; convite com e-mail exato; `atualizado_em` | 1 | 2,5 a 3 |
| **3. Registro no servidor** | Defeitos 2, 14, 5; desfazer com registro | 2 | ~3 |
| **4. Correções de tela** | Defeitos 9, 10, 12, 16, 8, 15 | 3 | 2,5 a 3 |
| **5. Pessoas e convites** | Estado "sem acesso", tela Pessoas, **convite por e-mail do login** | 2 | 3 a 4 |
| **6. Encerramentos, resultado e prazo sem máscara** | Situações e motivos, desistência, prazo perdido com responsável, resultado com data e confirmação, data prevista, recurso, pós-aprovação, duas datas no recálculo e na data informada | 3, 4 | 3 a 4 |
| **7. Documentos** | Colar lista, status e conferência, link do Drive, anexo privado com versões, Baixar tudo, privacidade atualizada | 3 | 4 a 5 |
| **8. Motor de alertas e painel da administradora** | `alertas.ts` com todos os itens de 2.4, Prazos da carteira, sino, central, Novidades, abas de Editais | 6, 7 | 4 a 5 |
| **9. Visão do cliente** | "O que é seu agora" sem disfarce, edital simplificado, documentos com os dois caminhos, central e sino, atualização ao voltar à aba e a cada 60 s (defeito 13) | 8 | 3 a 4 |
| **10. Painel de resultados** | Números clicáveis, taxa com número bruto, filtro por ano, para cliente, organização e carteira | 6 | 2,5 a 3 |
| **11. Organização e exportação** | Ficha da organização; exportação com pessoas, convites, perguntas, registro, encerramentos, motivos, lista de arquivos, datas e ids | 5, 10 | ~3 |
| **12. Preparação dos e-mails, sem envio** | Tabelas de envio e preferências, modo desligado, Configurações, Minha conta, descadastro, prévia do que sairia amanhã | 8, 9 | 3 a 3,5 |
| **13. Envio dos e-mails** (**bloqueado**) | 13a: eventos 1 a 10 na hora, em modo teste. 13b: lembretes das 8h (entregas, recurso, pós-aprovação), Agenda da administradora e resumo das 18h com `pg_cron`, em modo teste | 12, DNS | 8 a 10 |
| 14. Opcionais | Realtime, papel equipe, WhatsApp, gravar a lista de documentos direto pela AMC IA, cópia automática dos anexos para o `G:` | decisão nova | a definir |

**Conferência por pacote**
1. `read_file` do painel mostra a busca de finalizados. O edital de teste finalizado aparece em "Finalizados" sem mudar o contador de andamento.
2. SELECT em `information_schema.role_table_grants` sem `anon` nem TRUNCATE. `pg_constraint` do registro com SET NULL. Como cliente, pelo console, uma pergunta com `autor_papel` forjado grava como cliente.
3. `dados.ts` sem insert no registro. Marcar e desmarcar um documento gera 2 linhas com o autor certo. Salvar o roteiro 3 vezes não gera linha. Insert direto no registro falha.
4. Salvar a submissão 3 vezes não mexe na hora. "Voltar ao sugerido" grava `ritmo` nulo. O atalho abre a etapa. Edital sem acesso mostra mensagem amigável.
5. Cadastro sem convite fica "Aguardando liberação" e sem papel no banco. O convite `+teste` chega por e-mail e o cadastro cai na organização certa.
6. Encerrar sem motivo é recusado. Com D ontem e sem submissão, o edital aparece "Prazo perdido" para os dois, com o responsável. O projeto marcado com atraso gera a aprovação com as duas datas. Resultado pede confirmação e data.
7. Colar 3 linhas cria 3 documentos. O cliente anexa um PDF; a administradora recusa com motivo e a linha volta a pendente. Um segundo cliente de outra organização não abre o arquivo (SELECT nas regras de `storage.objects` e teste pelo endereço). "Baixar tudo" traz a versão aceita.
8. `alertas.ts` só importa `prazos.ts` e `agenda.ts`. Com hoje em 13/09, o OK aparece "em 2 dias". Atraso da Mobilizando aparece no painel e na visão do cliente.
9. Em tela de celular, "Fazer agora" aparece na primeira dobra. O atraso da Mobilizando aparece para o cliente com a mesma cor. Duas abas se atualizam sem recarregar.
10. Os números batem com `select desfecho, motivo_nao_submissao, resultado, count(*) from editais group by 1,2,3`. A taxa mostra o número bruto.
11. O CSV abre no Excel com acentos e todas as colunas novas.
12. `cron.job` sem nenhum job. A prévia bate com as regras de 2.4.
13. SELECT em `envios_email` e `cron.job`. Uma semana em modo teste antes de ligar. Registrar a exceção no `CLAUDE.md` e em `docs/automacoes-desligadas.md`.

**Depois de todo pacote:** repetir as consultas de permissões, regras de linha, gatilhos e armazenamento, porque o Lovable pode reescrever regras sem avisar.

---

## 4. Decisões da captadora (respondidas em 13/09/2026)

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

---

## 5. Riscos e fora do escopo

**Riscos e como reduzir cada um**
- **O Lovable reescreve regras.** Conferência por SQL depois de cada pacote.
- **Mensagem grande para no meio.** Pacotes de até cerca de 5 créditos, com "se não couber, pare e liste o que faltou".
- **Duas cópias da regra de prazo** (tela e função de e-mail). Cópia literal, com o teste de 05/10/2026 dentro da função.
- **Arquivos sensíveis no Lovable.** Armazenamento privado, regra por organização, sem link público e teste de acesso cruzado no pacote 7.
- **Dois lugares para procurar documento** (portal e Drive). O portal mostra em cada linha por onde veio o envio, e "Baixar tudo" leva os anexos para o Drive.
- **Limite baixo do e-mail nativo do login.** Afeta só convite e recuperação de senha.
- **Horário de verão, se voltar.** Ajustar os 2 horários do cron.
- **Dados de teste no banco real.** Só a "Organização Teste", levada para Apagados no fim.

**Fora do escopo:** carteira, funil e valores (ficam no CaptaHub); integração com CaptaHub e AMC IA; WhatsApp; relatório financeiro; limpeza automática por tempo; dado pessoal além de nome e e-mail.

---

## 6. Arquivos críticos

**No projeto Lovable (532312b5)**
- `src/lib/prazos.ts` e `src/lib/agenda.ts`: reutilizados, sem mudança de regra.
- `src/lib/alertas.ts`: novo, pacote 8.
- `src/lib/dados.ts`: sai o `registrar()`.
- `src/components/portal/edital.tsx`, `formulario.tsx` e `comum.tsx`.
- `src/routes/_authenticated/painel.tsx`, `edital.$id.tsx`, `apagados.tsx`, `notificacoes.tsx` e as rotas novas (resultados, pessoas, organizações, alertas, minha conta).
- `src/lib/perfil.functions.ts`: convite com e-mail exato e estado "sem acesso".
- `supabase/migrations/`: permissões, regras de linha, gatilhos, funções, tabelas novas e armazenamento.

**Na máquina local**
- `docs/portal-clientes-especificacao.md`: atualizar com esta arquitetura.
- `docs/portal-clientes-mensagem-3-pendente.md`: é o pacote 1.

---

## 7. Próximos passos

1. ~~Salvar o plano em `docs/` e fazer o commit.~~ Feito em 13/09.
2. ~~Registrar as respostas das 12 decisões.~~ Feito nesta revisão.
3. Enviar o pacote 1 quando houver crédito (5 diários renovam às 21h de Brasília) e conferir.
4. Escrever o pacote 2 como arquivo em `docs/` antes de enviar, e seguir assim com cada pacote.
5. Atualizar `docs/portal-clientes-especificacao.md` para refletir esta arquitetura.
