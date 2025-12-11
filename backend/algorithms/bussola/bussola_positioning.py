# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\bussola\bussola_positioning.py
# Última atualização: 2025-12-11T09:59:20.620871

from __future__ import annotations
from typing import Dict, Any


class BussolaPositioning:
    """
    Determina o posicionamento final do indivíduo na Bússola.
    Combina:
    - coordenadas
    - direção
    - matriz comportamental
    Produz:
    - estilo predominante
    - estilo complementar
    """

    def compute(self, data: Dict[str, Any]) -> Dict[str, Any]:

        angle = data["directions"]["angle"]
        magnitude = data["directions"]["magnitude"]

        # Estilo predominante baseado no ângulo
        if angle >= 0 and angle < 90:
            primary = "Explorador"
        elif angle >= 90 and angle < 180:
            primary = "Conector Social"
        elif angle < 0 and angle >= -90:
            primary = "Analista Reservado"
        else:
            primary = "Executor Estrutural"

        # Estilo complementar baseado na intensidade
        if magnitude > 3.0:
            secondary = "Alta Intensidade"
        elif magnitude > 1.5:
            secondary = "Equilibrado"
        else:
            secondary = "Low-profile"

        return {
            "primary_style": primary,
            "secondary_style": secondary,
            "position_score": round(magnitude, 3)
        }
