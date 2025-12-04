"""
MindScan — Normalization Engine (ULTRA)
Inovexa Software — Engenharia Ultra Superior

Função:
- Normalização segura e coerente de valores psicométricos.
- Suporte a tolerância suave (soft clamp).
- Detecção de outliers.
"""

from typing import Dict, Any


class NormalizationEngine:
    def _to_float(self, value: Any) -> float:
        try:
            return float(value)
        except Exception:
            return 0.0

    def _clamp(self, v: float) -> float:
        return max(0.0, min(1.0, v))

    def _soft_clamp(self, v: float) -> float:
        if v < 0.0:
            return v + 0.1
        if v > 1.0:
            return v - 0.1
        return v

    def _is_outlier(self, v: float) -> bool:
        return v < -1 or v > 2

    def execute(self, block: Dict[str, Any]) -> Dict[str, Any]:
        normalized = {}
        outliers = []

        for key, value in block.items():
            if isinstance(value, (int, float)):
                vf = self._to_float(value)
                if self._is_outlier(vf):
                    outliers.append(key)
                vf = self._soft_clamp(self._clamp(vf))
                normalized[key] = vf
            else:
                normalized[key] = value

        normalized["_normalization"] = {
            "engine": "NormalizationEngine(ULTRA)",
            "outliers": outliers
        }

        return normalized
