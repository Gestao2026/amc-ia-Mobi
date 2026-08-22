---
description: Descobrir por que o Instagram ou o LinkedIn parou de responder e destravar, sem tentativa e erro.
---

# /redes-diagnosticar

Diagnostica a conexão com o Instagram e o LinkedIn e devolve a causa e a correção. Existe porque essas conexões caem de forma previsível, e o sintoma que chega ao captador ("ontem estava conectado e hoje não está") não revela qual das três camadas quebrou.

Nunca chute. Percorra a sequência: cada passo elimina uma camada.

## As três camadas, e por que confundi-las custa horas

| Camada | O que é | Como cai |
|---|---|---|
| 1. Conector | Claude → seu servidor no Render | hibernação apaga a sessão, que vive em memória |
| 2. Autorização | seu servidor → a rede social | token expira, é revogado, ou vive em memória |
| 3. Capacidade | o que a API permite | escopo faltando ou produto não aprovado |

A camada 1 cai **toda segunda-feira e depois de cada publicação de código**. Isso é esperado, não é defeito. A camada 2 sobrevive, porque o token está na ponte.

## Passos

1. **Anuncie:**
   ```
   🔍 Próximo passo: diagnosticar a conexão das redes (4 passos). Tempo estimado: cerca de 60 segundos.
   ```

2. **Camada 1.** Verifique se as ferramentas da rede aparecem na sessão (`ToolSearch` por `+instagram` ou `+linkedin`).

   - **Não aparecem:** o conector caiu. Oriente clicar em **Reconectar** no painel de conectores. É o caso mais comum e resolve em segundos. Pare aqui.
   - **Aparecem:** siga.

3. **Camada 2.** Chame `instagram_mcp_status` ou `linkedin_mcp_status` e leia três campos:

   | Campo | Valor | O que fazer |
   |---|---|---|
   | `oauth` | `nao_configurado` | falta variável no Render; ver `variaveis_ausentes` |
   | `instagram`/`linkedin` | `conectado` | a conexão está boa; o problema é da camada 3 |
   | `instagram`/`linkedin` | `nao_conectado` | autorização perdida; siga o passo 4 |

4. **Por que a autorização se perdeu.** Leia `onde_o_token_fica_guardado`:

   - **`memory`:** o token morre a cada hibernação. É configuração errada, não acaso. Corrija no Render para `ponte` e acrescente as três variáveis da ponte. O campo `aviso_de_persistencia` traz o texto para mostrar ao captador.
   - **`ponte`:** o token expirou ou foi revogado. Rode `{rede}_oauth_iniciar`, entregue a URL ao captador e peça para autorizar. Expira em 10 minutos.

5. **Se a ponte não responder**, teste por fora e leia o código:

   ```bash
   curl -s -o /dev/null -w '%{http_code}\n' -X POST \
     https://ponte.mobilizando.org/token-instagram.php \
     -H 'Content-Type: application/json' -d '{"acao":"ler"}'
   ```

   | Código | Causa |
   |---|---|
   | **401** | **certo.** No ar, config completo, recusando por falta do segredo |
   | 403 | bloqueado pelo `.htaccess`, que libera uma lista fechada de nomes |
   | 404 | arquivo fora do docroot real (ver armadilhas) |
   | 500 | config não encontrado, ou com campo vazio |

6. **Camada 3.** Se a conexão está boa mas a ferramenta recusa, é limite de permissão, e nem sempre tem conserto:

   | Sintoma | Causa | Tem solução? |
   |---|---|---|
   | LinkedIn recusa publicar (403) | falta `w_member_social`, ou a autorização é anterior à mudança de escopo | sim, acrescentar e reautorizar |
   | LinkedIn não devolve métrica | exige Community Management API, não aprovada | **não**, é do lado do LinkedIn |
   | Instagram recusa uma métrica | varia com tipo de conta e idade da publicação | a resposta traz a mensagem da Meta |
   | Instagram não publica | decisão de projeto, trava estrutural no código | não, e é intencional |

7. **Relate ao captador** em linguagem comum: qual camada quebrou, por quê, e o que ele precisa fazer. Nunca despeje código de status na conversa.

## Fatos que evitam diagnóstico errado

**A hibernação é a causa raiz da maioria dos sintomas.** O plano gratuito do Render adormece o serviço após cerca de 15 minutos ocioso. Um ping externo (cron-job.org, `*/10 8-20 * * 1-5`) mantém os dois acordados no horário comercial. Fora dele, dormem.

**O tempo limite do ping precisa ser 30 segundos.** Acordar leva uns 12. Com limite baixo, o ping desiste no meio, o serviço volta a dormir, e o ciclo se repete indefinidamente. Foi assim que o Instagram ficou preso enquanto o LinkedIn funcionava: diferença de ordem dos acontecimentos, não de configuração.

**O token do Instagram vence em 60 dias.** A renovação automática não está implementada. Autorizado em 21/08/2026, vence por volta de **20/10/2026**. Ao expirar, é reautorizar.

**Resposta lenta não é erro.** Doze segundos significa que o serviço estava dormindo e acordou. Menos de um segundo significa acordado.

## Armadilhas da HostGator, se precisar mexer na ponte

Leia `mcp-instagram/ponte-hostgator/README.md` **antes** de tocar em qualquer arquivo lá. Em resumo:

- Existem **duas pastas `ponte-mcp`**. A que o servidor usa fica em `/home2/rosepa59/home2/rosepa59/ponte-mcp/public`, caminho que parece erro de digitação e não é.
- **O Gerenciador de Arquivos do cPanel mente.** Já negou arquivo que existia, escondeu o `.htaccess` com os ocultos ligados, e listou um item numa pasta de quatro. Use a busca, e confirme sempre por `curl`.
- O `.htaccess` é **compartilhado** e libera uma lista fechada. Arquivo novo nasce bloqueado com 403.
- O `token.php` em produção tem o alvo **escrito dentro do arquivo**. Trocar `ALVO` no config não faz nada.

## O que este comando não faz

Não reconecta o conector (só o captador consegue, no painel), não autoriza contas sozinho (a senha é digitada apenas no site da rede) e não publica nada.
