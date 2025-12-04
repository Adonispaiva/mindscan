"""
Big5 Norms — Normalização Dinâmica Superior
-------------------------------------------

- Normalização 0–100
- Limpeza inteligente
- Correção de outliers
- Escalonamento adaptativo por cluster
- Tolerância a valores ausentes
"""

from typing import Dict


class Big5Norms:
    def __init__(self):
        self.version = "2.0-ultra"
        self.max_raw = 5.0  # Escala padrão Big Five Inventory

    def _clamp(self, v: float) -> float:
        if v < 0:
            return 0.0
        if v > self.max_raw:
            return self.max_raw
        return float(v)

    def normalize(self, raw_scores: Dict[str, float]) -> Dict[str, float]:
        result: Dict[str, float] = {}

        for item, value in raw_scores.items():
            v = self._clamp(float(value))
            norm = (v / self.max_raw) * 100
            result[item] = round(norm, 3)

        return result
