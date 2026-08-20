"""
Composição do fluxo OAuth da Camada 2 (mcp-instagram para Instagram).

Este módulo não contém regra nova de OAuth: ele apenas liga, numa única
peça com estado compartilhado, o que existe solto nos demais módulos:

    build_authorization_request  (oauth_flow)
        -> o captador autoriza no Instagram e a Meta chama o callback
        -> process_callback      (oauth_callback, valida o state)
        -> exchange_code_for_token (token_exchange, duas etapas)
        -> exchange_and_store_token -> TokenStore

O estado compartilhado é o motivo de este módulo existir: o `state`
gerado ao iniciar a autorização precisa ser validado depois, no
callback, pelo MESMO StateStore. Sem um objeto de vida longa segurando
esse StateStore, todo callback seria rejeitado como state inválido.

Nenhuma função aqui imprime, registra em log ou devolve access token,
client secret, authorization code ou state. `start_authorization`
devolve a URL de autorização (que contém o state, por definição do
protocolo), mas nunca o state isolado, e nunca o client secret, que
sequer entra na URL.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable

from mcp_instagram.auth_instagram.oauth_callback import (
    CallbackParams,
    CallbackResult,
    process_callback,
)
from mcp_instagram.auth_instagram.oauth_flow import (
    AuthorizationRequest,
    InstagramOAuthConfig,
    build_authorization_request,
)
from mcp_instagram.auth_instagram.state_store import StateStore
from mcp_instagram.auth_instagram.token_exchange import (
    HttpTransport,
    TokenExchangeConfig,
    TokenExchangeResult,
    exchange_and_store_token,
    exchange_code_for_token,
)
from mcp_instagram.auth_instagram.token_store import (
    EncryptedCredentialBackend,
    InMemoryCredentialBackend,
    TokenStore,
    Win32CredentialBackend,
)
from mcp_instagram.config import (
    TOKEN_STORE_BACKEND_PONTE,
    TOKEN_STORE_BACKEND_SUPABASE,
    TOKEN_STORE_BACKEND_WINDOWS,
    InstagramConfig,
)


@dataclass(frozen=True)
class InstagramOAuthRuntime:
    """
    Fluxo OAuth do Instagram pronto para uso, com StateStore e TokenStore
    de vida longa compartilhados entre o início da autorização e o
    callback.
    """

    config: InstagramConfig
    state_store: StateStore
    token_store: TokenStore
    transport: HttpTransport
    clock: Callable[[], float] = time.time

    def start_authorization(self) -> AuthorizationRequest:
        """
        Gera um state novo e monta a URL de autorização do Instagram.
        Não acessa rede: só devolve a URL que o captador precisa abrir.
        """
        oauth_config = InstagramOAuthConfig(
            client_id=self.config.client_id,
            redirect_uri=self.config.redirect_uri,
            scopes=list(self.config.scopes),
        )
        return build_authorization_request(oauth_config, self.state_store)

    def handle_callback(self, params: CallbackParams) -> CallbackResult:
        """
        Processa o callback da Meta: valida o state (uso único) e, só
        então, troca o authorization code por access token e grava no
        TokenStore.

        Exceções de troca (TokenExchangeError, TransportError) e de
        gravação sobem para quem chamou: o tratamento HTTP pertence à
        rota, não a esta camada.
        """
        return process_callback(params, self.state_store, self._exchange_and_store)

    def has_valid_token(self) -> bool:
        """True se há um access token gravado e dentro da validade. Nunca devolve o token."""
        return self.token_store.has_valid_token()

    def connected_user_id(self) -> str | None:
        """
        Id da conta do Instagram que autorizou, ou None se não houver
        autorização gravada. Não é segredo e não dá acesso a nada
        sozinho: serve para o captador confirmar QUAL conta ficou
        conectada.
        """
        metadata = self.token_store.get_token_metadata()
        return metadata.user_id if metadata is not None else None

    def token_expires_at(self) -> float | None:
        """Momento (epoch seconds) em que a autorização expira, ou None."""
        metadata = self.token_store.get_token_metadata()
        return metadata.expires_at if metadata is not None else None

    def _exchange_and_store(self, authorization_code: str) -> TokenExchangeResult:
        exchange_config = TokenExchangeConfig(
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            redirect_uri=self.config.redirect_uri,
        )
        return exchange_and_store_token(
            authorization_code,
            lambda code: exchange_code_for_token(exchange_config, code, self.transport, self.clock),
            self.token_store,
        )


def build_credential_backend(config: InstagramConfig):
    """
    Escolhe o backend de credencial conforme a configuração já resolvida.
    Não acessa rede nem o Credential Manager: só instancia (as duas
    coisas só acontecem na primeira leitura ou gravação).

    Nos backends remotos, o armazenamento vem sempre envelopado pela
    cifragem: o token é cifrado no processo antes de sair para o banco,
    o que devolve remotamente a propriedade que o DPAPI dá localmente. A
    validade da chave já foi conferida em `resolve_instagram_config`, na
    inicialização.
    """
    if config.token_store_backend == TOKEN_STORE_BACKEND_WINDOWS:
        return Win32CredentialBackend()

    if config.token_store_backend == TOKEN_STORE_BACKEND_PONTE:
        # Imports locais: só quem roda com este backend precisa deles.
        from mcp_instagram.auth_instagram.crypto import TokenCipher
        from mcp_instagram.auth_instagram.ponte_backend import PonteCredentialBackend

        ponte = PonteCredentialBackend(url=config.ponte_url, secret=config.ponte_secret)
        return EncryptedCredentialBackend(
            inner=ponte,
            cipher=TokenCipher.from_base64_key(config.token_encryption_key),
        )

    if config.token_store_backend == TOKEN_STORE_BACKEND_SUPABASE:
        from mcp_instagram.auth_instagram.crypto import TokenCipher
        from mcp_instagram.auth_instagram.supabase_backend import (
            DEFAULT_TABLE,
            SupabaseCredentialBackend,
        )

        remoto = SupabaseCredentialBackend(
            base_url=config.supabase_url,
            api_key=config.supabase_key,
            table=config.supabase_table or DEFAULT_TABLE,
        )
        return EncryptedCredentialBackend(
            inner=remoto,
            cipher=TokenCipher.from_base64_key(config.token_encryption_key),
        )

    return InMemoryCredentialBackend()


def build_runtime(config: InstagramConfig) -> InstagramOAuthRuntime:
    """
    Monta o runtime completo a partir da configuração resolvida. Não
    acessa rede nem o Credential Manager: só instancia as peças (o
    HttpxTransport só abre conexão quando `post` ou `get` é de fato
    chamado).
    """
    # Import local: httpx2 só é necessário quando a Camada 2 está de fato
    # configurada, então o servidor continua importável mesmo num
    # ambiente sem ele.
    from mcp_instagram.auth_instagram.http_transport import HttpxTransport

    return InstagramOAuthRuntime(
        config=config,
        state_store=StateStore(),
        token_store=TokenStore(backend=build_credential_backend(config)),
        transport=HttpxTransport(),
    )
