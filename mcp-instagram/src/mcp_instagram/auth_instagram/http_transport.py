"""
Implementação real do HttpTransport (Camada 2, mcp-instagram para
Instagram).

Este é o único módulo do componente que de fato abre uma conexão de
rede para a Meta, e só na troca de authorization code por access token.
Nenhuma chamada à API de conteúdo do Instagram existe aqui.

Biblioteca: `httpx2`, a linha 2.x do httpx, já presente no ambiente como
dependência do próprio SDK `mcp`.

Segurança:
- na etapa 1 (POST), client_secret e authorization code viajam somente
  no corpo, porque quem monta a requisição é
  `build_short_lived_token_request` (token_exchange.py) e este módulo
  apenas a executa;
- na etapa 2 (GET), a Meta exige client_secret e token na query string.
  Este módulo passa esses valores pelo parâmetro `params` do httpx2, e
  nunca os concatena manualmente numa string de URL que pudesse acabar
  em log ou mensagem de erro;
- as exceções do httpx2 são convertidas em `TransportError` com
  `from None`, para que o traceback encadeado não carregue o objeto
  `Request` do httpx2 (que referencia corpo e query, onde estão as
  credenciais);
- nenhuma função aqui imprime, registra em log ou inclui corpo de
  requisição, query, credencial ou token em mensagem de erro;
- redirecionamento automático fica desligado, para as credenciais nunca
  serem reenviadas a um host diferente do endpoint oficial da Meta.
"""

from __future__ import annotations

import httpx2

from mcp_instagram.auth_instagram.token_exchange import HttpResponse, TransportError

DEFAULT_TIMEOUT_SECONDS = 10.0


class HttpxTransport:
    """Transporte HTTP real, cumprindo o Protocol `HttpTransport`."""

    def __init__(
        self,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        httpx_transport: "httpx2.BaseTransport | None" = None,
    ) -> None:
        """
        `httpx_transport` é o transporte interno do próprio httpx2. Em
        produção fica None (o httpx2 usa o transporte real de rede); nos
        testes recebe um `httpx2.MockTransport`, para que estes mesmos
        métodos sejam exercitados de ponta a ponta sem nenhum pacote sair
        da máquina.
        """
        self._timeout_seconds = timeout_seconds
        self._httpx_transport = httpx_transport

    def post(self, url: str, data: dict) -> HttpResponse:
        """
        Executa o POST da etapa 1 e devolve a resposta crua. Não
        interpreta o corpo: quem valida status, JSON e access_token é
        `exchange_code_for_token` (token_exchange.py).
        """
        return self._executar("POST", url, data=data)

    def get(self, url: str, params: dict) -> HttpResponse:
        """Executa o GET da etapa 2 e devolve a resposta crua."""
        return self._executar("GET", url, params=params)

    def _executar(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        params: dict | None = None,
    ) -> HttpResponse:
        try:
            with httpx2.Client(
                timeout=self._timeout_seconds,
                follow_redirects=False,
                transport=self._httpx_transport,
            ) as client:
                resposta = client.request(method, url, data=data, params=params)
        except httpx2.TimeoutException:
            raise TransportError("Timeout na comunicação com a Meta.") from None
        except httpx2.HTTPError:
            raise TransportError("Falha de rede na comunicação com a Meta.") from None

        return HttpResponse(status_code=resposta.status_code, text=resposta.text)

    def __repr__(self) -> str:
        return f"HttpxTransport(timeout_seconds={self._timeout_seconds!r})"
