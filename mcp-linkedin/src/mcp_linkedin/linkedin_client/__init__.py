"""
Ferramentas MCP de negocio (leitura do perfil e publicacao).

Ao contrario do mcp-instagram, que e somente leitura por construcao,
este componente PUBLICA. O transporte precisa saber escrever, entao a
protecao nao pode ser estrutural: ela e explicita e vive nas
ferramentas, onde publicar exige texto vindo de quem chama e uma
confirmacao em segunda chamada.
"""

from mcp_linkedin.linkedin_client.publicacao import (
    LIMITE_CARACTERES,
    ClienteLinkedIn,
    ErroDaApi,
    PermissaoAusenteError,
    SemAutorizacaoError,
    TextoInvalidoError,
)
from mcp_linkedin.linkedin_client.transporte import (
    ErroDeTransporte,
    RespostaLinkedIn,
    TransporteLinkedIn,
    TransporteLinkedInHttpx,
)

__all__ = [
    "LIMITE_CARACTERES",
    "ClienteLinkedIn",
    "ErroDaApi",
    "ErroDeTransporte",
    "PermissaoAusenteError",
    "RespostaLinkedIn",
    "SemAutorizacaoError",
    "TextoInvalidoError",
    "TransporteLinkedIn",
    "TransporteLinkedInHttpx",
]
