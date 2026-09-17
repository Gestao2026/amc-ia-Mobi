# Portal do Cliente: convite por e-mail e por WhatsApp

> Pedido da captadora em 14/09/2026, à noite: "Quero enviar o convite por e-mail e esse mesmo e-mail é que ela vai acessar e realizar o cadastro com senha. No e-mail deve conter o link do portal e as orientações para acesso, o que é o portal e como ela vai utilizar de forma simples, objetiva e clara. Da mesma forma será o link que eu enviar pelo WhatsApp [...] não devemos criar milhares de regras. Faça assim e me retorne."

## Decisão de desenho

- O convite continua sendo registrado no portal, com e-mail e organização, como já é hoje.
- O portal monta a mensagem pronta. A captadora envia pela conta dela: um botão abre o Gmail com o e-mail escrito, outro abre o WhatsApp com a mesma mensagem, e um terceiro copia o texto.
- A pessoa cria a conta em "Primeiro acesso, criar conta" com o e-mail convidado e já entra na organização. Isso já funciona hoje.
- **Sem serviço de envio, sem domínio, sem limite de envio e sem regra nova no banco.** O envio automático pelo próprio portal continua no pacote 13, quando houver domínio verificado.
- Um único acerto no login: quem já tinha conta sem organização e tem convite pendente passa a entrar na organização do convite. Sem isso, o convite falhava justamente para quem se cadastrou antes.

## Mensagem enviada ao Lovable

```
Convite por e-mail e por WhatsApp, só tela e login. Não crie tabela, coluna, regra de acesso, gatilho, migração nem serviço de envio de e-mail. Não mexa em etapas, prazos, registro nem nas outras páginas.

1. Novo arquivo src/lib/convite-mensagem.ts
- Constante PORTAL_URL = "https://portal.mobilizando.org/auth" (fixa, não usar window.location).
- Função montarConvite({ organizacao, email }) que devolve { assunto, texto, linkGmail, linkWhatsApp }.
- assunto: "Convite para o Portal do Cliente Mobilizando"
- texto, exatamente assim (trocando {organizacao}, {email} e {link}):

Olá!

A Mobilizando convidou você para acessar o Portal do Cliente da {organizacao}.

O QUE É O PORTAL
É o espaço onde acompanhamos juntos cada edital: em que etapa está, os prazos, os documentos e a aprovação do projeto. Tudo fica registrado em um só lugar.

COMO ENTRAR PELA PRIMEIRA VEZ
1. Acesse {link}
2. Clique em "Primeiro acesso, criar conta".
3. Use este e-mail: {email}
   Precisa ser exatamente este, porque é ele que libera o acesso à sua organização.
4. Crie uma senha e, se o portal pedir, confirme o cadastro pelo e-mail que você vai receber.
5. Nas próximas vezes, entre com o mesmo e-mail e a senha.

COMO USAR
- No painel aparecem os editais em andamento e o prazo de cada entrega.
- Clique no edital para ver a etapa atual e o que falta.
- Quando for a sua vez, o portal mostra o que fazer: dar o OK para seguir, marcar os documentos enviados, contar a ideia do projeto ou aprovar o projeto.
- Tudo o que você marca ou envia fica registrado para a equipe da Mobilizando.

Esqueceu a senha? Na tela de entrada, clique em "Esqueci minha senha".

Dúvidas? É só responder esta mensagem.

Equipe Mobilizando

- linkGmail: "https://mail.google.com/mail/?view=cm&fs=1&to=" + encodeURIComponent(email) + "&su=" + encodeURIComponent(assunto) + "&body=" + encodeURIComponent(texto)
- linkWhatsApp: "https://wa.me/?text=" + encodeURIComponent(texto)

2. Componente BotoesConvite({ organizacao, email }) no mesmo arquivo ou em src/components/portal
- Três botões: "Enviar por e-mail" (abre linkGmail em nova aba), "Enviar pelo WhatsApp" (abre linkWhatsApp em nova aba) e "Copiar mensagem" (copia assunto + linha em branco + texto; aviso "Mensagem copiada.").
- Abaixo dos botões, um "Ver mensagem" recolhível que mostra o texto como vai sair.

3. Painel, formulário "Convidar pessoa" (src/routes/_authenticated/painel.tsx)
- Trocar o aviso "O envio de e-mail ainda não está ligado..." por: "Depois de registrar, envie o convite pelo seu e-mail ou pelo WhatsApp. A pessoa cria a senha com este mesmo e-mail e já entra na organização escolhida."
- Ao registrar com sucesso, não fechar o formulário: mostrar "Convite registrado para {email}." com o BotoesConvite daquele convite e um botão "Concluir" que fecha. Trocar o toast para "Convite registrado."

4. Página da organização (src/routes/_authenticated/organizacao.$id.tsx), bloco "Convites pendentes"
- Em cada convite, abaixo do e-mail e da data, mostrar o BotoesConvite com o nome da organização e o e-mail do convite.

5. Login (src/lib/perfil.functions.ts, garantirSessao)
- Hoje o convite só é lido quando a pessoa ainda não tem papel. Acrescentar: se a pessoa já tem papel "cliente" e o perfil está sem organização, procurar convite pendente para o e-mail dela; se houver, gravar a organização do convite no perfil e marcar o convite como aceito. Nada mais muda nessa função.

Ao terminar, liste os arquivos alterados.
```

## Execução

- Enviada em 14/09/2026, 23h25. Concluída com 3,5 créditos. Versão `2ff18070` para `7537060b`, e o Lovable compilou sem erro.
- Arquivos:
  - `src/lib/convite-mensagem.ts` (novo): mensagem, assunto e os links do Gmail e do WhatsApp.
  - `src/components/portal/convite-mensagem.tsx` (novo): os três botões e o "Ver mensagem".
  - `painel.tsx`: depois de registrar, o formulário mostra os botões e o "Concluir".
  - `organizacao.$id.tsx`: os botões em cada convite pendente.
  - `perfil.functions.ts`: quem é cliente sem organização entra pela do convite pendente.
- Conferido no código: o texto saiu exatamente como pedido, sem nenhuma migração nova (continuam 17) e sem mudança no banco.
- Falta publicar e testar na tela.
