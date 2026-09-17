# Portal do Cliente. Correção do painel em branco depois de entrar

> 14/09/2026. Aplicado, publicado e testado na tela pela captadora.

**Defeito.** Depois de entrar com e-mail e senha, o painel ficava em branco até dar F5.

**Causa.** O gancho de sessão guarda a consulta `["sessao"]` por 60 segundos. Na tela de entrar, essa consulta ficava guardada como "ninguém logado". Ao ir para `/painel`, o painel usava a resposta guardada e não mostrava nada.

A causa foi achada lendo os arquivos do site publicado, sem crédito.

**Correção.** Só em `src/routes/auth.tsx`: depois do login certo, e também ao criar conta com sessão, a tela descarta a consulta `["sessao"]` antes de ir para o painel.

**Execução**
- Uma mensagem ao Lovable, **0,9 crédito**, versão `88d88da2` para `e4945166`.
- Nenhuma mudança em banco, migração ou outro arquivo.
- Publicado às 19h24 de Brasília (`index-B6Y_0eSW.js`, `auth-B2JeGW22.js`).
- Teste na tela aprovado: o painel aparece sem F5.
