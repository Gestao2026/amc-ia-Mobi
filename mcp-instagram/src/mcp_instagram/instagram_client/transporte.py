"""
Transporte HTTP para a API de leitura do Instagram (Graph API).

Este módulo é o único do pacote `instagram_client` que abre conexão de
rede. Ele é separado do transporte da Camada 2
(`auth_instagram/http_transport.py`) de propósito: aquele existe só para
a troca de authorization code por access token, é coberto por testes
próprios e não deve ganhar responsabilidade nova. Aqui trafega outra
coisa (leitura de conteúdo e métrica), com outra regra de autenticação.

Segurança:
- o access token viaja no cabeçalho `Authorization: Bearer`, nunca na
  query string. A Graph API aceita as duas formas; o cabeçalho é
  escolhido porque query string vaza com facilidade para log de
  servidor, histórico e mensagem de erro;
- nenhuma função aqui imprime, registra em log ou inclui token,
  cabeçalho ou corpo em mensagem de erro;
- as exceções do httpx2 viram `ErroDeTransporte` com `from None`, para o
  traceback encadeado não carregar o objeto `Request` do httpx2, que
  referencia os cabeçalhos (onde está o token);
- redirecionamento automático fica desligado, para o token nunca ser
  reenviado a um host diferente do endpoint oficial da Meta.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

TEMPO_LIMITE_PADRAO_SEGUNDOS = 15.0


@dataclass(frozen=True)
class RespostaGraph:
    """Resposta crua da Graph API. Quem interpreta o corpo é o cliente de leitura."""

    status_code: int
    text: str


class ErroDeTransporte(Exception):
    """Falha de rede ao falar com a Graph API. Nunca contém token."""


class TransporteGraph(Protocol):
    """Contrato mínimo de transporte. Existe para o cliente ser testável sem rede."""

    def get(self, url: str, params: dict, token: str) -> RespostaGraph: ...


class TransporteGraphHttpx:
    """Transporte real, cumprindo o Protocol `TransporteGraph`."""

    def __init__(
        self,
        tempo_limite_segundos: float = TEMPO_LIMITE_PADRAO_SEGUNDOS,
        httpx_transport=None,
    ) -> None:
        """
        `httpx_transport` é o transporte interno do próprio httpx2. Em
        produção fica None (o httpx2 usa a rede real); nos testes recebe
        um `httpx2.MockTransport`, para estes mesmos métodos serem
        exercitados de ponta a ponta sem nenhum pacote sair da máquina.
        """
        self._tempo_limite_segundos = tempo_limite_segundos
        self._httpx_transport = httpx_transport

    def get(self, url: str, params: dict, token: str) -> RespostaGraph:
        """
        Executa o GET e devolve a resposta crua. Não interpreta o corpo:
        quem valida status e JSON é o cliente de leitura.
        """
        # Import local, no mesmo padrão do transporte da Camada 2: o
        # módulo continua importável em ambiente sem httpx2.
        import httpx2

        try:
            with httpx2.Client(
                timeout=self._tempo_limite_segundos,
                follow_redirects=False,
                transport=self._httpx_transport,
            ) as client:
                resposta = client.get(
                    url,
                    params=params,
                    headers={"Authorization": f"Bearer {token}"},
                )
        except httpx2.TimeoutException:
            raise ErroDeTransporte("Timeout na comunicação com a Meta.") from None
        except httpx2.HTTPError:
            raise ErroDeTransporte("Falha de rede na comunicação com a Meta.") from None

        return RespostaGraph(status_code=resposta.status_code, text=resposta.text)

    def __repr__(self) -> str:
        return f"TransporteGraphHttpx(tempo_limite_segundos={self._tempo_limite_segundos!r})"
