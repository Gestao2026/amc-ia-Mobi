# Portal do Cliente: link do convite abre direto o cadastro

> Pedido da captadora em 15/09/2026: "quero que ao enviar um e-mail ou whatsapp para o meu cliente ele já acesse o portal do cliente e cadastra o seu acesso e senha."

## Como era (publicado em 14/09)

- A mensagem levava a `portal.mobilizando.org/auth`, a tela de entrada.
- A pessoa precisava clicar em "Primeiro acesso, criar conta" e digitar o e-mail exatamente igual ao do convite.
- Depois, confirmar o cadastro por um segundo e-mail antes de conseguir entrar.

## Como fica

- Cada convite tem o próprio link: `portal.mobilizando.org/convite/{número do convite}`.
- O link abre direto a tela "Criar meu acesso", com o nome da organização e o e-mail do convite já preenchido e travado. A pessoa informa o nome, cria a senha e entra no painel na mesma hora, sem e-mail de confirmação. O link enviado pela captadora serve como a confirmação.
- **Convite já usado:** a tela avisa e oferece entrar com e-mail e senha.
- **E-mail que já tem conta:** a tela avisa e manda para a tela de entrada.
- Sem mudança no banco: a leitura do convite e a criação da conta acontecem no servidor do portal.

## Mensagem enviada ao Lovable

```
Link do convite que abre direto o cadastro. Não crie tabela, coluna, regra de acesso, gatilho nem migração. Não mexa em etapas, prazos, registro, na tela /auth nem nas outras páginas, fora o que está abaixo.

1. Funções no servidor (novo arquivo src/lib/convite.functions.ts), usando o supabaseAdmin como em perfil.functions.ts
a) lerConvite({ conviteId }), sem exigir login: busca em convites o id informado. Se não existir, devolve { situacao: "invalido" }. Se aceito_em estiver preenchido, devolve { situacao: "usado" }. Se estiver pendente, devolve { situacao: "pendente", email, organizacao } (organizacao = nome da organização do convite). Não devolve nenhum outro dado.
b) criarAcessoPorConvite({ conviteId, nome, senha }), sem exigir login: lê o convite de novo e só segue se estiver pendente. Senha com pelo menos 6 caracteres. Cria o usuário com supabaseAdmin.auth.admin.createUser({ email: convite.email, password: senha, email_confirm: true, user_metadata: { nome } }). Se o e-mail já tiver conta, devolve { situacao: "ja_tem_conta" } sem alterar nada. Em sucesso, devolve { situacao: "criado", email: convite.email }. Não marca o convite como aceito: isso continua acontecendo no primeiro login, em garantirSessao, que já liga a pessoa à organização do convite.

2. Nova página pública src/routes/convite.$id.tsx (sem login), no mesmo visual da tela /auth (Pagina, cartão max-w-md)
- Título "Criar meu acesso" e o texto "Você recebeu um convite da Mobilizando para o Portal do Cliente da {organizacao}."
- Campos: Nome (obrigatório), E-mail (preenchido com o do convite e travado, só leitura), Senha e Repetir senha (as duas iguais, mínimo 6 caracteres).
- Botão "Criar meu acesso". Em sucesso: entrar com supabase.auth.signInWithPassword com o e-mail e a senha, depois await queryClient.invalidateQueries({ queryKey: ["sessao"] }) e navegar para /painel com replace, igual à tela /auth.
- Convite "usado": "Este convite já foi usado. Entre com o seu e-mail e senha." e botão "Ir para a entrada" (/auth).
- Convite "invalido": "Convite não encontrado. Peça um novo convite à Mobilizando." e o mesmo botão.
- "ja_tem_conta": aviso "Este e-mail já tem acesso ao portal. Entre com a sua senha." e botão "Ir para a entrada".
- Se a pessoa já estiver logada ao abrir a página, mandar para /painel.
- Registrar a rota em routeTree.gen.ts e liberar /convite/$id como página pública, igual a /auth e /privacidade.

3. Mensagem do convite (src/lib/convite-mensagem.ts)
- montarConvite passa a receber { organizacao, email, conviteId }. O link passa a ser "https://portal.mobilizando.org/convite/" + conviteId (fixo, não usar window.location). Manter PORTAL_URL = "https://portal.mobilizando.org" para a volta.
- Trocar só o bloco "COMO ENTRAR PELA PRIMEIRA VEZ" e a linha "Esqueceu a senha" por exatamente isto (o resto do texto fica igual):

COMO CRIAR O SEU ACESSO
1. Clique neste link: {link do convite}
2. Informe o seu nome e crie uma senha. O seu e-mail ({email}) já vem preenchido.
3. Clique em "Criar meu acesso". Pronto: você já entra no portal.

Nas próximas vezes, acesse https://portal.mobilizando.org e entre com o mesmo e-mail e a senha. Esqueceu a senha? Na tela de entrada, clique em "Esqueci minha senha".

4. Botões do convite
- BotoesConvite passa a receber conviteId e repassa para montarConvite.
- Painel, formulário "Convidar pessoa": ao registrar, pegar o id do convite criado (insert com .select("id").single()) e passar ao BotoesConvite.
- Página da organização, "Convites pendentes": passar convite.id.

Ao terminar, compile e liste os arquivos alterados.
```

## Execução

- Enviada em 15/09/2026 e concluída com **4,3 créditos**. Versão `7537060b` para `dbf0f955`, e o Lovable compilou sem erro.
- Arquivos:
  - `src/lib/convite.functions.ts` (novo): lê o convite e cria o acesso, as duas funções no servidor.
  - `src/routes/convite.$id.tsx` (novo): a página "Criar meu acesso".
  - `convite-mensagem.ts`, `convite-mensagem.tsx`, `painel.tsx` e `organizacao.$id.tsx`: o link por convite.
  - `routeTree.gen.ts`: registro da página nova.
- Conferido: o texto da mensagem saiu como pedido; o banco continua com 17 migrações, 1 convite e 1 usuário. Endereço de convite inexistente ou malformado cai em "Convite não encontrado".
- **Publicado em 15/09/2026 e conferido no ar:** a página `portal.mobilizando.org/convite/…` responde, a mensagem já leva o link do convite e os textos novos ("Criar meu acesso", "Repetir senha", "Este convite já foi usado") estão na versão publicada.
- Falta o teste ponta a ponta com uma conta de cliente. O portal ainda não tem nenhum edital, então o painel do cliente abriria vazio.
