"""
TEIQue Risk Map
Mapeia riscos emocionais específicos com base nas dimensões e fatores agregados.
"""

from typing import Dict, List


class TeiqueRiskMap:
    """
    Produz um mapa detalhado de riscos emocionais, cognitivos e sociais.
    """

    def __init__(self):
        self.version = "1.0"

        # Mapeamentos oficiais MindScan (baseados em literatura TEIQue)
        self.dimension_risk_map = {
            "impulsividade": "Dificuldade em controlar reações imediatas.",
            "controle_emocional": "Vulnerabilidade a perda de estabilidade emocional.",
            "autoestima": "Risco de autocrítica acentuada e insegurança.",
            "empatia": "Possível desconexão emocional em interações sociais.",
            "autorregulacao": "Dificuldade em ajustar estado emocional em demandas complexas.",
            "adaptabilidade": "Baixa flexibilidade diante de mudanças.",
        }

    def build(self, risk_flags: List[str]) -> Dict[str, str]:
        """
        Recebe uma lista de dimensões de risco e retorna um mapa explicativo.
        """
        details = {}

        for dim in risk_flags:
            desc = self.dimension_risk_map.get(
                dim,
                "Risco emocional identificado nesta dimensão."
            )
            details[dim] = desc

        return {
            "module": "TEIQue",
            "version": self.version,
            "risks": details
        }
