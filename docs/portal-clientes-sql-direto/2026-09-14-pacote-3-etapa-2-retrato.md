# Retrato antes da Etapa 2 do pacote 3 (14/09/2026)

> Tirado só com leitura, antes de qualquer alteração. Referência para comparar o depois.

## Tabelas alvo

| Tabela | Papel | Permissões |
|---|---|---|
| `registro` | `authenticated` | INSERT, SELECT |
| `registro` | `postgres` | todas |
| `registro` | `service_role` | todas |
| `registro` | `sandbox_exec` | INSERT, SELECT |
| `marcos` | `authenticated` | DELETE, INSERT, SELECT |
| `marcos` | `postgres` | todas |
| `marcos` | `service_role` | todas |
| `marcos` | `sandbox_exec` | INSERT, SELECT |

ACL bruta:
- `registro`: `postgres=arwdDxtm/postgres service_role=arwdDxtm/postgres sandbox_exec=ar/postgres authenticated=ar/postgres`
- `marcos`: `postgres=arwdDxtm/postgres service_role=arwdDxtm/postgres sandbox_exec=ar/postgres authenticated=ard/postgres`

Regras de linha ligadas nas duas (`rls=true`, `force=false`).

## Regras de linha das tabelas alvo (texto completo, todas `PERMISSIVE` e para `authenticated`)

| Tabela / regra | Operação | USING | WITH CHECK |
|---|---|---|---|
| registro / registro cria | INSERT | | `private.edital_visivel(edital_id) AND autor_id = auth.uid()` |
| registro / registro le | SELECT | `private.eh_admin() OR (edital_id IS NOT NULL AND private.edital_visivel(edital_id))` | |
| marcos / marcos admin total | ALL | `private.eh_admin()` | `private.eh_admin()` |
| marcos / marcos cliente desmarca os seus | DELETE | `private.edital_editavel_cliente(edital_id) AND chave IN (ok, documentos, esboco, aprovacao)` | |
| marcos / marcos cliente le | SELECT | `private.edital_visivel(edital_id)` | |
| marcos / marcos cliente marca os seus | INSERT | | `private.edital_editavel_cliente(edital_id) AND chave IN (ok, documentos, esboco, aprovacao)` |

## Resto do banco (assinaturas para comparação)

- `authenticated` nas outras 9 tabelas:
  - config_notificacoes: INSERT, SELECT, UPDATE;
  - convites: INSERT, SELECT, UPDATE;
  - documentos_extras: DELETE, INSERT, SELECT, UPDATE;
  - editais: DELETE, INSERT, SELECT, UPDATE;
  - organizacoes: INSERT, SELECT, UPDATE;
  - papeis: SELECT;
  - perfis: SELECT, UPDATE;
  - perguntas: INSERT, SELECT;
  - respostas: INSERT, SELECT, UPDATE.
- `anon`: nenhuma permissão.
- **20 regras de linha das outras tabelas** (26 no total com as 6 de `registro` e `marcos`; os relatórios anteriores disseram 29 e 23 por erro de contagem), md5 de operação e expressões:
  - config admin total `7c3774e9`;
  - config cliente le `adafd4e8`;
  - convites admin total `7c3774e9`;
  - documentos admin total `7c3774e9`;
  - documentos cliente le `528127ca`;
  - documentos cliente marca enviado `1d299cea`;
  - editais admin total `7c3774e9`;
  - editais cliente le os da organizacao `f2e894c1`;
  - organizacoes admin total `7c3774e9`;
  - organizacoes cliente le a sua `188202fe`;
  - papeis le o proprio `8779b7e0`;
  - perfis admin total `7c3774e9`;
  - perfis atualiza o proprio `7470624e`;
  - perfis le o proprio `c30327a6`;
  - perguntas cria `01c35d24`;
  - perguntas le `528127ca`;
  - respostas admin total `7c3774e9`;
  - respostas cliente cria `a4830990`;
  - respostas cliente edita `1d299cea`;
  - respostas cliente le `528127ca`.
- **25 gatilhos**, tipo e md5 da função:
  - convites.normaliza_convite_email_trg 23 `f1c6817f`;
  - documentos_extras: define_data_envio_documento_trg 23 `339bd14d`, registra_evento_documento_trg 29 `5340e863`, trava_documentos_cliente_trg 19 `17353760`, trava_documentos_fora_andamento_trg 31 `b28792ab`;
  - editais: atualiza_edital_atualizado_em_trg 19 `2e5a3905`, permite_apagar_edital_trg 11 `977ed7ad`, registra_edital_apagado_de_vez_trg 9 `c7b80af2`, registra_evento_edital_trg 21 `24535ae1`, trava_edital_fora_andamento_trg 19 `addf48b4`;
  - marcos: define_marcacao_trg 7 `fbf08d44`, protege_autoria_marcacao_trg 19 `0327bca2`, registra_evento_marco_trg 13 `0a21689b`, trava_marcos_fora_andamento_trg 31 `b28792ab`;
  - organizacoes: normaliza_nome_organizacao_trg 19 `d649ddac`, registra_correcao_nome_organizacao_trg 17 `0d0cd8e9`;
  - perfis.trava_perfil_cliente_trg 19 `ca74ffc9`;
  - perguntas: define_autor_pergunta_trg 7 `50c93cd7`, registra_evento_pergunta_trg 5 `98ace9d8`, trava_perguntas_fora_andamento_trg 31 `b28792ab`;
  - registro: define_nome_registro_trg 7 `595d3c61`, protege_registro_trg 27 `fbdf9623`;
  - respostas: registra_evento_resposta_trg 21 `92d58af8`, trava_respostas_cliente_trg 19 `34aefc88`, trava_respostas_fora_andamento_trg 31 `b28792ab`.
- `desmarcar_entrega`: SECURITY DEFINER, md5 `e8d8d05d`, EXECUTE para `authenticated` sim, para `anon` não.
- **Contagem:**
  - registro 0;
  - editais 0;
  - marcos 0;
  - documentos 0;
  - respostas 0;
  - perguntas 0;
  - perfis 1;
  - papeis 1;
  - convites 1;
  - organizacoes 8.

## Risco residual registrado, fora do pacote 3: papel `sandbox_exec`

- Pode entrar no banco, **ignora as regras de linha** e não é superusuário. Único membro: `postgres`.
- Tem INSERT e SELECT nas 11 tabelas públicas, inclusive `registro` e `marcos`.
- Não está ligado a `authenticated`, `anon` nem `authenticator`: **não é acesso de usuário do portal**.
- Aparece nas permissões padrão do esquema desde a conferência do pacote 2. Pelo nome e pela configuração, parece ser o papel de ambiente de teste do Lovable Cloud (inferência, sem documentação no projeto).
- Com ele, ainda seria possível inserir linha no registro por fora dos gatilhos. Alterar e apagar continuam barrados pela trava `protege_registro`.
- **Decisão da captadora em 14/09/2026:** não alterar, não revogar, não criar regra; investigar depois, fora do pacote 3.
