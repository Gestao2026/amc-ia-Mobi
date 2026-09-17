-- Portal do Cliente Mobilizando. Administradora pode tudo (decisões 34 a 38), parte de banco por SQL direto (sem crédito)
-- Autorização da captadora em 14/09/2026. Roda depois da mensagem do Lovable com a página da organização e a liberação das telas.
-- Não está em supabase/migrations.
--
-- Retrato de antes:
--   responder_versao_projeto md5 b7f8b1d680469ab5637eb8c4ef06976b
--   trava_mover_edital_com_atividade md5 94deba37c6f3702b0ac8aaf2cad49015
--   registra_evento_resposta md5 0577ac4c6862cace26d451eb0aa3ecdc
--   registra_evento_versao_projeto md5 9454dd4146ccfca25baa3756ff6ec7e3
--   projeto_versoes: sem DELETE para authenticated, 2 regras (ler e enviar)
--
-- RESULTADO (14/09/2026): aplicado sem erro, depois da mensagem do Lovable (6,1 créditos, versão 71d2d7fc para 2ff18070,
-- migração 20260915011458_4d55cd06 que troca a regra de apagar do espaço projeto-arquivos para comprovante e versões).
-- Teste desfeito, 11 passos aprovados:
--   a administradora responde o OK, envia a ideia, marca e apaga as respostas ("Apagou a resposta do OK" e "Apagou a resposta da ideia");
--   ela aprova a V1 e a etapa 6 fica feita no nome dela; a V2 derruba a aprovação;
--   apagar a V2 faz a V1 aprovada voltar a valer; sem versões, as etapas 5 e 6 abrem;
--   ela apaga o arquivo de versão; a resposta dela não trava mover de organização; o cliente não apaga versão.
-- Regras das outras tabelas iguais. 0 dado de teste.
-- Observações: a numeração recomeça do maior número que sobrou (apagar tudo e enviar de novo volta a ser V1);
-- respostas do OK e da ideia e documentos marcados pela administradora contam como atividade na trava de mover (a tabela não guarda o autor).

DO $admin_pode$
BEGIN
  IF md5(pg_get_functiondef('public.responder_versao_projeto'::regproc)) <> 'b7f8b1d680469ab5637eb8c4ef06976b' THEN RAISE EXCEPTION 'Retrato divergente: responder_versao_projeto.'; END IF;
  IF md5(pg_get_functiondef('public.trava_mover_edital_com_atividade'::regproc)) <> '94deba37c6f3702b0ac8aaf2cad49015' THEN RAISE EXCEPTION 'Retrato divergente: trava_mover.'; END IF;
  IF md5(pg_get_functiondef('public.registra_evento_resposta'::regproc)) <> '0577ac4c6862cace26d451eb0aa3ecdc' THEN RAISE EXCEPTION 'Retrato divergente: registra_evento_resposta.'; END IF;
  IF md5(pg_get_functiondef('public.registra_evento_versao_projeto'::regproc)) <> '9454dd4146ccfca25baa3756ff6ec7e3' THEN RAISE EXCEPTION 'Retrato divergente: registra_evento_versao_projeto.'; END IF;
  IF has_table_privilege('authenticated','public.projeto_versoes','DELETE') THEN RAISE EXCEPTION 'Retrato divergente: authenticated já apaga versão.'; END IF;
  IF (SELECT count(*) FROM pg_policies WHERE schemaname='public' AND tablename='projeto_versoes') <> 2 THEN RAISE EXCEPTION 'Retrato divergente: regras de projeto_versoes.'; END IF;

  -- 1. A administradora responde a versão pelo cliente (decisão 34)
  EXECUTE $fn$
CREATE OR REPLACE FUNCTION public.responder_versao_projeto(_versao_id uuid, _resposta text, _ajustes text, _nome_cargo text)
 RETURNS void
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public', 'private'
AS $function$
DECLARE
  v_versao public.projeto_versoes%ROWTYPE;
BEGIN
  IF auth.uid() IS NULL THEN
    RAISE EXCEPTION 'É preciso entrar no portal para responder.';
  END IF;

  SELECT pv.*
  INTO v_versao
  FROM public.projeto_versoes pv
  JOIN public.editais e ON e.id = pv.edital_id
  WHERE pv.id = _versao_id
    AND e.situacao = 'em_andamento'
    AND (private.eh_admin() OR e.organizacao_id = private.minha_organizacao());

  IF NOT FOUND THEN
    RAISE EXCEPTION 'Você não pode responder a este projeto.';
  END IF;

  IF v_versao.numero <> (
    SELECT max(pv.numero)
    FROM public.projeto_versoes pv
    WHERE pv.edital_id = v_versao.edital_id
  ) THEN
    RAISE EXCEPTION 'Só a versão atual do projeto pode ser respondida.';
  END IF;

  IF v_versao.resposta IS NOT NULL THEN
    RAISE EXCEPTION 'Esta versão já foi respondida.';
  END IF;

  IF _resposta NOT IN ('aprovado', 'ajustes') THEN
    RAISE EXCEPTION 'Resposta inválida.';
  END IF;

  IF _resposta = 'ajustes' AND private.texto_limpo(_ajustes) IS NULL THEN
    RAISE EXCEPTION 'Diga o que precisa mudar.';
  END IF;

  UPDATE public.projeto_versoes
  SET resposta = _resposta,
      ajustes = CASE WHEN _resposta = 'aprovado' THEN NULL ELSE private.texto_limpo(_ajustes) END,
      nome_cargo = private.texto_limpo(_nome_cargo),
      respondido_em = now(),
      respondido_por = auth.uid()
  WHERE id = _versao_id;
END;
$function$
  $fn$;

  -- 2. A administradora apaga versão (decisão 37)
  GRANT DELETE ON public.projeto_versoes TO authenticated;
  CREATE POLICY "projeto_versoes admin apaga em andamento" ON public.projeto_versoes FOR DELETE TO authenticated
    USING (private.eh_admin() AND EXISTS (SELECT 1 FROM public.editais e WHERE e.id = projeto_versoes.edital_id AND e.situacao = 'em_andamento'));

  -- 3. Registro e marcações também ao apagar versão
  EXECUTE $fn$
CREATE OR REPLACE FUNCTION public.registra_evento_versao_projeto()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public', 'private'
AS $function$
DECLARE
  _atual public.projeto_versoes%ROWTYPE;
BEGIN
  IF TG_OP = 'INSERT' THEN
    PERFORM private.grava_registro(NEW.edital_id, 'Enviou o projeto para aprovação', 'V' || NEW.numero || ': ' || NEW.arquivo_nome);
    INSERT INTO public.marcos (edital_id, chave) VALUES (NEW.edital_id, 'projeto') ON CONFLICT (edital_id, chave) DO NOTHING;
    DELETE FROM public.marcos WHERE edital_id = NEW.edital_id AND chave = 'aprovacao';
    RETURN NULL;
  END IF;

  IF TG_OP = 'DELETE' THEN
    -- apagar de vez o edital apaga as versões em cascata: nada a registrar
    IF NOT EXISTS (SELECT 1 FROM public.editais WHERE id = OLD.edital_id) THEN
      RETURN NULL;
    END IF;
    PERFORM private.grava_registro(OLD.edital_id, 'Apagou a versão do projeto',
      'V' || OLD.numero || ': ' || OLD.arquivo_nome || CASE WHEN OLD.resposta = 'aprovado' THEN '; estava aprovada' WHEN OLD.resposta = 'ajustes' THEN '; tinha ajustes solicitados' ELSE '' END);
    SELECT * INTO _atual FROM public.projeto_versoes WHERE edital_id = OLD.edital_id ORDER BY numero DESC LIMIT 1;
    IF NOT FOUND THEN
      DELETE FROM public.marcos WHERE edital_id = OLD.edital_id AND chave IN ('projeto', 'aprovacao');
    ELSIF _atual.resposta = 'ajustes' THEN
      DELETE FROM public.marcos WHERE edital_id = OLD.edital_id AND chave IN ('projeto', 'aprovacao');
    ELSE
      INSERT INTO public.marcos (edital_id, chave) VALUES (OLD.edital_id, 'projeto') ON CONFLICT (edital_id, chave) DO NOTHING;
      IF _atual.resposta = 'aprovado' THEN
        INSERT INTO public.marcos (edital_id, chave) VALUES (OLD.edital_id, 'aprovacao') ON CONFLICT (edital_id, chave) DO NOTHING;
      ELSE
        DELETE FROM public.marcos WHERE edital_id = OLD.edital_id AND chave = 'aprovacao';
      END IF;
    END IF;
    RETURN NULL;
  END IF;

  IF OLD.resposta IS NULL AND NEW.resposta = 'aprovado' THEN
    PERFORM private.grava_registro(NEW.edital_id, 'Aprovou o projeto', 'V' || NEW.numero || COALESCE('; ' || NEW.nome_cargo, ''));
    INSERT INTO public.marcos (edital_id, chave) VALUES (NEW.edital_id, 'aprovacao') ON CONFLICT (edital_id, chave) DO NOTHING;
  ELSIF OLD.resposta IS NULL AND NEW.resposta = 'ajustes' THEN
    PERFORM private.grava_registro(NEW.edital_id, 'Pediu ajustes no projeto', 'V' || NEW.numero || ': ' || COALESCE(NEW.ajustes, ''));
    DELETE FROM public.marcos WHERE edital_id = NEW.edital_id AND chave IN ('projeto', 'aprovacao');
  END IF;
  RETURN NULL;
END;
$function$
  $fn$;

  DROP TRIGGER registra_evento_versao_projeto_trg ON public.projeto_versoes;
  CREATE TRIGGER registra_evento_versao_projeto_trg AFTER INSERT OR UPDATE OR DELETE ON public.projeto_versoes FOR EACH ROW EXECUTE FUNCTION public.registra_evento_versao_projeto();

  -- 4. Registro "Apagou a resposta do OK" e "Apagou a resposta da ideia"
  EXECUTE $fn$
CREATE OR REPLACE FUNCTION public.registra_evento_resposta()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public', 'private'
AS $function$
DECLARE
  _antes public.respostas;
  _detalhe text;
  _mudancas text[] := ARRAY[]::text[];
BEGIN
  IF TG_OP = 'UPDATE' THEN
    _antes := OLD;
  END IF;

  IF private.texto_limpo(NEW.ok_escolha) IS NULL AND private.texto_limpo(NEW.ok_observacoes) IS NULL
     AND COALESCE(private.texto_limpo(_antes.ok_escolha), private.texto_limpo(_antes.ok_observacoes)) IS NOT NULL THEN
    PERFORM private.grava_registro(NEW.edital_id, 'Apagou a resposta do OK', NULL);
  ELSIF private.texto_limpo(NEW.ok_escolha) IS DISTINCT FROM private.texto_limpo(_antes.ok_escolha) THEN
    _detalhe := private.texto_limpo(NEW.ok_escolha);
    IF private.texto_limpo(NEW.ok_observacoes) IS DISTINCT FROM private.texto_limpo(_antes.ok_observacoes) THEN
      _detalhe := concat_ws('; ', _detalhe, 'observações atualizadas');
    END IF;
    PERFORM private.grava_registro(NEW.edital_id, 'Respondeu o OK', _detalhe);
  ELSIF private.texto_limpo(NEW.ok_observacoes) IS DISTINCT FROM private.texto_limpo(_antes.ok_observacoes) THEN
    PERFORM private.grava_registro(NEW.edital_id, 'Atualizou as observações do OK', NULL);
  END IF;

  IF private.texto_limpo(NEW.esboco_modo) IS DISTINCT FROM private.texto_limpo(_antes.esboco_modo) THEN
    _mudancas := _mudancas || 'a escolha'::text;
  END IF;
  -- Ideia do Projeto, forma A (pacote 7B)
  IF private.texto_limpo(NEW.ideia_o_que_fazer) IS DISTINCT FROM private.texto_limpo(_antes.ideia_o_que_fazer) THEN
    _mudancas := _mudancas || 'O que você quer fazer'::text;
  END IF;
  IF private.texto_limpo(NEW.ideia_para_quem) IS DISTINCT FROM private.texto_limpo(_antes.ideia_para_quem) THEN
    _mudancas := _mudancas || 'Para quem'::text;
  END IF;
  IF private.texto_limpo(NEW.ideia_onde) IS DISTINCT FROM private.texto_limpo(_antes.ideia_onde) THEN
    _mudancas := _mudancas || 'Onde'::text;
  END IF;
  IF private.texto_limpo(NEW.ideia_por_que) IS DISTINCT FROM private.texto_limpo(_antes.ideia_por_que) THEN
    _mudancas := _mudancas || 'Por que isso é importante'::text;
  END IF;
  IF private.texto_limpo(NEW.ideia_resultado) IS DISTINCT FROM private.texto_limpo(_antes.ideia_resultado) THEN
    _mudancas := _mudancas || 'O que você espera alcançar'::text;
  END IF;
  -- Ideia do Projeto, forma B, esboço de 11 itens (pacote 7B)
  IF private.texto_limpo(NEW.esboco_nome) IS DISTINCT FROM private.texto_limpo(_antes.esboco_nome) THEN
    _mudancas := _mudancas || 'Nome ou ideia do projeto'::text;
  END IF;
  IF private.texto_limpo(NEW.esboco_proponente) IS DISTINCT FROM private.texto_limpo(_antes.esboco_proponente) THEN
    _mudancas := _mudancas || 'Quem é o proponente'::text;
  END IF;
  IF private.texto_limpo(NEW.esboco_problema) IS DISTINCT FROM private.texto_limpo(_antes.esboco_problema) THEN
    _mudancas := _mudancas || 'Problema ou necessidade'::text;
  END IF;
  IF private.texto_limpo(NEW.esboco_publico) IS DISTINCT FROM private.texto_limpo(_antes.esboco_publico) THEN
    _mudancas := _mudancas || 'Público-alvo'::text;
  END IF;
  IF private.texto_limpo(NEW.esboco_local) IS DISTINCT FROM private.texto_limpo(_antes.esboco_local) THEN
    _mudancas := _mudancas || 'Local de execução'::text;
  END IF;
  IF private.texto_limpo(NEW.esboco_objetivo) IS DISTINCT FROM private.texto_limpo(_antes.esboco_objetivo) THEN
    _mudancas := _mudancas || 'Objetivo principal'::text;
  END IF;
  IF private.texto_limpo(NEW.esboco_atividades) IS DISTINCT FROM private.texto_limpo(_antes.esboco_atividades) THEN
    _mudancas := _mudancas || 'Atividades previstas'::text;
  END IF;
  IF private.texto_limpo(NEW.esboco_resultados) IS DISTINCT FROM private.texto_limpo(_antes.esboco_resultados) THEN
    _mudancas := _mudancas || 'Resultados esperados'::text;
  END IF;
  IF private.texto_limpo(NEW.esboco_duracao) IS DISTINCT FROM private.texto_limpo(_antes.esboco_duracao) THEN
    _mudancas := _mudancas || 'Duração aproximada'::text;
  END IF;
  IF private.texto_limpo(NEW.esboco_recursos) IS DISTINCT FROM private.texto_limpo(_antes.esboco_recursos) THEN
    _mudancas := _mudancas || 'Recursos necessários'::text;
  END IF;
  IF private.texto_limpo(NEW.esboco_diferencial) IS DISTINCT FROM private.texto_limpo(_antes.esboco_diferencial) THEN
    _mudancas := _mudancas || 'Diferencial da ideia'::text;
  END IF;
  -- Roteiro antigo de 8 itens: a tela não usa mais, mas continua registrado se mudar
  IF private.texto_limpo(NEW.esboco_o_que) IS DISTINCT FROM private.texto_limpo(_antes.esboco_o_que) THEN
    _mudancas := _mudancas || 'O quê'::text;
  END IF;
  IF private.texto_limpo(NEW.esboco_para_quem) IS DISTINCT FROM private.texto_limpo(_antes.esboco_para_quem) THEN
    _mudancas := _mudancas || 'Para quem (roteiro antigo)'::text;
  END IF;
  IF private.texto_limpo(NEW.esboco_onde) IS DISTINCT FROM private.texto_limpo(_antes.esboco_onde) THEN
    _mudancas := _mudancas || 'Onde (roteiro antigo)'::text;
  END IF;
  IF private.texto_limpo(NEW.esboco_quando) IS DISTINCT FROM private.texto_limpo(_antes.esboco_quando) THEN
    _mudancas := _mudancas || 'Quando'::text;
  END IF;
  IF private.texto_limpo(NEW.esboco_como) IS DISTINCT FROM private.texto_limpo(_antes.esboco_como) THEN
    _mudancas := _mudancas || 'Como'::text;
  END IF;
  IF private.texto_limpo(NEW.esboco_com_quem) IS DISTINCT FROM private.texto_limpo(_antes.esboco_com_quem) THEN
    _mudancas := _mudancas || 'Com quem'::text;
  END IF;
  IF private.texto_limpo(NEW.esboco_quanto) IS DISTINCT FROM private.texto_limpo(_antes.esboco_quanto) THEN
    _mudancas := _mudancas || 'Quanto'::text;
  END IF;
  IF private.texto_limpo(NEW.esboco_o_que_existe) IS DISTINCT FROM private.texto_limpo(_antes.esboco_o_que_existe) THEN
    _mudancas := _mudancas || 'O que já existe'::text;
  END IF;

  IF cardinality(_mudancas) > 0 THEN
    IF COALESCE(
         private.texto_limpo(_antes.esboco_modo),
         private.texto_limpo(_antes.ideia_o_que_fazer),
         private.texto_limpo(_antes.ideia_para_quem),
         private.texto_limpo(_antes.ideia_onde),
         private.texto_limpo(_antes.ideia_por_que),
         private.texto_limpo(_antes.ideia_resultado),
         private.texto_limpo(_antes.esboco_nome),
         private.texto_limpo(_antes.esboco_proponente),
         private.texto_limpo(_antes.esboco_problema),
         private.texto_limpo(_antes.esboco_publico),
         private.texto_limpo(_antes.esboco_local),
         private.texto_limpo(_antes.esboco_objetivo),
         private.texto_limpo(_antes.esboco_atividades),
         private.texto_limpo(_antes.esboco_resultados),
         private.texto_limpo(_antes.esboco_duracao),
         private.texto_limpo(_antes.esboco_recursos),
         private.texto_limpo(_antes.esboco_diferencial),
         private.texto_limpo(_antes.esboco_o_que),
         private.texto_limpo(_antes.esboco_para_quem),
         private.texto_limpo(_antes.esboco_onde),
         private.texto_limpo(_antes.esboco_quando),
         private.texto_limpo(_antes.esboco_como),
         private.texto_limpo(_antes.esboco_com_quem),
         private.texto_limpo(_antes.esboco_quanto),
         private.texto_limpo(_antes.esboco_o_que_existe)
       ) IS NULL THEN
      PERFORM private.grava_registro(NEW.edital_id, 'Enviou o esboço, objeto ou ideia', private.texto_limpo(NEW.esboco_modo));
    ELSIF COALESCE(
         private.texto_limpo(NEW.esboco_modo),
         private.texto_limpo(NEW.ideia_o_que_fazer), private.texto_limpo(NEW.ideia_para_quem), private.texto_limpo(NEW.ideia_onde),
         private.texto_limpo(NEW.ideia_por_que), private.texto_limpo(NEW.ideia_resultado),
         private.texto_limpo(NEW.esboco_nome), private.texto_limpo(NEW.esboco_proponente), private.texto_limpo(NEW.esboco_problema),
         private.texto_limpo(NEW.esboco_publico), private.texto_limpo(NEW.esboco_local), private.texto_limpo(NEW.esboco_objetivo),
         private.texto_limpo(NEW.esboco_atividades), private.texto_limpo(NEW.esboco_resultados), private.texto_limpo(NEW.esboco_duracao),
         private.texto_limpo(NEW.esboco_recursos), private.texto_limpo(NEW.esboco_diferencial),
         private.texto_limpo(NEW.esboco_o_que), private.texto_limpo(NEW.esboco_para_quem), private.texto_limpo(NEW.esboco_onde),
         private.texto_limpo(NEW.esboco_quando), private.texto_limpo(NEW.esboco_como), private.texto_limpo(NEW.esboco_com_quem),
         private.texto_limpo(NEW.esboco_quanto), private.texto_limpo(NEW.esboco_o_que_existe)
       ) IS NULL THEN
      PERFORM private.grava_registro(NEW.edital_id, 'Apagou a resposta da ideia', NULL);
    ELSE
      PERFORM private.grava_registro(NEW.edital_id, 'Atualizou o esboço, objeto ou ideia', 'Mudou: ' || array_to_string(_mudancas, ', '));
    END IF;
  END IF;

  _mudancas := ARRAY[]::text[];
  IF private.texto_limpo(NEW.aprovacao_escolha) IS DISTINCT FROM private.texto_limpo(_antes.aprovacao_escolha) THEN
    _detalhe := private.texto_limpo(NEW.aprovacao_escolha);
    IF private.texto_limpo(NEW.aprovacao_ajustes) IS DISTINCT FROM private.texto_limpo(_antes.aprovacao_ajustes) THEN
      _detalhe := concat_ws('; ', _detalhe, 'ajustes atualizados');
    END IF;
    IF private.texto_limpo(NEW.aprovacao_nome_cargo) IS DISTINCT FROM private.texto_limpo(_antes.aprovacao_nome_cargo) THEN
      _detalhe := concat_ws('; ', _detalhe, 'nome e cargo atualizados');
    END IF;
    PERFORM private.grava_registro(NEW.edital_id, 'Respondeu a aprovação', _detalhe);
  ELSE
    IF private.texto_limpo(NEW.aprovacao_ajustes) IS DISTINCT FROM private.texto_limpo(_antes.aprovacao_ajustes) THEN
      _mudancas := _mudancas || 'O que precisa mudar'::text;
    END IF;
    IF private.texto_limpo(NEW.aprovacao_nome_cargo) IS DISTINCT FROM private.texto_limpo(_antes.aprovacao_nome_cargo) THEN
      _mudancas := _mudancas || 'Nome e cargo de quem aprovou'::text;
    END IF;
    IF cardinality(_mudancas) > 0 THEN
      PERFORM private.grava_registro(NEW.edital_id, 'Atualizou a resposta da aprovação', 'Mudou: ' || array_to_string(_mudancas, ', '));
    END IF;
  END IF;

  RETURN NULL;
END;
$function$
  $fn$;

  -- 5. Só resposta de versão feita por cliente conta como atividade do cliente
  EXECUTE $fn$
CREATE OR REPLACE FUNCTION public.trava_mover_edital_com_atividade()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public', 'private'
AS $function$
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
                private.texto_limpo(r.aprovacao_ajustes), private.texto_limpo(r.aprovacao_nome_cargo),
                private.texto_limpo(r.ideia_o_que_fazer), private.texto_limpo(r.ideia_para_quem),
                private.texto_limpo(r.ideia_onde), private.texto_limpo(r.ideia_por_que),
                private.texto_limpo(r.ideia_resultado), private.texto_limpo(r.esboco_nome),
                private.texto_limpo(r.esboco_proponente), private.texto_limpo(r.esboco_problema),
                private.texto_limpo(r.esboco_publico), private.texto_limpo(r.esboco_local),
                private.texto_limpo(r.esboco_objetivo), private.texto_limpo(r.esboco_atividades),
                private.texto_limpo(r.esboco_resultados), private.texto_limpo(r.esboco_duracao),
                private.texto_limpo(r.esboco_recursos), private.texto_limpo(r.esboco_diferencial)
              ) IS NOT NULL)
     OR EXISTS (
       SELECT 1 FROM public.perguntas q
        WHERE q.edital_id = OLD.id AND q.autor_papel = 'cliente')
     OR EXISTS (
       SELECT 1 FROM public.documentos_extras d
        WHERE d.edital_id = OLD.id AND d.enviado)
     OR EXISTS (
       SELECT 1 FROM storage.objects o
         JOIN public.papeis p ON p.user_id::text = o.owner_id AND p.role = 'cliente'
        WHERE o.bucket_id = 'ideia-documentos'
          AND (storage.foldername(o.name))[1] = OLD.id::text)
     OR EXISTS (
       SELECT 1 FROM public.projeto_versoes v
         JOIN public.papeis p ON p.user_id = v.respondido_por AND p.role = 'cliente'
        WHERE v.edital_id = OLD.id AND v.resposta IS NOT NULL)
  THEN
    RAISE EXCEPTION 'Este edital já tem atividade do cliente e não pode mudar de organização.';
  END IF;

  RETURN NEW;
END;
$function$
  $fn$;
END
$admin_pode$;

-- ROLLBACK, só com OK da captadora:
-- DROP POLICY "projeto_versoes admin apaga em andamento" ON public.projeto_versoes; REVOKE DELETE ON public.projeto_versoes FROM authenticated;
-- DROP TRIGGER registra_evento_versao_projeto_trg ON public.projeto_versoes; recriar AFTER INSERT OR UPDATE;
-- Reaplicar responder_versao_projeto (migração 20260915002743), registra_evento_versao_projeto e trava_mover (2026-09-14-pacote-7c-banco.sql),
-- registra_evento_resposta (2026-09-14-pacote-7b-banco.sql).
