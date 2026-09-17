# Portal do Cliente. Pacote 4, correções de tela

> **Situação em 14/09/2026: APLICADO E CONFERIDO; CÓDIGO AINDA NÃO PUBLICADO NO SITE.**
> - **Banco, SQL direto, 0 crédito:** `docs/portal-clientes-sql-direto/2026-09-14-pacote-4-banco.sql`. Retrato conferido antes; trava `trava_mover_edital_com_atividade_trg` criada; `registra_evento_edital` com "Voltou ao ritmo sugerido" (md5 `ca541208`). Teste desfeito aprovado em todos os passos, inclusive estado atual, autoria, sem sessão e salvar outros dados com atividade. Depois: 24 regras iguais; os outros 24 gatilhos iguais; permissões de tabelas e das funções anteriores iguais; Etapa 2 do pacote 3 intacta; `sandbox_exec` igual; 0 dados de teste.
> - **Lovable, uma mensagem, 2,9 créditos:** texto da seção 4.1; versão `167caa16` para `4adbf2f3`; só `agenda.ts` e `edital.tsx`; sem migração; sem plano; compilou uma vez; etapa 4 intacta.
> - **Conferência depois:** o banco segue igual ao de depois do SQL direto (o Lovable não mexeu em banco).
> - **Pendência:** portal.mobilizando.org ainda serve o pacote anterior (`index-CL0wm02P`), então o pacote 4 precisa ser publicado no Lovable pela captadora. Enquanto isso não quebra nada: a tela antiga grava o ritmo preenchido e já mostra a recusa da trava.
> - Testes T1 a T6 no primeiro edital real, depois da publicação.
>
> **Texto original da especificação:** Escrita em 14/09/2026 sobre o Mapa Operacional v1.0, a arquitetura consolidada (seções 1, 2.10 e 3) e o código atual lido sem crédito (`edital.tsx`, `agenda.ts`, `prazos.ts`, o site publicado) e o banco lido por SELECT.
>
> **Caminho híbrido:** o banco vai por SQL direto (sem crédito), e o código por uma única mensagem curta ao Lovable.
>
> **Base:** o pacote 3 está concluído. Os gatilhos de registro já cobrem nome, órgão, link, organização, ritmo e edição de documento.

## Decisões da captadora (14/09/2026)

1. **Teste na tela:** no primeiro edital real. Sem Organização Teste e sem edital de teste persistente.
2. **Atividade do cliente:** qualquer marcação, resposta, pergunta ou documento marcado como enviado por um cliente.
3. **Histórico de "voltar ao sugerido":** "Voltou ao ritmo sugerido".
4. **Edital inexistente ou sem acesso:** "Este edital não existe ou você não tem acesso a ele."
5. **Trava de mover organização:** gatilho por SQL direto, desde que preserve integralmente as regras de segurança e não exija mudança de tipos.

## Dependência adicional encontrada na conferência

**O cálculo de prazos não aplica o ritmo sugerido quando o ritmo está vazio.**
- `src/lib/agenda.ts`, `prazosDoEdital`, chama `calcularPrazos(dia_d, data_dossie, edital.ritmo)`.
- `calcularPrazos` devolve nada quando o ritmo é vazio.
- Se o pacote só gravasse o ritmo vazio (defeito 10), os prazos daquele edital virariam "A calcular" no painel, em "O que depende de você", na régua e nas etapas.

**Correção:** `prazosDoEdital` passa a usar o ritmo gravado ou, se vazio, o sugerido (`ritmoSugerido`, que já existe em `prazos.ts`).
- Isso **aplica a regra da especificação original**: "ao abrir um edital sem ritmo escolhido, o portal sugere o mais folgado que cabe". Não cria regra nova.
- Se nenhum ritmo couber, continua "A calcular", com o aviso que já existe.

**Consequência:** o Lovable passa a mexer em 2 arquivos, e não 1: `edital.tsx` e `agenda.ts`.

## Pontos de interpretação (propostas, para confirmar junto da autorização)

1. **Atividade é o estado atual.** Marcação feita e depois desfeita não conta. Se preferir que conte, a trava passa a ler o histórico em vez das tabelas.
2. **Resposta e documento marcado como enviado contam como atividade do cliente**, mesmo sem o banco guardar quem os gravou: pela tela, só o cliente grava resposta e marca "enviado". Marcação e pergunta têm autor gravado e são conferidas pelo papel.
3. **Mensagem da recusa:** "Este edital já tem atividade do cliente e não pode mudar de organização."
4. **Preenchimento de nome, órgão e link:** nome e órgão obrigatórios; link opcional, sem checagem de formato. É a mesma regra do cadastro de edital novo, que já existe.
5. **A mensagem amigável aparece para qualquer falha ao abrir o edital** (inexistente, sem acesso, endereço inválido ou queda de conexão), para nunca mostrar texto técnico.

---

## 1. Objetivo

Fechar os buracos de uso da página do edital (defeitos 8, 10, 12, 15 e 16), sem tela nova, sem mudar permissões e sem tocar na Ideia do Projeto.

## 2. Escopo

### 2.1 Entra

| Defeito | Correção | Onde |
|---|---|---|
| 8 | mover de organização só sem atividade do cliente | banco (SQL direto); a tela já mostra a mensagem do banco |
| 10 | voltar ao ritmo sugerido, gravando o ritmo vazio; prazos seguem o sugerido; histórico "Voltou ao ritmo sugerido" | banco (SQL direto) e código |
| 12 | o atalho de "O que depende de você" abre a etapa | código |
| 15 | editar nome, órgão e link do edital; editar a linha de documento | código |
| 16 | mensagem amigável para edital inexistente ou sem acesso | código |

### 2.2 Não entra

- **Ideia do Projeto** (formas A, B e C e complementação), **nem versão provisória**: `CamposEsboco`, `OPCOES_ESBOCO` e `CAMPOS_ESBOCO` ficam intactos.
- Farol, "O que é seu agora?", "Fazer agora" e etapa da jornada (pacotes 8 e 9).
- Obrigatório ou facultativo, conferência, anexo e confirmação da submissão (pacote 7).
- Encerramentos, desistência e prazo perdido (pacote 6).
- Pessoas, convites e "sem acesso" (pacote 5).
- Defeito 9, já corrigido no pacote 3.
- Qualquer mudança de permissão, regra de acesso ou tipo.
- `sandbox_exec`.

---

## 3. Parte por SQL direto (sem crédito)

**Quando:** antes da mensagem ao Lovable, com o OK da captadora.

**Método:**
1. Salvar o SQL em `docs/portal-clientes-sql-direto/`.
2. Tirar retrato.
3. Aplicar num bloco que confere o retrato.
4. Comparar com o retrato.
5. Rodar um teste em transação desfeita.

**Não muda tipos:** funções de gatilho não entram no `types.ts`. Comprovado no pacote 3, em que só `desmarcar_entrega` entrou.

### 3.1 Texto do histórico ao voltar ao sugerido

`CREATE OR REPLACE` de `public.registra_evento_edital()`, com a assinatura atual `24535ae1` conferida antes, igual à de hoje em tudo, menos dois trechos:

```sql
-- trecho 1: só o ritmo mudou
IF _mudou_ritmo AND NOT (_mudou_org OR _mudou_dia_d OR _mudou_dossie OR _mudou_nome OR _mudou_orgao OR _mudou_link) THEN
  IF NEW.ritmo IS NULL THEN
    PERFORM private.grava_registro(NEW.id, 'Voltou ao ritmo sugerido', NULL);
  ELSE
    PERFORM private.grava_registro(NEW.id, 'Mudou o ritmo', private.nome_ritmo(NEW.ritmo));
  END IF;

-- trecho 2: ritmo mudou junto com outros dados
IF _mudou_ritmo THEN
  _lista := _lista || CASE WHEN NEW.ritmo IS NULL THEN 'voltou ao ritmo sugerido' ELSE 'ritmo para ' || private.nome_ritmo(NEW.ritmo) END;
END IF;
```

- A execução, o dono, a proteção e o `search_path` ficam como estão: `CREATE OR REPLACE` preserva as permissões.
- O gatilho `registra_evento_edital_trg` não é recriado.

### 3.2 Trava de mover organização

```sql
CREATE OR REPLACE FUNCTION public.trava_mover_edital_com_atividade()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, private
AS $$
BEGIN
  IF NEW.organizacao_id IS NOT DISTINCT FROM OLD.organizacao_id THEN
    RETURN NEW;
  END IF;

  IF EXISTS (
       SELECT 1 FROM public.marcos m
         JOIN public.papeis p ON p.user_id = m.feito_por AND p.role = 'cliente'
        WHERE m.edital_id = OLD.id)
     OR EXISTS (
       SELECT 1 FROM public.respostas r
        WHERE r.edital_id = OLD.id
          AND COALESCE(
                private.texto_limpo(r.ok_escolha), private.texto_limpo(r.ok_observacoes),
                private.texto_limpo(r.esboco_modo), private.texto_limpo(r.esboco_o_que),
                private.texto_limpo(r.esboco_para_quem), private.texto_limpo(r.esboco_onde),
                private.texto_limpo(r.esboco_quando), private.texto_limpo(r.esboco_como),
                private.texto_limpo(r.esboco_com_quem), private.texto_limpo(r.esboco_quanto),
                private.texto_limpo(r.esboco_o_que_existe), private.texto_limpo(r.aprovacao_escolha),
                private.texto_limpo(r.aprovacao_ajustes), private.texto_limpo(r.aprovacao_nome_cargo)
              ) IS NOT NULL)
     OR EXISTS (
       SELECT 1 FROM public.perguntas q
        WHERE q.edital_id = OLD.id AND q.autor_papel = 'cliente')
     OR EXISTS (
       SELECT 1 FROM public.documentos_extras d
        WHERE d.edital_id = OLD.id AND d.enviado)
  THEN
    RAISE EXCEPTION 'Este edital já tem atividade do cliente e não pode mudar de organização.';
  END IF;

  RETURN NEW;
END;
$$;

REVOKE ALL ON FUNCTION public.trava_mover_edital_com_atividade() FROM PUBLIC, anon, authenticated;

CREATE TRIGGER trava_mover_edital_com_atividade_trg
BEFORE UPDATE OF organizacao_id ON public.editais
FOR EACH ROW EXECUTE FUNCTION public.trava_mover_edital_com_atividade();
```

**Segurança preservada:**
- nenhuma permissão nem regra de acesso muda;
- a função só lê e recusa, sem execução para `anon` e `authenticated`;
- as travas existentes seguem intactas. Todas são `BEFORE UPDATE`, e qualquer recusa desfaz a gravação.

**Na tela:** `DadosEdital` já mostra `error.message` numa notificação. A recusa aparece sem mudança de código.

### 3.3 Teste desfeito do SQL direto (sem crédito, com OK)

1. Edital sem atividade muda de organização, e o histórico registra "organização para ...".
2. A mudança é recusada com a mensagem, e nada muda, depois de cada uma destas situações:
   - marcação do cliente;
   - resposta com conteúdo;
   - pergunta do cliente;
   - documento marcado como enviado.
3. A administradora marca "projeto" (autor administradora) e a troca continua permitida, porque não é atividade do cliente.
4. Ritmo de "padrao" para vazio: "Voltou ao ritmo sugerido". Ritmo para "apertado": "Mudou o ritmo, Apertado (10 dias)". Dia D e ritmo vazio juntos: "dia D para ...; voltou ao ritmo sugerido".
5. Salvar os mesmos dados não gera linha.
6. Comparação com o retrato:
   - 24 regras iguais;
   - os 25 gatilhos anteriores iguais, menos a assinatura de `registra_evento_edital`, que muda de propósito;
   - mais 1 gatilho novo;
   - permissões iguais;
   - `sandbox_exec` intocado;
   - 0 dados de teste.

---

## 4. Parte pelo Lovable (código)

**Arquivos:** `src/lib/agenda.ts` e `src/components/portal/edital.tsx`. Nenhum outro.

| Arquivo | Trecho | Mudança |
|---|---|---|
| `agenda.ts` | `prazosDoEdital` | usa o ritmo gravado ou, se vazio, `ritmoSugerido(dia_d, data_dossie)` |
| `edital.tsx` | `PaginaEdital` | qualquer erro ao abrir mostra "Este edital não existe ou você não tem acesso a ele." |
| `edital.tsx` | `DadosEdital` | campos Nome do edital, Órgão e Link do edital (opcional), só para a administradora e só em andamento; salvar grava nome e órgão sem espaços nas pontas e link vazio como nulo; "Salvar dados do edital" desabilitado com nome ou órgão vazios; o ritmo passa a gravar `ritmo \|\| null` em vez de `ritmo \|\| sugerido` |
| `edital.tsx` | `EtapasEdital` e `Dependencias` | ao chegar ou clicar num endereço `#etapa-N`, a etapa N abre; clicar de novo no mesmo cartão reabre |
| `edital.tsx` | `Documentos` | botão "Editar" por linha, só para a administradora e só em andamento; vira dois campos com "Salvar" e "Cancelar"; "Salvar" desabilitado com documento vazio ou igual |

**Não muda:**
- a aparência fora desses campos;
- a Ideia do Projeto;
- as outras etapas, a régua, a tabela de ritmos, as notas e as ações da Mobilizando;
- o registro (o banco já registra).

### 4.1 Texto mínimo a enviar (copiar daqui, só depois da autorização e do SQL direto aplicado)

> Pacote 4. Só `src/lib/agenda.ts` e `src/components/portal/edital.tsx`. Não crie plano, migração nem teste de navegador; não leia outros arquivos; compile uma vez. O banco já foi ajustado direto (registro pelo banco, trava de mover organização e texto "Voltou ao ritmo sugerido"): não mexa em banco, permissões, regras nem gatilhos, e não recrie INSERT em registro nem DELETE em marcos.
>
> 1. agenda.ts, prazosDoEdital: use `edital.ritmo ?? (edital.dia_d && edital.data_dossie ? ritmoSugerido(edital.dia_d, edital.data_dossie) : null)` no lugar de `edital.ritmo`, importando `ritmoSugerido` de ./prazos.
> 2. edital.tsx, PaginaEdital: no Aviso de erro ao abrir, mostre sempre "Este edital não existe ou você não tem acesso a ele."
> 3. DadosEdital: acrescente, em uma linha acima dos campos atuais, os campos "Nome do edital", "Órgão" e "Link do edital" (dica "Opcional"), com o mesmo estado travado dos outros. No salvar, grave também nome e órgão com trim e link com trim ou null, e troque `ritmo: proximoRitmo` por `ritmo: ritmo || null`. Desabilite "Salvar dados do edital" se nome ou órgão estiverem vazios.
> 4. EtapasEdital: num useEffect, leia `window.location.hash` no formato `#etapa-N`, ao montar e no evento hashchange, e acrescente N a `abertas`. Em Dependencias, no clique do cartão, se o hash já for o mesmo, dispare `window.dispatchEvent(new HashChangeEvent("hashchange"))`.
> 5. Documentos: para a administradora em edital em andamento, um botão "Editar" por linha que troca documento e onde pede por dois campos com "Salvar" e "Cancelar"; "Salvar" faz update de documento (trim) e onde_pede (trim ou null) e fica desabilitado se documento estiver vazio ou nada mudar; mostre o erro do banco em toast.
>
> Não altere nada além disto, em especial a etapa 4 (esboço). Português do Brasil, com acentuação e sem travessão.

---

## 5. Critérios de aceite

**Banco (SQL direto)**
- B1. Existe `trava_mover_edital_com_atividade_trg` (BEFORE UPDATE OF `organizacao_id` em `editais`), com a função sem execução para `anon` e `authenticated`.
- B2. `registra_evento_edital` registra "Voltou ao ritmo sugerido" e "voltou ao ritmo sugerido" na lista; o resto do texto fica igual.
- B3. 24 regras iguais; os outros 24 gatilhos com assinatura igual; permissões iguais; `sandbox_exec` intocado; `types.ts` sem necessidade de mudança.
- B4. O teste desfeito (3.3) passa, e ficam 0 dados de teste.

**Código (Lovable)**
- C1. A diferença entre versões mostra só `agenda.ts` e `edital.tsx`.
- C2. `prazosDoEdital` com ritmo vazio usa o sugerido; com ritmo gravado, fica igual.
- C3. `CamposEsboco`, `OPCOES_ESBOCO`, `CAMPOS_ESBOCO` e `etapas.ts` sem mudança.
- C4. Nenhuma migração nova; conferência de que o INSERT em `registro` e o DELETE em `marcos` continuam fora.
- C5. O portal compila e o site publicado traz o código novo.

**Na tela (no primeiro edital real, decisão 1)**
- T1. A administradora edita nome, órgão e link, e o histórico ganha uma linha; salvar sem mudança não gera linha; nome ou órgão vazio não salva.
- T2. "Usar o sugerido" grava ritmo vazio, os prazos continuam calculados pelo sugerido, e o histórico mostra "Voltou ao ritmo sugerido".
- T3. Clicar num cartão de "O que depende de você" abre a etapa; clicar de novo reabre.
- T4. Endereço de edital inexistente mostra a mensagem amigável.
- T5. Com atividade do cliente, trocar a organização mostra a recusa e nada muda.
- T6. Editar linha de documento funciona e registra.
- Também no primeiro edital real: as pendências de tela do pacote 3.

## 6. Créditos

| Parte | Estimativa |
|---|---|
| SQL direto (3.1 e 3.2) e teste desfeito | **0** |
| Lovable, 2 arquivos, mensagem curta, sem plano, sem migração e sem navegador | **mínimo 2**; provável 2 a 4; teto observado 5 a 6 |
| Conferência depois (diferença entre versões, site publicado e banco) | **0** |

**Por que o mínimo não é zero:** o Lovable cobra mesmo para ler os dois arquivos e compilar. O menor pacote até hoje (nome da organização, um arquivo e uma migração) custou 1,9.

## 7. Ordem de execução, depois da autorização

1. SQL direto 3.1 e 3.2: retrato, aplicação conferida e comparação.
2. Teste desfeito 3.3. **Se falhar, parar.**
3. Mensagem 4.1 ao Lovable, uma só.
4. Conferência sem crédito: diferença, site publicado e banco.
5. Parar e relatar. Os testes T1 a T6 ficam para o primeiro edital real.

## 8. Rollback

- **SQL direto:**
  - `DROP TRIGGER trava_mover_edital_com_atividade_trg ON public.editais;` e `DROP FUNCTION public.trava_mover_edital_com_atividade();`;
  - reaplicar `registra_evento_edital` com a definição de assinatura `24535ae1`, guardada no arquivo de SQL antes de aplicar.
- **Código:** restaurar no Lovable a versão anterior ao envio, anotando o identificador antes.
- **Histórico:** as linhas criadas no meio ficam, porque o registro não se apaga.

## 9. Riscos

| Risco | Como reduzir |
|---|---|
| O Lovable ler ou mudar mais do que o pedido e gastar mais | texto curto e fechado; conferência C1 e C3 |
| O Lovable recriar permissões da Etapa 2 ou mexer em gatilhos | aviso na mensagem; conferência C4 e retrato |
| A troca de `prazosDoEdital` mudar a leitura de editais com ritmo gravado | só age com ritmo vazio; hoje nenhum edital existe, e o cadastro grava o ritmo |
| Resposta ou documento gravado pela administradora por fora da tela contar como atividade do cliente | interpretação 2; só é possível por fora da tela |
| Mais drift entre o banco e as migrações do Lovable | registrar em `docs/portal-clientes-sql-direto/` e avisar na mensagem |
