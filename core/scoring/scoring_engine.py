from __future__ import annotations

from typing import Any, Dict

from core.scoring.score_aggregator import ScoreAggregator


class ScoringEngine:
    """
    Engine de scoring do Core.
    Entrada esperada: dict de resultados do pipeline (por módulo).
    Saída: dict "scores" padronizado com:
      - score por módulo (mean + normalized + label)
      - score geral (overall)
    """

    def __init__(self) -> None:
        self._agg = ScoreAggregator()

    def run(self, results: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(results, dict):
            raise ValueError("results deve ser dict")

        modules = self._agg.aggregate_modules(results)
        overall = self._agg.overall(modules)

        modules_out: Dict[str, Any] = {}
        for name, m in modules.items():
            modules_out[name] = {
                "mean": m.mean,
                "min": m.min_value,
                "max": m.max_value,
                "normalized_0_1": m.normalized_0_1,
                "label": m.label,
                "values": m.raw_values,  # transparência para auditoria
            }

        return {
            "module": "scoring",
            "modules": modules_out,
            "overall": overall,
        }
