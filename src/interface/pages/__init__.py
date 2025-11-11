"""
Inicializador do pacote pages
"""

from .dados_pessoais import PaginaDadosPessoais
from .ficha_treino import PaginaFichaTreino
from .resultados import PaginaResultados
from .informacoes import PaginaInformacoes

__all__ = [
    'PaginaDadosPessoais',
    'PaginaFichaTreino',
    'PaginaResultados',
    'PaginaInformacoes',
]
