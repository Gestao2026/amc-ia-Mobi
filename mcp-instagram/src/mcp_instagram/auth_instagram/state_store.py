"""
Armazenamento efemero e validacao do `state` anti-CSRF do fluxo OAuth
Instagram (Camada 2, mcp-instagram -> Instagram).

Escopo desta peca: somente o `state`. Nenhuma URL de autorizacao,
nenhum authorization code, nenhum token e nenhuma chamada de rede
pertencem a este modulo.

Os states ficam apenas em memoria do processo, nunca em disco. Cada
state gerado e de uso unico: a primeira chamada a
`validate_and_consume` para um determinado valor o remove do
armazenamento, seja o resultado valido ou invalido, o que impede
reaproveitamento (replay) mesmo de um state ja expirado.

O valor do state nunca deve ser registrado em log por quem usar este
modulo; nenhuma chamada de log existe aqui.
"""

from __future__ import annotations

import secrets
import time
from dataclasses import dataclass, field
from typing import Callable

DEFAULT_TTL_SECONDS = 600  # 10 minutos


@dataclass
class StateStore:
    """Gera, guarda e valida states de uso unico, somente em memoria."""

    ttl_seconds: float = DEFAULT_TTL_SECONDS
    clock: Callable[[], float] = time.monotonic
    _created_at: dict = field(default_factory=dict, init=False, repr=False)

    def generate(self) -> str:
        """Gera um state novo, criptograficamente seguro, e o registra."""
        state = secrets.token_urlsafe(32)
        self._created_at[state] = self.clock()
        return state

    def validate_and_consume(self, state: str) -> bool:
        """
        Valida um state e o remove do armazenamento (uso unico),
        independentemente do resultado. Retorna True somente se o
        state existia e ainda estava dentro da janela de expiracao.
        """
        created_at = self._created_at.pop(state, None)
        if created_at is None:
            return False
        return (self.clock() - created_at) <= self.ttl_seconds

    def __len__(self) -> int:
        return len(self._created_at)
