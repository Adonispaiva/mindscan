"""
Performance Predictor
Gera previsões de performance a partir das dimensões normalizadas.
"""

from typing import Dict, Any


class PerformancePredictor:
    """
    Previsão linear simples baseada em:
    - média das dimensões
    - pesos específicos
    """

    def __init__(self):
        self.version = "1.0"

        self.weights = {
            "produtividade": 0.25,
            "execucao": 0.25,
            "autonomia": 0.20,
            "consistencia": 0.15,
            "foco": 0.15,
        }

    def predict(self, dims: Dict[str, float]) -> Dict[str, Any]:
        score = 0.0

        for dim, weight in self.weights.items():
            score += dims.get(dim, 0) * weight / 100

        return {
            "prediction_score": round(score * 100, 2),
            "message": "Previsão de performance calculada com base nas dimensões.",
            "version": self.version,
        }
