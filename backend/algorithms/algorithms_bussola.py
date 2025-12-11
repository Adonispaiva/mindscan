# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\algorithms_bussola.py
# Última atualização: 2025-12-11T09:59:20.573935

from __future__ import annotations
import numpy as np
from typing import Dict, Any


class BussolaAlgorithm:
    """
    Algoritmo completo da Bússola de Talentos.
    Processos:
    - vetorização dimensional
    - normalização angular
    - cálculo de quadrante
    - índice interno MindScan
    """

    def compute(self, scores: Dict[str, float]) -> Dict[str, Any]:

        # 1. Vetorização básica: (Exploração, Estabilidade)
        x = scores.get("exploracao", 0)
        y = scores.get("estabilidade", 0)

        # 2. magnitude do vetor
        magnitude = np.sqrt(x**2 + y**2)

        # 3. ângulo
        angle = np.degrees(np.arctan2(y, x))

        # 4. quadrante
        if angle >= 0 and angle < 90:
            quad = "Alto-Exploração"
        elif angle >= 90 and angle < 180:
            quad = "Estabilidade-Social"
        elif angle >= -180 and angle < -90:
            quad = "Baixa-Exploração"
        else:
            quad = "Estabilidade-Reservada"

        return {
            "vector": {"x": x, "y": y, "magnitude": magnitude, "angle": angle},
            "quadrant": quad,
        }
