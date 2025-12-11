# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\performance\performance_norms.py
# Última atualização: 2025-12-11T09:59:20.714601

"""
Performance Norms
Normaliza os valores brutos do questionário de performance para 0–100.
"""

from typing import Dict


class PerformanceNorms:
    def __init__(self):
        self.version = "1.0"
        self.max_raw = 10.0  # normalização universal 0–100

    def normalize(self, raw_scores: Dict[str, float]) -> Dict[str, float]:
        normalized = {}

        for item, value in raw_scores.items():
            v = max(min(float(value), self.max_raw), 0)
            normalized[item] = (v / self.max_raw) * 100

        return normalized
