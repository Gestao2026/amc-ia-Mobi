# Portal do Cliente Mobilizando. Nova arquitetura e plano de execução

## Contexto

O portal foi construído no Lovable em três rodadas (12 e 13/09/2026, cerca de 12,6 créditos) a partir de `docs/portal-clientes-especificacao.md`. Todas as telas existem, a conta da captadora é a única administradora e o banco tem 8 organizações e nenhum edital.

A captadora pediu uma arquitetura melhor, com:
- visão da administradora e visão do cliente bem separadas;
- funcionalidades próprias para cada lado;
- **alertas de todos os prazos dos dois lados**.

O plano deve incluir as correções já identificadas (finalizados fora do painel e comparação de e-mail do convite) e será ajustado junto com ela antes de qualquer envio ao Lovable.

A auditoria de hoje foi feita só com leitura: código pelo `read_file`, banco por SELECT em `pg_policies`, `pg_trigger` e `information_schema`. Ela confirmou o que funciona, achou 17 defeitos e confirmou que **`pg_cron` e `pg_net` estão disponíveis** no Lovable Cloud, ainda não instalados. Portanto, os e-mails automáticos são tecnicamente viáveis.

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
- **Uma camada só de proteção:** as tabelas têm permissão total para `anon` e `authenticated`, e tudo depende da regra de linha.
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

## 2. Arquitetura proposta

### 2.1 Papéis

| Papel | Decisão |
|---|---|
| **Administradora** | Poder total. É a captadora. |
| **Cliente** | Todas as pessoas da organização veem e escrevem igual. |
| **Sem acesso** (novo) | Criou conta sem convite: vê "Aguardando liberação da Mobilizando" e nenhum dado. |
| **Equipe** | Fica para depois. O banco já aceita o papel, sem tela. |

### 2.2 Visão da administradora

1. **Painel "Prazos da carteira"** (tela inicial)
   - Blocos: Atrasados, dividido entre do cliente e da Mobilizando; Vence hoje; Vence amanhã; Próximos 7 dias; Dia D passou sem submissão; Aguardando resultado; Pendências de cadastro (convites pendentes e pessoas sem acesso).
   - Cada linha: organização, edital, entrega, de quem é, data, D-n, cor do nível e link direto para a etapa.
   - Filtros: organização, "só minhas entregas" e "só do cliente".
2. **Organizações**
   - Ficha de cada uma: nome editável, pessoas, edital em andamento, histórico de finalizados com resultado e chaves de notificação da organização.
3. **Pessoas**
   - Convites pendentes, com reenviar e cancelar.
   - Pessoas sem acesso, com atribuir organização.
   - Mover pessoa entre organizações e retirar acesso, sempre com registro.
4. **Editais**
   - Abas Em andamento, Finalizados (aguardando resultado primeiro) e Apagados, com busca.
5. **Página do edital: o que só ela faz**
   - Editar nome, órgão, link, dia D, dossiê e ritmo, com botão "Voltar ao sugerido".
   - Editar a lista de documentos, inclusive o texto de cada linha.
   - Marcar projeto e submissão com data informável, e o protocolo com a hora certa.
   - Mover o edital de organização, só quando o cliente ainda não mexeu.
   - Finalizar, e marcar o resultado com data escolhida e confirmação.
   - Apagar.
   - Bloco "E-mails deste edital": enviados, falhas e prévia do que sairia amanhã.
6. **Central de alertas** e sino com número no topo, mais "Novidades desde a sua última visita".
7. **Configurações**
   - Chaves por escopo e modo de envio (desligado, teste, ligado).
   - Histórico de e-mails.
   - Exportar tudo.
8. **Apagados** como hoje, com o registro protegido.

### 2.3 Visão do cliente (celular primeiro)

1. **Início "O que é seu agora"**
   - Um cartão grande com a entrega mais urgente e o botão **Fazer agora**, que abre a etapa já expandida.
   - Logo abaixo, uma linha neutra: "Aguardando a Mobilizando: projeto previsto para qui, 29/09".
   - Depois, os editais em andamento e o link Histórico.
2. **Página do edital simplificada**
   - Ordem: contador, sua próxima entrega, as 4 entregas, as etapas (as dele abertas, as da Mobilizando resumidas), "Falar com a Mobilizando" e o registro.
   - A tabela de ritmos e as notas ficam num bloco fechado, "Como os prazos foram calculados".
3. **Histórico:** finalizados com data de submissão e resultado.
4. **Central de alertas** e sino: as entregas dele por nível e as novidades da Mobilizando.
5. **Minha conta:** nome editável, preferências de e-mail, contato da Mobilizando e privacidade.
6. **Descadastro** por link do e-mail, aberto e sem login, com token aleatório.
7. **Nunca apaga nada.** "Desfazer marcação" existe, passa pelo banco e fica no registro.

### 2.4 Alertas dos dois lados

**Motor único.** Arquivo novo `src/lib/alertas.ts`, que só usa `prazosDoEdital`, `feitosDoEdital` e `situacaoDoPrazo`. Nenhuma data gravada e nenhuma lista nova de feriados. Funções: `alertasDoEdital()` e `alertasDaCarteira()`.

**Níveis:** a calcular (só a administradora vê); em N dias; em 3 dias; em 2 dias; vence amanhã; vence hoje; atrasado há N dias; encerrado (depois do dia D, só a administradora vê e nunca vira e-mail).

**Espera, para não alertar quem ainda não pode agir**

| Entrega | De quem | Alerta quando | Enquanto espera, mostra |
|---|---|---|---|
| OK | cliente | o dossiê foi informado | "a calcular" para a administradora |
| Documentos, Esboço | cliente | sempre | nada |
| Projeto | Mobilizando | sempre | "bloqueado pelo cliente" se esboço ou documentos estão atrasados |
| Aprovação | cliente | o projeto foi marcado | "Aguardando o projeto da Mobilizando" |
| Submissão | Mobilizando | sempre | "aguardando aprovação" se ela não veio |

O OK respondido "não vamos entrar" suspende os alertas do cliente e gera para a administradora: "Decidir: finalizar edital".

**Quem recebe o quê**

| Item | Dentro do portal (sem custo e sem DNS) | Por e-mail (pacote 10) |
|---|---|---|
| 4 entregas do cliente | Cliente: sino e início. Administradora: painel de prazos | **Autorizado em 12/09:** 3 dias antes, no dia e a cada 2 dias no atraso (no máximo 5), cópia para a administradora, um e-mail por dia por edital, nada depois do dia D, só em dia útil às 8h |
| 2 entregas da Mobilizando | Administradora: painel e sino. Cliente: linha neutra "aguardando" | **Extensão, depende da confirmação dela:** só para a administradora, numa "Agenda de hoje" às 8h, e só em dia com vencimento ou atraso |
| 4 eventos do cliente (OK, esboço, documentos, aprovação) | Novidades da administradora | **Autorizado:** aviso na hora para a administradora |
| 4 eventos da Mobilizando (edital novo, documentos acrescentados, projeto enviado, submissão) | Novidades do cliente | **Autorizado:** aviso na hora para a organização; "documentos acrescentados" espera 30 min para juntar |
| Resumo diário | Não se aplica | **Autorizado:** 18h, dia útil, só para a administradora, pula dia sem atividade e não repete aviso já enviado |

**Guarda e controle de repetição**
- Tabela `envios_email`, que nunca é apagada.
- Único por (edital, dia) para lembrete e único por dia para o resumo e a agenda.
- Contagem de avisos de atraso.
- `registro.avisado_na_hora`, para o resumo não repetir.
- Tabela `preferencias_email` por pessoa, com token de descadastro.
- `envio_modo` nasce **desligado**. No modo teste, tudo vai só para a captadora, com "[TESTE]" no assunto.

**Agendamento**
- `pg_cron` com `pg_net` chamando uma função do Lovable Cloud: 8h (`0 11 * * 1-5` UTC) e 18h (`0 21 * * 1-5` UTC).
- Os avisos na hora saem por gatilho no banco, sem cron.
- A função confere feriado com uma cópia literal de `prazos.ts`, testada contra o exemplo de 05/10/2026.
- **Nenhum job é criado antes do pacote 10**, da confirmação dela e do DNS. Até lá, os alertas existem só quando alguém abre a tela, o que respeita a regra "nada roda sozinho".

### 2.5 Dados e segurança

| Mudança | Defeito |
|---|---|
| Revogar a permissão de `anon`; `authenticated` fica só com o necessário; sem TRUNCATE | 7 |
| O autor, o nome e o papel da pergunta são definidos pelo banco | 1 |
| Autor e data da marcação são definidos pelo banco; a administradora pode informar a data, e o registro guarda as duas | 3 |
| Documento ganha `marcado_em` e `marcado_por` do servidor; `enviado_em` vira data declarada | 3 |
| O registro é escrito só por gatilhos do banco; a tela perde o INSERT e `registrar()` sai de `dados.ts` | 2 |
| Respostas registradas só quando a escolha muda; salvar o roteiro não gera linha | 14 |
| O registro sobrevive ao "apagar de vez" (SET NULL, com cópia do nome do edital), fica travado contra edição e exclusão, e o próprio "apagar de vez" é registrado e exige o nome digitado | 4 |
| O cliente perde o DELETE; desfazer passa pela função `desmarcar_entrega`, com registro | 5 |
| O convite casa pelo e-mail exato; sem convite, sem papel; confirmação de e-mail do login ligada | 6 |
| Função `mover_edital` recusa quando já há atividade do cliente | 8 |
| Chaves estrangeiras em `config_notificacoes`; `editais.atualizado_em` | 17 |
| `perfis.visto_ate`, `preferencias_email`, `envios_email`, `registro.avisado_na_hora` | alertas |

Regras consolidadas:
1. Duas camadas de proteção: permissão mínima e regra de linha.
2. Autor, data e registro saem do servidor.
3. Registro e histórico de e-mail não se editam nem se apagam.
4. O cliente nunca tem DELETE.
5. Segredos do serviço de e-mail só nos segredos do Lovable Cloud.
6. Toda mensagem ao Lovable termina com "não altere regras de linha, permissões nem gatilhos fora do que foi pedido".

---

## 3. Execução em pacotes

Custo total estimado: **32 a 38 créditos**, algo como 8 dias no plano gratuito ou um mês de Pro somado aos 5 diários. Cada pacote é uma mensagem ao Lovable, enviada só com o OK dela. A conferência é sempre gratuita, por `read_file` e SELECT.

**Contas de teste:** a administradora e um cliente de teste, com o alias `+teste` do Gmail dela e a "Organização Teste". Edital de teste: dia D em 05/10/2026, dossiê em 11/09/2026 e ritmo padrão.

| Pacote | Entra | Depende de | Créditos |
|---|---|---|---|
| **1. Finalizados no painel** | Texto de `docs/portal-clientes-mensagem-3-pendente.md`, sozinho, como ela pediu (11) | nada | ~1 |
| **2. Blindagem do banco, só SQL** | 7, 1, 3, 4, 17; convite com e-mail exato (6 parcial); `atualizado_em` | 1 | 2,5 a 3 |
| **3. Registro no servidor** | 2, 14, 5; remover `registrar()` das telas | 2 | ~3 |
| **4. Correções de tela** | 9, 10, 12, 16, 8, 15; resultado com data e confirmação | 3 | 2,5 a 3 |
| **5. Pessoas e convites** | Estado "sem acesso", tela Pessoas, convite pelo e-mail nativo do login (sem DNS) (6 completo) | 2 | 3 a 4 |
| **6. Motor de alertas e painel da administradora** | `alertas.ts`, Prazos da carteira, sino, central, Novidades, abas de Editais | 3, 4 | 3,5 a 4,5 |
| **7. Visão do cliente** | "O que é seu agora", edital simplificado, central e sino, Histórico, atualização ao voltar à aba e a cada 60 s (13) | 6 | 3 a 4 |
| **8. Organização, exportação e privacidade** | Ficha da organização; exportação com pessoas, convites, perguntas, registro, datas e ids; privacidade sem "cinco anos" e com e-mail de contato | 5 | ~3 |
| **9. Preparação dos e-mails, sem envio** | Tabelas de envio e preferências, modo desligado, Configurações, Minha conta, descadastro, prévia do que sairia amanhã | 6, 7 | 3 a 3,5 |
| **10. Envio dos e-mails** (**bloqueado**) | 10a: avisos na hora em modo teste. 10b: lembretes das 8h, agenda da administradora e resumo das 18h com `pg_cron`, em modo teste | 9, DNS, confirmação | 7 a 9 |
| 11. Opcionais | Realtime, papel equipe, envio de arquivos, WhatsApp | decisão nova | a definir |

**Conferência por pacote**
1. `read_file` do painel mostra a busca de finalizados. Finalizar o edital de teste faz ele aparecer em "Finalizados" com "Aguardando resultado", sem mudar o contador de andamento.
2. SELECT em `information_schema.role_table_grants` sem `anon` nem TRUNCATE. `pg_constraint` do registro com SET NULL. Pelo console, como cliente, uma pergunta com `autor_papel` forjado grava como cliente.
3. `dados.ts` sem insert no registro. Marcar e desmarcar um documento gera 2 linhas com o autor certo. Salvar o roteiro 3 vezes não gera linha. Insert direto no registro falha.
4. Salvar a submissão 3 vezes não mexe na hora. "Voltar ao sugerido" grava `ritmo` nulo. O atalho abre a etapa. Edital sem acesso mostra mensagem amigável.
5. Cadastro sem convite fica "Aguardando liberação" e sem papel no banco. Atribuir pela tela libera o acesso. O convite `+teste` chega.
6. `alertas.ts` só importa `prazos.ts` e `agenda.ts`. Com hoje em 13/09, o OK aparece "em 2 dias". Marcar como cliente tira o alerta e cria uma Novidade.
7. Em tela de celular, "Fazer agora" aparece na primeira dobra. A aprovação mostra "Aguardando o projeto" até o projeto ser marcado. Duas abas se atualizam sem recarregar.
8. O CSV abre no Excel com acentos e todas as colunas. `read_file` da página de privacidade.
9. `pg_extension` e `cron.job` sem nenhum job. A prévia bate com D-3, o dia do prazo e o atraso a cada 2 dias.
10. SELECT em `envios_email` e `cron.job`. Uma semana em modo teste antes de ligar. Registrar a exceção no `CLAUDE.md` e em `docs/automacoes-desligadas.md`.

**Depois de todo pacote:** repetir as consultas de permissões, regras de linha e gatilhos, porque o Lovable pode reescrever regras sem avisar.

---

## 4. Decisões pendentes da captadora (com recomendação)

1. **E-mail das suas próprias entregas** (projeto e submissão): só para você, numa "Agenda de hoje" às 8h, em dia com vencimento ou atraso.
2. **O cliente vê atraso da Mobilizando?** Só uma linha neutra, "Aguardando a Mobilizando, previsto para dd/mm", sem vermelho.
3. **O cliente pode desfazer uma marcação?** Sim, com registro, só com o edital em andamento.
4. **Aprovação quando o projeto sai atrasado:** recalcular a partir do envio real, sem passar da véspera da submissão.
5. **"Não vamos entrar":** parar os lembretes do cliente e avisar você para finalizar.
6. **Quem recebe e-mail na organização:** todas as pessoas com acesso, cada uma podendo se descadastrar.
7. **Mais de um edital em andamento na mesma organização:** permitir, com aviso ao abrir o segundo.
8. **Mover edital entre organizações:** só sem atividade do cliente.
9. **Você pode informar a data das suas marcações?** Sim, com as duas datas no registro.
10. **E-mail de contato na privacidade:** o Gmail agora, `@mobilizando.org` depois do DNS.
11. **Papel equipe:** não agora.
12. **Convite pelo e-mail nativo do login antes do DNS:** sim.

---

## 5. Riscos e fora do escopo

**Riscos e como reduzir cada um**
- **O Lovable reescreve regras.** Conferência por SQL depois de cada pacote.
- **Mensagem grande para no meio.** Pacotes de até cerca de 4 créditos, com "se não couber, pare e liste o que faltou".
- **Duas cópias da regra de prazo** (tela e função de e-mail). Cópia literal, com o teste de 05/10/2026 dentro da função.
- **Limite baixo do e-mail nativo do login.** Afeta só convite e recuperação de senha.
- **Horário de verão, se voltar.** Ajustar os 2 horários do cron.
- **Dados de teste no banco real.** Só a "Organização Teste", levada para Apagados no fim.

**Fora do escopo:** carteira, funil e valores (ficam no CaptaHub); integração com CaptaHub e AMC IA; envio de arquivos; WhatsApp; relatórios; limpeza automática por tempo; dado pessoal além de nome e e-mail.

---

## 6. Arquivos críticos

**No projeto Lovable (532312b5)**
- `src/lib/prazos.ts` e `src/lib/agenda.ts`: reutilizados, sem mudança de regra.
- `src/lib/alertas.ts`: novo, pacote 6.
- `src/lib/dados.ts`: sai o `registrar()`.
- `src/components/portal/edital.tsx`, `src/components/portal/formulario.tsx` e `src/components/portal/comum.tsx`.
- `src/routes/_authenticated/painel.tsx`, `edital.$id.tsx`, `apagados.tsx` e `notificacoes.tsx`.
- `src/lib/perfil.functions.ts`: convite com e-mail exato e estado "sem acesso".
- `supabase/migrations/`: permissões, regras de linha, gatilhos, funções e tabelas novas.

**Na máquina local**
- `docs/portal-clientes-especificacao.md`: atualizar com esta arquitetura depois de aprovada.
- `docs/portal-clientes-mensagem-3-pendente.md`: é o pacote 1.

---

## 7. Primeiros passos depois da aprovação

1. Salvar este plano em `docs/portal-clientes-arquitetura.md` e fazer o commit.
2. Registrar as respostas das 12 decisões e ajustar os pacotes afetados.
3. Enviar o pacote 1 quando houver crédito (5 diários renovam às 21h de Brasília) e conferir.
4. Escrever cada pacote seguinte como arquivo em `docs/` antes de enviar, igual às mensagens 2 e 3, para nunca perder o texto se o crédito faltar.
