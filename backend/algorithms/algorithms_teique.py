# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\algorithms_teique.py
# Última atualização: 2025-12-11T09:59:20.573935

from __future__ import annotations
import numpy as np
from typing import Dict, Any


class TEIQueAlgorithm:
    """
    Algoritmo avançado TEIQue.
    Similar ao ScoringTEIQue, porém a nível de engine:
    - normalização estatística
    - pesos dinâmicos
    - índice emocional global
    """

    DEFAULT_WEIGHTS = {
        "bem_estar": 0.28,
        "autocontrole": 0.22,
        "emocionalidade": 0.26,
        "sociabilidade": 0.24
    }

    def compute(self, factors: Dict[str, float]) -> Dict[str, Any]:

        values = list(factors.values())
        mean = np.mean(values)
        std = np.std(values) or 1

        z_scores = {f: (v - mean) / std for f, v in factors.items()}

        weighted_index = sum(
            z_scores[f] * self.DEFAULT_WEIGHTS.get(f, 0.25)
            for f in z_scores
        )

        return {
            "raw_factors": factors,
            "z_scores": z_scores,
            "weighted_index": weighted_index
        }
