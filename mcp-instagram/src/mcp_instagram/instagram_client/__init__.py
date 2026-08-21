"""
Ferramentas MCP de negócio (leitura de perfil e métricas).

Somente leitura. O cliente exposto aqui não publica, não edita, não
exclui, não comenta, não responde mensagem e não administra anúncio: o
transporte que ele usa expõe apenas `get`, então a limitação é
estrutural, não uma promessa.
"""

from mcp_instagram.instagram_client.leitura import (
    ClienteLeituraInstagram,
    ErroDaApi,
    SemAutorizacaoError,
)
from mcp_instagram.instagram_client.transporte import (
    ErroDeTransporte,
    RespostaGraph,
    TransporteGraph,
    TransporteGraphHttpx,
)

__all__ = [
    "ClienteLeituraInstagram",
    "ErroDaApi",
    "ErroDeTransporte",
    "RespostaGraph",
    "SemAutorizacaoError",
    "TransporteGraph",
    "TransporteGraphHttpx",
]
