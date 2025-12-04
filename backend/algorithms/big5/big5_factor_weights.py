"""
Big5 Factor Weights — Versão Ultra Superior
-------------------------------------------

Estabelece pesos estratégicos para cada dimensão Big Five
no contexto MindScan, influenciando:

- cálculos compostos
- previsões comportamentais
- análise de riscos
- interpretação contextual

Os pesos aqui servem como "força relativa" das dimensões.
"""

from typing import Dict


class Big5FactorWeights:
    def __init__(self):
        self.version = "2.0-ultra"

        # Pesos calibrados para análise global
        self.weights = {
            "abertura": 0.21,
            "conscienciosidade": 0.26,
            "extroversao": 0.19,
            "amabilidade": 0.17,
            "neuroticismo": 0.17,
        }

    def apply(self, dims: Dict[str, float]) -> Dict[str, float]:
        weighted = {}

        for dim, value in dims.items():
            w = self.weights.get(dim, 0)
            weighted[dim] = round((value * w) / 100, 5)

        return weighted
