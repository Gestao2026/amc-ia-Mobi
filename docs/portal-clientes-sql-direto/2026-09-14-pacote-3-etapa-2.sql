-- Portal do Cliente Mobilizando. Pacote 3, Etapa 2 (registro no servidor)
-- Aplicado DIRETO no banco pela AMC IA, sem crédito do Lovable, com autorização da captadora em 14/09/2026 (opção 1).
-- Não está em supabase/migrations do projeto Lovable. Avisar o Lovable no próximo envio.
-- Especificação: docs/portal-clientes-pacote-3-registro.md, seções 7 e 9.2 (Migração 2) e a redefinição das etapas.
-- Retrato de antes: docs/portal-clientes-sql-direto/2026-09-14-pacote-3-etapa-2-retrato.md
-- Fora do escopo e intocado: o papel sandbox_exec (risco residual registrado no retrato).
--
-- O bloco confere o retrato antes de alterar. Se algo divergir, nada é aplicado.
--
-- RESULTADO (14/09/2026): aplicado sem erro. Conferência depois: registro com só SELECT para authenticated;
-- marcos com INSERT e SELECT; as 2 regras removidas; 24 regras e 25 gatilhos restantes idênticos ao retrato;
-- sandbox_exec intocado. Teste desfeito de A10, A11, A16 e A17 aprovado; 0 dados de teste no banco.

DO $etapa2$
BEGIN
  IF NOT has_table_privilege('authenticated', 'public.registro', 'INSERT') THEN
    RAISE EXCEPTION 'Retrato divergente: authenticated não tem INSERT em registro.';
  END IF;
  IF NOT has_table_privilege('authenticated', 'public.marcos', 'DELETE') THEN
    RAISE EXCEPTION 'Retrato divergente: authenticated não tem DELETE em marcos.';
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE schemaname = 'public' AND tablename = 'registro' AND policyname = 'registro cria') THEN
    RAISE EXCEPTION 'Retrato divergente: regra "registro cria" não existe.';
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE schemaname = 'public' AND tablename = 'marcos' AND policyname = 'marcos cliente desmarca os seus') THEN
    RAISE EXCEPTION 'Retrato divergente: regra "marcos cliente desmarca os seus" não existe.';
  END IF;

  REVOKE INSERT ON public.registro FROM authenticated;
  DROP POLICY "registro cria" ON public.registro;
  REVOKE DELETE ON public.marcos FROM authenticated;
  DROP POLICY "marcos cliente desmarca os seus" ON public.marcos;
END
$etapa2$;

-- Reversão, só com OK da captadora:
-- GRANT INSERT ON public.registro TO authenticated;
-- CREATE POLICY "registro cria" ON public.registro FOR INSERT TO authenticated
--   WITH CHECK (private.edital_visivel(edital_id) AND autor_id = auth.uid());
-- GRANT DELETE ON public.marcos TO authenticated;
-- CREATE POLICY "marcos cliente desmarca os seus" ON public.marcos FOR DELETE TO authenticated
--   USING (private.edital_editavel_cliente(edital_id) AND chave = ANY (ARRAY['ok'::marco_chave, 'documentos'::marco_chave, 'esboco'::marco_chave, 'aprovacao'::marco_chave]));
