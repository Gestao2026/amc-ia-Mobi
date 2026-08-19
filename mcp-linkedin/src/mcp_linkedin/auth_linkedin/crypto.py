"""
Cifragem em envelope do access token do LinkedIn (Camada 2), para
armazenamento remoto.

Por que existe: no Windows local, o access token e protegido pelo
proprio sistema (Credential Manager / DPAPI), e nao precisa de
cifragem propria. Num armazenamento remoto (Supabase), essa protecao
nao existe: o token ficaria legivel para qualquer um com acesso ao
banco ou a um dump dele. Este modulo devolve a mesma propriedade que o
DPAPI dava localmente, cifrando o segredo ANTES de ele sair do
processo.

A chave nunca fica no banco: ela vem do ambiente
(LINKEDIN_TOKEN_ENCRYPTION_KEY, um secret no Render). Banco e chave
ficam em dominios de confianca diferentes, entao um dump vazado do
banco, sozinho, nao entrega o token.

Algoritmo: AES-256-GCM, autenticado (AEAD). Um nonce aleatorio de 12
bytes e gerado a cada cifragem e guardado junto do texto cifrado, no
formato base64(nonce || ciphertext). Nonce novo por operacao e
obrigatorio no GCM: repetir nonce com a mesma chave quebra a
seguranca do modo.

Nenhuma funcao aqui imprime, loga ou inclui chave, texto claro ou
texto cifrado em mensagem de erro.
"""

from __future__ import annotations

import base64
import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# AES-256: 32 bytes de chave. O nonce de 12 bytes e o tamanho
# recomendado para o GCM.
KEY_SIZE_BYTES = 32
NONCE_SIZE_BYTES = 12


class InvalidEncryptionKeyError(ValueError):
    """Chave de cifragem ausente ou malformada. Nunca contem a chave."""


class TokenDecryptionError(Exception):
    """Texto cifrado invalido, corrompido ou cifrado com outra chave. Nunca contem segredo."""


def generate_key_base64() -> str:
    """
    Gera uma chave nova, pronta para virar o valor de
    LINKEDIN_TOKEN_ENCRYPTION_KEY. Usada pelo operador uma unica vez,
    nunca automaticamente pelo servidor.
    """
    return base64.b64encode(AESGCM.generate_key(bit_length=256)).decode()


class TokenCipher:
    """Cifra e decifra um segredo curto com AES-256-GCM."""

    def __init__(self, key: bytes) -> None:
        if len(key) != KEY_SIZE_BYTES:
            raise InvalidEncryptionKeyError(
                f"A chave de cifragem precisa ter {KEY_SIZE_BYTES} bytes (AES-256)."
            )
        self._aesgcm = AESGCM(key)

    @classmethod
    def from_base64_key(cls, encoded_key: str) -> "TokenCipher":
        """Constroi a partir do valor base64 lido do ambiente."""
        try:
            key = base64.b64decode(encoded_key, validate=True)
        except (ValueError, TypeError):
            raise InvalidEncryptionKeyError(
                "A chave de cifragem nao esta em base64 valido."
            ) from None
        return cls(key)

    def encrypt(self, plaintext: str) -> str:
        """Devolve base64(nonce || ciphertext). Nonce novo a cada chamada."""
        nonce = os.urandom(NONCE_SIZE_BYTES)
        ciphertext = self._aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
        return base64.b64encode(nonce + ciphertext).decode()

    def decrypt(self, encoded: str) -> str:
        """
        Decifra o que `encrypt` produziu.

        Levanta TokenDecryptionError se o valor estiver corrompido,
        truncado, ou tiver sido cifrado com outra chave (o GCM e
        autenticado, entao adulteracao e detectada, nao silenciada).
        """
        try:
            bruto = base64.b64decode(encoded, validate=True)
        except (ValueError, TypeError):
            raise TokenDecryptionError("Valor armazenado nao esta em base64 valido.") from None

        if len(bruto) <= NONCE_SIZE_BYTES:
            raise TokenDecryptionError("Valor armazenado esta truncado.")

        nonce, ciphertext = bruto[:NONCE_SIZE_BYTES], bruto[NONCE_SIZE_BYTES:]

        try:
            return self._aesgcm.decrypt(nonce, ciphertext, None).decode("utf-8")
        except InvalidTag:
            raise TokenDecryptionError(
                "Nao foi possivel decifrar o valor armazenado (chave diferente ou dado adulterado)."
            ) from None
        except UnicodeDecodeError:
            raise TokenDecryptionError("Valor decifrado nao e texto valido.") from None

    def __repr__(self) -> str:
        # Nunca expor a chave.
        return "TokenCipher(key='***')"
