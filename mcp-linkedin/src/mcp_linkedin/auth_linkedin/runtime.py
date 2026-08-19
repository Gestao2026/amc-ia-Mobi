"""
Composicao do fluxo OAuth da Camada 2 (mcp-linkedin -> LinkedIn),
Etapa 7B.

Este modulo nao contem regra nova de OAuth: ele apenas liga, numa
unica peca com estado compartilhado, o que ja existia solto desde as
Etapas 3 e 4:

    build_authorization_request  (oauth_flow)
        -> LinkedIn autoriza e chama o callback
        -> process_callback      (oauth_callback, valida o state)
        -> exchange_code_for_token (token_exchange, via HttpTransport)
        -> exchange_and_store_token -> TokenStore

O estado compartilhado e o motivo de este modulo existir: o `state`
gerado ao iniciar a autorizacao precisa ser validado depois, no
callback, pelo MESMO StateStore. Sem um objeto de vida longa
segurando esse StateStore, todo callback seria rejeitado como state
invalido.

Nenhuma funcao aqui imprime, loga ou devolve access token, client
secret, authorization code ou state. `start_authorization` devolve a
URL de autorizacao (que contem o state, por definicao do protocolo),
mas nunca o state isolado, e nunca o client secret, que sequer entra
na URL.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable

from mcp_linkedin.auth_linkedin.oauth_callback import CallbackParams, CallbackResult, process_callback
from mcp_linkedin.auth_linkedin.oauth_flow import (
    AuthorizationRequest,
    LinkedInOAuthConfig,
    build_authorization_request,
)
from mcp_linkedin.auth_linkedin.state_store import StateStore
from mcp_linkedin.auth_linkedin.token_exchange import (
    HttpTransport,
    TokenExchangeConfig,
    TokenExchangeResult,
    exchange_and_store_token,
    exchange_code_for_token,
)
from mcp_linkedin.auth_linkedin.token_store import (
    EncryptedCredentialBackend,
    InMemoryCredentialBackend,
    TokenStore,
    Win32CredentialBackend,
)
from mcp_linkedin.config import (
    TOKEN_STORE_BACKEND_PONTE,
    TOKEN_STORE_BACKEND_SUPABASE,
    TOKEN_STORE_BACKEND_WINDOWS,
    LinkedInConfig,
)


@dataclass(frozen=True)
class LinkedInOAuthRuntime:
    """
    Fluxo OAuth do LinkedIn pronto para uso, com StateStore e
    TokenStore de vida longa compartilhados entre o inicio da
    autorizacao e o callback.
    """

    config: LinkedInConfig
    state_store: StateStore
    token_store: TokenStore
    transport: HttpTransport
    clock: Callable[[], float] = time.time

    def start_authorization(self) -> AuthorizationRequest:
        """
        Gera um state novo e monta a URL de autorizacao do LinkedIn.
        Nao acessa rede: so devolve a URL que o captador precisa abrir.
        """
        oauth_config = LinkedInOAuthConfig(
            client_id=self.config.client_id,
            redirect_uri=self.config.redirect_uri,
            scopes=list(self.config.scopes),
        )
        return build_authorization_request(oauth_config, self.state_store)

    def handle_callback(self, params: CallbackParams) -> CallbackResult:
        """
        Processa o callback do LinkedIn: valida o state (uso unico) e,
        so entao, troca o authorization code por access token e grava
        no TokenStore.

        Excecoes de troca (TokenExchangeError, TransportError) e de
        gravacao sobem para quem chamou: o tratamento HTTP pertence a
        rota, nao a esta camada.
        """
        return process_callback(params, self.state_store, self._exchange_and_store)

    def has_valid_token(self) -> bool:
        """True se ha um access token gravado e ainda dentro da validade. Nunca devolve o token."""
        return self.token_store.has_valid_token()

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


def build_credential_backend(config: LinkedInConfig):
    """
    Escolhe o backend de credencial conforme a configuracao ja
    resolvida. Nao acessa rede nem o Credential Manager: so instancia
    (as duas coisas so acontecem na primeira leitura ou gravacao).

    No backend de producao (supabase), o armazenamento remoto vem
    sempre envelopado pela cifragem: o token e cifrado no processo
    antes de sair para o banco. A validade da chave ja foi conferida
    em `resolve_linkedin_config`, na inicializacao.
    """
    if config.token_store_backend == TOKEN_STORE_BACKEND_WINDOWS:
        return Win32CredentialBackend()

    if config.token_store_backend == TOKEN_STORE_BACKEND_PONTE:
        # Imports locais: so quem roda com este backend precisa deles.
        from mcp_linkedin.auth_linkedin.crypto import TokenCipher
        from mcp_linkedin.auth_linkedin.ponte_backend import PonteCredentialBackend

        ponte = PonteCredentialBackend(url=config.ponte_url, secret=config.ponte_secret)
        return EncryptedCredentialBackend(
            inner=ponte,
            cipher=TokenCipher.from_base64_key(config.token_encryption_key),
        )

    if config.token_store_backend == TOKEN_STORE_BACKEND_SUPABASE:
        # Imports locais: so quem roda com o backend de producao
        # precisa destes modulos.
        from mcp_linkedin.auth_linkedin.crypto import TokenCipher
        from mcp_linkedin.auth_linkedin.supabase_backend import (
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


def build_runtime(config: LinkedInConfig) -> LinkedInOAuthRuntime:
    """
    Monta o runtime completo a partir da configuracao resolvida. Nao
    acessa rede nem o Credential Manager: so instancia as pecas (o
    HttpxTransport so abre conexao quando `post` e de fato chamado).
    """
    # Import local: httpx2 so e necessario quando a Camada 2 esta de
    # fato configurada, entao o servidor continua importavel mesmo num
    # ambiente sem ele.
    from mcp_linkedin.auth_linkedin.http_transport import HttpxTransport

    return LinkedInOAuthRuntime(
        config=config,
        state_store=StateStore(),
        token_store=TokenStore(backend=build_credential_backend(config)),
        transport=HttpxTransport(),
    )
