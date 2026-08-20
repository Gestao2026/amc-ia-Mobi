"""
Processamento logico do callback OAuth do Instagram (Camada 2,
mcp-instagram -> Instagram).

Este modulo NAO abre porta, NAO inicia servidor HTTP e NAO se acopla
a nenhum framework web (Flask, FastAPI, Starlette). Ele recebe os
parametros de um callback ja extraidos por quem quer que fale HTTP de
verdade (uma etapa futura, fora deste modulo), e decide o que fazer:
validar o state, checar erro OAuth do provedor, e encaminhar o
authorization code para a troca por token, atraves de um
`TokenExchanger` injetavel.

Nao executa OAuth real, nao acessa o Instagram, nao usa Client ID ou
Client Secret (isso pertence a token_exchange.py, chamado somente
atraves do TokenExchanger injetado, nunca importado diretamente
aqui).

Seguranca:
- o state e validado ANTES de qualquer coisa acontecer com o code;
- o state e sempre consumido (uso unico) assim que validado, mesmo
  que o code venha ausente ou o token_exchanger falhe depois, para
  impedir replay do mesmo callback;
- nenhuma funcao aqui imprime, loga ou inclui authorization code,
  state ou access token em mensagem de erro; `CallbackParams.__repr__`
  mascara `code` e `state` mesmo se o objeto for impresso por
  acidente (ex. em um traceback).
- se `token_exchanger` levantar uma excecao, ela se propaga sem ser
  capturada aqui: o tratamento de erro da troca em si pertence ao
  modulo token_exchange, nao a este.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from mcp_instagram.auth_instagram.state_store import StateStore


class CallbackOutcome(str, Enum):
    """Proximo passo indicado pelo processamento do callback."""

    TOKEN_EXCHANGE_STARTED = "token_exchange_started"
    REJECTED_STATE_MISSING = "rejected_state_missing"
    REJECTED_STATE_INVALID = "rejected_state_invalid"
    REJECTED_CODE_MISSING = "rejected_code_missing"
    REJECTED_OAUTH_ERROR = "rejected_oauth_error"


@dataclass(frozen=True)
class CallbackParams:
    """
    Parametros de um callback OAuth, ja extraidos de uma requisicao
    HTTP por outra camada. Este modulo nao sabe nem precisa saber de
    onde vieram.
    """

    code: str | None = None
    state: str | None = None
    error: str | None = None
    error_description: str | None = None

    def __repr__(self) -> str:
        # Nunca expor code/state, mesmo que este objeto va parar num
        # log ou traceback por acidente.
        return (
            "CallbackParams("
            f"code={'***' if self.code else None!r}, "
            f"state={'***' if self.state else None!r}, "
            f"error={self.error!r}, "
            f"error_description={self.error_description!r})"
        )


class TokenExchanger(Protocol):
    """Interface minima para encaminhar o authorization code, injetavel para teste."""

    def __call__(self, authorization_code: str) -> object: ...


@dataclass(frozen=True)
class CallbackResult:
    """Estrutura segura devolvida ao final do processamento do callback."""

    outcome: CallbackOutcome
    detail: str
    oauth_error: str | None = None
    oauth_error_description: str | None = None
    token_exchange_result: object | None = None


def process_callback(
    params: CallbackParams,
    state_store: StateStore,
    token_exchanger: TokenExchanger,
) -> CallbackResult:
    """
    Processa um callback OAuth ja extraido, na ordem:

    1. state precisa existir;
    2. state precisa ser valido (StateStore.validate_and_consume, uso unico);
    3. so depois disso, verifica se o Instagram retornou erro OAuth;
    4. so depois disso, verifica se o authorization code veio;
    5. so entao encaminha o code para o token_exchanger injetado.
    """
    if not params.state:
        return CallbackResult(
            outcome=CallbackOutcome.REJECTED_STATE_MISSING,
            detail="Callback sem state. Requisicao rejeitada.",
        )

    state_valido = state_store.validate_and_consume(params.state)
    if not state_valido:
        return CallbackResult(
            outcome=CallbackOutcome.REJECTED_STATE_INVALID,
            detail="State invalido, expirado ou ja utilizado. Requisicao rejeitada.",
        )

    if params.error:
        return CallbackResult(
            outcome=CallbackOutcome.REJECTED_OAUTH_ERROR,
            detail="Instagram retornou um erro OAuth no callback.",
            oauth_error=params.error,
            oauth_error_description=params.error_description,
        )

    if not params.code:
        return CallbackResult(
            outcome=CallbackOutcome.REJECTED_CODE_MISSING,
            detail="Callback sem authorization code. Requisicao rejeitada.",
        )

    resultado_exchange = token_exchanger(params.code)

    return CallbackResult(
        outcome=CallbackOutcome.TOKEN_EXCHANGE_STARTED,
        detail="Authorization code encaminhado para troca por token.",
        token_exchange_result=resultado_exchange,
    )
