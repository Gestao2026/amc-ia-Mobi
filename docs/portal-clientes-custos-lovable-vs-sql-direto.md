# Portal do Cliente. Custo por pacote: só Lovable ou híbrido com SQL direto

> **Comparação, escrita em 14/09/2026. Nada foi aplicado.** Serve para decidir, pacote a pacote, o que vai pelo Lovable e o que a AMC IA aplica direto no banco, sem crédito.

## 1. O que já foi gasto (valores informados pelo Lovable)

| Envio | Previsto | Real |
|---|---|---|
| Construção, 12 e 13/09 | não havia | cerca de 12,6 |
| Pacote 1 | ~1 | 2,1 |
| Pacote 2 (primeiro envio e continuação) | 2,5 a 3 | 10,0 (1,1 + 8,9) |
| Nome da organização | ~1 | 1,9 |
| Pacote 3, Etapa 1 | ~3 | 8,0 |
| **Total conhecido** | | **cerca de 34,6** |

Sem valor registrado: o pedido da logomarca e uma pergunta curta de madrugada.

**Fator observado em 14/09:** 22 créditos reais contra cerca de 7,5 previstos, ou **quase 3 vezes**. Mandar o SQL pronto não reduziu o custo da Etapa 1: o Lovable gasta lendo arquivos inteiros, compilando e conferindo por conta própria.

## 2. Os dois caminhos

**Só Lovable.** Banco e código na mesma mensagem.
- A migração fica registrada em `supabase/migrations/`.
- O arquivo de tipos (`types.ts`) é regenerado.
- O Lovable fica sabendo de tudo.

**Híbrido.**
- A AMC IA aplica o SQL direto pela conexão de consulta, com custo zero de crédito.
- O Lovable recebe só a parte de código.

### Regra para decidir, por tipo de mudança

| Mudança de banco | Caminho | Por quê |
|---|---|---|
| Revogar ou conceder permissão, criar ou remover regra de linha | **SQL direto** | não muda os tipos do código |
| Corpo de gatilho ou função interna (sem ser chamada pela tela) | **SQL direto** | não muda os tipos |
| Índice, checagem, correção de dado | **SQL direto** | não muda os tipos |
| Agendamento (`pg_cron`) | **SQL direto** | não muda os tipos |
| Tabela nova, coluna nova, função chamada pela tela, armazenamento de arquivos | **Lovable** | o `types.ts` precisa ser regenerado, senão o código não compila ou o Lovable não enxerga o dado |
| Função de servidor (edge function) e todo código de tela | **Lovable** | só o Lovable edita o código |

### A troca, e como reduzir

| Risco do SQL direto | Como reduzir |
|---|---|
| A mudança não fica na pasta de migrações do projeto | todo SQL direto é salvo antes, na íntegra, em `docs/portal-clientes-sql-direto/AAAA-MM-DD-nome.sql`, com um registro de quem autorizou, quando e o resultado |
| O Lovable não sabe da mudança e pode "desfazer" num pacote futuro | toda mensagem ao Lovable passa a dizer, em uma linha, o que foi aplicado direto desde o último envio, e a conferência depois de cada pacote compara as permissões, regras e gatilhos com o retrato anterior |
| Um projeto recriado a partir das migrações nasceria sem essas mudanças | numa mensagem futura que já vá ao Lovable, pedir que ele grave as mudanças diretas como uma migração "já aplicada" (custo baixo, junto de outro pacote) |
| Erro de SQL aplicado sem compilação do portal | só entra por SQL direto o que não mexe em tipos, e tudo passa por uma transação com teste antes |

**Toda aplicação direta continua pedindo o OK da captadora a cada vez**, como os envios ao Lovable.

## 3. Comparação pacote a pacote

A estimativa "só Lovable" aplica o fator observado (entre 2,5 e 3) às estimativas originais da arquitetura. É projeção, não medição.

| Pacote | O que é banco puro (SQL direto) | O que precisa do Lovable | Só Lovable | Híbrido |
|---|---|---|---|---|
| 3, Etapa 2 | 4 linhas: revogar INSERT em `registro`, remover "registro cria", revogar DELETE em `marcos`, remover "marcos cliente desmarca os seus" | nada | 1 a 3 | **0** |
| 4, correções de tela | trava de "mover edital" com atividade do cliente, se feita como gatilho | "voltar ao sugerido", atalho, mensagem amigável, editar nome, órgão, link e linha de documento | 7 a 8 | 6 a 7 |
| 5, pessoas e convites | regra de "sem acesso" no cadastro (gatilho do cadastro e regras de linha) | tela Pessoas, estado "Aguardando liberação" | 8 a 11 | 7 a 9 |
| 6, encerramentos e prazo | travas e checagens de motivo | colunas novas (`desfecho`, `motivo_nao_submissao`, datas) e as telas | 8 a 11 | 6 a 9 |
| 7, documentos | regras de acesso do armazenamento, checagens de situação | coluna `obrigatorio`, tabela de versões, armazenamento, telas, confirmação da submissão | 13 a 16 | 10 a 13 |
| 7B, Ideia e complementação | gatilhos de registro dos dados novos | tabela de complementos, colunas das formas A e C, telas | 8 a 11 | 7 a 9 |
| 8, motor de alertas e Farol | quase nada | `alertas.ts`, etapa da jornada, painel da administradora | 12 a 15 | 12 a 15 |
| 9, visão do cliente | nada | telas | 9 a 12 | 9 a 12 |
| 10, painel de resultados | nada | telas e consultas | 7 a 8 | 7 a 8 |
| 11, organização e exportação | nada | ficha e exportação | ~8 | ~8 |
| 12, preparação dos e-mails | regras de acesso das tabelas de envio | tabelas novas, telas de configuração e prévia | 8 a 9,5 | 6 a 8 |
| 13, envio dos e-mails | jobs do `pg_cron` | função de envio e integração com o serviço | 22 a 27 | 18 a 23 |
| **Total** | | | **111 a 139,5** | **96 a 121** |

**Economia do híbrido: cerca de 15 a 18 créditos, entre 13% e 15%.** A economia é modesta porque a maior parte do custo é código de tela, que só o Lovable edita.

## 4. Outras formas de gastar menos, sem aplicar nada ainda

1. **Mensagens mais secas ao Lovable:** "não rode testes de navegador, compile uma vez só, leia só as linhas indicadas". Não dá para medir o efeito antes, mas o que mais consumiu na Etapa 1 foi leitura e verificação.
2. **Juntar pacotes pequenos de código na mesma mensagem**, quando não dependem um do outro, para o Lovable ler os arquivos uma vez só.
3. **Maior alavanca, a investigar:** se o projeto do Lovable estiver ligado a um repositório do GitHub, o código também poderia ser editado fora do Lovable, sem crédito, e sincronizado. Isso exige conferir a ligação, decidir em qual repositório e se o envio ao GitHub é aceito para esse projeto. Nada disso foi verificado nem feito.

## 5. Recomendação

- **Etapa 2 do pacote 3 por SQL direto:** custo zero e sem mexer em tipos. **Antes, o teste de comportamento da Etapa 1**, também por conexão direta, numa transação desfeita, com custo zero e sem deixar dado.
- **Dali em diante, o híbrido pela regra da seção 2**, com o SQL salvo em `docs/portal-clientes-sql-direto/` e o OK da captadora a cada aplicação.
- **Investigar a ligação com o GitHub** antes do pacote 8, que é quase só código.
