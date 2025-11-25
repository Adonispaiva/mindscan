# algorithm_output.py
# MindScan Rebuild – Modelo Unificado de Saída dos Algoritmos
# Versão Definitiva • Estrutura Avançada Pydantic-Style
# Autor: Leo Vinci — IA Supervisora Inovexa
# Última atualização: 23/11/2025
# -------------------------------------------------------------------------
# Este módulo define o formator oficial de saída padronizada
# para qualquer algoritmo da camada backend.algorithms:
#
#   - big5
#   - teique
#   - dass21
#   - esquemas
#   - performance
#   - bussola
#   - ocai
#   - cross_insights
#
# Todos os algoritmos devem retornar um objeto compatível com
# este modelo, garantindo padronização, validação e integridade.
# -------------------------------------------------------------------------

from dataclasses import dataclass, field
from typing import Dict, Any
import datetime


class ValidationError(Exception):
    pass


def require(condition: bool, message: str):
    if not condition:
        raise ValidationError(message)


@dataclass
class AlgorithmOutput:
    """
    Modelo universal de saída dos algoritmos MindScan.
    """

    model: str                                # nome do algoritmo
    results: Dict[str, Any]                   # scores normalizados ou estruturados
    metadata: Dict[str, Any]                  # detalhes, descrições, ranges, etc.
    dimensions: Any = None                    # lista de dimensões (opcional)
    raw_data: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    # ---------------------------------------------------------------------
    # Validação final
    # ---------------------------------------------------------------------

    def __post_init__(self):
        require(isinstance(self.model, str) and len(self.model) > 0,
                "model deve ser string não vazia.")

        require(isinstance(self.results, dict) and len(self.results) > 0,
                "results deve ser dicionário não vazio.")

        require(isinstance(self.metadata, dict),
                "metadata deve ser dicionário.")

        require(isinstance(self.raw_data, dict),
                "raw_data deve ser dicionário.")

        require(isinstance(self.timestamp, str) and len(self.timestamp) > 0,
                "timestamp inválido.")

    # ---------------------------------------------------------------------
    # Conversão final padronizada
    # ---------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "results": self.results,
            "metadata": self.metadata,
            "dimensions": self.dimensions,
            "raw_data": self.raw_data,
            "timestamp": self.timestamp
        }

    # ---------------------------------------------------------------------
    # Resumo simplificado
    # ---------------------------------------------------------------------

    def summary(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "dimensions": self.dimensions,
            "keys": list(self.results.keys()),
        }
