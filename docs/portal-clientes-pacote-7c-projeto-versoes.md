# Portal do Cliente. Pacote 7C: projeto por versões, aprovação e submissão

> **Aprovada e aplicada em 14/09/2026. Não publicada.**
>
> **Execução**
> - Lovable: 1 mensagem, **7,1 créditos**, versão `45c3f22b` para `aebba0c8`. Migração `20260915002743_656c93d2`.
> - SQL direto, 0 crédito: `docs/portal-clientes-sql-direto/2026-09-14-pacote-7c-banco.sql`.
>
> **Conferência**
> - Teste desfeito com 26 passos aprovados.
> - O que já existia está igual ao retrato.
> - 0 dado de teste guardado.
>
> **Segunda mensagem, 14/09**
> - Lovable: **4,3 créditos**, versão `aebba0c8` para `71d2d7fc`, migração `20260915004424_40e66559`.
> - **Prazo pelo envio real** (decisão 6, aprovada pela captadora), por `ajustarPrazosPelasVersoes` em `prazos.ts`, que entra depois do cálculo de sempre e não mexe em `calcularPrazos`:
>   - a aprovação vale na data mais tarde entre a prevista e o envio da versão atual mais N dias úteis;
>   - depois de pedido de ajustes, o projeto vale na data mais tarde entre a prevista e o pedido mais N dias úteis;
>   - N = 1 no Apertado e 2 nos outros ritmos; nenhuma das duas passa da véspera da submissão;
>   - quando muda, a tela mostra as duas datas.
>   - Aplicado na página do edital e nos dois painéis.
> - **Correção da Etapa 7 para o cliente:** o bloco usa só a versão gravada.
> - **Registro "Anexou o comprovante":** teste desfeito aprovado; o arquivo de versão não gera essa linha.
> - Banco igual ao retrato, fora a função e o gatilho novos.
>
> **Pendências achadas na conferência**
> 1. ~~Defeito na tela do cliente, Etapa 7~~: corrigido na segunda mensagem.
> 2. ~~"Anexou o comprovante" fora do registro~~: corrigido na segunda mensagem.
> 3. **O `sandbox_exec` ganhou INSERT e SELECT em `projeto_versoes`** pela regra automática dele. Não foi alterado.
> 4. **O registro fica com linhas a mais:** além de "Enviou o projeto" e "Aprovou o projeto", as marcações automáticas geram "Marcou" e "Desmarcou entrega".
> Base: Mapa Operacional v1.0, decisões 25 a 33 (quinta rodada), seções 5.2, 8 e 9. "Como trabalhamos juntos", Etapas 5 a 7, atualizado em 14/09.

## 1. Decisões da captadora (14/09)

| Nº | Ponto | Decisão |
|---|---|---|
| 1 | Pedido de ajustes | a jornada volta para a Etapa 5 |
| 2 | Formato do projeto | PDF e Word |
| 3 | Versões antigas | o cliente vê e baixa todas |
| 4 | Apagar versão | nunca; o erro se corrige com uma versão nova e uma observação |
| 5 | Nova versão depois de aprovada | a aprovação volta a ficar pendente |
| 6 | Prazo da aprovação | **sem resposta; fica como está hoje nesta entrega** (ver seção 6) |
| 7 | Nome e cargo de quem aprovou | opcional |
| 8 | Comprovante | arquivo (PDF ou imagem), link ou os dois |
| 9 | Submissão sem a versão atual aprovada | não pede confirmação |

## 2. As telas

### Etapa 5. Elaboramos o projeto

**Administradora, com o edital em andamento**
- Bloco "Enviar projeto para aprovação":
  - arquivo PDF, DOC ou DOCX, até 50 MB;
  - "Observação para o cliente", opcional;
  - botão "Enviar versão".
- Ao enviar, o portal numera (V1, V2...), grava a data e quem enviou, e **conclui a etapa sozinho**.
- Perguntas e respostas continuam como hoje.
- **Sai o botão "Marcar como feito" desta etapa.**

**Os dois lados**
- "**Versão atual: V2**, enviada em 15/09/2026", com o nome do arquivo, a observação e "Baixar projeto".
- **Histórico do projeto:** tabela com Versão, Enviada em, Situação e Baixar.
- A Situação é uma destas:
  - "Aguardando sua aprovação";
  - "Aprovada em 16/09";
  - "Ajustes solicitados em 15/09";
  - "Substituída pela V3".

### Etapa 6. Você aprova ou pede ajustes

**Cliente, com o edital em andamento e uma versão atual sem resposta**
- "Projeto em análise: V2".
- Escolha única: "Aprovar esta versão" ou "Solicitar ajustes".
- Com "Solicitar ajustes", aparece "O que precisa mudar?", obrigatório.
- "Nome e cargo de quem aprovou", opcional.
- Botão "Enviar resposta".

**Depois da resposta** (os dois lados veem)
- "V2 aprovada em 16/09/2026 por {nome}" ou "Ajustes solicitados na V1 em 15/09/2026", com o texto.
- A resposta não se edita. Mudou de ideia? Pede ajustes, e a Mobilizando envia nova versão.
- **Sai o botão "Marcar como feito" desta etapa.**
- Os campos antigos da aprovação saem da tela. Estão vazios e ficam no banco.

**Sem versão enviada:** "O projeto ainda não foi enviado para a sua aprovação."

### Etapa 7. Submetemos o projeto

**Administradora**
- Campos de hoje (protocolo, data e hora), mais:
  - "Versão submetida": lista das versões, já marcando a última aprovada, ou a última enviada se nenhuma foi aprovada;
  - "Link do comprovante", opcional;
  - "Comprovante (arquivo)", opcional, com PDF, JPG ou PNG, os botões Visualizar e Substituir.
- Registrar sem a versão atual aprovada **não pede confirmação**.

**Cliente**
- "Projeto submetido: V2 · Protocolo 123456 · 16/09/2026, 14h32", com "Abrir comprovante" (arquivo e/ou link).

## 3. Como a jornada se comporta

| Acontecimento | Etapa 5 | Etapa 6 | De quem é a vez |
|---|---|---|---|
| A administradora envia V1 | concluída | aguardando | cliente |
| O cliente pede ajustes na V1 | **reaberta** | aberta | Mobilizando |
| A administradora envia V2 | concluída | aguardando | cliente |
| O cliente aprova a V2 | concluída | **concluída** | Mobilizando (submissão) |
| A administradora envia V3 depois da aprovação | concluída | **reaberta** (aprovação da V2 perde a validade) | cliente |

Por baixo, isso usa as marcações que já existem: `projeto` e `aprovacao`. **Quem marca e desmarca é o banco**, a partir das versões e das respostas, e não o botão da tela. Assim, o prazo, o painel e "O que depende de você" continuam funcionando sem mudança.

## 4. O que muda, e por qual caminho

**Pelo Lovable (uma mensagem, 7 a 9 créditos; ou duas, ver seção 7)**

1. **Migração**
   - Tabela nova `projeto_versoes`:
     - `id`, `edital_id` (apaga junto com o edital), `numero`;
     - `arquivo_caminho`, `arquivo_nome`, `observacao`;
     - `enviado_em`, `enviado_por`;
     - `resposta` (aprovado ou ajustes), `ajustes`, `nome_cargo`, `respondido_em` e `respondido_por`;
     - `numero` único por edital.
   - Regras de acesso de `projeto_versoes`:
     - **ler:** quem vê o edital;
     - **criar:** só a administradora, com edital em andamento;
     - **responder:** só o cliente da organização, com edital em andamento, só na versão mais recente e só se ela ainda não tiver resposta, pela função `responder_versao_projeto(versao, resposta, ajustes, nome_cargo)`;
     - **apagar:** ninguém.
   - Permissões: `authenticated` com SELECT e INSERT; sem UPDATE direto nem DELETE; `anon` sem acesso.
   - Em `editais`, colunas novas: `versao_submetida_id` (referência à versão) e `comprovante_link`.
   - Espaço de arquivos privado `projeto-arquivos`, até 50 MB, com PDF, DOC, DOCX, JPG e PNG. Pastas:
     - `{edital}/versoes/`;
     - `{edital}/comprovante/`.
   - Regras de acesso do espaço:
     - **ler:** quem vê o edital;
     - **anexar:** só a administradora, com edital em andamento;
     - **apagar:** só a administradora, com edital em andamento e só dentro de `comprovante/`.
2. **Código**
   - Etapas 5, 6 e 7 em `edital.tsx`.
   - Um arquivo novo para enviar e abrir arquivos do projeto e do comprovante.
   - `types.ts` com a tabela e as colunas novas.

**Por SQL direto, sem crédito, depois da migração**

3. **Gatilhos de `projeto_versoes`:**
   - `numero`, `enviado_em` e `enviado_por` definidos pelo banco;
   - ao criar uma versão: marca `projeto` e desmarca `aprovacao`;
   - ao responder "ajustes": desmarca `projeto`;
   - ao responder "aprovado": marca `aprovacao` com o cliente como autor;
   - `respondido_em` e `respondido_por` definidos pelo banco.
4. **Registro:**
   - "Enviou o projeto para aprovação: V2 (arquivo)";
   - "Aprovou o projeto: V2";
   - "Pediu ajustes no projeto: V1";
   - "Anexou o comprovante";
   - "Registrou a submissão" passa a dizer a versão.
5. **Travas:**
   - `trava_edital_fora_andamento` passa a proteger `versao_submetida_id` e `comprovante_link` em edital finalizado;
   - `trava_mover_edital_com_atividade` passa a contar a resposta do cliente numa versão.
6. **Tipos de arquivo do espaço**, se o Lovable criar sem a restrição, como aconteceu nas duas vezes anteriores.

**Sem crédito, já feito em 14/09**

7. Mapa Operacional: decisões 25 a 33; seções 5.2, 6, 8 e 9; pendências 5 e 6 encerradas.
8. `como-trabalhamos-juntos.md`: Etapas 5, 6 e 7.

**Não muda:** Etapas 1 a 4; prazos (ver seção 6); documentos extras; PDF do edital; Ideia do Projeto; painel; exportação; permissões existentes; `sandbox_exec`.

## 5. Conferência

- Retrato do banco antes e depois. A diferença de arquivos tem de ficar só nos listados.
- Teste desfeito, em transação:
  - a administradora envia V1: a etapa 5 fica feita e o registro grava a linha;
  - o cliente pede ajustes: a etapa 5 reabre;
  - o cliente não responde versão antiga nem responde duas vezes;
  - a administradora envia V2 e o cliente aprova: a etapa 6 fica feita;
  - a administradora envia V3: a aprovação cai;
  - cliente de outra organização não lê nem responde; ninguém apaga versão;
  - a submissão guarda a versão e o link, e não muda depois de finalizado;
  - o espaço de arquivos segue as regras de acesso.
- Nenhum dado de teste guardado. Não publicar até a captadora revisar.

## 6. Prazo da aprovação (decisão 6, pendente)

- **Hoje:** o prazo da aprovação é calculado a partir da data **prevista** do projeto (por exemplo, 2 dias úteis depois do D-6 no ritmo padrão).
- **Recomendação:** contar a partir do envio **real** de cada versão, mostrando as duas datas quando mudar ("nenhum prazo mascarado").
- **Isso mexe no motor de prazos** e fica fora desta entrega, até a captadora decidir. Custo estimado se aprovado: 1 a 2 créditos.

## 7. Uma ou duas mensagens

| Opção | Conteúdo | Crédito |
|---|---|---|
| **Uma mensagem** | Etapas 5, 6 e 7 juntas | 7 a 9 |
| **Duas mensagens** | primeiro as Etapas 5 e 6 (versões e aprovação); depois a Etapa 7 (versão submetida e comprovante) | 5 a 6, depois 2 a 3 |

## 8. Riscos e pendências

1. **Arquivos órfãos:** "apagar de vez" um edital apaga as versões da tabela, mas não os arquivos do espaço, como acontece com o PDF e a ideia. Fica para o Pacote 7.
2. **Teste das Etapas 5 e 6 na tela:** só com conta de cliente.
3. **O portal não diz quem é a pessoa responsável pela aprovação.** Qualquer pessoa da organização pode aprovar, como hoje.
4. **Cópias antigas de "Como trabalhamos juntos"** (`.docx`, `.pdf` e `.html`) continuam desatualizadas.
