"""
Schema Summary
Consolida o perfil dimensional (item-level) gerado pelo SchemaProfileBuilder.
"""

from typing import Dict, Any


class SchemaSummary:
    """
    Summary intermediário usado no pipeline — abaixo do nível dos 18 Esquemas.
    """

    def __init__(self):
        self.version = "1.0"

    def build(
        self,
        dimensions: Dict[str, float],
        alerts: list,
        profile: Dict[str, Any],
        risks: Dict[str, str],
    ) -> Dict[str, Any]:
        """
        Gera o bloco final com:
        - dimensões
        - alertas
        - riscos
        - predominâncias
        """

        top2 = sorted(
            dimensions.items(),
            key=lambda x: x[1],
            reverse=True
        )[:2]

        return {
            "module": "Esquemas",
            "version": self.version,
            "summary": {
                "top_dimensions": [d[0] for d in top2],
                "alerts": alerts,
                "risks": risks,
                "profile": profile,
            },
            "details": {
                "dimensions_raw": dimensions,
                "alerts_full": alerts,
                "risks_full": risks,
                "profile_full": profile,
            },
        }
