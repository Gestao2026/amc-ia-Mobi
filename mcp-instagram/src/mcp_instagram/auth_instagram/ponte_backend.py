"""
Backend de producao do TokenStore atraves da ponte HTTPS na HostGator.

Arquitetura:

    Render (este codigo) --HTTPS autenticado--> ponte.mobilizando.org/token.php
                                                        |
                                                        v
                                            MySQL em localhost (HostGator)

Por que existe: o MySQL da HostGator so aceita conexao externa se uma
faixa de IP for liberada, e os IPs de saida do Render sao faixas CIDR
COMPARTILHADAS com todos os outros clientes da regiao. Liberar essa
faixa exporia o banco a qualquer servico hospedado no Render. Com a
ponte, o MySQL continua escutando so em localhost e nada precisa ser
liberado.

Este backend guarda o que receber, exatamente como receber. Ele NAO
cifra nada: a cifragem e responsabilidade do
`EncryptedCredentialBackend` (token_store.py), que envelopa este. Por
isso o PHP do outro lado so ve texto cifrado, e NUNCA recebe a chave
AES, que existe apenas no ambiente do Render.

Seguranca:
- so aceita URL https:// (validado em config.py, na inicializacao);
- o segredo da ponte viaja somente em cabecalho, nunca na URL nem no
  corpo;
- `__repr__` mascara o segredo;
- qualquer resposta fora de 2xx e erro, inclusive 3xx: com
  follow_redirects desligado, um redirecionamento significa que a
  requisicao nao foi atendida pela ponte, e seguir adiante trataria o
  corpo do redirecionamento como se fosse dado;
- as excecoes do httpx2 viram TokenStoreBackendError com `from None`,
  para o traceback encadeado nao carregar o objeto Request (que
  referencia os cabecalhos, onde esta o segredo);
- nenhuma funcao aqui imprime, loga ou inclui segredo da ponte, texto
  cifrado ou access token em mensagem de erro.
"""

from __future__ import annotations

import json

import httpx2

from mcp_instagram.auth_instagram.token_store import TokenStoreBackendError

DEFAULT_TIMEOUT_SECONDS = 10.0

ACAO_LER = "ler"
ACAO_GRAVAR = "gravar"
ACAO_EXCLUIR = "excluir"

# Cabecalho proprio, e nao `Authorization`: em hospedagem
# compartilhada o `Authorization` costuma ser removido pelo
# CGI/FastCGI antes de chegar ao PHP. O token.php aceita os dois, mas
# este e o que funciona sem depender de configuracao do servidor.
CABECALHO_SEGREDO = "X-MCP-Ponte-Secret"

STATUS_OK = "ok"
STATUS_VAZIO = "vazio"


class PonteCredentialBackend:
    """Cumpre o Protocol `CredentialBackend` sobre a ponte HTTPS."""

    def __init__(
        self,
        url: str,
        secret: str,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        httpx_transport: "httpx2.BaseTransport | None" = None,
    ) -> None:
        """
        `httpx_transport` e o transporte interno do proprio httpx2. Em
        producao fica None (rede real); nos testes recebe um
        `httpx2.MockTransport`, para exercitar este mesmo codigo sem
        nenhum pacote sair da maquina.
        """
        self._url = url
        self._secret = secret
        self._timeout_seconds = timeout_seconds
        self._httpx_transport = httpx_transport

    def write(self, target_name: str, secret: str) -> None:
        """Grava (ou substitui) o segredo ja cifrado."""
        self._post({"acao": ACAO_GRAVAR, "alvo": target_name, "secret": secret})

    def read(self, target_name: str) -> str | None:
        """Devolve o segredo cifrado gravado, ou None se nao existir nenhum."""
        corpo = self._post({"acao": ACAO_LER, "alvo": target_name})

        if corpo.get("status") == STATUS_VAZIO:
            return None

        valor = corpo.get("secret")
        return valor if isinstance(valor, str) and valor else None

    def delete(self, target_name: str) -> None:
        """Remove o segredo, se houver. Apagar o que nao existe nao e erro."""
        self._post({"acao": ACAO_EXCLUIR, "alvo": target_name})

    def _post(self, payload: dict) -> dict:
        headers = {
            # O segredo so em cabecalho. Nunca na URL (que costuma ser
            # registrada em log de proxy e de servidor) nem no corpo.
            CABECALHO_SEGREDO: self._secret,
            "Authorization": f"Bearer {self._secret}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        try:
            with httpx2.Client(
                timeout=self._timeout_seconds,
                follow_redirects=False,
                transport=self._httpx_transport,
            ) as client:
                resposta = client.post(self._url, headers=headers, json=payload)
        except httpx2.TimeoutException:
            raise TokenStoreBackendError("Timeout ao falar com a ponte de armazenamento.") from None
        except httpx2.HTTPError:
            raise TokenStoreBackendError("Falha de rede ao falar com a ponte de armazenamento.") from None

        if not 200 <= resposta.status_code < 300:
            # 3xx incluido: com follow_redirects desligado, um
            # redirecionamento significa que a ponte NAO atendeu a
            # requisicao. O corpo fica fora da mensagem de proposito.
            raise TokenStoreBackendError(
                f"Ponte de armazenamento recusou a operacao (HTTP {resposta.status_code})."
            )

        try:
            corpo = json.loads(resposta.text)
        except json.JSONDecodeError:
            raise TokenStoreBackendError("Resposta da ponte de armazenamento nao e JSON valido.") from None

        if not isinstance(corpo, dict):
            raise TokenStoreBackendError("Resposta da ponte de armazenamento nao e um objeto JSON.")

        status = corpo.get("status")
        if status not in (STATUS_OK, STATUS_VAZIO):
            raise TokenStoreBackendError("Ponte de armazenamento devolveu um status inesperado.")

        return corpo

    def __repr__(self) -> str:
        # Nunca expor o segredo da ponte.
        return f"PonteCredentialBackend(url={self._url!r}, secret='***')"
