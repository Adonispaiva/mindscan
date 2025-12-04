"""
TEIQue Summary
Gera um resumo executivo e técnico a partir de:
- scores individuais
- fatores agregados
- forças
- riscos
"""

from typing import Dict, Any, List


class TeiqueSummary:
    """
    Consolida todas as informações do TEIQue em um resumo unificado.
    """

    def __init__(self):
        self.version = "1.0"

    def build(
        self,
        scores: Dict[str, float],
        factors: Dict[str, float],
        strengths: Dict[str, str],
        risks: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Retorna estrutura padrão utilizada pelo MindScanEngine
        e pelos renderizadores de relatório PDF.
        """

        summary = {
            "average": self._compute_average(scores),
            "dominant_factors": self._top_factors(factors),
            "strengths": list(strengths.keys()),
            "risks": list(risks.keys()),
        }

        return {
            "module": "TEIQue",
            "version": self.version,
            "summary": summary,
            "details": {
                "scores": scores,
                "factors": factors,
                "strengths_desc": strengths,
                "risks_desc": risks,
            }
        }

    def _compute_average(self, scores: Dict[str, float]) -> float:
        if not scores:
            return 0
        return sum(scores.values()) / len(scores)

    def _top_factors(self, factors: Dict[str, float]) -> List[str]:
        if not factors:
            return []
        sorted_f = sorted(factors.items(), key=lambda x: x[1], reverse=True)
        return [f for f, _ in sorted_f[:2]]
