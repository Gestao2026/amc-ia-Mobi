"""
Transporte HTTP para a API do LinkedIn.

Diferente do transporte equivalente do mcp-instagram, este precisa
saber ESCREVER: publicar no perfil e um POST, nao um GET. Por isso ele
expoe `post`, e nao so `get`.

Isso remove a trava estrutural que o Instagram tem, onde escrever e
impossivel porque o transporte nao sabe. Aqui a trava passa a ser
outra, e vive uma camada acima: nenhuma ferramenta publica sem texto
explicito vindo de quem chamou, e o servidor nunca inventa conteudo.

Seguranca:
- o access token viaja no cabecalho `Authorization: Bearer`, nunca na
  query string, que vaza com facilidade para log e historico;
- nenhuma funcao aqui imprime, registra em log ou inclui token,
  cabecalho ou corpo em mensagem de erro;
- as excecoes do httpx2 viram `ErroDeTransporte` com `from None`, para
  o traceback encadeado nao carregar o objeto `Request` do httpx2, que
  referencia os cabecalhos (onde esta o token);
- redirecionamento automatico fica desligado, para o token nunca ser
  reenviado a um host diferente do endpoint oficial do LinkedIn.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

TEMPO_LIMITE_PADRAO_SEGUNDOS = 20.0

# O LinkedIn versiona a API por cabecalho, nao por caminho. Sem este
# cabecalho a API `/rest/` recusa a chamada. O valor e uma data
# AAAAMM, e o LinkedIn mantem cada versao por cerca de um ano.
VERSAO_API_PADRAO = "202508"


@dataclass(frozen=True)
class RespostaLinkedIn:
    """Resposta crua da API. Quem interpreta o corpo e o cliente."""

    status_code: int
    text: str
    # O id da publicacao criada volta neste cabecalho, nao no corpo.
    id_criado: str | None = None


class ErroDeTransporte(Exception):
    """Falha de rede ao falar com o LinkedIn. Nunca contem token."""


class TransporteLinkedIn(Protocol):
    """Contrato minimo de transporte. Existe para o cliente ser testavel sem rede."""

    def get(self, url: str, params: dict, token: str) -> RespostaLinkedIn: ...

    def post(self, url: str, corpo: dict, token: str) -> RespostaLinkedIn: ...


class TransporteLinkedInHttpx:
    """Transporte real, cumprindo o Protocol `TransporteLinkedIn`."""

    def __init__(
        self,
        tempo_limite_segundos: float = TEMPO_LIMITE_PADRAO_SEGUNDOS,
        versao_api: str = VERSAO_API_PADRAO,
        httpx_transport=None,
    ) -> None:
        """
        `httpx_transport` e o transporte interno do proprio httpx2. Em
        producao fica None (o httpx2 usa a rede real); nos testes recebe
        um `httpx2.MockTransport`, para estes mesmos metodos serem
        exercitados de ponta a ponta sem nenhum pacote sair da maquina.
        """
        self._tempo_limite_segundos = tempo_limite_segundos
        self._versao_api = versao_api
        self._httpx_transport = httpx_transport

    def get(self, url: str, params: dict, token: str) -> RespostaLinkedIn:
        """Executa o GET e devolve a resposta crua, sem interpretar o corpo."""
        return self._executar("GET", url, token, params=params)

    def post(self, url: str, corpo: dict, token: str) -> RespostaLinkedIn:
        """Executa o POST e devolve a resposta crua, sem interpretar o corpo."""
        return self._executar("POST", url, token, json=corpo)

    def _executar(self, metodo: str, url: str, token: str, params=None, json=None):
        # Import local, no mesmo padrao do transporte da Camada 2: o
        # modulo continua importavel em ambiente sem httpx2.
        import httpx2

        cabecalhos = {
            "Authorization": f"Bearer {token}",
            "X-Restli-Protocol-Version": "2.0.0",
            "LinkedIn-Version": self._versao_api,
        }

        try:
            with httpx2.Client(
                timeout=self._tempo_limite_segundos,
                follow_redirects=False,
                transport=self._httpx_transport,
            ) as client:
                resposta = client.request(
                    metodo, url, params=params, json=json, headers=cabecalhos
                )
        except httpx2.TimeoutException:
            raise ErroDeTransporte("Timeout na comunicacao com o LinkedIn.") from None
        except httpx2.HTTPError:
            raise ErroDeTransporte("Falha de rede na comunicacao com o LinkedIn.") from None

        return RespostaLinkedIn(
            status_code=resposta.status_code,
            text=resposta.text,
            id_criado=resposta.headers.get("x-restli-id"),
        )

    def __repr__(self) -> str:
        return (
            f"TransporteLinkedInHttpx(tempo_limite_segundos={self._tempo_limite_segundos!r}, "
            f"versao_api={self._versao_api!r})"
        )
