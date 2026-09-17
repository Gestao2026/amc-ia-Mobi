-- Portal do Cliente Mobilizando. Pacote 4, parte de banco (SQL direto, sem crédito do Lovable)
-- Autorização da captadora em 14/09/2026. Especificação: docs/portal-clientes-pacote-4-correcoes-de-tela.md, seção 3.
-- Não está em supabase/migrations do projeto Lovable. Avisado na mensagem do pacote 4.
--
-- Retrato de antes (14/09/2026):
--   regras 24, md5_regras 1c1ee7678e8ff1ec887102dc541e1c8b
--   gatilhos 25, md5_gatilhos 578c0f89b7f748c24d9d33c90819fe05, md5 sem registra_evento_edital_trg e677d2a77f2bc90252f6273df6044db4
--   md5_permissoes_tabelas 8ccbb6a184c393688062aff8f89bc108, md5_permissoes_funcoes 9a1e49b19b1246758f9f4666b4d0c0a4
--   registra_evento_edital md5 24535ae105cdebc2a3213cdb4c04e9b3, ACL postgres=X/postgres service_role=X/postgres
--   Etapa 2 do pacote 3 intacta; sandbox_exec com INSERT e SELECT nas 11 tabelas; trava de mover inexistente
--   dados: registro 0, editais 0, organizacoes 8, perfis 1, papeis 1, convites 1, usuarios de teste 0
--
-- RESULTADO (14/09/2026): aplicado sem erro.
--   Teste desfeito aprovado: "Voltou ao ritmo sugerido"; "Mudou o ritmo | Apertado (10 dias)"; "dia D para 06/10/2026; voltou ao ritmo sugerido";
--   salvar igual sem linha; mover sem atividade permitido e registrado; recusado com marcação, resposta, pergunta do cliente e documento enviado;
--   marcação e resposta desfeitas não contam; pergunta e marcação da administradora não contam; sem sessão também recusa;
--   salvar outros dados com a mesma organização e com atividade continua funcionando.
--   Depois: regras 24 iguais; 26 gatilhos (os outros 24 iguais, registra_evento_edital novo md5 ca54120830e1ac5ba25e3bb2c8f742a3, mais a trava);
--   permissões de tabelas e das funções anteriores iguais; ACL da trava e de registra_evento_edital só postgres e service_role;
--   Etapa 2 do pacote 3 intacta; sandbox_exec igual; 0 dados de teste.

DO $pacote4$
BEGIN
  IF md5(pg_get_functiondef('public.registra_evento_edital'::regproc)) <> '24535ae105cdebc2a3213cdb4c04e9b3' THEN
    RAISE EXCEPTION 'Retrato divergente: registra_evento_edital não está na versão esperada.';
  END IF;
  IF EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'trava_mover_edital_com_atividade') THEN
    RAISE EXCEPTION 'Retrato divergente: a trava de mover já existe.';
  END IF;
  IF (SELECT count(*) FROM pg_trigger t JOIN pg_class c ON c.oid = t.tgrelid JOIN pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname = 'public' AND NOT t.tgisinternal) <> 25 THEN
    RAISE EXCEPTION 'Retrato divergente: número de gatilhos diferente de 25.';
  END IF;

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
     OR NEW.submetido_em IS DISTINCT FROM OLD.submetido_em THEN
    PERFORM private.grava_registro(NEW.id, 'Registrou a submissão', private.texto_limpo(NEW.protocolo));
  END IF;

  RETURN NULL;
END;
$function$
  $fn$;

  EXECUTE $fn$
CREATE FUNCTION public.trava_mover_edital_com_atividade()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, private
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
$function$
  $fn$;

  REVOKE ALL ON FUNCTION public.trava_mover_edital_com_atividade() FROM PUBLIC, anon, authenticated;

  CREATE TRIGGER trava_mover_edital_com_atividade_trg
  BEFORE UPDATE OF organizacao_id ON public.editais
  FOR EACH ROW EXECUTE FUNCTION public.trava_mover_edital_com_atividade();
END
$pacote4$;

-- ROLLBACK, só com OK da captadora:
-- DROP TRIGGER trava_mover_edital_com_atividade_trg ON public.editais;
-- DROP FUNCTION public.trava_mover_edital_com_atividade();
-- Reaplicar public.registra_evento_edital() com a versão de assinatura 24535ae105cdebc2a3213cdb4c04e9b3,
-- que é o texto acima com os dois trechos originais:
--   (1) IF _mudou_ritmo AND NOT (...) THEN PERFORM private.grava_registro(NEW.id, 'Mudou o ritmo', private.nome_ritmo(NEW.ritmo));
--   (2) IF _mudou_ritmo THEN _lista := _lista || ('ritmo para ' || private.nome_ritmo(NEW.ritmo)); END IF;
-- (definição completa também em supabase/migrations/20260914190906_15804b30-f202-4c7c-809a-b4b4fd8bb1b6.sql do projeto Lovable)
