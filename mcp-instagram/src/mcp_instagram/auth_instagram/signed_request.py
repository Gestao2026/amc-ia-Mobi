"""
Verificação do `signed_request` da Meta (Camada 2, mcp-instagram).

A Meta usa este formato para avisar o servidor de dois eventos, ambos
exigidos por ela para qualquer aplicativo do Instagram:

  1. **Desautorização**: a pessoa removeu o aplicativo nas configurações
     do Instagram.
  2. **Exclusão de dados**: a pessoa pediu que os dados dela sejam
     apagados.

Nos dois casos a Meta chama uma rota pública deste servidor por POST,
sem nenhum token de autenticação nosso. A prova de que a chamada veio
mesmo da Meta é a assinatura: o corpo vem no formato

    base64url(assinatura) . base64url(payload)

onde a assinatura é um HMAC-SHA256 do texto do payload, calculado com o
Client Secret do aplicativo. Como esse segredo existe apenas na Meta e
no ambiente deste servidor, uma assinatura válida só pode ter sido
produzida por ela.

Sem essa verificação, qualquer pessoa que descobrisse a URL poderia
apagar a autorização do captador enviando um POST vazio. Por isso a
comparação é feita com `hmac.compare_digest`, que gasta o mesmo tempo
para qualquer entrada e não vaza informação por medição de tempo.

Nenhuma função aqui imprime, registra em log ou inclui o segredo, a
assinatura ou o conteúdo do payload em mensagem de erro.
"""

from __future__ import annotations

import base64
import binascii
import hmac
import json
from hashlib import sha256
from typing import Any

ALGORITMO_ESPERADO = "HMAC-SHA256"


class InvalidSignedRequestError(Exception):
    """Requisição assinada ausente, malformada ou com assinatura inválida. Nunca contém segredo."""


def _decodificar_base64url(valor: str) -> bytes:
    """
    Decodifica base64url. A Meta envia sem os '=' de preenchimento, que
    o decodificador do Python exige, então eles são recolocados aqui.
    """
    preenchimento = "=" * (-len(valor) % 4)
    try:
        return base64.urlsafe_b64decode(valor + preenchimento)
    except (binascii.Error, ValueError):
        raise InvalidSignedRequestError("Trecho da requisição assinada não está em base64url válido.") from None


def parse_signed_request(signed_request: str | None, app_secret: str) -> dict[str, Any]:
    """
    Confere a assinatura e devolve o payload já decodificado.

    A ordem importa: a assinatura é conferida ANTES de o payload ser
    interpretado como dado, para que conteúdo não autenticado nunca
    chegue a influenciar decisão nenhuma.
    """
    if not signed_request:
        raise InvalidSignedRequestError("Requisição sem o campo signed_request.")

    partes = signed_request.split(".")
    if len(partes) != 2:
        raise InvalidSignedRequestError("Formato inesperado da requisição assinada.")

    assinatura_codificada, payload_codificado = partes

    assinatura_recebida = _decodificar_base64url(assinatura_codificada)

    # O HMAC é calculado sobre o TEXTO do payload como veio, ainda
    # codificado, e não sobre o JSON já decodificado: qualquer
    # renormalização mudaria os bytes e invalidaria a comparação.
    assinatura_esperada = hmac.new(
        app_secret.encode("utf-8"),
        payload_codificado.encode("utf-8"),
        sha256,
    ).digest()

    if not hmac.compare_digest(assinatura_recebida, assinatura_esperada):
        raise InvalidSignedRequestError("Assinatura da requisição não confere.")

    bruto = _decodificar_base64url(payload_codificado)

    try:
        payload = json.loads(bruto)
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise InvalidSignedRequestError("Conteúdo da requisição assinada não é um JSON válido.") from None

    if not isinstance(payload, dict):
        raise InvalidSignedRequestError("Conteúdo da requisição assinada não é um objeto JSON.")

    # A Meta declara o algoritmo dentro do próprio payload. Recusar
    # qualquer outro impede que uma mudança futura, ou uma tentativa de
    # rebaixamento, seja aceita em silêncio.
    if payload.get("algorithm") != ALGORITMO_ESPERADO:
        raise InvalidSignedRequestError("Algoritmo de assinatura não suportado.")

    return payload


def build_signed_request(payload: dict[str, Any], app_secret: str) -> str:
    """
    Monta uma requisição assinada válida.

    Existe para os testes conseguirem exercitar a verificação sem
    depender da Meta. Não é usada em produção: este servidor verifica
    assinatura, nunca produz uma.
    """
    payload_json = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    payload_codificado = base64.urlsafe_b64encode(payload_json).decode().rstrip("=")

    assinatura = hmac.new(
        app_secret.encode("utf-8"),
        payload_codificado.encode("utf-8"),
        sha256,
    ).digest()
    assinatura_codificada = base64.urlsafe_b64encode(assinatura).decode().rstrip("=")

    return f"{assinatura_codificada}.{payload_codificado}"
