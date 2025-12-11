# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\scoring_engine.py
# Última atualização: 2025-12-11T09:59:20.834001

# MindScan Scoring Engine — Ultra Superior
# Motor de cálculo central: aplica matriz de pesos, normalização
# e transforma indicadores em score global e setorial.

from backend.engine.normalizer import Normalizer
from backend.engine.validator import Validator

class ScoringEngine:

    def __init__(self, weights=None):
        self.normalizer = Normalizer()
        self.validator = Validator()
        self.weights = weights or {}

    def compute(self, indicators):
        """Calcula score global a partir de indicadores."""

        self.validator.ensure_numeric_map(indicators)

        scaled = self.normalizer.zscore(indicators)

        weights = {k: self.weights.get(k, 1) for k in scaled}
        total_weight = sum(weights.values())

        score = sum(scaled[k] * weights[k] for k in scaled) / total_weight

        return {
            "scaled": scaled,
            "score_global": round(score, 4),
            "weights": weights,
        }
