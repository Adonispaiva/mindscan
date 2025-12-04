"""
Performance Scoring Matrix
Gera uma matriz de pontuação consolidada para uso em comparações:
- individuais
- grupais
- evolutivas (combinada com time series)
"""

from typing import Dict, Any


class PerformanceScoringMatrix:
    def __init__(self):
        self.version = "1.0"

        # Pesos definidos pelo modelo MindScan
        self.weights = {
            "produtividade": 0.24,
            "execucao": 0.24,
            "autonomia": 0.20,
            "consistencia": 0.16,
            "foco": 0.16,
        }

    def compute(self, dims: Dict[str, float]) -> Dict[str, Any]:
        matrix_score = 0

        for dim, weight in self.weights.items():
            matrix_score += dims.get(dim, 0) * weight / 100

        return {
            "module": "Performance",
            "version": self.version,
            "matrix_score": round(matrix_score * 100, 2),
            "weights": self.weights,
            "dimensions_used": dims,
        }
