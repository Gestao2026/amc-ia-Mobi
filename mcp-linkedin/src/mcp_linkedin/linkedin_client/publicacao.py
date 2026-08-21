"""
Cliente de leitura e publicacao no LinkedIn.

O que este modulo PODE fazer, e por que so isso:

  ler o proprio perfil      escopo `openid`/`profile`, aprovado
  publicar no perfil        escopo `w_member_social`, produto
                            "Compartilhe no LinkedIn", aprovado

O que ele NAO pode, e nao adianta tentar:

  ler metricas e engajamento    exige Community Management API
  publicar como Pagina          exige Community Management API
  ler publicacoes existentes    exige Community Management API

A Community Management API nao esta aprovada no aplicativo nem entrou
na fila de analise. Isso e limitacao externa, do lado do LinkedIn, e
nao tem contorno tecnico deste lado.

REGRA DE OURO DESTE MODULO: publicar exige texto explicito recebido de
quem chamou. Nao ha valor padrao, nao ha texto gerado aqui, nao ha
reaproveitamento de rascunho. Texto vazio levanta erro em vez de virar
uma publicacao em branco no perfil de alguem.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable

from mcp_linkedin.linkedin_client.transporte import RespostaLinkedIn, TransporteLinkedIn

BASE_API = "https://api.linkedin.com"

# Endpoint OpenID Connect. Devolve o `sub`, que e o identificador do
# membro, e sem ele nao ha como dizer ao LinkedIn quem e o autor.
URL_PERFIL = f"{BASE_API}/v2/userinfo"

URL_PUBLICACOES = f"{BASE_API}/rest/posts"

# O LinkedIn recusa publicacao acima deste tamanho. Conferir aqui evita
# uma ida ate a API para receber um erro que ja era previsivel.
LIMITE_CARACTERES = 3000

VISIBILIDADES = ("PUBLIC", "CONNECTIONS")


class SemAutorizacaoError(Exception):
    """Nao existe access token valido guardado. Nunca contem token."""


class TextoInvalidoError(ValueError):
    """O texto da publicacao esta vazio ou excede o limite do LinkedIn."""


class PermissaoAusenteError(Exception):
    """
    A autorizacao atual nao inclui `w_member_social`. Erro proprio, e
    nao um `ErroDaApi` generico, porque a solucao e especifica e vale a
    pena dizer qual e: acrescentar o escopo e autorizar de novo.
    """


@dataclass(frozen=True)
class ErroDaApi(Exception):
    """Erro devolvido pelo proprio LinkedIn, com a mensagem original dele."""

    mensagem: str
    status_http: int | None = None
    codigo: str | None = None

    def __str__(self) -> str:
        return self.mensagem

    def como_dicionario(self) -> dict:
        return {"erro": self.mensagem, "status_http": self.status_http, "codigo": self.codigo}


class ClienteLinkedIn:
    """
    Leitura do perfil e publicacao no perfil pessoal.

    Recebe o token por funcao (`obter_token`) em vez de guarda-lo em
    atributo, para o token ser lido do TokenStore no momento do uso:
    assim, revogar a autorizacao passa a valer ja na chamada seguinte.
    """

    def __init__(
        self,
        transporte: TransporteLinkedIn,
        obter_token: Callable[[], str | None],
    ) -> None:
        self._transporte = transporte
        self._obter_token = obter_token

    # -----------------------------------------------------------------
    # Leitura
    # -----------------------------------------------------------------

    def perfil(self) -> dict:
        """
        Dados do proprio perfil: nome, foto e o identificador do membro.
        E a unica leitura possivel com os escopos aprovados.
        """
        token = self._token()
        resposta = self._transporte.get(URL_PERFIL, {}, token)
        return _interpretar(resposta)

    def urn_do_autor(self) -> str:
        """
        Identificador do membro no formato que a API de publicacao exige.
        Vem do `sub` do OpenID Connect.
        """
        dados = self.perfil()
        sub = dados.get("sub")
        if not sub:
            raise ErroDaApi(
                mensagem=(
                    "O LinkedIn nao devolveu o identificador do membro. "
                    "Confirme que o escopo 'openid' esta autorizado."
                )
            )
        return f"urn:li:person:{sub}"

    # -----------------------------------------------------------------
    # Publicacao
    # -----------------------------------------------------------------

    def publicar(self, texto: str, visibilidade: str = "PUBLIC") -> dict:
        """
        Publica um texto no perfil pessoal de quem autorizou.

        `texto` e obrigatorio e vem de quem chamou. Este metodo nao tem
        texto padrao e nao gera conteudo: uma publicacao no perfil de
        alguem nunca deve nascer de um valor default.
        """
        texto_limpo = (texto or "").strip()

        if not texto_limpo:
            raise TextoInvalidoError(
                "O texto da publicacao esta vazio. Informe o texto que deve ser publicado."
            )

        if len(texto_limpo) > LIMITE_CARACTERES:
            raise TextoInvalidoError(
                f"O texto tem {len(texto_limpo)} caracteres e o LinkedIn aceita no maximo "
                f"{LIMITE_CARACTERES}. Reduza {len(texto_limpo) - LIMITE_CARACTERES} caracteres."
            )

        if visibilidade not in VISIBILIDADES:
            raise TextoInvalidoError(
                f"Visibilidade invalida: use {' ou '.join(VISIBILIDADES)}."
            )

        token = self._token()
        autor = self.urn_do_autor()

        corpo = {
            "author": autor,
            "commentary": texto_limpo,
            "visibility": visibilidade,
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
        }

        resposta = self._transporte.post(URL_PUBLICACOES, corpo, token)

        if resposta.status_code == 403:
            raise PermissaoAusenteError(
                "A autorizacao atual nao permite publicar. Acrescente 'w_member_social' "
                "a variavel LINKEDIN_SCOPES no servidor e autorize a conta novamente."
            )

        _interpretar(resposta, aceita_corpo_vazio=True)

        return {
            "id": resposta.id_criado,
            "visibilidade": visibilidade,
            "caracteres": len(texto_limpo),
        }

    # -----------------------------------------------------------------
    # Interno
    # -----------------------------------------------------------------

    def _token(self) -> str:
        token = self._obter_token()
        if not token:
            raise SemAutorizacaoError(
                "Nao existe autorizacao valida do LinkedIn neste servidor. "
                "Use a ferramenta linkedin_oauth_iniciar para autorizar."
            )
        return token


def _interpretar(resposta: RespostaLinkedIn, aceita_corpo_vazio: bool = False) -> dict:
    """
    Converte a resposta crua em dicionario, ou levanta `ErroDaApi` com a
    mensagem do proprio LinkedIn.

    `aceita_corpo_vazio` existe porque a criacao de publicacao responde
    201 com corpo vazio: o id vem no cabecalho. Sem esta excecao, uma
    publicacao bem-sucedida seria reportada como erro de JSON.
    """
    corpo_bruto = (resposta.text or "").strip()

    if not corpo_bruto:
        if aceita_corpo_vazio and 200 <= resposta.status_code < 300:
            return {}
        raise ErroDaApi(
            mensagem="O LinkedIn respondeu sem conteudo.",
            status_http=resposta.status_code,
        )

    try:
        corpo = json.loads(corpo_bruto)
    except (ValueError, TypeError):
        raise ErroDaApi(
            mensagem="O LinkedIn devolveu uma resposta que nao e JSON valido.",
            status_http=resposta.status_code,
        ) from None

    if not isinstance(corpo, dict):
        raise ErroDaApi(
            mensagem="O LinkedIn devolveu um JSON em formato inesperado.",
            status_http=resposta.status_code,
        )

    if resposta.status_code >= 400:
        raise ErroDaApi(
            mensagem=str(
                corpo.get("message") or "O LinkedIn recusou a chamada sem detalhar o motivo."
            ),
            status_http=resposta.status_code,
            codigo=corpo.get("code") or corpo.get("serviceErrorCode"),
        )

    return corpo
