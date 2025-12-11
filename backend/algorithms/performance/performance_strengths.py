# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\performance\performance_strengths.py
# Última atualização: 2025-12-11T09:59:20.714601

"""
Performance Strengths
Identifica forças profissionais a partir das dimensões de performance.
"""

from typing import Dict


class PerformanceStrengths:
    def __init__(self):
        self.version = "1.0"

        self.strength_map = {
            "produtividade": "Alta capacidade de entrega.",
            "execucao": "Execução precisa com baixo retrabalho.",
            "autonomia": "Independência e responsabilidade elevada.",
            "consistencia": "Estabilidade e previsibilidade operacional.",
            "foco": "Priorização eficiente e concentração.",
        }

    def extract(self, dims: Dict[str, float]) -> Dict[str, str]:
        strengths = {}

        for dim, value in dims.items():
            if value >= 70:
                strengths[dim] = self.strength_map.get(
                    dim,
                    "Força associada à dimensão."
                )

        return strengths
