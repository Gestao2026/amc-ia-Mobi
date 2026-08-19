"""
Troca de authorization code por access token do LinkedIn (Camada 2,
mcp-linkedin -> LinkedIn), Authorization Code Flow.

    authorization_code -> LinkedIn token endpoint -> access_token + expires_in

Este modulo separa duas responsabilidades:

1. `build_token_request` monta a requisicao (metodo, URL, corpo),
   como dado puro, sem executar nada;
2. `exchange_code_for_token` executa essa requisicao atraves de um
   transporte HTTP injetavel (`HttpTransport`), interpreta a
   resposta e calcula `expires_at`.

Nao executa OAuth real, nao abre navegador, nao acessa o LinkedIn
diretamente (nenhuma implementacao real de `HttpTransport` existe
aqui). O Client Secret e o authorization code so viajam no corpo da
requisicao POST, nunca na URL, e nenhuma funcao deste modulo imprime,
loga ou inclui Client Secret, authorization code ou access token em
mensagem de erro.

`exchange_and_store_token` compoe o resultado de uma troca
(`TokenExchangeResult`, access_token + expires_at) com o TokenStore
(Etapa 3D), que ja aceita exatamente esses dois valores em
`save_access_token(access_token, expires_at)`. Essa funcao so grava
no TokenStore se o exchange (via `token_exchanger` injetado) tiver
sido bem-sucedido; se ele falhar, nada e gravado. Ela nao sabe nada
de HttpTransport: quem monta o `token_exchanger` (uma chamada parcial
de `exchange_code_for_token` com config/transport/clock ja fixados,
em producao, ou um fake nos testes) e responsabilidade de quem chama.
"""

from __future__ import annotations

import json as json_module
from dataclasses import dataclass
from typing import Callable, Protocol

from mcp_linkedin.auth_linkedin.token_store import TokenStore

TOKEN_ENDPOINT = "https://www.linkedin.com/oauth/v2/accessToken"

_CAMPOS_SENSIVEIS = {"client_secret", "code"}


@dataclass(frozen=True)
class TokenExchangeConfig:
    """Credenciais e redirect_uri do app Mobi, usados somente na troca code -> token."""

    client_id: str
    client_secret: str
    redirect_uri: str


@dataclass(frozen=True)
class TokenRequest:
    """Requisicao HTTP preparada, ainda nao executada."""

    method: str
    url: str
    form_data: dict

    def __repr__(self) -> str:
        # Nunca expor client_secret/code, mesmo que este objeto va
        # parar num log ou traceback por acidente.
        campos_mascarados = {
            chave: ("***" if chave in _CAMPOS_SENSIVEIS else valor)
            for chave, valor in self.form_data.items()
        }
        return f"TokenRequest(method={self.method!r}, url={self.url!r}, form_data={campos_mascarados!r})"


@dataclass(frozen=True)
class HttpResponse:
    """Resposta crua devolvida por um HttpTransport."""

    status_code: int
    text: str


class HttpTransport(Protocol):
    """Interface minima de transporte HTTP, injetavel para teste."""

    def post(self, url: str, data: dict) -> HttpResponse: ...


class TransportError(Exception):
    """Erro de transporte (timeout, conexao recusada etc). Nunca contem segredo."""


class TokenExchangeError(Exception):
    """Erro ao interpretar a resposta do token endpoint. Nunca contem segredo."""


@dataclass(frozen=True)
class TokenExchangeResult:
    """Resultado pronto para ser entregue a TokenStore.save_access_token(...)."""

    access_token: str
    expires_at: float


def build_token_request(config: TokenExchangeConfig, authorization_code: str) -> TokenRequest:
    """
    Monta a requisicao POST de troca code -> token, sem executa-la.

    client_secret e authorization_code vao somente no corpo
    (form_data), nunca sao concatenados na URL.
    """
    form_data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": config.redirect_uri,
        "client_id": config.client_id,
        "client_secret": config.client_secret,
    }
    return TokenRequest(method="POST", url=TOKEN_ENDPOINT, form_data=form_data)


def exchange_code_for_token(
    config: TokenExchangeConfig,
    authorization_code: str,
    transport: HttpTransport,
    clock: Callable[[], float],
) -> TokenExchangeResult:
    """
    Executa a troca atraves do transporte injetado, interpreta a
    resposta e calcula expires_at = agora (via clock) + expires_in.
    """
    request = build_token_request(config, authorization_code)

    try:
        response = transport.post(request.url, request.form_data)
    except TransportError:
        raise
    except TimeoutError:
        raise TransportError("Timeout na troca de authorization code por token.") from None
    except Exception:
        raise TransportError("Falha de transporte na troca de authorization code por token.") from None

    if response.status_code == 400:
        raise TokenExchangeError("LinkedIn recusou a requisicao (HTTP 400): parametros invalidos.")
    if response.status_code == 401:
        raise TokenExchangeError("LinkedIn recusou a requisicao (HTTP 401): credenciais invalidas.")
    if response.status_code == 403:
        raise TokenExchangeError("LinkedIn recusou a requisicao (HTTP 403): acesso negado.")
    if response.status_code != 200:
        raise TokenExchangeError(f"LinkedIn retornou status HTTP inesperado: {response.status_code}.")

    try:
        payload = json_module.loads(response.text)
    except json_module.JSONDecodeError:
        raise TokenExchangeError("Resposta do LinkedIn nao e um JSON valido.") from None

    if not isinstance(payload, dict):
        raise TokenExchangeError("Resposta do LinkedIn nao e um objeto JSON valido.")

    if "error" in payload:
        raise TokenExchangeError("LinkedIn retornou um erro OAuth na troca de token.")

    access_token = payload.get("access_token")
    if not access_token or not isinstance(access_token, str):
        raise TokenExchangeError("Resposta do LinkedIn nao contem access_token valido.")

    expires_in = payload.get("expires_in")
    if expires_in is None:
        raise TokenExchangeError("Resposta do LinkedIn nao contem expires_in.")
    if isinstance(expires_in, bool) or not isinstance(expires_in, (int, float)) or expires_in <= 0:
        raise TokenExchangeError("Resposta do LinkedIn contem expires_in invalido.")

    expires_at = clock() + expires_in
    return TokenExchangeResult(access_token=access_token, expires_at=expires_at)


class TokenExchangeCallable(Protocol):
    """Interface minima de um exchange ja pronto para ser chamado com so o code."""

    def __call__(self, authorization_code: str) -> TokenExchangeResult: ...


def exchange_and_store_token(
    authorization_code: str,
    token_exchanger: TokenExchangeCallable | Callable[[str], TokenExchangeResult],
    token_store: TokenStore,
) -> TokenExchangeResult:
    """
    Executa a troca (via `token_exchanger` injetado) e, somente se ela
    for bem-sucedida e o resultado for valido, grava no TokenStore.

    Se `token_exchanger` levantar uma excecao (troca falhou), essa
    excecao se propaga e NADA e gravado no TokenStore. Se
    `token_store.save_access_token` levantar uma excecao (falha do
    backend de credencial), ela tambem se propaga; nem esta funcao
    nem os modulos que ela chama incluem access_token ou Client
    Secret em nenhuma mensagem de erro.
    """
    result = token_exchanger(authorization_code)

    if not result.access_token or not isinstance(result.access_token, str):
        raise ValueError("Resultado da troca sem access_token valido; nada foi gravado.")

    if (
        not isinstance(result.expires_at, (int, float))
        or isinstance(result.expires_at, bool)
        or result.expires_at <= 0
    ):
        raise ValueError("Resultado da troca com expires_at invalido; nada foi gravado.")

    token_store.save_access_token(result.access_token, result.expires_at)
    return result
