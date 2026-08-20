"""
Troca de authorization code por access token do Instagram (Camada 2,
mcp-instagram para Instagram).

DIFERENÇA CENTRAL EM RELAÇÃO AO LINKEDIN: no Instagram a troca tem DUAS
etapas obrigatórias, não uma.

    1. authorization_code  -> api.instagram.com/oauth/access_token
                              devolve um token de CURTA duração (1 hora)
                              e o id da conta. Não devolve expires_in.

    2. token de curta      -> graph.instagram.com/access_token
                              (grant_type=ig_exchange_token)
                              devolve o token de LONGA duração
                              (60 dias) e o expires_in de verdade.

Parar na etapa 1 produziria uma conexão que morre em uma hora, o que na
prática não é uma conexão. Por isso `exchange_code_for_token` só
considera a troca concluída depois da etapa 2.

Este módulo separa responsabilidades como o equivalente do mcp-linkedin:

1. `build_short_lived_token_request` e `build_long_lived_token_request`
   montam as requisições como dado puro, sem executar nada;
2. `exchange_code_for_token` executa as duas através de um transporte
   HTTP injetável (`HttpTransport`), interpreta as respostas e calcula
   `expires_at`.

Segurança:
- na etapa 1, o Client Secret e o authorization code viajam somente no
  corpo do POST, nunca na URL;
- na etapa 2, a Meta exige o Client Secret e o token na QUERY STRING do
  GET. Não existe variante POST documentada para esse endpoint, então a
  alternativa seria não ter token de longa duração. A mitigação é
  estrita: `TokenRequest.__repr__` mascara os dois valores, nenhuma
  função aqui imprime, registra em log ou inclui a URL montada em
  mensagem de erro, e o transporte real (http_transport.py) converte as
  exceções com `from None` para o traceback não carregar o objeto da
  requisição;
- nenhuma mensagem de erro deste módulo contém Client Secret,
  authorization code ou access token.
"""

from __future__ import annotations

import json as json_module
from dataclasses import dataclass
from typing import Callable, Protocol

from mcp_instagram.auth_instagram.token_store import TokenStore

SHORT_LIVED_TOKEN_ENDPOINT = "https://api.instagram.com/oauth/access_token"
LONG_LIVED_TOKEN_ENDPOINT = "https://graph.instagram.com/access_token"

_CAMPOS_SENSIVEIS = {"client_secret", "code", "access_token"}


@dataclass(frozen=True)
class TokenExchangeConfig:
    """Credenciais e redirect_uri do aplicativo, usados somente na troca."""

    client_id: str
    client_secret: str
    redirect_uri: str


@dataclass(frozen=True)
class TokenRequest:
    """Requisição HTTP preparada, ainda não executada."""

    method: str
    url: str
    params: dict

    def __repr__(self) -> str:
        # Nunca expor client_secret, code ou access_token, mesmo que
        # este objeto vá parar num log ou traceback por acidente.
        campos_mascarados = {
            chave: ("***" if chave in _CAMPOS_SENSIVEIS else valor)
            for chave, valor in self.params.items()
        }
        return f"TokenRequest(method={self.method!r}, url={self.url!r}, params={campos_mascarados!r})"


@dataclass(frozen=True)
class HttpResponse:
    """Resposta crua devolvida por um HttpTransport."""

    status_code: int
    text: str


class HttpTransport(Protocol):
    """Interface mínima de transporte HTTP, injetável para teste."""

    def post(self, url: str, data: dict) -> HttpResponse: ...

    def get(self, url: str, params: dict) -> HttpResponse: ...


class TransportError(Exception):
    """Erro de transporte (timeout, conexão recusada). Nunca contém segredo."""


class TokenExchangeError(Exception):
    """Erro ao interpretar a resposta da Meta. Nunca contém segredo."""


@dataclass(frozen=True)
class ShortLivedToken:
    """Resultado da etapa 1: token de curta duração e id da conta."""

    access_token: str
    user_id: str


@dataclass(frozen=True)
class TokenExchangeResult:
    """Resultado final, pronto para ser entregue ao TokenStore."""

    access_token: str
    expires_at: float
    user_id: str | None = None


def build_short_lived_token_request(
    config: TokenExchangeConfig, authorization_code: str
) -> TokenRequest:
    """
    Monta a requisição POST da etapa 1 (code para token de curta
    duração), sem executá-la.

    client_secret e authorization_code vão somente no corpo, nunca
    concatenados na URL.
    """
    form_data = {
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "grant_type": "authorization_code",
        "redirect_uri": config.redirect_uri,
        "code": authorization_code,
    }
    return TokenRequest(method="POST", url=SHORT_LIVED_TOKEN_ENDPOINT, params=form_data)


def build_long_lived_token_request(
    config: TokenExchangeConfig, short_lived_token: str
) -> TokenRequest:
    """
    Monta a requisição GET da etapa 2 (token de curta para token de
    longa duração), sem executá-la.

    A Meta só documenta este endpoint como GET com os parâmetros na
    query string, incluindo o Client Secret. Ver a nota de segurança no
    topo do módulo.
    """
    params = {
        "grant_type": "ig_exchange_token",
        "client_secret": config.client_secret,
        "access_token": short_lived_token,
    }
    return TokenRequest(method="GET", url=LONG_LIVED_TOKEN_ENDPOINT, params=params)


def _validar_status(status_code: int) -> None:
    """Traduz o status HTTP da Meta, sem nunca ecoar o corpo da resposta."""
    if status_code == 400:
        raise TokenExchangeError("A Meta recusou a requisição (HTTP 400): parâmetros inválidos.")
    if status_code == 401:
        raise TokenExchangeError("A Meta recusou a requisição (HTTP 401): credenciais inválidas.")
    if status_code == 403:
        raise TokenExchangeError("A Meta recusou a requisição (HTTP 403): acesso negado.")
    if status_code != 200:
        raise TokenExchangeError(f"A Meta retornou status HTTP inesperado: {status_code}.")


def _decodificar_payload(texto: str) -> dict:
    """Decodifica o JSON da Meta e recusa qualquer coisa que não seja um objeto."""
    try:
        payload = json_module.loads(texto)
    except json_module.JSONDecodeError:
        raise TokenExchangeError("A resposta da Meta não é um JSON válido.") from None

    if not isinstance(payload, dict):
        raise TokenExchangeError("A resposta da Meta não é um objeto JSON válido.")

    if "error" in payload or "error_type" in payload:
        raise TokenExchangeError("A Meta retornou um erro OAuth na troca de token.")

    return payload


def _extrair_token_curto(payload: dict) -> ShortLivedToken:
    """
    Lê o token de curta duração e o id da conta.

    A Meta usa dois formatos para esta resposta, conforme a versão do
    aplicativo: o atual embrulha tudo numa lista em `data`, e o legado
    devolve os campos na raiz. Os dois são aceitos aqui, porque o
    formato depende de configuração do painel da Meta, fora do nosso
    controle, e falhar por isso seria um erro difícil de diagnosticar.
    """
    dados = payload
    bloco = payload.get("data")
    if isinstance(bloco, list) and bloco and isinstance(bloco[0], dict):
        dados = bloco[0]

    access_token = dados.get("access_token")
    if not access_token or not isinstance(access_token, str):
        raise TokenExchangeError("A resposta da Meta não contém access_token válido.")

    user_id = dados.get("user_id")
    if user_id is None:
        raise TokenExchangeError("A resposta da Meta não contém o identificador da conta.")

    return ShortLivedToken(access_token=access_token, user_id=str(user_id))


def _extrair_expires_in(payload: dict) -> float:
    """Lê e valida o expires_in da etapa 2."""
    expires_in = payload.get("expires_in")
    if expires_in is None:
        raise TokenExchangeError("A resposta da Meta não contém expires_in.")
    if isinstance(expires_in, bool) or not isinstance(expires_in, (int, float)) or expires_in <= 0:
        raise TokenExchangeError("A resposta da Meta contém expires_in inválido.")
    return float(expires_in)


def _executar(chamada: Callable[[], HttpResponse]) -> HttpResponse:
    """
    Executa uma chamada de transporte convertendo qualquer falha em
    TransportError, sem deixar a exceção original encadeada (ela pode
    referenciar o objeto da requisição, onde estão as credenciais).
    """
    try:
        return chamada()
    except TransportError:
        raise
    except TimeoutError:
        raise TransportError("Timeout na troca de authorization code por token.") from None
    except Exception:
        raise TransportError(
            "Falha de transporte na troca de authorization code por token."
        ) from None


def exchange_code_for_token(
    config: TokenExchangeConfig,
    authorization_code: str,
    transport: HttpTransport,
    clock: Callable[[], float],
) -> TokenExchangeResult:
    """
    Executa as DUAS etapas da troca através do transporte injetado e
    devolve o token de longa duração, com
    expires_at = agora (via clock) + expires_in.

    Se a etapa 2 falhar, a função inteira falha: um token de uma hora
    não é uma conexão utilizável, e devolvê-lo silenciosamente daria ao
    captador a impressão falsa de que a conexão está estabelecida.
    """
    curto_request = build_short_lived_token_request(config, authorization_code)
    resposta_curta = _executar(
        lambda: transport.post(curto_request.url, curto_request.params)
    )
    _validar_status(resposta_curta.status_code)
    token_curto = _extrair_token_curto(_decodificar_payload(resposta_curta.text))

    longo_request = build_long_lived_token_request(config, token_curto.access_token)
    resposta_longa = _executar(
        lambda: transport.get(longo_request.url, longo_request.params)
    )
    _validar_status(resposta_longa.status_code)
    payload_longo = _decodificar_payload(resposta_longa.text)

    access_token = payload_longo.get("access_token")
    if not access_token or not isinstance(access_token, str):
        raise TokenExchangeError(
            "A resposta da Meta não contém o access_token de longa duração."
        )

    expires_at = clock() + _extrair_expires_in(payload_longo)

    return TokenExchangeResult(
        access_token=access_token,
        expires_at=expires_at,
        user_id=token_curto.user_id,
    )


class TokenExchangeCallable(Protocol):
    """Interface mínima de um exchange já pronto para ser chamado só com o code."""

    def __call__(self, authorization_code: str) -> TokenExchangeResult: ...


def exchange_and_store_token(
    authorization_code: str,
    token_exchanger: TokenExchangeCallable | Callable[[str], TokenExchangeResult],
    token_store: TokenStore,
) -> TokenExchangeResult:
    """
    Executa a troca (via `token_exchanger` injetado) e, somente se ela
    for bem-sucedida e o resultado for válido, grava no TokenStore.

    Se `token_exchanger` levantar uma exceção (troca falhou), essa
    exceção se propaga e NADA é gravado. Se `save_access_token` falhar,
    a exceção também se propaga; nem esta função nem os módulos que ela
    chama incluem access_token ou Client Secret em mensagem de erro.
    """
    result = token_exchanger(authorization_code)

    if not result.access_token or not isinstance(result.access_token, str):
        raise ValueError("Resultado da troca sem access_token válido; nada foi gravado.")

    if (
        not isinstance(result.expires_at, (int, float))
        or isinstance(result.expires_at, bool)
        or result.expires_at <= 0
    ):
        raise ValueError("Resultado da troca com expires_at inválido; nada foi gravado.")

    token_store.save_access_token(result.access_token, result.expires_at, result.user_id)
    return result
