"""
Schema Output Formatter
Formata o bloco final de saída para o motor MindScan, consolidando:
- dimensões
- esquemas classificados
- fatores
- insights
- necessidades emocionais
- riscos
"""

from typing import Dict, Any


class SchemaOutputFormatter:
    """
    Converte os dados de Esquemas em um payload padronizado.
    """

    def __init__(self):
        self.version = "1.0"

    def format(
        self,
        normalized: Dict[str, float],
        classified: Dict[str, float],
        profile: Dict[str, Any],
        summary: Dict[str, Any],
        insights: Dict[str, str],
        risk_map: Dict[str, str],
    ) -> Dict[str, Any]:
        return {
            "module": "Esquemas",
            "version": self.version,
            "scores": normalized,
            "classified": classified,
            "profile": profile,
            "summary": summary,
            "insights": insights,
            "risk_map": risk_map,
        }
