# Portal do Cliente. PDF do edital (Etapa 1)

> Autorizado pela captadora em 14/09/2026. Aplicado e conferido no mesmo dia. **Publicado por ela em 14/09**. Conferido às 18h46 de Brasília: portal.mobilizando.org serve `index-BClxc3Q4.js`, com o PDF do edital no Novo edital, na página do edital e na Privacidade. O primeiro PDF real já está no espaço, na pasta do edital em andamento.
>
> **Teste na tela, 14/09:**
> - A primeira tentativa de substituir não gravou nada. O original ficou intacto, e não houve perda.
> - A segunda, às 18h52, funcionou: ficou só o PDF novo (1 arquivo, 1,5 MB, application/pdf), e o anterior foi apagado.
> - Abrir foi testado pela captadora. Esse passo não deixa marca no banco.
> - Falta abrir como cliente.

## O que entrou

- Espaço de arquivos privado `editais-pdf`, até 50 MB. Endereço de cada arquivo: `{código do edital}/{data e hora}-{nome sem acento}.pdf`.
- "PDF do edital" (opcional) no Novo edital, abaixo do link, e no bloco "Este edital" da página do edital: nome do arquivo e "Abrir PDF" para os dois lados; "Enviar PDF" ou "Substituir PDF" só para a administradora, com o edital em andamento.
- Substituir envia o novo e só depois apaga o anterior.
- Abrir usa link temporário de 300 segundos. Não existe link público.
- Privacidade: "O portal guarda apenas o PDF do edital, que é documento público. Não guarda documento pessoal, CPF nem dado bancário."
- O PDF do edital fica separado dos documentos da organização, que são do Pacote 7.

## Regras de acesso (storage.objects, só `authenticated`)

| Regra | Quem |
|---|---|
| `editais-pdf le quem ve o edital` (SELECT) | administradora sempre; cliente só do edital da própria organização e não apagado |
| `editais-pdf admin envia em andamento` (INSERT) | só administradora, só edital em andamento |
| `editais-pdf admin apaga em andamento` (DELETE) | só administradora, só edital em andamento |
| UPDATE e anon | nenhuma regra |

## Execução

- Lovable: uma mensagem, **3,8 créditos**, versão `4adbf2f3` para `88d88da2`.
- Arquivos: `src/lib/pdf-edital.ts` (novo), `src/routes/_authenticated/painel.tsx`, `src/components/portal/edital.tsx`, `src/routes/privacidade.tsx`, `supabase/migrations/20260914212859_29417932-3ac4-41c0-9924-302935fb3ef7.sql`.
- **Divergência:** o Lovable criou o espaço com a ferramenta própria dele, e não pela migração. A migração só tem as 3 regras. O espaço nasceu **sem a restrição de tipo** (`allowed_mime_types` vazio).
- **Corrigido em 14/09 por SQL direto**, com OK da captadora e sem crédito: `update storage.buckets set allowed_mime_types = array['application/pdf'] where id = 'editais-pdf';`. O bloco conferia o estado antes de aplicar.
  - Conferência: o espaço aceita só `application/pdf`, é privado e tem limite de 50 MB.
  - Banco idêntico ao retrato: regras, gatilhos, funções, colunas e permissões. As 3 regras do armazenamento também estão iguais.
  - Portal na mesma versão `88d88da2`.
  - Os 17 testes, repetidos e desfeitos, passaram de novo.
  - 0 arquivos e 0 usuários de teste.

## Conferência

- Banco antes e depois: 24 regras das tabelas, 26 gatilhos, 39 funções, colunas, permissões das tabelas e do armazenamento, `sandbox_exec` e `anon`, todos com assinatura idêntica. Etapa 2 do Pacote 3 intacta.
- Teste desfeito, 17 passos aprovados:
  - a administradora envia em edital em andamento;
  - recusados: envio pelo cliente, em edital finalizado, fora da pasta de um edital, em outro espaço e sem login;
  - o cliente A lê o PDF em andamento e o finalizado, e não lê o apagado;
  - o cliente B não lê nada da organização A; a administradora lê tudo;
  - ninguém altera arquivo;
  - o cliente não apaga; a administradora não apaga em finalizado, e apaga em andamento;
  - nenhuma linha nova no registro.
- Depois do teste: 0 usuários de teste, 0 arquivos, 1 edital real, 1 linha no registro.

## Riscos e pendências

1. Restrição de tipo no servidor: corrigida (ver Execução).
2. Enviar ou substituir o PDF não entra no registro do edital, por decisão.
3. "Apagar de vez" um edital não apaga o PDF, que fica guardado sem edital. Tratar junto com o Pacote 7.
4. Mais uma estrutura criada fora da migração (o espaço de arquivos).
5. No Novo edital, um arquivo que não seja PDF só é recusado depois de o edital ser criado. O edital é aberto, e o aviso manda enviar de novo na página do edital.
6. Teste na tela: depois da publicação, com o edital real.
