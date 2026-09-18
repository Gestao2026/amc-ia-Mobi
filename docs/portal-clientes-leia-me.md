# Portal do Cliente Mobilizando: base do projeto

Situação em 15/09/2026. Site: https://portal.mobilizando.org. Feito no Lovable (Lovable Cloud, sobre Supabase).

> Este é o `00-LEIA-ME.md` do pacote montado em 15/09 na pasta `Implentações Claude\PORTAL DO CLIENTE - BASE` da Área de Trabalho. Os demais arquivos do pacote já moravam no projeto com outros nomes; a lista abaixo aponta para eles.

## Ordem de leitura e o que manda

1. **[portal-clientes-mapa-operacional-v1.md](portal-clientes-mapa-operacional-v1.md)**: a fonte da verdade. Etapas, prazos, papéis e as decisões numeradas de 1 a 43. Em caso de conflito com qualquer outro arquivo, vale o Mapa.
2. **[portal-clientes-arquitetura.md](portal-clientes-arquitetura.md)**: como o portal está construído, os pacotes 1 a 14 com custo e situação, defeitos conhecidos e regras de segurança.
3. **[como-trabalhamos-juntos.md](../marketing/entregas/comercial/como-trabalhamos-juntos.md)**: o texto que o cliente recebe, com as 7 etapas na linguagem dele.
4. **[Roteiro do esboço - Mobilizando.docx](../marketing/entregas/comercial/)**: modelo em Word da forma B da Ideia do Projeto (Etapa 4), com os 11 itens.
5. **[portal-clientes-especificacao.md](portal-clientes-especificacao.md)**: a primeira especificação, de 12/09. Serve como histórico; o Mapa a substituiu onde as duas divergem.
6. **[portal-clientes-custos-lovable-vs-sql-direto.md](portal-clientes-custos-lovable-vs-sql-direto.md)**: o critério para decidir o que vai pelo Lovable (gasta crédito) e o que vai por SQL direto no banco (não gasta).
7. **Um arquivo por entrega**, em ordem cronológica, cada um com o que foi pedido, a mensagem enviada ao Lovable, o custo e como foi conferido:
   - [portal-clientes-pacote-2-blindagem.md](portal-clientes-pacote-2-blindagem.md)
   - [portal-clientes-nome-da-organizacao.md](portal-clientes-nome-da-organizacao.md)
   - [portal-clientes-pacote-3-registro.md](portal-clientes-pacote-3-registro.md)
   - [portal-clientes-pacote-4-correcoes-de-tela.md](portal-clientes-pacote-4-correcoes-de-tela.md)
   - [portal-clientes-pdf-do-edital.md](portal-clientes-pdf-do-edital.md)
   - [portal-clientes-correcao-login.md](portal-clientes-correcao-login.md)
   - [portal-clientes-pacote-7b-ideia-do-projeto.md](portal-clientes-pacote-7b-ideia-do-projeto.md)
   - [portal-clientes-pacote-7c-projeto-versoes.md](portal-clientes-pacote-7c-projeto-versoes.md)
   - [portal-clientes-convite-por-email-e-whatsapp.md](portal-clientes-convite-por-email-e-whatsapp.md)
   - [portal-clientes-convite-link-direto.md](portal-clientes-convite-link-direto.md)
   - [portal-clientes-aviso-de-edital-novo.md](portal-clientes-aviso-de-edital-novo.md)
8. **[portal-clientes-sql-direto/](portal-clientes-sql-direto/)**: os scripts aplicados direto no banco, fora das migrações do Lovable, com o retrato de antes e o resultado. Na cópia preparada para o ChatGPT, os `.sql` foram renomeados para `.sql.txt` para o upload aceitar.

## O que está publicado e funcionando

- As 7 etapas, com os prazos calculados a partir do último dia das inscrições e dos três ritmos.
- Registro de tudo no banco, com autor e data.
- Ideia do Projeto nas três formas, e o projeto por versões, com aprovação presa à versão.
- Tudo liberado para a administradora, que faz e apaga pelo cliente, e a página de cada organização.
- Convite por e-mail e por WhatsApp, com link que abre direto o cadastro do cliente.

## O que está pronto e ainda não publicado

- **Aviso de edital novo** ([portal-clientes-aviso-de-edital-novo.md](portal-clientes-aviso-de-edital-novo.md)): o bloco "Avisar o cliente" na página do edital.

## O que ainda falta construir

- Pacotes 5 a 13 da arquitetura: documentos com anexo, Farol e painel de alertas, visão nova do cliente, painel de resultados, exportação e os e-mails automáticos.
- O e-mail automático depende do domínio da Mobilizando verificado no serviço de envio.

## Em aberto

- Teste na tela, ponta a ponta, com uma conta de cliente. O portal está sem nenhum edital cadastrado.
- A numeração das versões do projeto reaproveita o número de uma versão apagada.
- As respostas do OK e da ideia e os documentos não guardam o autor; preenchidos pela administradora, contam como atividade do cliente na trava de mover o edital de organização.
- Regerar o Word, o PDF e o HTML antigos do "Como trabalhamos juntos" a partir do `.md` atualizado.

## Regras de trabalho do projeto

- A captadora publica; nada é publicado por outra pessoa ou ferramenta.
- Economizar crédito do Lovable: banco, regras e gatilhos por SQL direto sempre que possível; tela e migração em uma mensagem só.
- Toda mudança é conferida: retrato do banco antes, teste que se desfaz sozinho, diferença do código e, depois da publicação, o site no ar.
- Nenhum dado de teste permanente.
- Texto para o cliente em português do Brasil, sem travessão.

## Crédito do Lovable gasto até aqui

PDF do edital 3,8 + correção do login 0,9 + aviso de documentos 1,0 + botão "Marcar como enviado" 1,5 + Ideia do Projeto 6,1 + projeto por versões 7,1 + prazo real e comprovante 4,3 + administradora pode tudo 6,1 + convite 3,5 + link do convite 4,3 + aviso de edital 2,2 = **40,8 créditos**.
