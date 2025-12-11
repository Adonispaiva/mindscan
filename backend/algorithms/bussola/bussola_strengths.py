# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\bussola\bussola_strengths.py
# Última atualização: 2025-12-11T09:59:20.620871

from __future__ import annotations
from typing import Dict, Any


class BussolaStrengths:
    """
    Identifica forças naturais com base nos eixos principais.
    """

    def compute(self, dims: Dict[str, float]) -> Dict[str, Any]:

        strengths = {}

        if dims.get("exploracao", 0) > 3:
            strengths["criatividade"] = "Alta capacidade de inovação e visão ampla."

        if dims.get("estabilidade", 0) > 3:
            strengths["organizacao"] = "Consistência, previsibilidade e disciplina."

        if dims.get("socialidade", 0) > 3:
            strengths["colaboracao"] = "Facilidade em criar conexões e trabalhar em equipe."

        if dims.get("foco", 0) > 3:
            strengths["execucao"] = "Alta capacidade de execução e finalização de tarefas."

        if not strengths:
            strengths["geral"] = "Pontos fortes equilibrados, sem destaque predominante."

        return strengths
