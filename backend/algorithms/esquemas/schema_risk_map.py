"""
Schema Risk Map
Mapeia riscos psicodinâmicos com base nas dimensões intermediárias (item-level).
"""

from typing import Dict


class SchemaRiskMap:
    """
    Detecta riscos precoces em padrões dimensionais,
    antes da consolidação nos 18 Esquemas de Young.
    """

    def __init__(self):
        self.version = "1.0"

        self.risk_descriptions = {
            "autorregulacao_emocional": "Dificuldades de modulação afetiva e rigidez emocional.",
            "vinculacao": "Riscos relacionados à conexão social e vínculos instáveis.",
            "autonomia": "Vulnerabilidade a dependência emocional ou medo excessivo.",
            "autoimagem": "Riscos relacionados à visão negativa de si mesmo.",
        }

    def generate(self, dimensions: Dict[str, float]) -> Dict[str, str]:
        """
        Riscos são retornados para dimensões >60.
        """
        risks = {}

        for dim, value in dimensions.items():
            if value >= 60:
                risks[dim] = self.risk_descriptions.get(
                    dim,
                    "Risco psicodinâmico associado à dimensão."
                )

        return risks
