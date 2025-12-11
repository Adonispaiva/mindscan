# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\teique\teique_risk_flags.py
# Última atualização: 2025-12-11T09:59:20.730228

"""
TEIQue — Risk Flags
Geração de bandeiras de risco emocionais utilizando padrões do MindScan.
"""

from typing import Dict, Any, List


class TeiqueRiskFlags:
    """
    Analisa scores individuais e fatores agregados para marcar riscos emocionais.
    """

    def __init__(self):
        self.version = "1.0"

        # Limiares oficiais MindScan
        self.threshold_low = 40
        self.threshold_high = 70

    def evaluate(self, scores: Dict[str, float], factors: Dict[str, float]) -> Dict[str, List[str]]:
        """
        Retorna:
            - riscos por dimensão
            - riscos por fator agregado
            - indicadores globais
        """

        dim_risks = [d for d, v in scores.items() if v < self.threshold_low]
        factor_risks = [f for f, v in factors.items() if v < self.threshold_low]

        global_risk = self._compute_global_risk(scores, factors)

        return {
            "dimension_risks": dim_risks,
            "factor_risks": factor_risks,
            "global_risk": global_risk,
        }

    def _compute_global_risk(self, scores: Dict[str, float], factors: Dict[str, float]) -> str:
        """
        Classifica risco global emocional.
        """

        avg = (
            sum(scores.values()) / len(scores)
            if scores else 0
        )

        if avg < self.threshold_low:
            return "alto"
        if avg < self.threshold_high:
            return "moderado"
        return "baixo"
