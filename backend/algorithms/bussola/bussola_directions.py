# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\bussola\bussola_directions.py
# Última atualização: 2025-12-11T09:59:20.618842

from __future__ import annotations
from typing import Dict, Any
import numpy as np


class BussolaDirections:
    """
    Calcula direção, quadrante e angulação comportamental.
    """

    def compute(self, vector_2d: Dict[str, float]) -> Dict[str, Any]:

        x = vector_2d.get("x", 0)
        y = vector_2d.get("y", 0)

        angle = float(np.degrees(np.arctan2(y, x))) if not (x == 0 and y == 0) else 0
        magnitude = float(np.sqrt(x ** 2 + y ** 2))

        if angle >= 0 and angle < 90:
            quadrant = "Exploração Ativa"
        elif angle >= 90 and angle < 180:
            quadrant = "Estabilidade Social"
        elif angle < 0 and angle >= -90:
            quadrant = "Exploração Reservada"
        else:
            quadrant = "Estabilidade Estrutural"

        return {
            "angle": angle,
            "quadrant": quadrant,
            "magnitude": magnitude,
        }
