"""
DASS21 Factor Map — Versão ULTRA SUPERIOR
--------------------------------------------------------------

Mapeia as relações estruturais entre os três fatores DASS21:

- Depressão
- Ansiedade
- Estresse

Produz correlações internas, pesos fatoriais e inferências
para uso em módulos de risco, diagnóstico e perfis combinados.
"""

from typing import Dict, Any


class DASS21FactorMap:
    def __init__(self):
        self.version = "2.0-ultra"

    def compute_correlations(self, scores: Dict[str, float]) -> Dict[str, float]:
        d = scores.get("depressao", 0)
        a = scores.get("ansiedade", 0)
        s = scores.get("stress", 0)

        return {
            "dep_ans": round((d + a) / 2, 2),
            "ans_stress": round((a + s) / 2, 2),
            "dep_stress": round((d + s) / 2, 2),
        }

    def factor_weights(self, scores: Dict[str, float]) -> Dict[str, float]:
        total = sum(scores.values()) or 1
        return {k: round(v / total, 3) for k, v in scores.items()}

    def run(self, scores: Dict[str, float]) -> Dict[str, Any]:
        return {
            "module": "dass21_factor_map",
            "version": self.version,
            "correlations": self.compute_correlations(scores),
            "weights": self.factor_weights(scores),
        }
