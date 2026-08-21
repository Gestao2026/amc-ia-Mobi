"""
Cliente de LEITURA da conta do Instagram (Graph API).

Somente leitura, por construção. Este módulo não tem nenhum método que
publique, edite, exclua, comente, responda mensagem ou administre
anúncio, e nenhum caminho de código que faça POST, PUT ou DELETE. O
transporte que ele recebe expõe apenas `get`, então a limitação não
depende da disciplina de quem escreve: ela é estrutural.

Os escopos configurados por padrão (`instagram_business_basic` e
`instagram_business_manage_insights`) sustentam exatamente o que está
aqui: dados do perfil, lista de publicações com engajamento, métrica de
uma publicação e métrica da conta.

Sobre métrica que volta vazia ou com erro: a disponibilidade de cada
métrica muda conforme o tipo de conta (Comercial entrega mais que
Criador de conteúdo) e conforme a idade da publicação. Quando a Meta
recusa uma métrica, este módulo devolve a mensagem da própria Meta em
vez de engolir o erro e fingir que o dado não existe. Diagnóstico errado
é pior que ausência de dado.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Callable

from mcp_instagram.instagram_client.transporte import RespostaGraph, TransporteGraph

BASE_GRAPH = "https://graph.instagram.com"
VERSAO_API_PADRAO = "v23.0"

# Campos do perfil. `followers_count` e `media_count` são os que
# sustentam qualquer leitura de crescimento; o resto é identificação.
CAMPOS_PERFIL = (
    "id",
    "username",
    "name",
    "account_type",
    "profile_picture_url",
    "followers_count",
    "follows_count",
    "media_count",
    "biography",
    "website",
)

# Campos de cada publicação. `like_count` e `comments_count` vêm aqui
# mesmo, sem precisar de uma chamada de métrica por publicação, o que
# torna a listagem barata.
CAMPOS_PUBLICACAO = (
    "id",
    "caption",
    "media_type",
    "media_product_type",
    "permalink",
    "timestamp",
    "like_count",
    "comments_count",
    "thumbnail_url",
    "media_url",
)

METRICAS_PUBLICACAO_PADRAO = (
    "reach",
    "likes",
    "comments",
    "saved",
    "shares",
    "total_interactions",
    "views",
)

METRICAS_CONTA_PADRAO = (
    "reach",
    "views",
    "total_interactions",
    "accounts_engaged",
)

LIMITE_PUBLICACOES_MAXIMO = 50
LIMITE_PUBLICACOES_PADRAO = 12

# A Meta recusa janela de métrica maior que 30 dias.
JANELA_DIAS_MAXIMA = 30
JANELA_DIAS_PADRAO = 28

SEGUNDOS_POR_DIA = 86400


class SemAutorizacaoError(Exception):
    """Não existe access token válido guardado. Nunca contém token."""


@dataclass(frozen=True)
class ErroDaApi(Exception):
    """
    Erro devolvido pela própria Graph API, repassado com a mensagem
    original da Meta. A mensagem da Meta descreve o problema (métrica
    indisponível, permissão faltando, id inexistente) e não contém
    credencial.
    """

    mensagem: str
    tipo: str | None = None
    codigo: int | None = None
    status_http: int | None = None

    def __str__(self) -> str:
        return self.mensagem

    def como_dicionario(self) -> dict:
        return {
            "erro": self.mensagem,
            "tipo": self.tipo,
            "codigo": self.codigo,
            "status_http": self.status_http,
        }


class ClienteLeituraInstagram:
    """
    Leitura da conta conectada. Recebe o token por função (`obter_token`)
    em vez de guardá-lo em atributo, para o token ser lido do TokenStore
    no momento do uso: assim, revogar ou apagar a autorização passa a
    valer já na chamada seguinte, sem o cliente segurar uma cópia velha.
    """

    def __init__(
        self,
        transporte: TransporteGraph,
        obter_token: Callable[[], str | None],
        versao_api: str = VERSAO_API_PADRAO,
        relogio: Callable[[], float] = time.time,
    ) -> None:
        self._transporte = transporte
        self._obter_token = obter_token
        self._versao_api = versao_api
        self._relogio = relogio

    # -----------------------------------------------------------------
    # Leituras
    # -----------------------------------------------------------------

    def perfil(self) -> dict:
        """Dados do perfil da conta conectada."""
        return self._get("me", {"fields": ",".join(CAMPOS_PERFIL)})

    def publicacoes(self, limite: int = LIMITE_PUBLICACOES_PADRAO) -> dict:
        """
        Publicações mais recentes, da mais nova para a mais antiga, já
        com curtidas e comentários.
        """
        return self._get(
            "me/media",
            {
                "fields": ",".join(CAMPOS_PUBLICACAO),
                "limit": _limitar(limite, 1, LIMITE_PUBLICACOES_MAXIMO),
            },
        )

    def metricas_publicacao(self, id_publicacao: str, metricas=None) -> dict:
        """Métricas de uma publicação específica."""
        escolhidas = tuple(metricas) if metricas else METRICAS_PUBLICACAO_PADRAO
        return self._get(f"{id_publicacao}/insights", {"metric": ",".join(escolhidas)})

    def metricas_conta(self, dias: int = JANELA_DIAS_PADRAO, metricas=None) -> dict:
        """
        Métricas agregadas da conta na janela pedida. A Meta recusa
        janela maior que 30 dias, então o valor é limitado aqui, em vez
        de virar um erro remoto sem explicação.
        """
        escolhidas = tuple(metricas) if metricas else METRICAS_CONTA_PADRAO
        janela = _limitar(dias, 1, JANELA_DIAS_MAXIMA)
        ate = int(self._relogio())
        desde = ate - janela * SEGUNDOS_POR_DIA
        return self._get(
            "me/insights",
            {
                "metric": ",".join(escolhidas),
                "metric_type": "total_value",
                "period": "day",
                "since": desde,
                "until": ate,
            },
        )

    # -----------------------------------------------------------------
    # Interno
    # -----------------------------------------------------------------

    def _get(self, caminho: str, params: dict) -> dict:
        token = self._obter_token()
        if not token:
            raise SemAutorizacaoError(
                "Não existe autorização válida do Instagram neste servidor. "
                "Use a ferramenta instagram_oauth_iniciar para autorizar."
            )

        url = f"{BASE_GRAPH}/{self._versao_api}/{caminho}"
        resposta = self._transporte.get(url, params, token)
        return _interpretar(resposta)


def _interpretar(resposta: RespostaGraph) -> dict:
    """
    Converte a resposta crua em dicionário, ou levanta `ErroDaApi` com a
    mensagem da própria Meta.
    """
    try:
        corpo = json.loads(resposta.text)
    except (ValueError, TypeError):
        raise ErroDaApi(
            mensagem="A Meta devolveu uma resposta que não é JSON válido.",
            status_http=resposta.status_code,
        ) from None

    if not isinstance(corpo, dict):
        raise ErroDaApi(
            mensagem="A Meta devolveu um JSON em formato inesperado.",
            status_http=resposta.status_code,
        )

    erro = corpo.get("error")
    if isinstance(erro, dict):
        raise ErroDaApi(
            mensagem=str(erro.get("message") or "A Meta recusou a consulta sem detalhar o motivo."),
            tipo=erro.get("type"),
            codigo=erro.get("code"),
            status_http=resposta.status_code,
        )

    if resposta.status_code >= 400:
        raise ErroDaApi(
            mensagem="A Meta recusou a consulta sem detalhar o motivo.",
            status_http=resposta.status_code,
        )

    return corpo


def _limitar(valor, minimo: int, maximo: int) -> int:
    """Mantém o valor dentro da faixa aceita pela Meta."""
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        return minimo
    return max(minimo, min(maximo, numero))
