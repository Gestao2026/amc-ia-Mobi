# Portal do Cliente. Nome da organização editável

> **Situação em 14/09/2026, 13h30: APLICADO E CONFERIDO, falta o teste na tela da captadora.** Enviado às 13h23 com o OK dela; o Lovable parou para aprovar o plano, ela aprovou no editor, e ele terminou às 13h28. Conferência sem crédito: `authenticated` com SELECT, INSERT e UPDATE em `organizacoes` e as outras 10 tabelas iguais ao pacote 2; `anon` sem nenhuma permissão; regras de linha iguais; dois gatilhos novos em `organizacoes` (`normaliza_nome_organizacao`, antes, e `registra_correcao_nome_organizacao`, depois, SECURITY DEFINER com search_path fixo), somando 20 gatilhos; em `painel.tsx`, o componente `EditarNomeOrganizacao` só no painel da administradora, com Salvar travado quando vazio ou igual e a atualização da lista `organizacoes`. O Lovable abriu o painel com a sessão da captadora no ambiente de teste dele só para clicar em Editar e Cancelar, sem salvar: o registro seguiu com 0 linhas e os 8 nomes intactos.
>
> **Situação anterior: escrito em 14/09/2026 e não enviado.** Aprovado pela captadora para ir **logo depois da continuação do pacote 2**, nunca antes nem junto: o registro da mudança de nome depende do `edital_id` opcional e da leitura total do registro pela administradora, que entram no pacote 2.
> Custo previsto: cerca de 1 crédito.
> Antecipa, do pacote 11, só o nome editável. O resto da ficha da organização continua lá.

## Por que existe

Em 14/09/2026 a captadora encontrou o nome "INSTITUTO DE DESENVOLVIMENTO INTEGRAL KUYPER" todo em maiúsculas e não havia onde corrigir. Com o OK dela, o nome foi trocado direto no banco (SQL de uma linha, na mesma madrugada) para "Instituto de Desenvolvimento Integral Kuyper". As outras sete organizações já estavam com a grafia certa. O campo abaixo é para as próximas correções.

---

## Texto a enviar (copiar daqui)

Uma mudança pequena e só ela: a administradora passa a poder corrigir o nome de uma organização. Não mude nada além disto.

1. TELA
No painel da administradora (src/routes/_authenticated/painel.tsx), no cartão de cada organização, ao lado do nome, um botão discreto "Editar nome". Ao clicar, o nome vira um campo de texto já preenchido, com os botões "Salvar" e "Cancelar". O botão Salvar fica desabilitado enquanto o campo estiver vazio ou igual ao nome atual. Ao salvar, mostre "Nome da organização salvo." e atualize as listas que mostram organizações. Em caso de erro, mostre a mensagem do banco. O cliente não vê o botão.

2. BANCO
a) Gatilho BEFORE UPDATE em public.organizacoes que grava o nome sem espaços nas pontas e recusa nome vazio, com a mensagem "O nome da organização não pode ficar vazio."
b) Gatilho AFTER UPDATE em public.organizacoes que, quando o nome muda, insere uma linha em public.registro com edital_id nulo, acao "Corrigiu o nome da organização", detalhe "de {nome antigo} para {nome novo}", autor_id = auth.uid() e autor_nome do perfil de quem alterou. A função é SECURITY DEFINER com search_path fixo. A tela não grava registro: quem grava é o gatilho.
c) Conceda de volta UPDATE em public.organizacoes ao papel authenticated. Essa permissão foi retirada na blindagem porque ainda não havia tela que editasse organização; agora há. A regra de linha "organizacoes admin total" já garante que só a administradora altera, e o cliente continua só lendo a própria organização. Não crie regra de linha nova e não mude nenhuma outra permissão.

Texto em português do Brasil, com acentuação correta e sem travessão.

Não altere regras de linha, permissões nem gatilhos fora do que foi pedido.

---

## Conferência depois do envio (sem crédito, só leitura)

1. Diferença entre versões: só `painel.tsx` e uma migração com os dois gatilhos de `organizacoes`.
2. `pg_trigger` em `organizacoes` com os dois gatilhos; `pg_policies` de `organizacoes` iguais às de antes; `authenticated` com SELECT, INSERT e UPDATE em `organizacoes` e nenhuma outra permissão mudada.
3. Na tela, a captadora corrige um nome qualquer e volta ao original. **Teste que grava, feito por ela.** Depois, SELECT no registro mostra as duas linhas "Corrigiu o nome da organização", com o nome dela e a hora.
