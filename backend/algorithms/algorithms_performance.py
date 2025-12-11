# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\algorithms_performance.py
# Última atualização: 2025-12-11T09:59:20.573935

from __future__ import annotations
import numpy as np
from typing import Dict, Any


class PerformanceAlgorithm:
    """
    Algoritmo de performance longitudinal.
    - análise de tendência
    - média móvel
    - índice de estabilidade
    """

    def compute(self, records: Dict[str, float]) -> Dict[str, Any]:

        # 1 — ordenação cronológica (semestres, períodos etc.)
        values = [v for _, v in sorted(records.items())]

        # 2 — tendência (coeficiente angular)
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0] if len(values) > 1 else 0

        # 3 — média móvel
        moving_avg = np.mean(values[-3:]) if len(values) >= 3 else np.mean(values)

        # 4 — índice global
        global_index = (moving_avg * 0.6) + (slope * 0.4)

        return {
            "trend": slope,
            "moving_avg": moving_avg,
            "global_index": global_index
        }
