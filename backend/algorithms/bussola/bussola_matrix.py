# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\bussola\bussola_matrix.py
# Última atualização: 2025-12-11T09:59:20.620871

from __future__ import annotations
from typing import Dict, Any
import numpy as np


class BussolaMatrix:
    """
    Cria uma matriz comportamental 4D:
        [Exploração, Estabilidade, Socialidade, Foco]
    Também calcula:
        - coesão
        - variância comportamental
    """

    def compute(self, dims: Dict[str, float]) -> Dict[str, Any]:

        arr = np.array([
            dims.get("exploracao", 0),
            dims.get("estabilidade", 0),
            dims.get("socialidade", 0),
            dims.get("foco", 0),
        ], dtype=float)

        cohesion = 1 / (1 + float(np.var(arr)))
        normalized = (arr - np.mean(arr)) / (np.std(arr) or 1)

        matrix = np.outer(normalized, normalized)

        return {
            "matrix": matrix.tolist(),
            "cohesion": cohesion,
            "normalized_vector": normalized.tolist(),
        }
