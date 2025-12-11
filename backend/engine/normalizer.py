# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\normalizer.py
# Última atualização: 2025-12-11T09:59:20.820000

"""
MindScan — Universal Normalizer (ULTRA)
Inovexa Software — Engenharia Ultra Superior

Camada utilitária de suporte:
- Normalização linear
- Clamp rígido e suave
- Conversão segura para float
"""

from typing import Any


class Normalizer:
    def to_float(self, value: Any) -> float:
        try:
            return float(value)
        except Exception:
            return 0.0

    def clamp(self, v: float, lo=0.0, hi=1.0) -> float:
        return max(lo, min(hi, v))

    def smooth(self, v: float) -> float:
        if v < 0.0:
            return v + 0.05
        if v > 1.0:
            return v - 0.05
        return v

    def normalize(self, value: Any, mode="default") -> float:
        v = self.to_float(value)
        if mode == "smooth":
            return self.smooth(self.clamp(v))
        return self.clamp(v)
