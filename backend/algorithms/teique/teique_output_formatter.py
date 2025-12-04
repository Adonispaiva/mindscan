"""
TEIQue Output Formatter
Converte resultados brutos do módulo TEIQue em um payload padronizado para o
MindScanEngine → Crosslinks → ReportService.
"""

from typing import Dict, Any


class TeiqueOutputFormatter:
    """
    Formata o resultado do TEIQue em um dicionário estruturado.
    """

    def __init__(self):
        self.version = "1.0"

    def format(self, scores: Dict[str, float], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recebe:
            scores = { dimensão: valor_padronizado_0_100 }
            metadata = { raw_scores, timestamps, norms_version, etc. }

        Retorna:
            payload estruturado para integração.
        """
        return {
            "module": "TEIQue",
            "version": self.version,
            "scores": scores,
            "highlights": self._extract_highlights(scores),
            "metadata": metadata,
        }

    def _extract_highlights(self, scores: Dict[str, float]) -> Dict[str, str]:
        """
        Identifica pontos fortes e vulnerabilidades.
        """
        if not scores:
            return {"strengths": [], "risks": []}

        sorted_dims = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        strengths = [d for d, v in sorted_dims[:3]]
        risks = [d for d, v in sorted_dims[-3:]]

        return {
            "strengths": strengths,
            "risks": risks,
        }
