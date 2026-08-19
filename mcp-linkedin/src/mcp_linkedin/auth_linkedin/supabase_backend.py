"""
Backend de producao do TokenStore: uma tabela dedicada no Supabase,
acessada pela API REST (PostgREST).

Por que Supabase: ja e o banco do CaptaHub, entao nao entra fornecedor
novo nem custo novo, e o padrao de falar com ele por HTTP puro (sem
SDK) ja e o do repositorio (`scripts/captahub-api.py`). Aqui usamos o
`httpx2`, que ja e dependencia declarada deste componente.

Este backend guarda o que receber, exatamente como receber. Ele NAO
cifra nada: a cifragem e responsabilidade do
`EncryptedCredentialBackend` (token_store.py), que envelopa este.
Assim cada peca tem uma responsabilidade so, e a cifragem pode ser
testada sem rede.

Isolamento (regra do CLAUDE.md): este componente tem credenciais
proprias, MCP_LINKEDIN_SUPABASE_URL e MCP_LINKEDIN_SUPABASE_KEY, e
nunca reaproveita o SUPABASE_KEY do .env da raiz do AMC-IA-Mobi.

Seguranca:
- a chave de API viaja somente em cabecalho, nunca na URL;
- `__repr__` mascara a chave;
- as excecoes do httpx2 viram TokenStoreBackendError com `from None`,
  para o traceback encadeado nao carregar o objeto Request (que
  referencia cabecalhos e corpo);
- nenhuma funcao aqui imprime, loga ou inclui chave de API, texto
  cifrado ou access token em mensagem de erro.
"""

from __future__ import annotations

import json
from urllib.parse import quote

import httpx2

DEFAULT_TABLE = "mcp_linkedin_tokens"
DEFAULT_TIMEOUT_SECONDS = 10.0

# Coluna que identifica a credencial (o TARGET_NAME do TokenStore) e
# coluna que guarda o segredo ja cifrado.
COLUNA_ALVO = "target_name"
COLUNA_SEGREDO = "secret"


# Reexportado de token_store para nao duplicar a classe: mais de um
# backend remoto a levanta, e a rota de callback precisa de um unico
# tipo para capturar. Importar daqui continua funcionando.
from mcp_linkedin.auth_linkedin.token_store import TokenStoreBackendError  # noqa: E402


class SupabaseCredentialBackend:
    """Cumpre o Protocol `CredentialBackend` sobre uma tabela do Supabase."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        table: str = DEFAULT_TABLE,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        httpx_transport: "httpx2.BaseTransport | None" = None,
    ) -> None:
        """
        `httpx_transport` e o transporte interno do proprio httpx2. Em
        producao fica None (rede real); nos testes recebe um
        `httpx2.MockTransport`, para exercitar este mesmo codigo sem
        nenhum pacote sair da maquina.
        """
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._table = table
        self._timeout_seconds = timeout_seconds
        self._httpx_transport = httpx_transport

    def write(self, target_name: str, secret: str) -> None:
        """
        Grava (ou substitui) a credencial. Usa upsert do PostgREST, o
        que exige uma restricao UNIQUE na coluna target_name (ver o
        DDL no README).
        """
        self._request(
            "POST",
            f"/rest/v1/{self._table}",
            json_body=[{COLUNA_ALVO: target_name, COLUNA_SEGREDO: secret}],
            extra_headers={"Prefer": "resolution=merge-duplicates"},
        )

    def read(self, target_name: str) -> str | None:
        """Devolve o segredo gravado, ou None se nao existir nenhum para este alvo."""
        resposta = self._request(
            "GET",
            f"/rest/v1/{self._table}?{COLUNA_ALVO}=eq.{quote(target_name, safe='')}"
            f"&select={COLUNA_SEGREDO}",
        )

        try:
            linhas = json.loads(resposta)
        except json.JSONDecodeError:
            raise TokenStoreBackendError("Resposta do armazenamento remoto nao e JSON valido.") from None

        if not isinstance(linhas, list) or not linhas:
            return None

        valor = linhas[0].get(COLUNA_SEGREDO)
        return valor if isinstance(valor, str) else None

    def delete(self, target_name: str) -> None:
        """Remove a credencial, se houver. Apagar o que nao existe nao e erro."""
        self._request(
            "DELETE",
            f"/rest/v1/{self._table}?{COLUNA_ALVO}=eq.{quote(target_name, safe='')}",
        )

    def _request(
        self,
        method: str,
        path: str,
        json_body: object | None = None,
        extra_headers: dict | None = None,
    ) -> str:
        headers = {
            # A chave so em cabecalho. Nunca na URL, que costuma ser
            # registrada em log de proxy e de servidor.
            "apikey": self._api_key,
            "Authorization": f"Bearer {self._api_key}",
            "Accept": "application/json",
        }
        if json_body is not None:
            headers["Content-Type"] = "application/json"
        if extra_headers:
            headers.update(extra_headers)

        try:
            with httpx2.Client(
                timeout=self._timeout_seconds,
                follow_redirects=False,
                transport=self._httpx_transport,
            ) as client:
                resposta = client.request(
                    method,
                    f"{self._base_url}{path}",
                    headers=headers,
                    json=json_body,
                )
        except httpx2.TimeoutException:
            raise TokenStoreBackendError("Timeout ao falar com o armazenamento remoto.") from None
        except httpx2.HTTPError:
            raise TokenStoreBackendError("Falha de rede ao falar com o armazenamento remoto.") from None

        if not 200 <= resposta.status_code < 300:
            # Qualquer coisa fora de 2xx e erro, inclusive 3xx: com
            # follow_redirects desligado, um redirecionamento significa
            # que a requisicao NAO foi atendida pelo Supabase, e seguir
            # adiante interpretaria o corpo de um redirecionamento como
            # se fosse dado.
            #
            # O corpo da resposta fica de fora da mensagem de proposito:
            # o PostgREST pode ecoar nele o dado enviado.
            raise TokenStoreBackendError(
                f"Armazenamento remoto recusou a operacao (HTTP {resposta.status_code})."
            )

        return resposta.text

    def __repr__(self) -> str:
        # Nunca expor a chave de API.
        return (
            f"SupabaseCredentialBackend(base_url={self._base_url!r}, "
            f"table={self._table!r}, api_key='***')"
        )
