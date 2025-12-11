# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\performance\performance_risk_map.py
# Última atualização: 2025-12-11T09:59:20.714601

"""
Performance Risk Map
Mapeia riscos profissionais com base nas dimensões normalizadas.
"""

from typing import Dict


class PerformanceRiskMap:
    def __init__(self):
        self.version = "1.0"

        self.risk_map = {
            "produtividade": "Risco de sobrecarga ou baixa entrega.",
            "execucao": "Risco de atraso, retrabalho ou baixa precisão.",
            "autonomia": "Dependência excessiva de supervisão.",
            "consistencia": "Variações de qualidade ou instabilidade.",
            "foco": "Dificuldade de priorização e dispersão.",
        }

    def map(self, dims: Dict[str, float]) -> Dict[str, str]:
        risks = {}

        for dim, value in dims.items():
            if value <= 30:
                risks[dim] = self.risk_map.get(
                    dim,
                    "Risco associado à dimensão."
                )

        return risks
