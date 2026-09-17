# Portal do Cliente. Pacote 7B, etapa 1: as três formas da Ideia do Projeto

> **Aprovada pela captadora e aplicada em 14/09/2026. Ainda não publicada**, porque ela revisa antes.
>
> **Execução**
> - **Lovable:** 1 mensagem, **6,1 créditos**, versão `015cc496` para `45c3f22b`. Migração `20260914234402_bf5eacf0`.
> - **SQL direto, 0 crédito:** tipos de arquivo do espaço, `registra_evento_resposta` e `trava_mover_edital_com_atividade`. O arquivo é `docs/portal-clientes-sql-direto/2026-09-14-pacote-7b-banco.sql`.
>
> **Conferência**
> - Funções, gatilhos, regras e permissões antigas estão iguais ao retrato.
> - Teste desfeito com 18 passos aprovados, e 0 dado de teste guardado.
> - **Divergência:** a administradora só anexa na forma C se o cliente já tiver escolhido "Já tenho o esboço em arquivo", porque a escolha da forma é travada para ela. A proposta P3 fica em parte sem atender.
> Base: Mapa Operacional v1.0, seção 7 e decisões 18 a 24, que é a fonte da verdade; e "Como trabalhamos juntos", atualizado em 14/09.
> Fica para depois: a complementação (mapa 7.4), o Farol, os avisos e o painel.

## 1. Decisões da captadora (14/09)

| Nº | Ponto | Decisão |
|---|---|---|
| 1 | Tipos de arquivo | PDF, Word (DOC e DOCX), imagem (JPG e PNG) e planilha |
| 2 | Tamanho | até 20 MB por arquivo |
| 3 | Quem anexa | a administradora e o cliente |
| 4 | Quem remove | só a administradora |
| 5 | Enviar | exige resposta |
| 6 | Ao enviar | a entrega vira "feito" sozinha |
| 7 | Complementação | depois |
| 8 | Esboço | os 11 itens da captadora; os 8 itens antigos saem |
| 9 | Nomes das opções | "Ainda estou começando", "Vou preencher o esboço aqui", "Já tenho o esboço em arquivo" |
| 10 | Obrigatórios do esboço | os 11 itens, menos o 10, Recursos necessários |
| 11 | Contador | sim, "N de 11 itens preenchidos" |
| 12 | Modelo Word para baixar | sim |

## 2. A tela da Etapa 4

As três formas são entradas da **mesma** Etapa 4, e não três etapas. A tela mostra só os campos da forma escolhida.

**Mensagem fixa**, no lugar do destaque de hoje (mapa 7.1):
> Sua ideia é o ponto de partida, não o projeto final. A Mobilizando desenvolve e adapta às regras e aos critérios do edital. O projeto pode mudar de formato, público ou valor para caber nas regras e pontuar melhor.

**Frase acima das opções:**
> Escolha a forma que combina com o que você já tem. Não precisa ser um texto pronto: responda o que souber, e o que faltar construímos juntos.

**As opções, com a explicação embaixo de cada uma**

| Opção | Explicação embaixo |
|---|---|
| Ainda estou começando | Tenho só a ideia. Respondo 5 perguntas curtas. |
| Vou preencher o esboço aqui | Escrevo o esboço seguindo 11 itens, um de cada vez. |
| Já tenho o esboço em arquivo | Tenho o esboço ou o projeto pronto. Anexo o documento. |

### A. Ainda estou começando (5 perguntas, todas obrigatórias)

| Pergunta | Dica embaixo (proposta, confirmar) |
|---|---|
| O que você quer fazer? | Em poucas palavras, a atividade ou a ação. Ex.: oficinas de teatro para jovens |
| Para quem? | Quem participa e, se souber, quantas pessoas |
| Onde? | O bairro, a cidade ou o espaço |
| Por que isso é importante? | O problema ou a necessidade que o projeto responde |
| O que você espera alcançar? | O que muda para as pessoas depois do projeto |

### B. Vou preencher o esboço aqui (11 itens)

| Item | Dica embaixo | Obrigatório |
|---|---|---|
| 1. Nome ou ideia do projeto | Mesmo que provisório. | sim |
| 2. Quem é o proponente | Pessoa, empresa, associação, coletivo, instituição etc. | sim |
| 3. Problema ou necessidade | O que o projeto pretende enfrentar ou transformar. | sim |
| 4. Público-alvo | Quem será beneficiado e, se possível, quantidade estimada. | sim |
| 5. Local de execução | Cidade ou território e, se já souber, os locais específicos. | sim |
| 6. Objetivo principal | O que você quer alcançar. | sim |
| 7. Atividades previstas | O que será feito na prática. | sim |
| 8. Resultados esperados | Quais mudanças ou entregas pretende gerar. | sim |
| 9. Duração aproximada | Por exemplo, 6, 12 ou 18 meses. | sim |
| 10. Recursos necessários | Uma estimativa de quanto imagina precisar, se souber. | **não** |
| 11. Diferencial da ideia | Por que esse projeto merece ser realizado e o que o torna diferente. | sim |

Embaixo dos campos, o contador "N de 11 itens preenchidos". Se falta algum obrigatório, a tela diz qual.

### C. Já tenho o esboço em arquivo

- Botão "Anexar documento". Embaixo: "Pode ser o esboço, um projeto anterior, uma apresentação ou uma planilha. PDF, Word, imagem ou planilha, até 20 MB."
- Tipos aceitos: PDF, DOC, DOCX, JPG, PNG, XLS, XLSX e CSV.
- Depois de anexar: o nome do arquivo e os botões Visualizar e Substituir; Remover só para a administradora.
- Link "Baixar o modelo Roteiro do esboço" (arquivo Word com os 11 itens), para quem prefere preencher com calma e anexar.

## 3. Regras de funcionamento (propostas para confirmar)

| Nº | Ponto | Proposta |
|---|---|---|
| P1 | Envio das formas A e B | botão "Enviar ideia" (A) ou "Enviar esboço" (B), só ativo com os obrigatórios preenchidos. Grava as respostas e marca a entrega como feita. Depois, o botão vira "Atualizar" e a entrega continua feita |
| P2 | Envio da forma C | anexar o arquivo já é o envio e marca a entrega como feita |
| P3 | A administradora anexa pelo cliente | o arquivo fica guardado e aparece para os dois, mas não marca a entrega, porque a entrega é do cliente |
| P4 | Substituir | a tela mostra só o arquivo mais recente. Como o cliente não apaga arquivo, os anteriores ficam guardados |
| P5 | Remover (só a administradora) | apaga todos os arquivos da ideia daquele edital. A entrega continua feita |
| P6 | Trocar de forma depois de enviar | pode. As respostas da forma antiga ficam guardadas e escondidas |
| P7 | O que a administradora vê | a forma escolhida e as respostas, travadas; na forma C, também Anexar, Substituir e Remover |
| P8 | Privacidade | "O portal guarda o PDF do edital e os arquivos que a organização envia na Ideia do Projeto, visíveis só para a organização e para a Mobilizando. Não guarda documento pessoal, CPF nem dado bancário." |
| P9 | Página pública "Como trabalhamos juntos" | a seção "O roteiro do esboço" vira "A ideia do projeto: três formas de enviar", com as 5 perguntas, os 11 itens e a linha sobre anexar, igual ao documento atualizado |

## 4. O que muda, e por qual caminho

**Pelo Lovable, numa única mensagem (estimativa de 5 a 7 créditos)**

1. **Migração**
   - 16 colunas de texto novas em `respostas`:
     - forma A: `ideia_o_que_fazer`, `ideia_para_quem`, `ideia_onde`, `ideia_por_que`, `ideia_resultado`;
     - forma B: `esboco_nome`, `esboco_proponente`, `esboco_problema`, `esboco_publico`, `esboco_local`, `esboco_objetivo`, `esboco_atividades`, `esboco_resultados`, `esboco_duracao`, `esboco_recursos`, `esboco_diferencial`.
   - As 8 colunas antigas do esboço deixam de ser usadas pela tela. Estão vazias (0 respostas em 14/09) e ficam no banco até uma limpeza decidida depois.
   - `esboco_modo` passa a guardar os três nomes novos.
   - Espaço de arquivos privado `ideia-documentos`, até 20 MB, com os tipos da seção 2C. Endereço: `{edital}/{data e hora}-{nome}`.
   - 3 regras de acesso em `storage.objects`:
     - **ler:** a administradora, ou o cliente da organização, com o edital não apagado;
     - **anexar:** a administradora, ou o cliente da organização, com o edital em andamento;
     - **apagar:** só a administradora, com o edital em andamento.
   - Gatilho de registro nesse espaço: "Anexou o documento da ideia" (com o nome) e "Removeu o documento da ideia".
2. **Arquivo público** `public/roteiro-do-esboco.docx`, que é o modelo Word, enviado junto com a mensagem.
3. **Código**
   - `src/lib/etapas.ts`: as três formas, as 5 perguntas, os 11 itens, a frase e a mensagem fixa. Sai `CAMPOS_ESBOCO` antigo.
   - `src/components/portal/edital.tsx`: a parte da Etapa 4.
   - `src/lib/ideia-documento.ts` (novo): anexar, listar, abrir e remover, no mesmo modelo do PDF do edital.
   - `src/routes/index.tsx`: seção pública.
   - `src/routes/privacidade.tsx`: a frase.
   - `types.ts` atualizado pelas colunas novas.

**Por SQL direto, sem crédito, depois da migração**

4. `registra_evento_resposta`: passa a olhar as 16 colunas novas no "Enviou/Atualizou o esboço, objeto ou ideia", dizendo quais campos mudaram, sempre só com mudança real (decisão 16).
5. `trava_mover_edital_com_atividade`: passa a contar as 16 colunas novas e os arquivos da ideia como atividade do cliente.
6. Se o Lovable criar o espaço sem os tipos de arquivo, corrigir como foi feito no PDF do edital.

**Sem crédito, já feito em 14/09**

7. Mapa Operacional: decisões 18 a 24 e seção 7.2.
8. `marketing/entregas/comercial/como-trabalhamos-juntos.md` atualizado.
9. Modelo `marketing/entregas/comercial/Roteiro do esboço - Mobilizando.docx` criado.

**Não muda:** Etapas 3, 5, 6 e 7; prazos; Farol; documentos extras; PDF do edital; permissões das tabelas; `sandbox_exec`; exportar tudo. Os campos novos entram na exportação só no Pacote 11.

## 5. Conferência

- Retrato do banco antes e depois. A diferença de arquivos tem de ficar só nos listados na seção 4.
- Teste desfeito, em transação:
  - o cliente grava as formas A e B; o banco não impede enviar incompleto, porque o obrigatório é conferido na tela;
  - a entrega vira feita, e o registro tem uma linha por mudança real;
  - o cliente anexa na forma C; o cliente de outra organização não lê nem anexa;
  - o cliente não apaga; a administradora apaga;
  - em edital finalizado, nada é aceito.
- Nenhum dado de teste guardado. Não publicar até a captadora revisar.

## 6. Riscos e pendências

1. **"Apagar de vez" um edital não apaga os arquivos da ideia,** igual ao PDF do edital. Fica para o Pacote 7.
2. **O gatilho de registro no armazenamento** depende de o Lovable conseguir criá-lo. Se não conseguir, o anexo aparece no registro só pela marcação da entrega.
3. **Teste na tela** das três formas só é possível com conta de cliente.
4. **Versões antigas guardadas** quando o cliente substitui (P4) ocupam a cota.
5. **Obrigatório só na tela:** o banco aceita resposta incompleta. É uma escolha para não travar rascunho; se precisar, uma trava no banco entra depois, sem crédito.
6. **Cópias antigas de "Como trabalhamos juntos"** (`.docx`, `.pdf` e `.html`, de 11/09) ainda trazem o roteiro de 8 itens. Precisam ser geradas de novo antes de ir a um cliente.
