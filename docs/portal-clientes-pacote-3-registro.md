# Portal do Cliente. Pacote 3, registro no servidor

> **Situação em 14/09/2026, 16h15: ETAPA 1 APLICADA E CONFERIDA SEM CRÉDITO; ETAPA 2 NÃO AUTORIZADA.**
> - **Decisões fechadas pela captadora (seção 12):** 1 sim (hora da submissão corrigida já); 2 sim ("Sistema" só sem sessão); 3 sim (antecipar o registro de edições); 4 sim (administradora desmarca qualquer entrega); 5 não (sem edital de teste persistente); 6 em duas etapas.
> - **Redefinição das etapas pela captadora:** a Etapa 1 cria os gatilhos, a função e muda o código, **sem revogar nada**; a Etapa 2 retira o INSERT em `registro`, a regra "registro cria", o DELETE em `marcos` e a regra "marcos cliente desmarca os seus". Isso muda a seção 9.3, onde a Migração 1 já revogava o INSERT.
> - **Enviada às 16h09 (hora de Brasília), com o SQL exato**; versão de antes `fcf678ca`, versão de depois `167caa16`; migração `20260914190906_15804b30`; **custo informado pelo Lovable: 8 créditos** (previsto: cerca de 3).
> - **Conferência sem crédito:** diferença só nos 6 arquivos previstos; 15 chamadas de `registrar()` removidas e nenhuma sobra; desmarcar pela função; hora da submissão pela função `paraCampoDataHora`; 5 gatilhos novos com os momentos certos; as 20 proteções antigas com a mesma assinatura (md5 de `pg_get_functiondef`); as 4 funções `private` antigas iguais; permissões e as 29 regras de linha idênticas ao retrato de antes; EXECUTE das auxiliares só do dono, dos gatilhos só do dono e do `service_role`, e de `desmarcar_entrega` também de `authenticated`, sem `anon`; auxiliares puras conferidas por SELECT sem gravação ("Sistema" sem sessão, datas, ritmo, título); registro com 0 linhas.
> - **Teste de comportamento (camada 2) feito em 14/09, com o OK da captadora, sem crédito**, em dois blocos desfeitos no fim; conferido depois: 0 registros, 0 editais, 0 usuários de teste, 1 convite, 1 perfil, 1 papel, 8 organizações.
>   - **42 passos, todos com o resultado esperado:** E1 a E8, D1 e D3 a D5, R1 a R6, P1, M1 e M2, com textos, detalhes, autor e nome do edital certos; salvamento igual, só espaços e campo em branco sem linha; dois grupos na mesma gravação com duas linhas; desmarcação aceita e recusada nos casos certos, com as três mensagens; administradora desmarcando entrega do cliente; "Sistema" sem id quando não há sessão; finalizar gera só "Finalizou o edital"; apagar de vez com filhos gera só "Apagou o edital" e "Apagou o edital de vez", sem cascata, e as 33 linhas anteriores ficam preservadas e desvinculadas.
>   - **Ponto esclarecido no segundo bloco:** o cliente que tenta alterar a resposta de edital finalizado não recebe erro, porque a regra de linha filtra a gravação (0 linhas alteradas, dado intacto, nenhuma linha no registro); a administradora e a marcação do cliente recebem a trava "Edital finalizado ou apagado está disponível somente para leitura." Comportamento anterior ao pacote 3 e inalcançável pela tela, que trava os campos em edital finalizado.
>   - **Critérios atendidos:** A13, A14, A15, A18, A19, A20 e A21. A16 e A17 ficam para a Etapa 2.
> - **ETAPA 2 APLICADA EM 14/09/2026, direto no banco, sem crédito do Lovable** (autorização da captadora, opção 1). SQL e retrato de antes em `docs/portal-clientes-sql-direto/2026-09-14-pacote-3-etapa-2.sql` e `...-retrato.md`.
>   - Aplicadas só as 4 alterações: sem INSERT de `authenticated` em `registro`; sem a regra "registro cria"; sem DELETE de `authenticated` em `marcos`; sem a regra "marcos cliente desmarca os seus".
>   - Depois: as 24 regras restantes e os 25 gatilhos com assinatura idêntica ao retrato; permissões das outras 9 tabelas iguais; `desmarcar_entrega` igual; `sandbox_exec` intocado.
>   - Teste desfeito: A10, A11, A16 e A17 atendidos (INSERT direto no registro e DELETE direto em marcações recusados para cliente e administradora, sem linha nova); gatilhos seguem registrando; a função segue desmarcando; apagar de vez com marcação segue funcionando pela cascata. Banco conferido depois: 0 dados de teste.
>   - **Não está em `supabase/migrations`.** Avisar o Lovable, em uma linha, no próximo envio.
>   - **Risco residual fora do pacote 3:** papel `sandbox_exec` (ver o retrato).
> - **Pacote 3 concluído no banco e no código.** Falta só o teste na tela, que depende de um edital real ou de decisão da captadora.
>
> **Texto original da especificação, escrito em 14/09/2026:** Escrita em 14/09/2026, a pedido da captadora, sobre `docs/portal-clientes-mapa-operacional-v1.md` (fonte da verdade) e `docs/portal-clientes-arquitetura.md` (seções 2.10, 2.11, 2.12 e 3).
>
> **Base desta especificação:** leitura do código do portal (`dados.ts`, `edital.tsx`, `painel.tsx`, `apagados.tsx`, `notificacoes.tsx`, `edital.$id.tsx`, `etapas.ts` e `prazos.ts`) e SELECT no banco em 14/09. Nada foi gravado.
>
> **O texto da mensagem ao Lovable não está aqui.** Ele será escrito a partir desta especificação depois da autorização da captadora e das decisões da seção 12.
>
> **Custo previsto:** cerca de 3 créditos. Pode ser dividido em duas mensagens (seção 9.3).

---

## O que muda para você, em linguagem simples

1. **O histórico passa a ser escrito pelo próprio banco.**
   - Hoje é a tela que escreve, depois da ação. Se essa gravação falhar, a ação acontece e o histórico fica sem a linha, sem ninguém saber.
   - Depois do pacote, ação e histórico viram uma coisa só: ou os dois acontecem, ou nenhum.
2. **Ninguém mais escreve no histórico por fora.** Hoje um cliente mais esperto consegue inserir uma linha falsa.
3. **O histórico para de repetir.** Salvar o mesmo conteúdo de novo não gera linha. Só a mudança real gera.
4. **Desmarcar uma entrega passa a ter um caminho próprio**, que confere quem pode desmarcar o quê e registra. Hoje o cliente apaga a marcação direto na tabela.
5. **Nada muda na aparência do portal.** As telas continuam iguais, com os mesmos botões e os mesmos textos no histórico.

---

## 1. Objetivo

Tornar o registro do edital **confiável, completo e sem repetição**, escrito **só pelo banco**, corrigindo os defeitos 2, 5 e 14 da arquitetura. Isso é a base para o que o mapa depende de um histórico íntegro: complemento da ideia, confirmação da submissão com justificativa, decisão de atraso e Farol.

## 2. Escopo

### 2.1 Entra

1. **Gatilhos de registro** para todos os eventos que hoje a tela registra (15 chamadas de `registrar()`, seção 3).
2. **Regra da mudança real** em todos os eventos (mapa, decisão 16, estendida a todos): sem mudança real, sem linha.
3. **Função `desmarcar_entrega`**, com as regras de quem desmarca o quê.
4. **Fim da escrita no registro pela tela:**
   - o papel autenticado perde a permissão de inserir em `registro`;
   - sai a regra de linha "registro cria";
   - sai a função `registrar()` do código.
5. **Fim do DELETE direto em `marcos`:**
   - o papel autenticado perde a permissão de apagar em `marcos`;
   - sai a regra de linha "marcos cliente desmarca os seus";
   - a tela passa a usar a função.
6. **Antecipação, sem tela nova** (decisão aberta 3, seção 12): o gatilho de `editais` já registra mudança de nome, órgão e link, e o de `documentos_extras` já registra edição de documento. Assim, o pacote 4, que cria essas telas, não precisa de migração de registro.

### 2.2 Não entra

- Nenhuma tela nova, nenhum texto novo na tela, nenhuma mudança de aparência.
- Formas A e C da Ideia do Projeto, complementação, obrigatório ou facultativo, confirmação da submissão, Farol e etapa da jornada. Cada um cria o próprio gatilho no seu pacote (regra 8 da arquitetura).
- "Cliente visualizou" (mapa, decisão 17).
- Correção da hora da submissão (defeito 9), que é do pacote 4, **salvo decisão contrária** (decisão aberta 1).
- Qualquer mudança nos gatilhos e travas existentes:
  - `trava_documentos_cliente`;
  - `trava_edital_fora_andamento`;
  - `trava_perfil_cliente`;
  - `trava_respostas_cliente`;
  - as quatro `trava_conteudo_edital_fora_andamento`;
  - os 10 gatilhos do pacote 2;
  - os 2 do nome da organização.
- Qualquer mudança nas regras de linha e permissões além das listadas na seção 7.

---

## 3. Retrato de hoje (14/09/2026, só leitura)

**Registro no banco:** 0 linhas. Colunas:
- `id`;
- `edital_id` (opcional, SET NULL);
- `edital_nome`, preenchido por gatilho;
- `autor_id`;
- `autor_nome`;
- `acao`;
- `detalhe`;
- `created_at`.

Travado contra alteração e exclusão desde o pacote 2.

**Quem já registra pelo banco:**
- `registra_edital_apagado_de_vez`: "Apagou o edital de vez";
- `registra_correcao_nome_organizacao`: "Corrigiu o nome da organização".

**Quem registra pela tela** (`registrar()` em `src/lib/dados.ts`, que **não confere erro**):

| # | Arquivo | Onde | Ação gravada hoje |
|---|---|---|---|
| 1 | `painel.tsx` | `FormEdital` | Abriu o edital |
| 2 | `apagados.tsx` | `restaurar` | Restaurou o edital |
| 3 | `edital.tsx` | `apagar` | Apagou o edital |
| 4 | `edital.tsx` | `DadosEdital` | Atualizou os dados do edital |
| 5 | `edital.tsx` | `useSalvarRespostas` | Respondeu o OK / Enviou o esboço, objeto ou ideia / Respondeu a aprovação (**a cada clique**) |
| 6 | `edital.tsx` | `Documentos`, adicionar | Acrescentou documento |
| 7 | `edital.tsx` | `Documentos`, remover | Removeu documento |
| 8 | `edital.tsx` | `Documentos`, marcar | Marcou documento como enviado / Desmarcou documento |
| 9 | `edital.tsx` | `Perguntas` | Escreveu uma pergunta ou resposta |
| 10 | `edital.tsx` | `Marcacao`, desmarcar | Desmarcou entrega |
| 11 | `edital.tsx` | `Marcacao`, marcar | Marcou entrega como feita |
| 12 | `edital.tsx` | `CamposSubmissao` | Registrou a submissão (**a cada clique**) |
| 13 | `edital.tsx` | `TabelaRitmos` | Mudou o ritmo |
| 14 | `edital.tsx` | `AcoesAdmin`, finalizar | Finalizou o edital |
| 15 | `edital.tsx` | `AcoesAdmin`, resultado | Marcou o resultado como aprovado / reprovado |

**Permissões do papel autenticado nas tabelas envolvidas:**

| Tabela | Operações |
|---|---|
| `registro` | SELECT, INSERT |
| `marcos` | SELECT, INSERT, DELETE |
| `respostas` | SELECT, INSERT, UPDATE |
| `documentos_extras` | SELECT, INSERT, UPDATE, DELETE |
| `perguntas` | SELECT, INSERT |
| `editais` | SELECT, INSERT, UPDATE, DELETE |

**Regras de linha envolvidas:**
- `registro`: "registro cria" (INSERT) e "registro le" (SELECT).
- `marcos`: "marcos admin total", "marcos cliente le", "marcos cliente marca os seus" e "marcos cliente desmarca os seus".
- Chave única em `marcos`: (`edital_id`, `chave`).

---

## 4. Eventos e comportamento esperado

### 4.1 Regras comuns a todos os eventos

1. **Quem grava:** um gatilho `AFTER`, na mesma transação da ação. A função é `SECURITY DEFINER`, com `search_path` fixo e execução revogada de `PUBLIC`, `anon` e `authenticated`, no mesmo padrão do pacote 2.
2. **Autor:**
   - `autor_id` = `auth.uid()`;
   - `autor_nome` = o nome do perfil, sem espaços nas pontas;
   - se o nome estiver vazio, a parte do e-mail antes do @;
   - **sem usuário** (ação feita direto no banco), `autor_id` nulo e `autor_nome` "Sistema" (decisão aberta 2).
3. **Nome do edital:** o gatilho `define_nome_registro`, que já existe, preenche `edital_nome`.
4. **Mudança real** (decisão 16, estendida):
   - comparação campo a campo com `IS DISTINCT FROM`;
   - texto comparado depois de tirar os espaços das pontas;
   - vazio e nulo valem o mesmo;
   - na inserção, o "antes" é tudo vazio;
   - campos técnicos nunca contam: `updated_at`, `atualizado_em`, `enviado_em`, `feito_em`, `feito_por`, `situacao_anterior`, `apagado_em`, `finalizado_em` e `resultado_em`.
5. **Sem mudança real, nenhuma linha.**
6. **Uma linha por grupo que mudou.** Uma gravação que mexe em dois grupos diferentes gera duas linhas.
7. **Exclusão em cascata não gera linha.** Quando o edital é apagado de vez, as entregas, documentos, respostas e perguntas saem junto. Os gatilhos de exclusão de `marcos` e `documentos_extras` conferem se o edital ainda existe; se não existe, não gravam. Sem isso, o apagar de vez quebraria, porque a linha nova apontaria para um edital que acabou de sair. O apagamento em si continua registrado pelo gatilho que já existe.
8. **Os textos de `acao` são os de hoje**, para a tela continuar igual. Textos novos só nos eventos que hoje não existem (marcados "novo").

### 4.2 `editais`: gatilho `AFTER INSERT OR UPDATE`

| Evento | Quando | `acao` | `detalhe` |
|---|---|---|---|
| E1 | inserção | Abriu o edital | nome do edital |
| E2 | `situacao` passa de em andamento ou finalizado para apagado | Apagou o edital | vazio |
| E3 | `situacao` sai de apagado | Restaurou o edital | vazio |
| E4 | `situacao` passa de em andamento para finalizado | Finalizou o edital | vazio |
| E5 | `resultado` muda para aprovado ou reprovado, sem mudança de `situacao` na mesma gravação | Marcou o resultado como aprovado / reprovado | vazio |
| E6 | só `ritmo` muda, entre os dados do edital | Mudou o ritmo | nome do ritmo, como em `NOMES_RITMO` ("Padrão (15 dias)") |
| E7 | muda ao menos um entre `organizacao_id`, `dia_d`, `data_dossie`, `nome`, `orgao` e `link`, com ou sem `ritmo` | Atualizou os dados do edital | lista separada por "; ", no formato de hoje (ver abaixo) |
| E8 | muda `protocolo` ou `submetido_em` | Registrou a submissão | protocolo, ou vazio |

**Formato do detalhe de E7**, igual ao que a tela monta hoje, mais os três campos antecipados:
- "organização para {nome da organização}";
- "dia D para {dd/mm/aaaa}";
- "data do dossiê para {dd/mm/aaaa}";
- "ritmo para {nome do ritmo}";
- "nome para {nome}" (novo);
- "órgão para {órgão}" (novo);
- "link para {link}" (novo).

Data vazia aparece como "A calcular", como hoje.

**Não geram linha:**
- finalizar grava `resultado = aguardando` junto: sai só E4;
- apagar grava `situacao_anterior` e `apagado_em`: sai só E2;
- mexer só em `atualizado_em`.

**Interação conhecida com o defeito 9:** hoje cada salvamento da submissão soma 3 horas a `submetido_em`. Como a hora muda de fato, **cada salvamento geraria E8** até a correção do pacote 4 (decisão aberta 1).

### 4.3 `marcos`: gatilho `AFTER INSERT OR DELETE`

| Evento | Quando | `acao` | `detalhe` |
|---|---|---|---|
| M1 | inserção | Marcou entrega como feita | título da entrega |
| M2 | exclusão, com o edital ainda existente | Desmarcou entrega | título da entrega |

**Títulos**, iguais a `TITULOS_MARCO` em `src/lib/prazos.ts`:

| Chave | Título |
|---|---|
| `ok` | Seu OK ao dossiê |
| `documentos` | Documentos extras enviados |
| `esboco` | Esboço, objeto ou ideia |
| `projeto` | Projeto enviado para aprovação |
| `aprovacao` | Sua aprovação ou pedido de ajustes |
| `submissao` | Submissão no portal do edital |

Marcar de novo a mesma entrega já é recusado pela chave única, então não há linha repetida.

### 4.4 `documentos_extras`: gatilho `AFTER INSERT OR UPDATE OR DELETE`

| Evento | Quando | `acao` | `detalhe` |
|---|---|---|---|
| D1 | inserção | Acrescentou documento | nome do documento |
| D2 | exclusão, com o edital ainda existente | Removeu documento | nome do documento |
| D3 | `enviado` passa de falso para verdadeiro | Marcou documento como enviado | nome do documento |
| D4 | `enviado` passa de verdadeiro para falso | Desmarcou documento | nome do documento |
| D5 (novo, antecipado) | muda `documento` ou `onde_pede`, pelo texto limpo | Editou documento | "de {antes} para {depois}", só do que mudou |

### 4.5 `respostas`: gatilho `AFTER INSERT OR UPDATE`

Três grupos, comparados separadamente. Os textos das escolhas são os de `src/lib/etapas.ts`, guardados como estão.

**Grupo OK** (`ok_escolha`, `ok_observacoes`)

| Evento | Quando | `acao` | `detalhe` |
|---|---|---|---|
| R1 | `ok_escolha` muda | Respondeu o OK | a escolha; se as observações também mudaram, acrescenta "; observações atualizadas" |
| R2 (novo) | só `ok_observacoes` muda | Atualizou as observações do OK | vazio |

**Grupo Ideia** (`esboco_modo` e os 8 campos `esboco_*`)

| Evento | Quando | `acao` | `detalhe` |
|---|---|---|---|
| R3 | o grupo estava todo vazio e passa a ter conteúdo | Enviou o esboço, objeto ou ideia | a escolha em `esboco_modo`, se houver |
| R4 (novo) | o grupo já tinha conteúdo e algo muda | Atualizou o esboço, objeto ou ideia | "Mudou: " e a lista, com "a escolha" e os títulos de `CAMPOS_ESBOCO` (O quê, Para quem, Onde, Quando, Como, Com quem, Quanto, O que já existe) |

**Grupo Aprovação** (`aprovacao_escolha`, `aprovacao_ajustes`, `aprovacao_nome_cargo`)

| Evento | Quando | `acao` | `detalhe` |
|---|---|---|---|
| R5 | `aprovacao_escolha` muda | Respondeu a aprovação | a escolha; acrescenta "; ajustes atualizados" e "; nome e cargo atualizados" quando for o caso |
| R6 (novo) | só `aprovacao_ajustes` ou `aprovacao_nome_cargo` muda | Atualizou a resposta da aprovação | "Mudou: " e a lista, com "O que precisa mudar" e "Nome e cargo de quem aprovou" |

### 4.6 `perguntas`: gatilho `AFTER INSERT`

| Evento | Quando | `acao` | `detalhe` |
|---|---|---|---|
| P1 | inserção | Escreveu uma pergunta ou resposta | o texto |

Pergunta não se edita nem se apaga (sem permissão), então não há outro evento.

### 4.7 Eventos que já existem e não mudam

| Tabela | Evento |
|---|---|
| `editais`, exclusão | Apagou o edital de vez (pacote 2) |
| `organizacoes`, alteração do nome | Corrigiu o nome da organização (14/09) |

---

## 5. Correção do registro repetido (defeito 14)

**Hoje:** `useSalvarRespostas` grava a resposta e chama `registrar()` a cada clique em "Salvar resposta", "Salvar esboço" ou "Salvar aprovação". O mesmo vale para "Salvar submissão". Três cliques no mesmo conteúdo são três linhas.

**Depois:**

| Situação | Linhas |
|---|---|
| Primeiro "Salvar esboço" com conteúdo | 1 (R3) |
| O mesmo "Salvar esboço" de novo, sem mudar nada | 0 |
| Mudar só espaços nas pontas de um campo | 0 |
| Apagar um campo e escrever o mesmo texto de volta, antes de salvar | 0 |
| Mudar o texto de "Onde" e salvar | 1 (R4, "Mudou: Onde") |
| Mudar a escolha do OK de "Tenho dúvidas" para "Quero seguir" | 1 (R1) |
| Salvar o OK com a mesma escolha e observação nova | 1 (R2) |
| "Salvar dados do edital" sem mudança | 0 |
| "Salvar submissão" com os mesmos protocolo e hora | 0 (mas veja o defeito 9 em 4.2) |

A tela deixa de chamar `registrar()` e **não recebe nenhuma lógica de comparação**. A comparação fica só no banco.

## 6. Função de desmarcação

**Assinatura:** `public.desmarcar_entrega(_edital_id uuid, _chave public.marco_chave) returns void`, `SECURITY DEFINER`, `search_path` fixo em `public, private`.

**Permissões:** revogar de `PUBLIC` e `anon`; conceder `EXECUTE` só a `authenticated`.

**Regras, nesta ordem:**
1. Sem usuário (`auth.uid()` nulo): recusa com "É preciso entrar no portal para desmarcar uma entrega."
2. Administradora (`private.eh_admin()`): pode desmarcar qualquer entrega, mantendo o poder que a regra "marcos admin total" já dá (decisão aberta 4).
3. Cliente: só as quatro entregas dele (`ok`, `documentos`, `esboco`, `aprovacao`) e só em edital da organização dele em andamento (`private.edital_editavel_cliente`). Fora disso, recusa com "Você não pode desmarcar esta entrega."
4. Apaga a linha de `marcos` daquele edital e chave.
5. Se nada foi apagado: recusa com "Esta entrega não está marcada como feita."

**Registro:** a função não grava no registro. Quem grava é o gatilho M2, disparado pela exclusão, com o autor real, porque `auth.uid()` continua sendo o de quem chamou.

**Edital finalizado ou apagado:** a trava que já existe (`trava_conteudo_edital_fora_andamento`) recusa com a mensagem de hoje, "Edital finalizado ou apagado está disponível somente para leitura."

**Na tela:** em `Marcacao`, o botão "Desmarcar" troca o DELETE direto por `supabase.rpc("desmarcar_entrega", { _edital_id, _chave })`. O botão "Marcar como feito" continua inserindo em `marcos`.

## 7. Regras de acesso

| Objeto | Hoje | Depois do pacote 3 |
|---|---|---|
| `registro`, papel autenticado | SELECT, INSERT | **SELECT** |
| `registro`, regra "registro cria" | existe | **removida** |
| `registro`, regra "registro le" | administradora lê tudo; cliente lê os visíveis | igual |
| `marcos`, papel autenticado | SELECT, INSERT, DELETE | **SELECT, INSERT** |
| `marcos`, regra "marcos cliente desmarca os seus" | existe | **removida** |
| `marcos`, demais regras | admin total, cliente lê, cliente marca os seus | iguais |
| `desmarcar_entrega` | não existe | EXECUTE só para `authenticated` |
| Funções dos gatilhos novos | não existem | sem EXECUTE para `PUBLIC`, `anon` e `authenticated` |
| Papel `anon` | nenhuma permissão | igual |
| Todas as outras tabelas, regras e travas | como no pacote 2 | iguais |

**Por que as funções dos gatilhos gravam mesmo sem permissão de inserir:** elas pertencem ao dono do banco, que ignora as regras de linha. Isso já foi comprovado no teste do pacote 2, com "Apagou o edital de vez".

## 8. Tratamento de erros

1. **Uma transação só.** Ação e registro acontecem juntos. Se o gatilho falhar, a ação inteira é desfeita e a tela mostra a mensagem do banco. Acaba a perda silenciosa de hoje.
2. **Mensagens em português**, com acentuação e sem travessão: as três da função (seção 6) e as das travas existentes.
3. **Na tela, nada novo a tratar.** Toda gravação já faz `if (error) throw new Error(error.message)` e mostra o erro. Só saem as chamadas de `registrar()`.
4. **Chamada ao registro que sobrar por engano:** depois da migração, qualquer inserção direta em `registro` é recusada. A conferência exige zero chamadas (critério A2).
5. **Parada no meio do envio** (seção 9.3): a ordem dos passos garante que o portal funcione em qualquer ponto de parada.
6. **Atualização da tela:** a página do edital já recarrega o registro depois de cada ação (`atualizar()` invalida a consulta `["edital", id]`, que busca o registro). Apagados já invalida a lista de apagados de vez. Nada a acrescentar.

## 9. Arquivos e migração

### 9.1 Arquivos de código

| Arquivo | Mudança | Não muda |
|---|---|---|
| `supabase/migrations/` | duas migrações novas (9.2) | nenhuma migração antiga |
| `src/lib/dados.ts` | sai a função `registrar()` | tipos e buscas |
| `src/components/portal/edital.tsx` | saem as 13 chamadas de `registrar()` e o import; `useSalvarRespostas` deixa de receber a ação; `Marcacao` desmarca pela função | aparência, textos, fluxo, validações e travas da tela |
| `src/routes/_authenticated/painel.tsx` | sai a chamada em `FormEdital` e o import | todo o resto, inclusive o nome editável |
| `src/routes/_authenticated/apagados.tsx` | sai a chamada em `restaurar` e o import | a confirmação por nome e "Apagados de vez" |
| `src/integrations/supabase/types.ts` | ganha `desmarcar_entrega` | o resto |

**Não serão tocados:** `notificacoes.tsx`, `edital.$id.tsx`, `perfil.functions.ts`, `prazos.ts`, `agenda.ts`, `etapas.ts`, `comum.tsx` e `formulario.tsx`.

**Variáveis que ficarem sem uso**, como `autor` em componentes que só o usavam para registrar, podem sair só para a compilação passar, sem outra mudança.

### 9.2 Migrações

**Migração 1: gatilhos, função e fim da escrita pela tela**
1. Funções auxiliares em `private`, sem EXECUTE para `anon` e `authenticated`:
   - `nome_do_autor()`: nome do perfil, ou a parte do e-mail antes do @, ou "Sistema";
   - `texto_limpo(text)`: `NULLIF(btrim(texto), '')`;
   - `titulo_marco(marco_chave)`;
   - `nome_ritmo(ritmo_tipo)`.
2. Funções e gatilhos:
   - `registra_evento_edital()` com `registra_evento_edital_trg`, AFTER INSERT OR UPDATE em `editais`;
   - `registra_evento_marco()` com `registra_evento_marco_trg`, AFTER INSERT OR DELETE em `marcos`;
   - `registra_evento_documento()` com `registra_evento_documento_trg`, AFTER INSERT OR UPDATE OR DELETE em `documentos_extras`;
   - `registra_evento_resposta()` com `registra_evento_resposta_trg`, AFTER INSERT OR UPDATE em `respostas`;
   - `registra_evento_pergunta()` com `registra_evento_pergunta_trg`, AFTER INSERT em `perguntas`.
3. `public.desmarcar_entrega(uuid, marco_chave)` com as permissões da seção 6.
4. `REVOKE INSERT ON public.registro FROM authenticated;` e `DROP POLICY "registro cria" ON public.registro;`

**Migração 2: fim do DELETE direto em marcações** (só depois de a tela usar a função)
1. `REVOKE DELETE ON public.marcos FROM authenticated;`
2. `DROP POLICY "marcos cliente desmarca os seus" ON public.marcos;`

**Dados a converter:** nenhum. O registro tem 0 linhas.

### 9.3 Ordem de execução e pontos seguros de parada

| Passo | O que | Se parar aqui |
|---|---|---|
| 1 | Migração 1 | Seguro. Os gatilhos registram. As chamadas antigas de `registrar()` passam a ser recusadas e, como a função não confere erro, falham em silêncio: **nada quebra e nada duplica**. O desmarcar antigo ainda funciona |
| 2 | Código (9.1) | Seguro. Sem `registrar()` e com o desmarcar pela função |
| 3 | Migração 2 | Seguro. Fecha o DELETE direto |
| 4 | Compilação e resposta com a lista de gatilhos, funções e permissões finais | Fim |

**Se o crédito não couber numa mensagem:** a mensagem A leva o passo 1, e a mensagem B leva os passos 2 a 4.

---

## 10. Critérios de aceite

**Código**
- A1. `src/lib/dados.ts` não tem `registrar`.
- A2. Nenhum arquivo em `src/` importa ou chama `registrar`.
- A3. `Marcacao` desmarca por `rpc("desmarcar_entrega")` e não tem `.from("marcos").delete()`.
- A4. A diferença entre versões mostra só os arquivos da seção 9.1.
- A5. O portal compila.

**Banco: estrutura**
- A6. Existem os 5 gatilhos novos com os momentos da seção 9.2.
- A7. Os 20 gatilhos e travas anteriores continuam iguais (`pg_get_functiondef` sem diferença).
- A8. `desmarcar_entrega` existe, é `SECURITY DEFINER`, tem `search_path` fixo e EXECUTE só para `authenticated`.
- A9. As funções dos gatilhos e as auxiliares não têm EXECUTE para `anon` nem `authenticated`.
- A10. `registro`: o papel autenticado só com SELECT; a regra "registro cria" não existe.
- A11. `marcos`: o papel autenticado com SELECT e INSERT; a regra "marcos cliente desmarca os seus" não existe.
- A12. `anon` sem nenhuma permissão; todas as outras permissões e regras de linha iguais às de depois do nome da organização.

**Banco: comportamento**
- A13. Cada evento das seções 4.2 a 4.6 gera exatamente uma linha, com a `acao`, o `detalhe`, o autor e o nome do edital certos.
- A14. Salvar a mesma resposta 3 vezes gera 0 linhas depois da primeira; mudar só espaços nas pontas gera 0.
- A15. Uma gravação que muda dois grupos gera duas linhas.
- A16. INSERT direto em `registro` é recusado, como cliente e como administradora.
- A17. DELETE direto em `marcos` é recusado, como cliente e como administradora.
- A18. O cliente desmarca a própria entrega em andamento pela função, com uma linha "Desmarcou entrega"; não desmarca "projeto" nem "submissão"; não desmarca em edital de outra organização nem fora de andamento; desmarcar o que não está marcado dá a mensagem certa.
- A19. A administradora desmarca qualquer entrega pela função, com registro.
- A20. Apagar de vez um edital com entregas, documentos, respostas e perguntas funciona e gera só "Apagou o edital de vez", mais as linhas antigas desvinculadas, **sem** "Desmarcou entrega" nem "Removeu documento" em cascata.
- A21. Uma ação recusada por trava (cliente em edital finalizado) não gera linha.

**Tela**
- A22. As telas ficam visualmente iguais e o histórico mostra os mesmos textos de hoje nos eventos que já existiam.

## 11. Estratégia de testes

**Camada 1: conferência sem crédito e sem gravar** (feita pela AMC IA logo depois do envio)
- `get_diff` e `read_file` para A1 a A5.
- SELECT em `pg_trigger`, `pg_proc` com `pg_get_functiondef`, `information_schema.role_table_grants`, `information_schema.routine_privileges` e `pg_policies` para A6 a A12, comparando com o retrato de 14/09.

**Camada 2: teste de comportamento** (grava dentro de uma transação desfeita no fim; **pede o OK da captadora antes**)
- Mesmo método do pacote 2: um bloco único que cria um cliente fictício e um edital de teste, executa cada ação como cliente e como administradora, confere o registro, e termina com erro proposital para desfazer tudo.
- Roteiro, na ordem:
  1. Abrir edital (E1).
  2. Mudar só o ritmo (E6), depois dia D e ritmo juntos (E7).
  3. Acrescentar, editar, marcar e desmarcar documento (D1, D5, D3, D4).
  4. Responder OK, salvar igual 3 vezes, mudar a observação, mudar a escolha (R1, zero, R2, R1).
  5. Salvar esboço vazio, com conteúdo, igual, só com espaços, mudando "Onde" (zero, R3, zero, zero, R4).
  6. Responder a aprovação e depois só o nome e cargo (R5, R6).
  7. Escrever pergunta (P1).
  8. Marcar entregas (M1).
  9. Desmarcar pela função nos casos permitidos e recusados (A18, A19).
  10. INSERT direto em registro e DELETE direto em marcos (A16, A17).
  11. Registrar a submissão (E8), finalizar (E4), marcar o resultado (E5).
  12. Tentar ação do cliente em edital finalizado (A21).
  13. Apagar (E2), restaurar (E3), apagar e apagar de vez (A20).
- Depois, confirmar por SELECT que nada ficou: 0 editais, 0 registros, 0 usuários de teste.

**Camada 3: teste na tela, feito pela captadora** (decisão aberta 5)
- Na conta dela, num edital de teste: abrir, mudar o ritmo, acrescentar e remover documento, marcar e desmarcar "Projeto enviado para aprovação", apagar, restaurar e apagar de vez.
- A cada passo, conferir o histórico do edital e o de "Apagados de vez".
- **Grava no banco real, e as linhas de registro ficam para sempre**, porque o registro não se apaga.

**Camada 4: depois do pacote**
- Repetir as consultas de permissões, regras de linha, gatilhos e armazenamento, porque o Lovable pode reescrever regras sem avisar.

## 12. Decisões abertas antes de implementar

1. **Hora da submissão (defeito 9).** Trazer a correção do pacote 4 para o pacote 3? Sem ela, cada "Salvar submissão" soma 3 horas e gera uma linha "Registrou a submissão" até o pacote 4. **Recomendação:** trazer, por ser pequena e evitar histórico falso.
2. **Autor sem usuário.** "Sistema" como nome quando a ação é feita direto no banco, sem login? Os dois gatilhos que já existem gravam nome vazio nesse caso e não serão alterados neste pacote.
3. **Antecipar o registro de edição** de nome, órgão e link do edital e de linha de documento, que ainda não têm tela (pacote 4)? **Recomendação:** sim, sem custo de tela e sem migração no pacote 4.
4. **Administradora desmarca qualquer entrega** pela função, como a regra "marcos admin total" já permite hoje? A alternativa é limitar às entregas da Mobilizando (projeto e submissão), como a tela mostra.
5. **Teste na tela.** Autorizar a criação de um edital de teste no banco real, sabendo que as linhas de registro dele ficam para sempre? A alternativa é fazer só as camadas 1 e 2 e testar na tela no primeiro edital real.
6. **Divisão do envio.** Uma mensagem só, com a instrução de parar num ponto seguro, ou já em duas mensagens (A e B)?

## 13. Riscos e rollback

### 13.1 Riscos

| Risco | Como reduzir |
|---|---|
| Apagar de vez quebrar pela cascata (linha nova apontando para edital apagado) | regra 4.1.7 e critério A20, testado na camada 2 |
| Linha duplicada (tela e gatilho) na janela entre migração e código | a migração 1 já tira o INSERT da tela; a chamada antiga falha em silêncio (9.3) |
| Cliente sem desmarcar entre a migração 2 e o código | a migração 2 só vem depois do código (9.3) |
| Histórico falso de submissão pelo defeito 9 | decisão aberta 1 |
| Texto do detalhe diferente do que a tela mostrava | textos copiados de `etapas.ts`, `prazos.ts` e do código atual; critério A22 |
| Lovable alterar travas, regras ou permissões fora do pedido | critérios A7 e A12, e a frase de fechamento da mensagem |
| Lovable "melhorar" a tela | critério A4 e a instrução de não mudar aparência nem textos |
| Mensagem parar no meio | pontos seguros de parada (9.3) |
| Gatilho lento | um INSERT por evento, sem consulta pesada; volume do portal irrelevante |

### 13.2 Rollback

**Antes do envio:** anotar o identificador da versão atual do código (`latest_commit_sha` pelo `get_project`) e guardar o retrato das permissões, regras e gatilhos.

**Se algo der errado depois:**
1. **Código:** restaurar no Lovable a versão anotada. Isso volta a tela, **mas não desfaz as migrações.**
2. **Banco:** migração de reversão, enviada só com o OK da captadora:
   - `DROP TRIGGER` dos 5 gatilhos novos e `DROP FUNCTION` das funções novas e auxiliares;
   - `GRANT INSERT ON public.registro TO authenticated;` e recriar a regra "registro cria" com `WITH CHECK (private.edital_visivel(edital_id) AND autor_id = auth.uid())`;
   - `GRANT DELETE ON public.marcos TO authenticated;` e recriar a regra "marcos cliente desmarca os seus" com `USING (private.edital_editavel_cliente(edital_id) AND chave = ANY (ARRAY['ok','documentos','esboco','aprovacao']::marco_chave[]))`.
3. **Linhas de registro criadas no meio do caminho ficam**, porque o registro não se apaga desde o pacote 2. Elas descrevem ações que aconteceram de verdade.
4. **Rollback parcial possível:** se só o código der problema, voltar o código e aplicar só o segundo e o terceiro itens da reversão, para a tela antiga voltar a inserir no registro e a apagar marcação. Os gatilhos podem ficar, mas então **cada ação gera linha duplicada** (a da tela e a do gatilho) até a correção.
