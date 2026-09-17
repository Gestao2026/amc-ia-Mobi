-- Portal do Cliente Mobilizando. Pacote 7C, parte de banco por SQL direto (sem crédito do Lovable)
-- Autorização da captadora em 14/09/2026 (docs/portal-clientes-pacote-7c-projeto-versoes.md, seção 4, itens 3 a 6).
-- Roda DEPOIS da migração 20260915002743_656c93d2 do Lovable. Não está em supabase/migrations.
--
-- Retrato de antes (depois da migração do Lovable):
--   projeto-arquivos: privado, 52428800, allowed_mime_types nulo
--   projeto_versoes: sem gatilhos
--   registra_evento_edital md5 ca54120830e1ac5ba25e3bb2c8f742a3
--   trava_edital_fora_andamento md5 addf48b4d68e1eb8e76ba16d7e689538
--   trava_mover_edital_com_atividade md5 f0c46566059110ee5588b90b54fe2262
--   Observação: o sandbox_exec ganhou INSERT e SELECT em projeto_versoes pela regra automática dele. Não alterado (decisão da captadora).
-- Limite: o registro "Anexou o comprovante" (arquivo) exige gatilho em storage.objects, que só o Lovable consegue criar.
--
-- RESULTADO (14/09/2026): aplicado sem erro. Gatilhos 26 para 30; funções 41 para 44. Regras, permissões antigas e storage antigo iguais.
-- Teste desfeito, 26 passos aprovados:
--   V1 com número, autor e observação definidos pelo banco (forja de número e resposta ignorada); etapa 5 feita;
--   outra organização não vê nem responde; cliente não envia versão, não deixa ajustes vazio, não responde duas vezes,
--   não altera direto, não responde versão antiga; ajustes reabre a etapa 5; admin não responde; ninguém apaga versão;
--   V2 = número 2; aprovação marca a etapa 6 com o cliente como autor; V3 derruba a aprovação e mantém a etapa 5;
--   submissão grava protocolo, V2 e link; em finalizado não muda versão nem link e não aceita versão nova;
--   cliente não anexa arquivo; cliente A lê, cliente B não; admin não apaga arquivo de versão e apaga comprovante;
--   resposta do cliente trava mover de organização. 0 dado de teste.

DO $pacote7c$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM storage.buckets WHERE id = 'projeto-arquivos' AND public = false AND file_size_limit = 52428800 AND allowed_mime_types IS NULL) THEN
    RAISE EXCEPTION 'Retrato divergente: projeto-arquivos não está como conferido.';
  END IF;
  IF EXISTS (SELECT 1 FROM pg_trigger WHERE tgrelid = 'public.projeto_versoes'::regclass AND NOT tgisinternal) THEN
    RAISE EXCEPTION 'Retrato divergente: projeto_versoes já tem gatilhos.';
  END IF;
  IF md5(pg_get_functiondef('public.registra_evento_edital'::regproc)) <> 'ca54120830e1ac5ba25e3bb2c8f742a3' THEN
    RAISE EXCEPTION 'Retrato divergente: registra_evento_edital.';
  END IF;
  IF md5(pg_get_functiondef('public.trava_edital_fora_andamento'::regproc)) <> 'addf48b4d68e1eb8e76ba16d7e689538' THEN
    RAISE EXCEPTION 'Retrato divergente: trava_edital_fora_andamento.';
  END IF;
  IF md5(pg_get_functiondef('public.trava_mover_edital_com_atividade'::regproc)) <> 'f0c46566059110ee5588b90b54fe2262' THEN
    RAISE EXCEPTION 'Retrato divergente: trava_mover_edital_com_atividade.';
  END IF;

  -- 1. Tipos de arquivo
  UPDATE storage.buckets SET allowed_mime_types = ARRAY[
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'image/jpeg',
    'image/png'
  ] WHERE id = 'projeto-arquivos';

  -- 2. Número, data e autor definidos pelo banco
  EXECUTE $fn$
CREATE FUNCTION public.define_versao_projeto()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, private
AS $function$
BEGIN
  PERFORM pg_advisory_xact_lock(hashtext('projeto_versoes:' || NEW.edital_id::text));
  SELECT COALESCE(max(numero), 0) + 1 INTO NEW.numero FROM public.projeto_versoes WHERE edital_id = NEW.edital_id;
  NEW.enviado_em := now();
  NEW.enviado_por := auth.uid();
  NEW.observacao := private.texto_limpo(NEW.observacao);
  NEW.resposta := NULL;
  NEW.ajustes := NULL;
  NEW.nome_cargo := NULL;
  NEW.respondido_em := NULL;
  NEW.respondido_por := NULL;
  RETURN NEW;
END;
$function$
  $fn$;

  -- 3. Versão enviada não muda; resposta só uma vez
  EXECUTE $fn$
CREATE FUNCTION public.protege_versao_projeto()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, private
AS $function$
BEGIN
  IF NEW.id IS DISTINCT FROM OLD.id OR NEW.edital_id IS DISTINCT FROM OLD.edital_id OR NEW.numero IS DISTINCT FROM OLD.numero
     OR NEW.arquivo_caminho IS DISTINCT FROM OLD.arquivo_caminho OR NEW.arquivo_nome IS DISTINCT FROM OLD.arquivo_nome
     OR NEW.observacao IS DISTINCT FROM OLD.observacao OR NEW.enviado_em IS DISTINCT FROM OLD.enviado_em
     OR NEW.enviado_por IS DISTINCT FROM OLD.enviado_por THEN
    RAISE EXCEPTION 'Uma versão enviada do projeto não pode ser alterada. Envie uma nova versão.';
  END IF;
  IF OLD.resposta IS NOT NULL THEN
    RAISE EXCEPTION 'Esta versão já foi respondida.';
  END IF;
  RETURN NEW;
END;
$function$
  $fn$;

  -- 4. Marcações da jornada e registro
  EXECUTE $fn$
CREATE FUNCTION public.registra_evento_versao_projeto()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, private
AS $function$
BEGIN
  IF TG_OP = 'INSERT' THEN
    PERFORM private.grava_registro(NEW.edital_id, 'Enviou o projeto para aprovação', 'V' || NEW.numero || ': ' || NEW.arquivo_nome);
    INSERT INTO public.marcos (edital_id, chave) VALUES (NEW.edital_id, 'projeto') ON CONFLICT (edital_id, chave) DO NOTHING;
    DELETE FROM public.marcos WHERE edital_id = NEW.edital_id AND chave = 'aprovacao';
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

  REVOKE ALL ON FUNCTION public.define_versao_projeto() FROM PUBLIC, anon, authenticated;
  REVOKE ALL ON FUNCTION public.protege_versao_projeto() FROM PUBLIC, anon, authenticated;
  REVOKE ALL ON FUNCTION public.registra_evento_versao_projeto() FROM PUBLIC, anon, authenticated;

  CREATE TRIGGER define_versao_projeto_trg BEFORE INSERT ON public.projeto_versoes FOR EACH ROW EXECUTE FUNCTION public.define_versao_projeto();
  CREATE TRIGGER protege_versao_projeto_trg BEFORE UPDATE ON public.projeto_versoes FOR EACH ROW EXECUTE FUNCTION public.protege_versao_projeto();
  CREATE TRIGGER trava_projeto_versoes_fora_andamento_trg BEFORE INSERT OR UPDATE OR DELETE ON public.projeto_versoes FOR EACH ROW EXECUTE FUNCTION public.trava_conteudo_edital_fora_andamento();
  CREATE TRIGGER registra_evento_versao_projeto_trg AFTER INSERT OR UPDATE ON public.projeto_versoes FOR EACH ROW EXECUTE FUNCTION public.registra_evento_versao_projeto();

  -- 5. Registro da submissão com a versão e o link do comprovante
  EXECUTE $fn$
CREATE OR REPLACE FUNCTION public.registra_evento_edital()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public', 'private'
AS $function$
DECLARE
  _mudou_org boolean;
  _mudou_dia_d boolean;
  _mudou_dossie boolean;
  _mudou_nome boolean;
  _mudou_orgao boolean;
  _mudou_link boolean;
  _mudou_ritmo boolean;
  _lista text[] := ARRAY[]::text[];
  _nome_org text;
  _versao integer;
BEGIN
  IF TG_OP = 'INSERT' THEN
    PERFORM private.grava_registro(NEW.id, 'Abriu o edital', NEW.nome);
    RETURN NULL;
  END IF;

  IF NEW.situacao IS DISTINCT FROM OLD.situacao THEN
    IF NEW.situacao = 'apagado' THEN
      PERFORM private.grava_registro(NEW.id, 'Apagou o edital', NULL);
    ELSIF OLD.situacao = 'apagado' THEN
      PERFORM private.grava_registro(NEW.id, 'Restaurou o edital', NULL);
    ELSIF NEW.situacao = 'finalizado' THEN
      PERFORM private.grava_registro(NEW.id, 'Finalizou o edital', NULL);
    END IF;
  ELSIF NEW.resultado IS DISTINCT FROM OLD.resultado AND NEW.resultado IN ('aprovado', 'reprovado') THEN
    PERFORM private.grava_registro(NEW.id, 'Marcou o resultado como ' || NEW.resultado::text, NULL);
  END IF;

  _mudou_org := NEW.organizacao_id IS DISTINCT FROM OLD.organizacao_id;
  _mudou_dia_d := NEW.dia_d IS DISTINCT FROM OLD.dia_d;
  _mudou_dossie := NEW.data_dossie IS DISTINCT FROM OLD.data_dossie;
  _mudou_nome := private.texto_limpo(NEW.nome) IS DISTINCT FROM private.texto_limpo(OLD.nome);
  _mudou_orgao := private.texto_limpo(NEW.orgao) IS DISTINCT FROM private.texto_limpo(OLD.orgao);
  _mudou_link := private.texto_limpo(NEW.link) IS DISTINCT FROM private.texto_limpo(OLD.link);
  _mudou_ritmo := NEW.ritmo IS DISTINCT FROM OLD.ritmo;

  IF _mudou_ritmo AND NOT (_mudou_org OR _mudou_dia_d OR _mudou_dossie OR _mudou_nome OR _mudou_orgao OR _mudou_link) THEN
    IF NEW.ritmo IS NULL THEN
      PERFORM private.grava_registro(NEW.id, 'Voltou ao ritmo sugerido', NULL);
    ELSE
      PERFORM private.grava_registro(NEW.id, 'Mudou o ritmo', private.nome_ritmo(NEW.ritmo));
    END IF;
  ELSIF _mudou_org OR _mudou_dia_d OR _mudou_dossie OR _mudou_nome OR _mudou_orgao OR _mudou_link THEN
    IF _mudou_org THEN
      SELECT nome INTO _nome_org FROM public.organizacoes WHERE id = NEW.organizacao_id;
      _lista := _lista || ('organização para ' || COALESCE(_nome_org, 'outra organização'));
    END IF;
    IF _mudou_dia_d THEN
      _lista := _lista || ('dia D para ' || private.data_br(NEW.dia_d));
    END IF;
    IF _mudou_dossie THEN
      _lista := _lista || ('data do dossiê para ' || private.data_br(NEW.data_dossie));
    END IF;
    IF _mudou_ritmo THEN
      _lista := _lista || CASE WHEN NEW.ritmo IS NULL THEN 'voltou ao ritmo sugerido' ELSE 'ritmo para ' || private.nome_ritmo(NEW.ritmo) END;
    END IF;
    IF _mudou_nome THEN
      _lista := _lista || ('nome para ' || COALESCE(private.texto_limpo(NEW.nome), 'em branco'));
    END IF;
    IF _mudou_orgao THEN
      _lista := _lista || ('órgão para ' || COALESCE(private.texto_limpo(NEW.orgao), 'em branco'));
    END IF;
    IF _mudou_link THEN
      _lista := _lista || ('link para ' || COALESCE(private.texto_limpo(NEW.link), 'em branco'));
    END IF;
    PERFORM private.grava_registro(NEW.id, 'Atualizou os dados do edital', array_to_string(_lista, '; '));
  END IF;

  IF private.texto_limpo(NEW.protocolo) IS DISTINCT FROM private.texto_limpo(OLD.protocolo)
     OR NEW.submetido_em IS DISTINCT FROM OLD.submetido_em
     OR NEW.versao_submetida_id IS DISTINCT FROM OLD.versao_submetida_id
     OR private.texto_limpo(NEW.comprovante_link) IS DISTINCT FROM private.texto_limpo(OLD.comprovante_link) THEN
    SELECT numero INTO _versao FROM public.projeto_versoes WHERE id = NEW.versao_submetida_id;
    PERFORM private.grava_registro(NEW.id, 'Registrou a submissão',
      concat_ws('; ', private.texto_limpo(NEW.protocolo),
                CASE WHEN _versao IS NOT NULL THEN 'V' || _versao END,
                CASE WHEN private.texto_limpo(NEW.comprovante_link) IS NOT NULL THEN 'comprovante: ' || private.texto_limpo(NEW.comprovante_link) END));
  END IF;

  RETURN NULL;
END;
$function$
  $fn$;

  -- 6. Edital finalizado ou apagado protege também a versão submetida e o link do comprovante
  EXECUTE $fn$
CREATE OR REPLACE FUNCTION public.trava_edital_fora_andamento()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
BEGIN
  IF OLD.situacao = 'em_andamento' THEN
    RETURN NEW;
  END IF;

  IF public.eh_admin()
     AND OLD.situacao = 'finalizado'
     AND NEW.id IS NOT DISTINCT FROM OLD.id
     AND NEW.organizacao_id IS NOT DISTINCT FROM OLD.organizacao_id
     AND NEW.nome IS NOT DISTINCT FROM OLD.nome
     AND NEW.orgao IS NOT DISTINCT FROM OLD.orgao
     AND NEW.link IS NOT DISTINCT FROM OLD.link
     AND NEW.dia_d IS NOT DISTINCT FROM OLD.dia_d
     AND NEW.data_dossie IS NOT DISTINCT FROM OLD.data_dossie
     AND NEW.ritmo IS NOT DISTINCT FROM OLD.ritmo
     AND NEW.finalizado_em IS NOT DISTINCT FROM OLD.finalizado_em
     AND NEW.protocolo IS NOT DISTINCT FROM OLD.protocolo
     AND NEW.submetido_em IS NOT DISTINCT FROM OLD.submetido_em
     AND NEW.versao_submetida_id IS NOT DISTINCT FROM OLD.versao_submetida_id
     AND NEW.comprovante_link IS NOT DISTINCT FROM OLD.comprovante_link
     AND NEW.created_by IS NOT DISTINCT FROM OLD.created_by
     AND NEW.created_at IS NOT DISTINCT FROM OLD.created_at
     AND (
       (NEW.situacao = 'finalizado'
        AND NEW.situacao_anterior IS NOT DISTINCT FROM OLD.situacao_anterior
        AND NEW.apagado_em IS NOT DISTINCT FROM OLD.apagado_em)
       OR
       (NEW.situacao = 'apagado'
        AND NEW.situacao_anterior = 'finalizado'
        AND NEW.apagado_em IS NOT NULL)
     ) THEN
    RETURN NEW;
  END IF;

  IF public.eh_admin()
     AND OLD.situacao = 'apagado'
     AND NEW.id IS NOT DISTINCT FROM OLD.id
     AND NEW.organizacao_id IS NOT DISTINCT FROM OLD.organizacao_id
     AND NEW.nome IS NOT DISTINCT FROM OLD.nome
     AND NEW.orgao IS NOT DISTINCT FROM OLD.orgao
     AND NEW.link IS NOT DISTINCT FROM OLD.link
     AND NEW.dia_d IS NOT DISTINCT FROM OLD.dia_d
     AND NEW.data_dossie IS NOT DISTINCT FROM OLD.data_dossie
     AND NEW.ritmo IS NOT DISTINCT FROM OLD.ritmo
     AND NEW.finalizado_em IS NOT DISTINCT FROM OLD.finalizado_em
     AND NEW.resultado IS NOT DISTINCT FROM OLD.resultado
     AND NEW.resultado_em IS NOT DISTINCT FROM OLD.resultado_em
     AND NEW.protocolo IS NOT DISTINCT FROM OLD.protocolo
     AND NEW.submetido_em IS NOT DISTINCT FROM OLD.submetido_em
     AND NEW.versao_submetida_id IS NOT DISTINCT FROM OLD.versao_submetida_id
     AND NEW.comprovante_link IS NOT DISTINCT FROM OLD.comprovante_link
     AND NEW.created_by IS NOT DISTINCT FROM OLD.created_by
     AND NEW.created_at IS NOT DISTINCT FROM OLD.created_at
     AND NEW.situacao = COALESCE(OLD.situacao_anterior, 'em_andamento')
     AND NEW.situacao_anterior IS NULL
     AND NEW.apagado_em IS NULL THEN
    RETURN NEW;
  END IF;

  RAISE EXCEPTION 'Edital finalizado ou apagado está disponível somente para leitura.';
END;
$function$
  $fn$;

  -- 7. Resposta do cliente a uma versão conta como atividade para a trava de mover
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
        WHERE v.edital_id = OLD.id AND v.resposta IS NOT NULL)
  THEN
    RAISE EXCEPTION 'Este edital já tem atividade do cliente e não pode mudar de organização.';
  END IF;

  RETURN NEW;
END;
$function$
  $fn$;
END
$pacote7c$;

-- ROLLBACK, só com OK da captadora:
-- DROP TRIGGER define_versao_projeto_trg, protege_versao_projeto_trg, trava_projeto_versoes_fora_andamento_trg, registra_evento_versao_projeto_trg ON public.projeto_versoes (um por vez);
-- DROP FUNCTION public.define_versao_projeto(), public.protege_versao_projeto(), public.registra_evento_versao_projeto();
-- UPDATE storage.buckets SET allowed_mime_types = NULL WHERE id = 'projeto-arquivos';
-- Reaplicar registra_evento_edital (docs/portal-clientes-sql-direto/2026-09-14-pacote-4-banco.sql),
-- trava_edital_fora_andamento (sem as duas linhas novas) e trava_mover_edital_com_atividade (2026-09-14-pacote-7b-banco.sql).
