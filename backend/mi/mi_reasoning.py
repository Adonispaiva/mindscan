# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\mi_reasoning.py
# Última atualização: 2025-12-11T09:59:20.872348

from __future__ import annotations
from typing import Dict, Any, List


class MIReasoning:
    """
    Realiza raciocínio inferencial baseado no conjunto completo de módulos.
    """

    def infer(self, modules: Dict[str, Any]) -> Dict[str, Any]:

        reasoning = {}

        if "bussola" in modules:
            buss = modules["bussola"]
            mag = buss.get("directions", {}).get("magnitude", 0)
            if mag > 3:
                reasoning["estilo"] = "Padrão comportamental intenso e direcionado."
            else:
                reasoning["estilo"] = "Padrão equilibrado ou moderado."

        if "big5" in modules:
            O = modules["big5"]["normalized"].get("O", 0)
            reasoning["criatividade"] = (
                "Alta criatividade." if O > 60 else "Criatividade moderada."
            )

        return reasoning
