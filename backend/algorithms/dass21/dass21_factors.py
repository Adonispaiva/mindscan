"""
DASS-21 Factors
Gera fatores agregados do DASS-21 para interpretação global.
"""

from typing import Dict


class Dass21Factors:
    """
    Constrói fatores emocionais derivados das três escalas base.
    """

    def __init__(self):
        self.version = "1.0"

    def compute(self, normalized_scores: Dict[str, float]) -> Dict[str, float]:
        """
        Retorna fatores agregados usados pelo MindScan.
        """

        depressao = normalized_scores.get("depressao", 0)
        ansiedade = normalized_scores.get("ansiedade", 0)
        estresse = normalized_scores.get("estresse", 0)

        # A lógica combina elementos clássicos de distress emocional.
        emotional_instability = (ansiedade + estresse) / 2
        cognitive_distortion = depressao
        physiological_tension = ansiedade

        return {
            "instabilidade_emocional": emotional_instability,
            "distorcao_cognitiva": cognitive_distortion,
            "tensao_fisiologica": physiological_tension,
            "indice_global": (
                emotional_instability + cognitive_distortion + physiological_tension
            ) / 3,
        }
