"""
Servidor MCP do mcp-instagram.

Ferramentas de conexão: `instagram_mcp_status` (diagnóstico),
`instagram_oauth_iniciar`, `instagram_oauth_status` e
`instagram_desconectar`.

Ferramentas de negócio, TODAS SOMENTE LEITURA: `instagram_perfil`,
`instagram_publicacoes`, `instagram_metricas_publicacao` e
`instagram_metricas_conta`. Este componente NÃO publica, não edita, não
exclui, não comenta, não responde mensagens e não administra anúncios.
A limitação é estrutural, não uma promessa: o cliente de leitura recebe
um transporte que expõe apenas `get`, e os escopos padrão
(`instagram_business_basic`, `instagram_business_manage_insights`) não
concedem escrita.

`instagram_desconectar` apaga a autorização guardada NESTE servidor.
Não é uma ação na conta do Instagram: nada é alterado, publicado ou
removido lá. É o botão de corte do lado do captador.

OAuth do Instagram (Camada 2): `resolve_instagram_config` (config.py) lê
INSTAGRAM_CLIENT_ID / INSTAGRAM_CLIENT_SECRET / MCP_PUBLIC_BASE_URL do
ambiente e, se presentes, liga o fluxo completo (URL de autorização,
callback, troca de code por token em duas etapas, TokenStore). Se
ausentes, a Camada 2 fica desligada e o servidor sobe normalmente sem
ela. O início do fluxo é uma FERRAMENTA MCP, não uma página: nenhuma
interface HTML existe neste componente. A única rota HTTP própria é o
callback, que a própria Meta chama, e que responde JSON.

OAuth do Claude (Camada 1): `resolve_claude_auth_config` lê
MCP_CLAUDE_CLIENT_ID / MCP_CLAUDE_CLIENT_SECRET / MCP_PUBLIC_BASE_URL e,
se presentes, protege a rota /mcp com um Authorization Server mínimo
(client estático, sem DCR, sem tela de consentimento, PKCE S256
validado pelo próprio SDK). Se ausentes (ex. desenvolvimento local via
stdio), a Camada 1 fica desligada.

Transporte: o mesmo servidor roda em dois modos, decididos pela variável
de ambiente MCP_TRANSPORT, sem duplicar código:

  MCP_TRANSPORT=stdio            (padrão, uso local)
      python -m mcp_instagram.server

  MCP_TRANSPORT=streamable-http  (uso remoto/produção)
      PORT=<porta da infraestrutura> MCP_TRANSPORT=streamable-http \
      python -m mcp_instagram.server
"""

import os
import secrets
import time
from dataclasses import dataclass
from typing import Mapping

from mcp.server.auth.provider import ProviderTokenVerifier
from mcp.server.auth.settings import AuthSettings, ClientRegistrationOptions, RevocationOptions
from mcp.server.mcpserver import MCPServer
from starlette.requests import Request
from starlette.responses import JSONResponse

from mcp_instagram.auth_claude.provider import ClaudeAuthProvider
from mcp_instagram.instagram_client.leitura import (
    JANELA_DIAS_PADRAO,
    LIMITE_PUBLICACOES_PADRAO,
    ClienteLeituraInstagram,
    ErroDaApi,
    SemAutorizacaoError,
)
from mcp_instagram.instagram_client.transporte import ErroDeTransporte, TransporteGraphHttpx
from mcp_instagram.auth_claude.session_store import ClaudeSessionStore
from mcp_instagram.auth_instagram.oauth_callback import CallbackOutcome, CallbackParams
from mcp_instagram.auth_instagram.runtime import InstagramOAuthRuntime, build_runtime
from mcp_instagram.auth_instagram.signed_request import (
    InvalidSignedRequestError,
    parse_signed_request,
)
from mcp_instagram.auth_instagram.token_exchange import TokenExchangeError, TransportError
from mcp_instagram.auth_instagram.token_store import TokenStoreBackendError
from mcp_instagram.config import (
    INSTAGRAM_CALLBACK_PATH,
    INSTAGRAM_DATA_DELETION_PATH,
    INSTAGRAM_DATA_DELETION_STATUS_PATH,
    INSTAGRAM_DEAUTHORIZE_PATH,
    TOKEN_STORE_BACKEND_MEMORY,
    missing_instagram_env_vars,
    resolve_instagram_config,
)

mcp = MCPServer("mcp-instagram")


# =====================================================================
# Descrição das permissões, em português, para o captador
# =====================================================================
#
# Existe para que a ferramenta de autorização possa dizer, ANTES de o
# captador clicar, exatamente o que cada permissão pedida permite fazer.
# É informação de interface, não configuração: mudar um texto aqui não
# muda nenhum escopo solicitado.

PERMISSOES = {
    "instagram_business_basic": {
        "nome": "Leitura básica do perfil",
        "permite": (
            "Identificar a conta e ler nome de usuário, foto, número de "
            "seguidores e a lista de publicações já existentes."
        ),
        "publicar": False,
        "editar": False,
        "excluir": False,
        "mensagens": False,
        "metricas": False,
        "anuncios": False,
    },
    "instagram_business_manage_insights": {
        "nome": "Leitura de métricas",
        "permite": (
            "Ler alcance, impressões, visualizações de perfil, desempenho "
            "por publicação e dados de audiência."
        ),
        "publicar": False,
        "editar": False,
        "excluir": False,
        "mensagens": False,
        "metricas": True,
        "anuncios": False,
    },
    "instagram_business_content_publish": {
        "nome": "Publicação de conteúdo",
        "permite": "Criar e publicar feed, carrossel, reels e stories.",
        "publicar": True,
        "editar": False,
        "excluir": False,
        "mensagens": False,
        "metricas": False,
        "anuncios": False,
    },
    "instagram_business_manage_comments": {
        "nome": "Gestão de comentários",
        "permite": "Ler, responder, ocultar e apagar comentários.",
        "publicar": False,
        "editar": False,
        "excluir": True,
        "mensagens": False,
        "metricas": False,
        "anuncios": False,
    },
    "instagram_business_manage_messages": {
        "nome": "Gestão de mensagens",
        "permite": "Ler e responder mensagens do Direct.",
        "publicar": False,
        "editar": False,
        "excluir": False,
        "mensagens": True,
        "metricas": False,
        "anuncios": False,
    },
}

COMO_REVOGAR = (
    "Para revogar: no Instagram, Configurações e privacidade, Aplicativos e "
    "sites, selecionar o aplicativo e Remover. Do lado da AMC IA, a "
    "ferramenta instagram_desconectar apaga a autorização guardada neste "
    "servidor imediatamente."
)


def descrever_permissoes(escopos) -> list[dict]:
    """
    Traduz a lista de escopos técnicos em descrições legíveis. Um escopo
    desconhecido é devolvido sem descrição, e explicitamente marcado
    como tal, em vez de ser omitido: esconder do captador uma permissão
    que ele vai conceder seria o pior desfecho possível aqui.
    """
    descricoes = []
    for escopo in escopos:
        detalhe = PERMISSOES.get(escopo)
        if detalhe is None:
            descricoes.append(
                {
                    "escopo": escopo,
                    "nome": "Permissão não catalogada neste servidor",
                    "permite": (
                        "Não há descrição registrada para esta permissão. "
                        "Confira no painel da Meta o que ela concede antes de autorizar."
                    ),
                }
            )
            continue
        descricoes.append({"escopo": escopo, **detalhe})
    return descricoes


# =====================================================================
# Camada 2: runtime OAuth do Instagram
# =====================================================================
#
# O runtime precisa ser de vida longa e único no processo: o state
# gerado por `instagram_oauth_iniciar` só pode ser validado pelo mesmo
# StateStore quando a Meta chamar o callback, e o token gravado pelo
# callback só é visível para as demais ferramentas se o TokenStore for o
# mesmo objeto.
#
# A resolução é preguiçosa (na primeira utilização, não no import) para
# que o módulo continue importável sem nenhuma variável de ambiente
# definida. O sentinela abaixo distingue "ainda não resolvido" de
# "resolvido como None" (Camada 2 desligada).

_RUNTIME_NAO_RESOLVIDO = object()
_instagram_runtime: InstagramOAuthRuntime | None | object = _RUNTIME_NAO_RESOLVIDO


def resolve_instagram_runtime(env=None) -> InstagramOAuthRuntime | None:
    """
    Monta o runtime da Camada 2 a partir do ambiente, ou devolve None se
    ela não estiver configurada. Não acessa rede.
    """
    config = resolve_instagram_config(env)
    if config is None:
        return None
    return build_runtime(config)


def get_instagram_runtime() -> InstagramOAuthRuntime | None:
    """Devolve o runtime único do processo, resolvendo-o na primeira chamada."""
    global _instagram_runtime
    if _instagram_runtime is _RUNTIME_NAO_RESOLVIDO:
        _instagram_runtime = resolve_instagram_runtime()
    return _instagram_runtime  # type: ignore[return-value]


@mcp.tool()
def instagram_mcp_status() -> dict:
    """Retorna o status do componente e da conexão, sem acessar o Instagram."""
    runtime = get_instagram_runtime()

    if runtime is None:
        return {
            "componente": "mcp-instagram",
            "oauth": "nao_configurado",
            "instagram": "nao_conectado",
            "status": "operacional",
            "variaveis_ausentes": missing_instagram_env_vars(),
        }

    conectado = runtime.has_valid_token()

    # Onde o token é guardado decide se a autorização sobrevive a um
    # reinício do contêiner. O backend 'memory' perde tudo quando o
    # serviço hiberna (no plano gratuito do Render isso acontece após
    # poucos minutos ocioso), e o sintoma que chega ao captador é
    # "ontem estava conectado e hoje não está". Sem este campo, esse
    # diagnóstico exige acesso ao painel do Render; com ele, a própria
    # ferramenta de status responde.
    backend = runtime.config.token_store_backend
    autorizacao_sobrevive_a_reinicio = backend != TOKEN_STORE_BACKEND_MEMORY

    return {
        "componente": "mcp-instagram",
        "oauth": "configurado",
        "instagram": "conectado" if conectado else "nao_conectado",
        "status": "operacional",
        "onde_o_token_fica_guardado": backend,
        "autorizacao_sobrevive_a_reinicio": autorizacao_sobrevive_a_reinicio,
        "aviso_de_persistencia": (
            None
            if autorizacao_sobrevive_a_reinicio
            else (
                "O token está apenas na memória deste servidor. Quando o serviço "
                "reiniciar ou hibernar, a autorização será perdida e será preciso "
                "autorizar de novo. Para a autorização durar, configure "
                "INSTAGRAM_TOKEN_STORE_BACKEND com 'ponte' e as variáveis da ponte."
            )
        ),
        "conta_conectada": runtime.connected_user_id() if conectado else None,
        "escopos_configurados": list(runtime.config.scopes),
        "somente_leitura": runtime.config.somente_leitura,
        "escopos_de_escrita": list(runtime.config.escopos_de_escrita),
        "acoes_possiveis": (
            "Nenhuma. Este servidor não publica, não edita, não exclui, não "
            "responde mensagens e não administra anúncios."
        ),
        "variaveis_ausentes": [],
    }


@mcp.tool()
def instagram_oauth_iniciar() -> dict:
    """
    Inicia a autorização do Instagram e devolve a URL que o captador
    precisa abrir no navegador, junto com a descrição exata de cada
    permissão que será solicitada.

    Não acessa o Instagram e não abre navegador: só monta a URL. Depois
    que o captador autorizar, a própria Meta chama o callback deste
    servidor, que conclui a troca por token automaticamente.
    """
    runtime = get_instagram_runtime()

    if runtime is None:
        return {
            "status": "nao_configurado",
            "detalhe": (
                "A conexão com o Instagram ainda não foi configurada neste servidor. "
                "Configure as variáveis listadas em variaveis_ausentes e reinicie o serviço."
            ),
            "variaveis_ausentes": missing_instagram_env_vars(),
        }

    autorizacao = runtime.start_authorization()

    return {
        "status": "aguardando_autorizacao",
        "url_autorizacao": autorizacao.url,
        "escopos_solicitados": list(runtime.config.scopes),
        "permissoes": descrever_permissoes(runtime.config.scopes),
        "somente_leitura": runtime.config.somente_leitura,
        "como_revogar": COMO_REVOGAR,
        "detalhe": (
            "Abra a URL acima no navegador, entre com a conta comercial do Instagram "
            "e autorize o acesso. Nenhuma senha é pedida por este servidor: a senha é "
            "digitada apenas no site do próprio Instagram. A autorização expira em 10 "
            "minutos. Depois de autorizar, confira o resultado com a ferramenta "
            "instagram_oauth_status."
        ),
    }


@mcp.tool()
def instagram_oauth_status() -> dict:
    """
    Informa se existe um access token válido do Instagram guardado neste
    servidor. Nunca devolve o token em si.
    """
    runtime = get_instagram_runtime()

    if runtime is None:
        return {
            "status": "nao_configurado",
            "detalhe": "A conexão com o Instagram ainda não foi configurada neste servidor.",
            "variaveis_ausentes": missing_instagram_env_vars(),
        }

    if runtime.has_valid_token():
        return {
            "status": "conectado",
            "conta_conectada": runtime.connected_user_id(),
            "expira_em": runtime.token_expires_at(),
            "escopos_concedidos": list(runtime.config.scopes),
            "somente_leitura": runtime.config.somente_leitura,
            "detalhe": (
                "Existe uma autorização válida do Instagram guardada neste servidor. "
                "Nenhuma ação foi executada na conta."
            ),
            "como_revogar": COMO_REVOGAR,
        }

    return {
        "status": "nao_conectado",
        "detalhe": (
            "Não existe autorização válida do Instagram. Use a ferramenta "
            "instagram_oauth_iniciar para autorizar."
        ),
    }


@mcp.tool()
def instagram_desconectar() -> dict:
    """
    Apaga a autorização do Instagram guardada NESTE servidor.

    Não executa nenhuma ação na conta do Instagram: nada é publicado,
    editado ou excluído lá. Depois disto, este servidor perde o acesso na
    hora. Para remover também o aplicativo do lado da Meta, use o próprio
    Instagram (ver como_revogar).
    """
    runtime = get_instagram_runtime()

    if runtime is None:
        return {
            "status": "nao_configurado",
            "detalhe": "A conexão com o Instagram não está configurada neste servidor.",
        }

    runtime.token_store.delete_access_token()

    return {
        "status": "desconectado",
        "detalhe": (
            "A autorização guardada neste servidor foi apagada. Nenhuma alteração "
            "foi feita na conta do Instagram."
        ),
        "como_revogar": COMO_REVOGAR,
    }


# =====================================================================
# Ferramentas de negócio: LEITURA da conta
# =====================================================================
#
# Todas somente leitura. O cliente usado aqui recebe um transporte que
# expõe apenas `get`, então nenhuma destas ferramentas pode publicar,
# editar, excluir, comentar ou responder mensagem, mesmo por engano.
#
# O cliente é preguiçoso e único no processo pelo mesmo motivo do
# runtime: ele lê o token do TokenStore a cada chamada, e precisa ser o
# MESMO TokenStore que o callback preencheu.

_CLIENTE_NAO_RESOLVIDO = object()
_cliente_leitura: "ClienteLeituraInstagram | None | object" = _CLIENTE_NAO_RESOLVIDO


def get_cliente_leitura() -> "ClienteLeituraInstagram | None":
    """
    Devolve o cliente de leitura único do processo, ou None se a Camada 2
    não estiver configurada. Não acessa rede: o transporte só abre
    conexão quando `get` é de fato chamado.
    """
    global _cliente_leitura
    if _cliente_leitura is _CLIENTE_NAO_RESOLVIDO:
        runtime = get_instagram_runtime()
        if runtime is None:
            _cliente_leitura = None
        else:
            _cliente_leitura = ClienteLeituraInstagram(
                transporte=TransporteGraphHttpx(),
                obter_token=runtime.token_store.get_access_token,
            )
    return _cliente_leitura  # type: ignore[return-value]


def _executar_leitura(operacao) -> dict:
    """
    Executa uma leitura e traduz as falhas possíveis em resposta de
    ferramenta. A mensagem de erro da Meta é repassada como veio: ela
    diz exatamente o que faltou (permissão, métrica indisponível, id
    inexistente) e não contém credencial. Trocá-la por um texto genérico
    só tornaria o problema mais difícil de resolver.
    """
    cliente = get_cliente_leitura()

    if cliente is None:
        return {
            "status": "nao_configurado",
            "detalhe": "A conexão com o Instagram não está configurada neste servidor.",
            "variaveis_ausentes": missing_instagram_env_vars(),
        }

    try:
        return {"status": "ok", "dados": operacao(cliente)}
    except SemAutorizacaoError as erro:
        return {"status": "nao_conectado", "detalhe": str(erro)}
    except ErroDaApi as erro:
        return {"status": "recusado_pela_meta", **erro.como_dicionario()}
    except ErroDeTransporte as erro:
        return {"status": "falha_de_rede", "detalhe": str(erro)}


@mcp.tool()
def instagram_perfil() -> dict:
    """
    Lê os dados do perfil da conta conectada: nome de usuário, tipo de
    conta, número de seguidores, número de publicações e biografia.

    Somente leitura. Nada é alterado na conta.
    """
    return _executar_leitura(lambda cliente: cliente.perfil())


@mcp.tool()
def instagram_publicacoes(limite: int = LIMITE_PUBLICACOES_PADRAO) -> dict:
    """
    Lista as publicações mais recentes, da mais nova para a mais antiga,
    com legenda, tipo, link, data, curtidas e comentários.

    `limite` aceita de 1 a 50; valor fora da faixa é ajustado para o mais
    próximo em vez de virar erro. Somente leitura.
    """
    return _executar_leitura(lambda cliente: cliente.publicacoes(limite))


@mcp.tool()
def instagram_metricas_publicacao(id_publicacao: str) -> dict:
    """
    Métricas de uma publicação específica: alcance, curtidas,
    comentários, salvamentos, compartilhamentos, interações e
    visualizações.

    O `id_publicacao` vem do campo `id` devolvido por
    `instagram_publicacoes`. Somente leitura.

    Nem toda métrica existe para toda publicação: o conjunto varia com o
    tipo de mídia e com o tipo de conta. Quando a Meta recusa uma
    métrica, a resposta traz a mensagem dela, não um erro genérico.
    """
    return _executar_leitura(lambda cliente: cliente.metricas_publicacao(id_publicacao))


@mcp.tool()
def instagram_metricas_conta(dias: int = JANELA_DIAS_PADRAO) -> dict:
    """
    Métricas agregadas da conta na janela pedida: alcance,
    visualizações, interações e contas engajadas.

    `dias` aceita de 1 a 30, que é o teto da Meta para esta consulta;
    valor maior é reduzido a 30 em vez de virar erro. Somente leitura.

    Conta do tipo Comercial entrega mais métrica que Criador de
    conteúdo. Se algo vier recusado, a resposta traz a explicação da
    própria Meta.
    """
    return _executar_leitura(lambda cliente: cliente.metricas_conta(dias))


@mcp.custom_route(INSTAGRAM_CALLBACK_PATH, methods=["GET"])
async def instagram_oauth_callback(request: Request) -> JSONResponse:
    """
    Callback OAuth chamado pela própria Meta depois que o captador
    autoriza. Rota pública por necessidade do protocolo (a Meta não envia
    o Bearer da Camada 1); a proteção contra chamada forjada é o `state`
    de uso único, validado por `process_callback` antes de qualquer coisa
    acontecer com o authorization code.

    Responde JSON, nunca HTML: este componente não tem interface web.
    Nenhuma resposta inclui o authorization code, o state ou o access
    token.
    """
    runtime = get_instagram_runtime()

    if runtime is None:
        return JSONResponse(
            {
                "status": "nao_configurado",
                "detalhe": "A conexão com o Instagram não está configurada neste servidor.",
            },
            status_code=503,
        )

    params = CallbackParams(
        code=request.query_params.get("code"),
        state=request.query_params.get("state"),
        error=request.query_params.get("error"),
        error_description=request.query_params.get("error_description"),
    )

    try:
        resultado = runtime.handle_callback(params)
    except (TokenExchangeError, TransportError, TokenStoreBackendError, ValueError):
        # A mensagem original fica de fora da resposta de propósito: ela
        # pertence ao operador do serviço, não ao navegador que chegou no
        # callback. Nenhuma delas contém segredo, mas expor detalhe
        # interno a quem abriu a URL não traz benefício.
        return JSONResponse(
            {
                "status": "erro_na_troca_de_token",
                "detalhe": (
                    "A autorização foi recebida, mas a troca por token falhou. "
                    "Tente novamente."
                ),
            },
            status_code=502,
        )

    if resultado.outcome is CallbackOutcome.TOKEN_EXCHANGE_STARTED:
        return JSONResponse(
            {
                "status": "conectado",
                "detalhe": "Instagram autorizado com sucesso. Pode fechar esta página.",
            },
            status_code=200,
        )

    corpo = {
        "status": "rejeitado",
        "motivo": resultado.outcome.value,
        "detalhe": resultado.detail,
    }
    if resultado.oauth_error:
        corpo["erro_instagram"] = resultado.oauth_error

    return JSONResponse(corpo, status_code=400)


# =====================================================================
# Rotas exigidas pela Meta: desautorização e exclusão de dados
# =====================================================================
#
# A Meta chama as duas por POST, com uma requisição assinada, e sem
# nenhum token de autenticação nosso. A prova de origem é a assinatura
# HMAC-SHA256 feita com o Client Secret (ver signed_request.py). Sem
# essa verificação, qualquer pessoa que descobrisse a URL poderia apagar
# a autorização do captador enviando um POST vazio.
#
# As duas fazem a mesma coisa do nosso lado, e isso é honesto: o único
# dado pessoal que este servidor guarda é o próprio token de acesso,
# junto do identificador da conta. Não há histórico, cópia de
# publicação, métrica arquivada ou qualquer outro dado para apagar,
# porque nenhuma ferramenta de leitura de conteúdo existe aqui. Apagar
# o token é, literalmente, apagar tudo.

# Códigos de confirmação dos pedidos de exclusão já atendidos. Ficam em
# memória do processo: reiniciar o serviço esvazia a lista, e um código
# antigo passa a responder "desconhecido". É uma limitação conhecida e
# aceitável, porque a exclusão em si (apagar o token) já aconteceu e é
# permanente; o que se perde é apenas o comprovante de consulta.
_EXCLUSOES_ATENDIDAS: dict[str, float] = {}


async def _verificar_requisicao_da_meta(request: Request, runtime) -> bool:
    """
    Confere a assinatura da requisição. Devolve True se veio mesmo da
    Meta. Nunca registra em log a requisição nem o segredo.
    """
    formulario = await request.form()
    valor = formulario.get("signed_request")

    try:
        parse_signed_request(
            valor if isinstance(valor, str) else None,
            runtime.config.client_secret,
        )
    except InvalidSignedRequestError:
        return False

    return True


@mcp.custom_route(INSTAGRAM_DEAUTHORIZE_PATH, methods=["POST"])
async def instagram_desautorizacao(request: Request) -> JSONResponse:
    """
    Chamada pela Meta quando a pessoa remove o aplicativo nas
    configurações do Instagram. Apaga a autorização guardada aqui.
    """
    runtime = get_instagram_runtime()

    if runtime is None:
        return JSONResponse({"status": "nao_configurado"}, status_code=503)

    if not await _verificar_requisicao_da_meta(request, runtime):
        return JSONResponse({"status": "rejeitado"}, status_code=400)

    runtime.token_store.delete_access_token()

    return JSONResponse({"status": "desautorizado"}, status_code=200)


@mcp.custom_route(INSTAGRAM_DATA_DELETION_PATH, methods=["POST"])
async def instagram_exclusao_de_dados(request: Request) -> JSONResponse:
    """
    Chamada pela Meta quando a pessoa pede exclusão dos dados. Apaga a
    autorização guardada e devolve, no formato exigido pela Meta, o
    endereço de acompanhamento e um código de confirmação.
    """
    runtime = get_instagram_runtime()

    if runtime is None:
        return JSONResponse({"status": "nao_configurado"}, status_code=503)

    if not await _verificar_requisicao_da_meta(request, runtime):
        return JSONResponse({"status": "rejeitado"}, status_code=400)

    runtime.token_store.delete_access_token()

    codigo = secrets.token_hex(8)
    _EXCLUSOES_ATENDIDAS[codigo] = time.time()

    base = runtime.config.public_base_url

    # Nomes de campo definidos pela Meta, por isso em inglês: ela recusa
    # a resposta se vierem com outro nome.
    return JSONResponse(
        {
            "url": f"{base}{INSTAGRAM_DATA_DELETION_STATUS_PATH}?codigo={codigo}",
            "confirmation_code": codigo,
        },
        status_code=200,
    )


@mcp.custom_route(INSTAGRAM_DATA_DELETION_STATUS_PATH, methods=["GET"])
async def instagram_exclusao_de_dados_status(request: Request) -> JSONResponse:
    """
    Página de acompanhamento do pedido de exclusão, cujo endereço a Meta
    exige que seja devolvido no pedido. Responde JSON, porque este
    componente não tem interface web.
    """
    codigo = request.query_params.get("codigo")

    if codigo and codigo in _EXCLUSOES_ATENDIDAS:
        return JSONResponse(
            {
                "status": "concluido",
                "detalhe": (
                    "A autorização e o identificador da conta foram apagados deste "
                    "servidor. Nenhum outro dado era guardado."
                ),
            },
            status_code=200,
        )

    return JSONResponse(
        {
            "status": "desconhecido",
            "detalhe": (
                "Não há registro deste código de confirmação neste servidor. Isso "
                "acontece quando o código não existe ou quando o serviço foi "
                "reiniciado depois da exclusão. A exclusão em si é permanente."
            ),
        },
        status_code=404,
    )


STREAMABLE_HTTP_HOST = "0.0.0.0"
STREAMABLE_HTTP_PATH = "/mcp"
VALID_TRANSPORTS = {"stdio", "streamable-http"}


class InvalidTransportConfigError(ValueError):
    """MCP_TRANSPORT ou PORT inválidos/incompletos. Nunca contém segredo."""


@dataclass(frozen=True)
class StdioRunConfig:
    """Configuração de execução local, via entrada/saída padrão do processo."""

    transport: str = "stdio"


@dataclass(frozen=True)
class StreamableHttpRunConfig:
    """Configuração de execução remota, via HTTP."""

    transport: str = "streamable-http"
    host: str = STREAMABLE_HTTP_HOST
    port: int = 0
    streamable_http_path: str = STREAMABLE_HTTP_PATH


def resolve_run_config(env: Mapping[str, str] | None = None):
    """
    Lê MCP_TRANSPORT (e PORT, quando aplicável) do ambiente informado
    (por padrão, os.environ) e devolve StdioRunConfig ou
    StreamableHttpRunConfig. Não inicia nenhum servidor, não abre porta,
    não acessa rede.
    """
    env = env if env is not None else os.environ

    transport = env.get("MCP_TRANSPORT", "stdio").strip()

    if transport not in VALID_TRANSPORTS:
        raise InvalidTransportConfigError(
            "MCP_TRANSPORT inválido: use 'stdio' ou 'streamable-http'."
        )

    if transport == "stdio":
        return StdioRunConfig()

    porta_bruta = env.get("PORT")
    if not porta_bruta:
        raise InvalidTransportConfigError(
            "MCP_TRANSPORT=streamable-http exige a variável PORT definida."
        )

    try:
        porta = int(porta_bruta)
    except ValueError:
        raise InvalidTransportConfigError("PORT precisa ser um número inteiro.") from None

    if not (0 < porta <= 65535):
        raise InvalidTransportConfigError("PORT fora do intervalo válido (1 a 65535).")

    return StreamableHttpRunConfig(port=porta)


@dataclass(frozen=True)
class ClaudeAuthConfig:
    """Configuração resolvida da Camada 1 (Claude e mcp-instagram), ou None se desligada."""

    provider: ClaudeAuthProvider
    token_verifier: ProviderTokenVerifier
    auth_settings: AuthSettings


def resolve_claude_auth_config(env: Mapping[str, str] | None = None) -> ClaudeAuthConfig | None:
    """
    Lê a configuração da Camada 1 do ambiente informado (por padrão,
    os.environ) e devolve um ClaudeAuthConfig, ou None se
    MCP_CLAUDE_CLIENT_ID ou MCP_PUBLIC_BASE_URL não estiverem definidos
    (Camada 1 desligada). Não inicia nenhum servidor, não acessa rede.

    DCR (/register) e revogação (/revoke) ficam desligados aqui de
    propósito: só um cliente estático é reconhecido, pré-registrado via
    MCP_CLAUDE_CLIENT_ID (e, opcionalmente, MCP_CLAUDE_CLIENT_SECRET).
    Nenhum desses valores é registrado em log aqui.
    """
    env = env if env is not None else os.environ

    client_id = env.get("MCP_CLAUDE_CLIENT_ID")
    base_url = env.get("MCP_PUBLIC_BASE_URL")

    if not client_id or not base_url:
        return None

    client_secret = env.get("MCP_CLAUDE_CLIENT_SECRET") or None
    base_url = base_url.rstrip("/")

    store = ClaudeSessionStore()
    provider = ClaudeAuthProvider(client_id=client_id, client_secret=client_secret, store=store)
    token_verifier = ProviderTokenVerifier(provider)

    auth_settings = AuthSettings(
        issuer_url=base_url,
        resource_server_url=f"{base_url}{STREAMABLE_HTTP_PATH}",
        client_registration_options=ClientRegistrationOptions(enabled=False),
        revocation_options=RevocationOptions(enabled=False),
    )

    return ClaudeAuthConfig(
        provider=provider, token_verifier=token_verifier, auth_settings=auth_settings
    )


def apply_claude_auth_config(server: MCPServer, auth_config: ClaudeAuthConfig) -> None:
    """
    Aplica a configuração da Camada 1 num MCPServer já construído.

    MCPServer não expõe um setter público para isto: estes são os mesmos
    atributos "privados" (`_auth_server_provider`, `_token_verifier`) e a
    configuração (`settings.auth`) que `streamable_http_app()`/`run()`
    leem em tempo de chamada, não em tempo de construção. Essa mutação
    pós-construção é o mecanismo necessário nesta versão do SDK, não uma
    escolha de conveniência, e não deve ser trocada sem reconferir contra
    uma versão futura do SDK. Foi extraída como função própria para que o
    teste de integração exercite exatamente este mesmo caminho.
    """
    server._auth_server_provider = auth_config.provider
    server._token_verifier = auth_config.token_verifier
    server.settings.auth = auth_config.auth_settings


def main() -> None:
    config = resolve_run_config()

    if isinstance(config, StreamableHttpRunConfig):
        auth_config = resolve_claude_auth_config()
        if auth_config is not None:
            apply_claude_auth_config(mcp, auth_config)

        mcp.run(
            transport="streamable-http",
            host=config.host,
            port=config.port,
            streamable_http_path=config.streamable_http_path,
        )
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
