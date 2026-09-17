-- Portal do Cliente Mobilizando. Pacote 7B, etapa 1, parte de banco por SQL direto (sem crédito do Lovable)
-- Autorização da captadora em 14/09/2026 (especificação docs/portal-clientes-pacote-7b-ideia-do-projeto.md, seção 4, itens 4 a 6).
-- Roda DEPOIS da migração 20260914234402_bf5eacf0 do Lovable. Não está em supabase/migrations.
--
-- Retrato de antes (14/09/2026, depois da migração do Lovable):
--   ideia-documentos: privado, 20971520 bytes, allowed_mime_types nulo
--   registra_evento_resposta md5 92d58af8e7c0ebd12a02e4dde1155749
--   trava_mover_edital_com_atividade md5 bdf82ebe572aca2d8571cdaf34ba9522
--   ACL das duas: postgres=X/postgres, service_role=X/postgres (CREATE OR REPLACE mantém)
--
-- RESULTADO (14/09/2026): aplicado sem erro.
--   Depois: 8 tipos no espaço ideia-documentos; registra_evento_resposta md5 0577ac4c6862cace26d451eb0aa3ecdc;
--   trava_mover_edital_com_atividade md5 f0c46566059110ee5588b90b54fe2262; ACL das duas igual.
--   Teste desfeito, 18 passos aprovados:
--     cliente envia a forma A e marca feito; salvar igual não gera registro; troca para a forma B e registra os itens que mudaram;
--     cliente anexa em andamento; anexar em finalizado é recusado; cliente não apaga e lê o próprio arquivo;
--     outra organização não lê nem anexa; a administradora anexa e lê tudo;
--     o arquivo da administradora não trava mover; o arquivo do cliente trava; a forma A trava;
--     a administradora apaga em andamento;
--     registro "Anexou/Removeu o documento da ideia" com o nome do arquivo.
--   Regras das tabelas, permissões, sandbox_exec e regras do editais-pdf iguais ao retrato. 0 dado de teste.

DO $pacote7b$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM storage.buckets WHERE id = 'ideia-documentos' AND public = false AND file_size_limit = 20971520 AND allowed_mime_types IS NULL) THEN
    RAISE EXCEPTION 'Retrato divergente: o espaço ideia-documentos não está como conferido.';
  END IF;
  IF md5(pg_get_functiondef('public.registra_evento_resposta'::regproc)) <> '92d58af8e7c0ebd12a02e4dde1155749' THEN
    RAISE EXCEPTION 'Retrato divergente: registra_evento_resposta não está na versão esperada.';
  END IF;
  IF md5(pg_get_functiondef('public.trava_mover_edital_com_atividade'::regproc)) <> 'bdf82ebe572aca2d8571cdaf34ba9522' THEN
    RAISE EXCEPTION 'Retrato divergente: trava_mover_edital_com_atividade não está na versão esperada.';
  END IF;
  IF (SELECT count(*) FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'respostas') <> 32 THEN
    RAISE EXCEPTION 'Retrato divergente: respostas não tem 32 colunas.';
  END IF;

  UPDATE storage.buckets SET allowed_mime_types = ARRAY[
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'image/jpeg',
    'image/png',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'text/csv'
  ] WHERE id = 'ideia-documentos';

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

  IF private.texto_limpo(NEW.ok_escolha) IS DISTINCT FROM private.texto_limpo(_antes.ok_escolha) THEN
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
  THEN
    RAISE EXCEPTION 'Este edital já tem atividade do cliente e não pode mudar de organização.';
  END IF;

  RETURN NEW;
END;
$function$
  $fn$;
END
$pacote7b$;

-- ROLLBACK, só com OK da captadora:
-- UPDATE storage.buckets SET allowed_mime_types = NULL WHERE id = 'ideia-documentos';
-- Reaplicar registra_evento_resposta (md5 92d58af8...) e trava_mover_edital_com_atividade (md5 bdf82ebe...):
-- as versões anteriores estão em supabase/migrations/20260914190906_15804b30 (resposta) e em
-- docs/portal-clientes-sql-direto/2026-09-14-pacote-4-banco.sql (trava).
