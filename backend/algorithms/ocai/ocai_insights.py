# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\ocai\ocai_insights.py
# Última atualização: 2025-12-11T09:59:20.698978

from __future__ import annotations
from typing import Dict, Any


class OCAIInsights:
    """
    Gera insights culturais com base no modelo OCAI.
    """

    def generate(self, normalized: Dict[str, float]) -> Dict[str, str]:

        insights = {}

        cla = normalized.get("cla", 0)
        ado = normalized.get("adocracia", 0)
        mer = normalized.get("mercado", 0)
        hie = normalized.get("hierarquia", 0)

        # Cultura predominante
        max_val = max(normalized.values())
        dominante = [k for k, v in normalized.items() if v == max_val][0]

        insights["cultura_dominante"] = f"A cultura predominante é: {dominante.upper()}."

        # Tendências específicas
        if ado > 30:
            insights["inovacao"] = "Forte tendência à inovação e experimentação."
        if mer > 30:
            insights["competitividade"] = "Ambiente competitivo, orientado a resultados."
        if cla > 30:
            insights["colaboracao"] = "Cultura colaborativa com foco em pessoas."
        if hie > 30:
            insights["estrutura"] = "Cultura estruturada, valorizando regras e processos."

        return insights
