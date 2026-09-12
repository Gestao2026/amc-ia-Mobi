# Portal do Cliente. Mensagem 2, pendente de crédito

> Escrita em 12/09/2026 e **não enviada**: o Lovable recusou com "workspace is out of credits".
> Quando houver crédito, esta mensagem vai inteira, de uma vez só, para gastar um crédito apenas.
> Contexto e regras completas em `docs/portal-clientes-especificacao.md`.

## O que já está pronto no projeto (construído na mensagem 1)

- Banco com onze tabelas e segurança por linha ligada em todas.
- Motor de prazos em `src/lib/prazos.ts`, conferido contra o teste obrigatório.
- Página aberta "Como trabalhamos juntos", página de privacidade, entrar e redefinir senha.
- Primeiro usuário vira administradora; convite por e-mail define a organização.
- Nenhum envio de e-mail, e os três interruptores nascem desligados.

## O que falta, e é o conteúdo da mensagem

Painel da administradora, painel do cliente, página do edital, página de Apagados e página de Notificações. Mais a correção da falha de segurança em `public.perfis`.

---

## Texto a enviar (copiar daqui)

Duas coisas nesta mensagem: uma correção de segurança e as telas de trabalho que ainda faltam. Continue sem configurar envio de e-mail: os interruptores ficam desligados.

1. CORREÇÃO DE SEGURANÇA, faça primeiro
A política "perfis atualiza o proprio" permite que a pessoa mude o próprio registro em public.perfis, inclusive a coluna organizacao_id. Assim, um cliente poderia apontar o perfil para outra organização e ver os editais dela. Crie uma trava igual à de documentos_extras: um gatilho BEFORE UPDATE em public.perfis que, quando quem edita não é administradora, bloqueia qualquer mudança em organizacao_id, id e email, deixando passar só o nome. Confira também que nenhuma outra tabela tenha brecha parecida em coluna que só a administradora deveria mudar.

2. AS TELAS QUE FALTAM
Use sempre as funções de src/lib/prazos.ts para qualquer data ou situação. Não reescreva o cálculo, não duplique regra de prazo, não crie outra lista de feriados. Use os textos de src/lib/etapas.ts.

a) Painel, depois de entrar. O conteúdo muda conforme o papel.
Administradora: lista das organizações, com quantos editais em andamento, a próxima entrega com data e a situação em cor; as organizações com entrega atrasada aparecem primeiro. Botões: Nova organização, Convidar pessoa (e-mail e organização), Novo edital e Exportar tudo, que baixa uma planilha CSV com organizações, editais, marcos, documentos e respostas. Um link para a página de Apagados e outro para as Notificações.
Cliente: nome da organização, os editais Em andamento em cartões (nome, órgão, o contador grande D-n, a próxima entrega dele com data e a situação em cor) e a lista de Finalizados, com a data de submissão e o resultado.

b) Página do edital, o coração do portal, nesta ordem:
Cabeçalho com nome, órgão, link do edital e botão de baixar em PDF (pode ser a impressão da página, com layout próprio de impressão).
Bloco "Este edital": organização, dia D, data do dossiê e ritmo. Para a administradora são campos editáveis; para o cliente aparecem preenchidos e travados.
Contador grande, com a frase do contador() de prazos.ts.
"O que depende de você": as quatro entregas do cliente, com data, rótulo D-n e situação em cor, cada uma levando à etapa ao ser clicada.
Régua do prazo: linha do tempo até o dia D, com as entregas do cliente acima da linha e as da Mobilizando abaixo, marcas de sete em sete dias e uma linha tracejada no dia de hoje. No celular ela rola na horizontal.
As sete etapas, que abrem e fecham com um clique, cada uma com o lado Nós, o lado Você, o prazo, a situação e os campos. Etapa 3: a escolha do OK, as observações e a tabela de documentos extras (a administradora acrescenta e remove linhas e escreve documento e onde o edital pede; o cliente só marca enviado e a data). Etapa 4: a escolha entre esboço pronto e só a ideia, mais os oito campos do roteiro. Etapa 5: perguntas e respostas, que os dois lados escrevem. Etapa 6: a escolha da aprovação, o que precisa mudar e o nome e cargo de quem aprovou. Etapa 7: protocolo e data e hora da submissão, só para a administradora. Cada entrega tem a marcação de feito com a data: o cliente marca as quatro dele, a administradora marca projeto e submissão.
Tabela dos três ritmos, com a coluna do ritmo escolhido em destaque e as datas calculadas; só a administradora troca o ritmo. Quando não houver ritmo escolhido, mostre o sugerido por ritmoSugerido() e, quando nenhum couber, o aviso AVISO_NENHUM_RITMO.
As três notas finais.
No fim, o registro do edital: quem fez o quê e quando, em ordem do mais novo para o mais antigo.

c) Ações da administradora na página do edital: Finalizar (pede confirmação, grava a data, o edital fica só para leitura dos dois lados e nasce com resultado aguardando); marcar o resultado como aprovado ou reprovado, com a data; e Apagar, que manda para Apagados.

d) Página de Apagados, só da administradora: os editais apagados, com Restaurar, que devolve à situação anterior, e Apagar de vez, que pede uma segunda confirmação e só então remove. Nada sai dali por tempo: não crie limpeza automática nem prazo de expurgo.

e) Página de Notificações, só da administradora: os três interruptores (lembrete de prazo, aviso na hora e resumo diário) nos escopos geral, por organização e por edital, todos desligados, gravando em config_notificacoes. Deixe claro na tela que o envio ainda não está ligado.

3. REGRAS QUE VALEM EM TODAS AS TELAS
Toda ação relevante grava uma linha em registro: marcar e desmarcar entrega, mudar dia D, ritmo ou data do dossiê, acrescentar ou remover documento, responder o OK, enviar o esboço, responder a aprovação, finalizar, marcar resultado, apagar e restaurar.
O cliente não apaga nada, em nenhuma tela.
Edital finalizado ou apagado não aceita edição de ninguém.
Mantenha a identidade visual já definida e o texto em português do Brasil, com acentuação correta e sem travessão. Pensado primeiro para o celular.
