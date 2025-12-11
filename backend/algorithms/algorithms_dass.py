# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\algorithms_dass.py
# Última atualização: 2025-12-11T09:59:20.573935

from __future__ import annotations
import numpy as np
from typing import Dict, Any


class DASSAlgorithm:
    """
    Algoritmo avançado do DASS-21.

    Implementa:
    - normalização por média e desvio-padrão
    - composições fatoriais (Depressão, Ansiedade, Estresse)
    - classificação baseada em valores contínuos
    - índice integrado MindScan
    """

    FACTOR_MAP = {
        "depressao": ["d1", "d2", "d3", "d4", "d5", "d6", "d7"],
        "ansiedade": ["a1", "a2", "a3", "a4", "a5", "a6", "a7"],
        "estresse":  ["s1", "s2", "s3", "s4", "s5", "s6", "s7"]
    }

    CLASSIFICATION = {
        "depressao":  [4, 7, 11, 14],
        "ansiedade":  [3, 5, 7, 9],
        "estresse":   [7, 9, 12, 16]
    }

    LABELS = ["Normal", "Leve", "Moderado", "Severo", "Extremamente Severo"]

    def compute(self, responses: Dict[str, int]) -> Dict[str, Any]:

        # 1 — Soma por fator
        factor_scores = {}
        for factor, items in self.FACTOR_MAP.items():
            factor_scores[factor] = sum(responses.get(i, 0) for i in items)

        # 2 — Normalização (Z-score)
        values = list(factor_scores.values())
        mean = np.mean(values)
        std = np.std(values) or 1
        normalized = {f: (v - mean) / std for f, v in factor_scores.items()}

        # 3 — Classificação
        classification = {}
        for factor, score in factor_scores.items():
            thresholds = self.CLASSIFICATION[factor]
            idx = sum(score > t for t in thresholds)
            classification[factor] = self.LABELS[idx]

        # 4 — Índice integrado
        integrated_index = (
            normalized["depressao"] * 0.34 +
            normalized["ansiedade"] * 0.33 +
            normalized["estresse"]  * 0.33
        )

        return {
            "raw_scores": factor_scores,
            "normalized": normalized,
            "classification": classification,
            "integrated_index": integrated_index
        }
