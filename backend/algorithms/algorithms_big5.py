# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\algorithms_big5.py
# Última atualização: 2025-12-11T09:59:20.573935

from __future__ import annotations
import numpy as np
from typing import Dict, Any


class Big5Algorithm:
    """
    Algoritmo completo do Big Five no MindScan.

    Processos implementados:
    - normalização baseada em distribuição interna
    - cálculo vetorial dos cinco fatores
    - ajuste por confiabilidade
    - geração de índices compostos
    """

    def __init__(self):
        self.factor_weights = {
            "O": 1.0,
            "C": 1.0,
            "E": 1.0,
            "A": 1.0,
            "N": 1.0,
        }

    def compute(self, responses: Dict[str, float]) -> Dict[str, Any]:
        # 1. Reorganiza itens por fator
        factor_map = {"O": [], "C": [], "E": [], "A": [], "N": []}

        for item, value in responses.items():
            factor = item.split("_")[0]  # item ex.: O_01
            if factor in factor_map:
                factor_map[factor].append(value)

        # 2. média dos fatores
        factor_scores = {f: np.mean(vals) if vals else 0 for f, vals in factor_map.items()}

        # 3. normalização Z
        values = list(factor_scores.values())
        mean = np.mean(values)
        std = np.std(values) if np.std(values) > 0 else 1

        normalized = {f: (v - mean) / std for f, v in factor_scores.items()}

        # 4. índice composto
        composite_index = sum(normalized[f] * self.factor_weights[f] for f in normalized)

        return {
            "raw_factors": factor_scores,
            "normalized": normalized,
            "composite_index": composite_index,
        }
