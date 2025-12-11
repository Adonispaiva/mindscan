# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\bussola\bussola_recommendations.py
# Última atualização: 2025-12-11T09:59:20.620871

from __future__ import annotations
from typing import Dict, Any


class BussolaRecommendations:
    """
    Gera recomendações de desenvolvimento baseadas nos eixos da Bússola:
    - Exploração
    - Estabilidade
    - Socialidade
    - Foco
    """

    def compute(self, dims: Dict[str, float]) -> Dict[str, Any]:

        recs = {}

        if dims.get("exploracao", 0) < 2:
            recs["exploracao"] = "Estimular curiosidade, inovação e experimentação."

        if dims.get("estabilidade", 0) < 2:
            recs["estabilidade"] = "Trabalhar rotinas, organização e previsibilidade."

        if dims.get("socialidade", 0) < 2:
            recs["socialidade"] = "Fortalecer comunicação e interação em grupo."

        if dims.get("foco", 0) < 2:
            recs["foco"] = "Refinar priorização, concentração e disciplina executiva."

        if not recs:
            recs["geral"] = "Perfil robusto: recomenda-se buscar desafios avançados."

        return recs
