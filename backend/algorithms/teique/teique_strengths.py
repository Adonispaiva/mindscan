# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\teique\teique_strengths.py
# Última atualização: 2025-12-11T09:59:20.730228

"""
TEIQue Strengths
Gera mapa de forças emocionais baseado nas dimensões e fatores agregados do TEIQue.
"""

from typing import Dict, List


class TeiqueStrengths:
    """
    Identifica forças emocionais com base em scores altos.
    """

    def __init__(self):
        self.version = "1.0"

        self.strength_descriptions = {
            "otimismo": "Capacidade de manter uma perspectiva positiva mesmo em desafios.",
            "autoestima": "Confiança consistente nas próprias capacidades.",
            "empatia": "Sensibilidade ampliada para emoções e necessidades alheias.",
            "relacoes": "Competência para construir vínculos saudáveis.",
            "adaptabilidade": "Flexibilidade emocional para lidar com mudanças.",
            "satisfacao": "Tendência a manter estabilidade emocional e bem-estar.",
        }

    def extract(self, scores: Dict[str, float]) -> Dict[str, str]:
        """
        Identifica dimensões de alta performance emocional (>= 70).
        """

        strengths = {}
        for dim, val in scores.items():
            if val >= 70:
                descr = self.strength_descriptions.get(
                    dim,
                    "Desempenho emocional consistentemente elevado."
                )
                strengths[dim] = descr

        return {
            "module": "TEIQue",
            "version": self.version,
            "strengths": strengths
        }
