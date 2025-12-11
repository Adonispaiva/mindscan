# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\bussola\bussola_crosslinks.py
# Última atualização: 2025-12-11T09:59:20.617855

from __future__ import annotations
from typing import Dict, Any


class BussolaCrossLinks:
    """
    Cria cruzamentos entre a Bússola e outros módulos:
        - Big Five (Exploration ↔ Abertura)
        - TEIQue (Estabilidade ↔ Autocontrole)
        - DASS (Estabilidade ↔ Estresse)
    """

    def compute(self, modules: Dict[str, Any]) -> Dict[str, Any]:

        cross = {}

        # Bússola
        bx = modules["bussola"]["coordinates"]["vector_2d"][0]  # exploração
        by = modules["bussola"]["coordinates"]["vector_2d"][1]  # estabilidade

        # Big Five — O
        O = modules["big5"]["normalized"].get("O", 0)

        # TEIQue — autocontrole
        AC = modules["teique"]["z_scores"].get("autocontrole", 0)

        # DASS — estresse
        stress = modules["dass"]["normalized"].get("estresse", 0)

        cross["criatividade_inovacao"] = round((bx * 0.6) + (O * 0.4), 3)
        cross["resiliencia_operacional"] = round((by * 0.7) + (AC * 0.3), 3)
        cross["risco_de_bloqueio"] = round(stress * 0.5 - by * 0.2, 3)

        return cross
