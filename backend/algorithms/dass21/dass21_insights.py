# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\dass21\dass21_insights.py
# Última atualização: 2025-12-11T09:59:20.667799

"""
DASS-21 Insights
Gera interpretações qualitativas automáticas das subescalas.
"""

from typing import Dict


class Dass21Insights:
    """
    Produz insights interpretativos para cada escala.
    """

    def __init__(self):
        self.version = "1.0"

        self.templates = {
            "depressao": {
                "baixo": "Oscilações emocionais dentro da normalidade.",
                "moderado": "Alguns sinais de rebaixamento afetivo.",
                "alto": "Indícios fortes de sofrimento depressivo."
            },
            "ansiedade": {
                "baixo": "Regulação adequada de ativação e alerta.",
                "moderado": "Tendência a níveis elevados de preocupação.",
                "alto": "Níveis intensos de ansiedade e hiperativação."
            },
            "estresse": {
                "baixo": "Boa gestão das demandas e pressões.",
                "moderado": "Níveis significativos de tensão emocional.",
                "alto": "Sobrecarga emocional intensa."
            },
        }

    def generate(self, severity: Dict[str, str]) -> Dict[str, str]:
        """
        severity:
            {"depressao": "moderado", ...}
        """
        insights = {}

        for scale, level in severity.items():
            scale_templates = self.templates.get(scale, {})
            insights[scale] = scale_templates.get(
                level,
                "Padrões emocionais observados nesta escala."
            )

        return insights
