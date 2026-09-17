# Portal do Cliente: avisar o cliente sobre um edital novo

> Pedido da captadora em 15/09/2026: "como será feito o alerta para o cliente para cada edital novo que eu incluir na plataforma?" Aprovado o caminho provisório, de 2 a 3 créditos.

## Por que assim

- O aviso automático de edital novo (sino e central de Novidades) é do **pacote 8**, e o e-mail na hora é do **pacote 13**, travado até o domínio ser verificado.
- Até lá, o cliente não fica sabendo de nada. A saída é a mesma do convite: o portal monta a mensagem pronta e a captadora envia pelo Gmail ou pelo WhatsApp.
- Não mexe no banco, não depende de domínio e não cria rotina que roda sozinha.

## Como fica

- Na página do edital, só para a administradora, um bloco **"Avisar o cliente"** com os três botões (e-mail, WhatsApp e copiar) e o "Ver mensagem".
- A mensagem traz o nome do edital, o órgão, o último dia das inscrições, o **link direto daquele edital** e o que o cliente faz primeiro.
- No botão do e-mail, os destinatários já vêm preenchidos com as pessoas cadastradas naquela organização.
- Serve para o edital novo e também para cobrar quando uma entrega atrasa.

## Mensagem enviada ao Lovable

```
Avisar o cliente sobre o edital, pelo e-mail ou pelo WhatsApp da administradora. Não crie tabela, coluna, regra de acesso, gatilho, migração nem serviço de envio. Não mexa em prazos, registro, etapas nem nas outras páginas, fora o que está abaixo.

1. Componente genérico em src/components/portal/convite-mensagem.tsx
- Criar e exportar BotoesMensagem({ assunto, texto, para }: { assunto: string; texto: string; para?: string }), com os mesmos três botões e o "Ver mensagem" que o BotoesConvite já tem hoje: "Enviar por e-mail" (abre https://mail.google.com/mail/?view=cm&fs=1&to=... com para, assunto e texto, tudo com encodeURIComponent; se para estiver vazio, manda to vazio), "Enviar pelo WhatsApp" (https://wa.me/?text=...) e "Copiar mensagem" (assunto + linha em branco + texto, aviso "Mensagem copiada.").
- BotoesConvite passa a usar o BotoesMensagem por dentro, sem mudar o que ele mostra hoje nem o texto do convite.

2. Novo arquivo src/lib/aviso-edital.ts
- montarAvisoEdital({ edital }), recebendo o edital com id, nome, orgao e dia_d. Usar formatarData e paraData de @/lib/prazos para a data, e o endereço fixo https://portal.mobilizando.org (não usar window.location).
- Devolve { assunto, texto }.
- assunto: `${nome do edital}: já está no Portal do Cliente`
- texto, exatamente assim (a linha do órgão só aparece se o edital tiver órgão; a linha do prazo só se tiver dia D):

Olá!

Abrimos no Portal do Cliente Mobilizando o edital {nome}.
Órgão: {orgao}
As inscrições vão até {dia D no formato dd/mm/aaaa}.

O QUE FAZER AGORA
1. Acesse {https://portal.mobilizando.org/edital/{id}}
2. Na Etapa 3, confirme se quer seguir com este edital e escreva suas observações, se tiver.
3. Ainda na Etapa 3, veja a lista de documentos e marque cada um que você enviar.

O portal mostra o prazo de cada entrega e de quem é a vez. Assim que você der o OK, seguimos com a elaboração do projeto.

Dúvidas? É só responder esta mensagem.

Equipe Mobilizando

3. Página do edital (src/components/portal/edital.tsx), só quando ehAdmin
- Abaixo do cabeçalho do edital, um bloco recolhível "Avisar o cliente" (botão que abre e fecha), com o BotoesMensagem montado pelo montarAvisoEdital.
- O campo para do e-mail recebe os e-mails das pessoas da organização do edital, separados por vírgula: buscar com supabase.from("perfis").select("email").eq("organizacao_id", edital.organizacao_id), só quando o bloco é aberto. Sem ninguém cadastrado, deixar vazio e mostrar a linha "Ninguém cadastrado nesta organização ainda. Envie pelo WhatsApp ou convide a pessoa primeiro."
- Não aparece para o cliente e não aparece em edital finalizado ou apagado.

Ao terminar, compile e liste os arquivos alterados.
```

## Execução

- Enviada em 15/09/2026 e concluída com **2,2 créditos**, dentro da faixa de 2 a 3 aprovada. Versão `dbf0f955` para `e74c0e2d`, compilada sem erro.
- Arquivos: `src/lib/aviso-edital.ts` (novo), `src/components/portal/convite-mensagem.tsx` (o componente genérico `BotoesMensagem`, que o `BotoesConvite` passou a usar) e `src/components/portal/edital.tsx` (o bloco "Avisar o cliente").
- Conferido no código: o texto saiu como pedido, a linha do órgão e a do prazo só aparecem quando existem, e o campo `dia_d` é o certo. Nenhuma migração nova (continuam 17) e nada mudou no banco.
- Falta publicar e testar na tela.
