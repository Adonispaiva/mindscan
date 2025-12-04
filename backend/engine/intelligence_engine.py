"""
MindScan — Intelligence Engine (ULTRA)
Inovexa Software — Engenharia Ultra Superior

Responsável por:
- Detectar padrões psicométricos avançados
- Calcular estabilidade comportamental
- Avaliar densidade emocional
- Estimar consistência geral do perfil
"""

from typing import Dict, Any, List


class IntelligenceEngine:
    # ----------------------------------------------------
    # Métricas auxiliares
    # ----------------------------------------------------
    def _average(self, values: List[float]) -> float:
        return sum(values) / len(values) if values else 0.0

    def _stability(self, values: List[float]) -> float:
        if not values:
            return 0.0
        avg = self._average(values)
        variance = sum((v - avg) ** 2 for v in values) / len(values)
        return 1 - min(1, variance)

    def _emotional_density(self, scores: Dict[str, float]) -> float:
        keys = [k for k in scores if "dass" in k or "tei" in k]
        vals = [scores[k] for k in keys if isinstance(scores[k], (int, float))]
        return self._average(vals)

    # ----------------------------------------------------
    # Execução principal
    # ----------------------------------------------------
    def execute(self, block: Dict[str, Any]) -> Dict[str, Any]:
        raw = block.get("scores", {})
        num_vals = [v for v in raw.values() if isinstance(v, (int, float))]

        avg = self._average(num_vals)
        stab = self._stability(num_vals)
        density = self._emotional_density(raw)

        patterns = [
            {"pattern": "avg_global", "value": round(avg, 4)},
            {"pattern": "behavioral_stability", "value": round(stab, 4)},
            {"pattern": "emotional_density", "value": round(density, 4)},
        ]

        return {
            "intelligence": patterns,
            "pattern_count": len(patterns),
            "engine": "IntelligenceEngine(ULTRA)"
        }
