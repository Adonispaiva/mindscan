"""
Esquemas Profile Builder
Constrói o perfil final dos 18 Esquemas incluindo:
- fatores agregados
- necessidades emocionais
- padrões predominantes
"""

from typing import Dict, Any

from .esquemas_factor_weights import EsquemasFactorWeights
from .esquemas_needs_map import EsquemasNeedsMap


class EsquemasProfileBuilder:
    """
    Gera o perfil psicodinâmico estruturado usado pelo MindScanEngine.
    """

    def __init__(self):
        self.version = "1.0"

        self.factor_engine = EsquemasFactorWeights()
        self.needs_engine = EsquemasNeedsMap()

    def build(self, classified: Dict[str, float]) -> Dict[str, Any]:
        factors = self.factor_engine.compute(classified)
        needs_map = self.needs_engine.map(classified)

        predominant = sorted(
            classified.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]

        return {
            "module": "Esquemas",
            "version": self.version,
            "factors": factors,
            "needs_map": needs_map["needs_map"],
            "predominant_schemas": [p[0] for p in predominant],
        }
