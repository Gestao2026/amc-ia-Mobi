# Portal do Cliente. Pacote 2, blindagem do banco

> **Situação em 14/09/2026, 13h: APLICADO E CONFERIDO.** Continuação enviada às 13h01 com o OK da captadora; o Lovable terminou às 13h05, com duas migrações (`20260914160256` e `20260914160505`) e ajustes em `edital.tsx`, `apagados.tsx`, `notificacoes.tsx`, `types.ts` e `perfil.functions.ts`. Conferência sem crédito, por SELECT e pela diferença entre versões:
> - `anon` sem nenhuma permissão nas 11 tabelas. Permissões padrão das tabelas criadas pelo `postgres` sem `anon`. **Ponto de atenção:** a permissão padrão do `supabase_admin` ainda dá tudo ao `anon` em tabela nova criada por esse papel; as migrações do Lovable rodam como `postgres`, então o risco é baixo, mas conferir depois de todo pacote.
> - `authenticated` sem TRUNCATE, REFERENCES e TRIGGER. **Diferenças em relação ao quadro 1c, justificadas pelo código:** `organizacoes` ficou sem UPDATE, `convites` sem DELETE e `config_notificacoes` sem DELETE. Consequência: o texto do nome da organização passou a pedir o UPDATE de volta.
> - Registro com SET NULL, `edital_nome`, travado contra alteração e exclusão, e leitura total pela administradora (feita alterando a regra "registro le", não com regra nova). Apagar de vez só em Apagados, com linha "Apagou o edital de vez". Funções donas do `postgres`, que ignora regras de linha, então a gravação do registro no apagamento não é barrada.
> - `config_notificacoes` com `organizacao_id` e `edital_id`, as duas chaves com CASCADE, a checagem por escopo e `escopo_id` removido.
> - Convite: gatilho de minúsculas, índice único entre pendentes e busca exata. O convite pendente da `e-missao.ong.br`, criado às 23h07 de 13/09, já estava normalizado.
> - `editais.atualizado_em` com gatilho; a trava de finalizado e apagado não compara essa coluna, então não há conflito.
> - As 8 travas antigas intactas, mais 10 gatilhos novos (18 no total).
> - Código: sem `ilike`, sem `autor_id`, `autor_nome`, `autor_papel`, `feito_por` e `enviado_em` nas gravações; nome digitado para apagar de vez e seção "Apagados de vez".
> - **Falta o teste de comportamento (item 7 da conferência), que grava no banco dentro de uma transação desfeita e pede o OK da captadora.**
>
> **Situação anterior, 14/09/2026, 2h10: enviado pela metade, nada aplicado.** Com o OK da captadora, o texto inteiro foi enviado. O Lovable fez só a leitura do código e das migrações, gastou 1,1 crédito e parou sem alterar nada, pedindo uma nova mensagem para continuar. A continuação (abaixo, em "Continuação a enviar") foi recusada por falta de crédito. Conferido por SELECT logo depois: banco igual ao retrato (77 permissões do `anon`, registro com CASCADE, `escopo_id` presente, 8 gatilhos).
>
> **Quando houver crédito:** enviar só a "Continuação a enviar", não o texto inteiro de novo. O Lovable guarda a conversa. Logo depois, e só depois, vai `docs/portal-clientes-nome-da-organizacao.md`.
>
> **Mudança no banco feita fora do Lovable, depois do retrato:** em 14/09, com o OK da captadora, o nome "INSTITUTO DE DESENVOLVIMENTO INTEGRAL KUYPER" foi trocado por "Instituto de Desenvolvimento Integral Kuyper" (UPDATE de uma linha em `organizacoes`). Nenhuma regra, permissão ou gatilho foi tocado.
>
> Escrito em 14/09/2026 e aprovado pela captadora na mesma madrugada.
> Custo previsto: 2,5 a 3 créditos. O Lovable pode parar para pedir aprovação do plano ou da mudança no banco: a aprovação é no editor.
> Base: `docs/portal-clientes-arquitetura.md`, pacote 2 (defeitos 7, 1, 3, 4 e 17, convite com e-mail exato e `atualizado_em`).

## O que muda para você, em linguagem simples

1. **Ninguém de fora do login toca no banco.** Hoje as tabelas aceitam, no papel, qualquer operação de quem nem entrou no portal. Só as regras de linha seguram. Depois, são duas travas.
2. **Quem escreveu a pergunta passa a ser definido pelo banco.** Hoje um cliente mais esperto consegue gravar uma pergunta como se fosse a Mobilizando.
3. **A data de "feito" e a data de envio do documento passam a ser a hora real.** Hoje dá para gravar a data que quiser por fora da tela.
4. **O registro sobrevive ao "Apagar de vez".** Hoje apagar de vez leva o registro junto e não deixa rastro. Depois: o registro fica, o apagamento vira uma linha nova, e o botão só libera depois de você digitar o nome do edital.
5. **As configurações de aviso ficam amarradas à organização e ao edital.** Hoje, se a organização some, a configuração fica solta no banco.
6. **O convite casa pelo e-mail exato.** Hoje a busca é "parecida": um e-mail com `_` pode casar com outro, e dois convites iguais fazem a pessoa entrar sem organização.
7. **O edital ganha a data da última alteração**, que vai servir aos alertas.

O que **não** entra aqui, para não misturar: o registro escrito só pelo banco (pacote 3), a "data informada" nas suas marcações (pacote 6), a confirmação de e-mail no cadastro e a tela de pessoas sem acesso (pacote 5).

## Retrato do banco antes do envio (14/09/2026, 1h55)

- **Permissões:** `anon` e `authenticated` com todas as operações, inclusive TRUNCATE, REFERENCES e TRIGGER, nas 11 tabelas.
- **Registro:** `registro_edital_id_fkey` com ON DELETE CASCADE; `edital_id` obrigatório.
- **Perguntas:** a regra de inserção confere só `autor_id = auth.uid()`; `autor_nome`, `autor_papel` e `created_at` vêm da tela.
- **Marcos:** `feito_em` com padrão `now()`, mas aceita valor enviado; `feito_por` vem da tela.
- **Documentos:** `enviado_em` vem da tela.
- **Configurações:** `escopo_id` sem chave estrangeira. Uma linha, escopo geral.
- **Convite:** `perfil.functions.ts` busca com `.ilike("email", email)` e `.maybeSingle()`.
- **Volume:** 0 editais, 0 registros, 0 perguntas, 0 marcos, 0 convites, 1 perfil. A migração não tem dado a converter.

---

## Texto a enviar (copiar daqui)

Blindagem do banco. Nenhuma tela nova além das duas mudanças pequenas descritas no item 5 e no item 7. Faça primeiro a migração do banco e depois os ajustes de código. Se não couber tudo nesta mensagem, pare num ponto em que o portal continue funcionando e liste o que faltou.

1. PERMISSÕES DE TABELA (duas camadas de proteção)
a) Revogue do papel anon todas as permissões em todas as tabelas do schema public. Nenhuma página aberta (Como trabalhamos juntos, Privacidade, Entrar) lê tabela; confira no código e, se alguma ler, me avise antes de revogar.
b) Faça o mesmo para as tabelas criadas daqui para frente: as permissões padrão do schema public não dão nada ao anon.
c) Do papel authenticated, revogue TRUNCATE, REFERENCES e TRIGGER em todas as tabelas, e conceda só as operações que o código de fato usa. A minha leitura do código dá o quadro abaixo; confira em src/ e, se encontrar diferença, siga o código e liste a diferença na resposta final:
- organizacoes: SELECT, INSERT, UPDATE
- editais: SELECT, INSERT, UPDATE, DELETE
- marcos: SELECT, INSERT, DELETE
- documentos_extras: SELECT, INSERT, UPDATE, DELETE
- respostas: SELECT, INSERT, UPDATE
- perguntas: SELECT, INSERT
- registro: SELECT, INSERT
- perfis: SELECT, UPDATE
- papeis: SELECT
- convites: SELECT, INSERT, UPDATE, DELETE
- config_notificacoes: SELECT, INSERT, UPDATE, DELETE
As regras de linha continuam como estão, salvo onde este texto pede mudança.

2. AUTOR DA PERGUNTA DEFINIDO PELO BANCO
Crie um gatilho BEFORE INSERT em public.perguntas que ignore o que a tela mandar e grave: autor_id = auth.uid(); autor_nome = o nome do perfil da pessoa (se estiver vazio, a parte do e-mail antes do @); autor_papel = 'administradora' quando private.eh_admin() for verdadeiro, senão 'cliente'; created_at = now(). Em src/components/portal/edital.tsx, a tela deixa de enviar autor_id, autor_nome e autor_papel na inserção.

3. DATAS DE FEITO E DE ENVIO DEFINIDAS PELO BANCO
a) public.marcos: gatilho BEFORE INSERT que grava feito_em = now() e feito_por = auth.uid(), ignorando o que vier da tela; gatilho BEFORE UPDATE que recusa qualquer mudança em feito_em ou feito_por, com a mensagem "A data e o autor da marcação são definidos pelo portal." A tela deixa de enviar feito_por.
b) public.documentos_extras: gatilho BEFORE INSERT OR UPDATE que define enviado_em pelo banco. Quando enviado passa de falso para verdadeiro, enviado_em = now(). Quando enviado fica falso, enviado_em = null. Quando enviado não muda, enviado_em fica igual ao valor antigo. Na inserção, enviado_em = now() se enviado vier verdadeiro, senão null. A tela deixa de enviar enviado_em.

4. O REGISTRO SOBREVIVE AO APAGAR DE VEZ
a) Em public.registro, torne edital_id opcional e troque a chave estrangeira para ON DELETE SET NULL.
b) Acrescente a coluna edital_nome (texto). Um gatilho BEFORE INSERT preenche edital_nome com o nome atual do edital, quando vier vazio.
c) O registro fica travado: um gatilho BEFORE UPDATE OR DELETE recusa qualquer exclusão e qualquer alteração, com uma única exceção, necessária para o SET NULL funcionar: a atualização em que edital_id passa de um valor para nulo e todas as outras colunas continuam iguais.
d) Nova regra de leitura em public.registro: a administradora lê todas as linhas, inclusive as de edital_id nulo. A regra atual do cliente continua.
e) Gatilho AFTER DELETE em public.editais que insere uma linha no registro com edital_id nulo, edital_nome igual ao nome do edital apagado, acao "Apagou o edital de vez", autor_id = auth.uid() e autor_nome do perfil de quem apagou. A função é SECURITY DEFINER com search_path fixo.
f) Gatilho BEFORE DELETE em public.editais que só deixa apagar edital com situacao = 'apagado', com a mensagem "Só é possível apagar de vez um edital que já está em Apagados."
g) Em src/routes/_authenticated/apagados.tsx: na confirmação de Apagar de vez, a administradora digita o nome do edital, e o botão "Confirmo, apagar de vez" só habilita quando o texto digitado for igual ao nome (ignorando espaços nas pontas). Troque o aviso para: "Apagar de vez remove o edital, as entregas, os documentos, as perguntas e as respostas. O registro fica guardado, e o apagamento também é registrado. Não há como voltar atrás."
h) Na mesma página, abaixo da lista, uma seção "Apagados de vez" que lista as linhas do registro com acao "Apagou o edital de vez": nome do edital, quem apagou e data e hora. Quando não houver, "Nenhum edital apagado de vez."

5. CONFIGURAÇÕES DE NOTIFICAÇÃO COM CHAVE ESTRANGEIRA
Em public.config_notificacoes, troque escopo_id por duas colunas: organizacao_id, com chave estrangeira para organizacoes ON DELETE CASCADE, e edital_id, com chave estrangeira para editais ON DELETE CASCADE. Copie os valores atuais de escopo_id conforme o escopo e só então remova escopo_id. Acrescente uma checagem: escopo 'geral' com as duas colunas nulas; escopo 'organizacao' com organizacao_id preenchido e edital_id nulo; escopo 'edital' com edital_id preenchido e organizacao_id nulo. Reescreva a regra de leitura do cliente com as colunas novas, sem ampliar o que ele vê: escopo geral, ou organizacao_id igual à organização dele, ou edital visível para ele. Ajuste src/routes/_authenticated/notificacoes.tsx e src/integrations/supabase/types.ts para as colunas novas, sem mudar o comportamento da tela.

6. CONVITE PELO E-MAIL EXATO
a) Em public.convites, um gatilho BEFORE INSERT OR UPDATE grava o e-mail sem espaços nas pontas e em minúsculas.
b) Índice único sobre o e-mail entre os convites ainda não aceitos (aceito_em nulo). Ao convidar um e-mail que já tem convite pendente, a tela mostra "Já existe um convite pendente para este e-mail."
c) Em src/lib/perfil.functions.ts, troque a busca .ilike("email", email) por igualdade exata com o e-mail do login sem espaços e em minúsculas, restrita a convites com aceito_em nulo.

7. DATA DA ÚLTIMA ALTERAÇÃO DO EDITAL
Acrescente em public.editais a coluna atualizado_em (timestamptz, obrigatória, padrão now()) e um gatilho BEFORE UPDATE que grava now() a cada alteração. O gatilho não pode interferir na trava de edital finalizado ou apagado que já existe.

8. AO TERMINAR, RESPONDA COM
- a lista das permissões finais de anon e authenticated por tabela;
- a lista dos gatilhos criados, com a tabela e o momento de cada um;
- as diferenças que você encontrou entre o quadro do item 1c e o código.

Texto em português do Brasil, com acentuação correta e sem travessão.

Não altere regras de linha, permissões nem gatilhos fora do que foi pedido.

---

## Continuação a enviar (copiar daqui)

Continue a partir da migração, exatamente conforme a mensagem anterior (itens 1 a 8). Não refaça a auditoria: use o que você já levantou. Não abra agentes auxiliares. Ordem: uma migração única com os itens 1 a 7 do banco; depois os ajustes de código em edital.tsx, apagados.tsx, notificacoes.tsx, types.ts e perfil.functions.ts; depois a compilação; e por fim a resposta pedida no item 8, incluindo as diferenças que a auditoria encontrou entre o quadro do item 1c e o código. Se ainda assim não couber, aplique a migração inteira e os ajustes de código que mantêm o portal funcionando com ela, e liste o que faltou.

Texto em português do Brasil, com acentuação correta e sem travessão.

Não altere regras de linha, permissões nem gatilhos fora do que foi pedido.

---

## Conferência depois do envio (sem crédito, só leitura)

1. `information_schema.role_table_grants`: nenhuma linha para `anon`; `authenticated` sem TRUNCATE, REFERENCES e TRIGGER, e com o quadro do item 1c ou com as diferenças que o Lovable justificou.
2. `pg_default_acl`: as permissões padrão do schema public sem `anon`.
3. `pg_constraint`: `registro_edital_id_fkey` com ON DELETE SET NULL; `config_notificacoes` com as duas chaves estrangeiras e a checagem; `escopo_id` removido.
4. `pg_trigger` e `pg_get_functiondef`: os gatilhos dos itens 2, 3, 4, 6 e 7, e as travas antigas intactas (`trava_documentos_cliente`, `trava_edital_fora_andamento`, `trava_perfil_cliente`, `trava_respostas_cliente` e as três `trava_conteudo_edital_fora_andamento`).
5. `pg_policies`: as regras antigas iguais ao retrato acima, mais a leitura total do registro pela administradora e a regra nova de leitura das configurações.
6. Código: `perfil.functions.ts` sem `ilike`; `edital.tsx` sem `autor_nome`, `autor_papel`, `feito_por` e `enviado_em` nas gravações; `apagados.tsx` com o nome digitado.
7. **Teste de comportamento, que grava no banco e por isso pede o OK da captadora antes:** simular, dentro de uma transação desfeita no fim, um cliente inserindo pergunta com `autor_papel = 'administradora'` e confirmar que grava `cliente`; tentar apagar e editar uma linha do registro e confirmar a recusa. O teste completo, com o cliente `+teste`, só é possível depois do pacote 5.

## Risco que fica aberto até o pacote 5

Com o convite casando pelo e-mail exato, continua valendo o risco de alguém criar conta com um e-mail convidado que não é dele, se a confirmação de e-mail do login estiver desligada. A confirmação entra no pacote 5. Até lá, só convidar quando a pessoa for criar a conta logo em seguida.
