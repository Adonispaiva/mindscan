# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\bussola\bussola_coordinates.py
# Última atualização: 2025-12-11T09:59:20.616784

from __future__ import annotations
from typing import Dict, Any
import numpy as np


class BussolaCoordinates:
    """
    Converte dimensões psicométricas da Bússola em coordenadas 2D e 4D.
    Dimensões típicas:
        - exploração
        - estabilidade
        - socialidade
        - foco
    """

    def compute(self, dims: Dict[str, float]) -> Dict[str, Any]:
        x = dims.get("exploracao", 0)
        y = dims.get("estabilidade", 0)
        s = dims.get("socialidade", 0)
        f = dims.get("foco", 0)

        vector_2d = np.array([x, y], dtype=float)
        vector_4d = np.array([x, y, s, f], dtype=float)

        magnitude_2d = float(np.linalg.norm(vector_2d))
        magnitude_4d = float(np.linalg.norm(vector_4d))

        return {
            "vector_2d": vector_2d.tolist(),
            "vector_4d": vector_4d.tolist(),
            "magnitude_2d": magnitude_2d,
            "magnitude_4d": magnitude_4d,
        }
