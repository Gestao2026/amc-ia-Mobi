"""
Implementacao real do HttpTransport (Camada 2, mcp-linkedin ->
LinkedIn), Etapa 7B.

Ate esta etapa, `HttpTransport` (token_exchange.py) existia so como
Protocol, com implementacoes falsas nos testes. Este e o unico modulo
do componente que de fato abre uma conexao de rede para o LinkedIn, e
so na troca de authorization code por access token.

Biblioteca: `httpx2`, a linha 2.x do httpx, ja presente no ambiente
como dependencia do proprio SDK `mcp` 2.0.0 (nenhuma instalacao nova
foi necessaria nesta etapa).

Seguranca:
- client_secret e authorization code viajam somente no corpo do POST
  (parametro `data`), nunca na URL, porque quem monta a requisicao e
  `build_token_request` (token_exchange.py) e este modulo apenas a
  executa;
- as excecoes do httpx2 sao convertidas em `TransportError` com
  `from None`, para que o traceback encadeado nao carregue o objeto
  `Request` do httpx2 (que referencia o corpo da requisicao, onde
  estao o client_secret e o code);
- nenhuma funcao aqui imprime, loga ou inclui corpo de requisicao,
  credencial ou token em mensagem de erro;
- redirecionamento automatico fica desligado (padrao do httpx2), para
  o corpo com as credenciais nunca ser reenviado a um host diferente
  do endpoint de token oficial.
"""

from __future__ import annotations

import httpx2

from mcp_linkedin.auth_linkedin.token_exchange import HttpResponse, TransportError

DEFAULT_TIMEOUT_SECONDS = 10.0


class HttpxTransport:
    """Transporte HTTP real, cumprindo o Protocol `HttpTransport`."""

    def __init__(
        self,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        httpx_transport: "httpx2.BaseTransport | None" = None,
    ) -> None:
        """
        `httpx_transport` e o transporte interno do proprio httpx2. Em
        producao fica None (o httpx2 usa o transporte real de rede);
        nos testes recebe um `httpx2.MockTransport`, para que este
        mesmo `post` seja exercitado de ponta a ponta sem nenhum pacote
        sair da maquina.
        """
        self._timeout_seconds = timeout_seconds
        self._httpx_transport = httpx_transport

    def post(self, url: str, data: dict) -> HttpResponse:
        """
        Executa o POST e devolve a resposta crua. Nao interpreta o
        corpo: quem valida status, JSON, access_token e expires_in e
        `exchange_code_for_token` (token_exchange.py).
        """
        try:
            with httpx2.Client(
                timeout=self._timeout_seconds,
                follow_redirects=False,
                transport=self._httpx_transport,
            ) as client:
                resposta = client.post(url, data=data)
        except httpx2.TimeoutException:
            raise TransportError("Timeout na comunicacao com o LinkedIn.") from None
        except httpx2.HTTPError:
            raise TransportError("Falha de rede na comunicacao com o LinkedIn.") from None

        return HttpResponse(status_code=resposta.status_code, text=resposta.text)

    def __repr__(self) -> str:
        return f"HttpxTransport(timeout_seconds={self._timeout_seconds!r})"
