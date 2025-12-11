# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\bussola\bussola_risks.py
# Última atualização: 2025-12-11T09:59:20.620871

from __future__ import annotations
from typing import Dict, Any


class BussolaRisks:
    """
    Identifica riscos comportamentais com base nos eixos da Bússola.
    - Baixa estabilidade → risco operacional
    - Baixa socialidade → risco de isolamento
    - Exploração extrema → dispersão
    """

    def compute(self, dims: Dict[str, float]) -> Dict[str, Any]:

        risks = {}

        est = dims.get("estabilidade", 0)
        soc = dims.get("socialidade", 0)
        exp = dims.get("exploracao", 0)

        if est < 1.5:
            risks["operacional"] = "Risco de inconsistência e baixa previsibilidade."

        if soc < 1.5:
            risks["isolamento"] = "Risco de baixa colaboração e conexão em equipe."

        if exp > 4.0:
            risks["dispersao"] = "Risco de dispersão, foco reduzido e excesso de ideias."

        if not risks:
            risks["geral"] = "Nenhum risco significativo detectado."

        return risks
