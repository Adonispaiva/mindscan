# ================================================================
#  MindScan — TEIQue Dimensions
#  Categoria: Algorithm — TEIQue
#  Responsável: Leo Vinci (Inovexa)
#
#  Objetivo:
#      Calcular as quatro dimensões globais do TEIQue a partir
#      das facetas:
#          - Bem-Estar       (happiness, self_esteem, optimism)
#          - Autocontrole   (stress_management, emotion_regulation, impulse_control)
#          - Emocionalidade (emotion_perception, emotion_expression,
#                            relationships, empathy)
#          - Sociabilidade  (assertiveness, emotion_management_others,
#                            social_awareness)
#
#  API pública:
#      TEIQueDimensionsCalculator.calculate(facets: dict) -> dict
#
#  Exemplo de uso:
#      calc = TEIQueDimensionsCalculator()
#      dims = calc.calculate(facets_dict)
# ================================================================

from typing import Dict, Any


class TEIQueDimensionsCalculator:
    """
    Calcula as dimensões globais do TEIQue a partir das facetas.

    Espera um dicionário no formato:

        {
            "happiness": 0–10,
            "self_esteem": 0–10,
            "optimism": 0–10,
            "stress_management": 0–10,
            "emotion_regulation": 0–10,
            "impulse_control": 0–10,
            "emotion_perception": 0–10,
            "emotion_expression": 0–10,
            "relationships": 0–10,
            "empathy": 0–10,
            "assertiveness": 0–10,
            "emotion_management_others": 0–10,
            "social_awareness": 0–10,
        }
    """

    WELL_BEING_KEYS = ("happiness", "self_esteem", "optimism")
    SELF_CONTROL_KEYS = ("stress_management", "emotion_regulation", "impulse_control")
    EMOTIONALITY_KEYS = (
        "emotion_perception",
        "emotion_expression",
        "relationships",
        "empathy",
    )
    SOCIABILITY_KEYS = (
        "assertiveness",
        "emotion_management_others",
        "social_awareness",
    )

    def calculate(self, facets: Dict[str, float]) -> Dict[str, Any]:
        """Calcula as dimensões e um score global médio."""

        well_being = self._avg(facets, self.WELL_BEING_KEYS)
        self_control = self._avg(facets, self.SELF_CONTROL_KEYS)
        emotionality = self._avg(facets, self.EMOTIONALITY_KEYS)
        sociability = self._avg(facets, self.SOCIABILITY_KEYS)

        dims = {
            "well_being": well_being,
            "self_control": self_control,
            "emotionality": emotionality,
            "sociability": sociability,
        }

        # média simples das dimensões
        global_score = round(
            sum(v for v in dims.values() if v is not None) / len(dims), 2
        )

        dims["global"] = global_score
        return dims

    # ------------------------------------------------------------
    #  Helpers
    # ------------------------------------------------------------
    @staticmethod
    def _avg(source: Dict[str, float], keys) -> float:
        values = [source[k] for k in keys if k in source]
        if not values:
            return 0.0
        return round(sum(values) / len(values), 2)


if __name__ == "__main__":
    example_facets = {
        "happiness": 7.0,
        "self_esteem": 6.5,
        "optimism": 7.2,
        "stress_management": 6.8,
        "emotion_regulation": 6.0,
        "impulse_control": 5.5,
        "emotion_perception": 7.0,
        "emotion_expression": 6.5,
        "relationships": 6.8,
        "empathy": 7.4,
        "assertiveness": 6.2,
        "emotion_management_others": 6.7,
        "social_awareness": 6.9,
    }

    calc = TEIQueDimensionsCalculator()
    print(calc.calculate(example_facets))
