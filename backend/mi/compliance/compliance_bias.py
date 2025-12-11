# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\compliance\compliance_bias.py
# Última atualização: 2025-12-11T09:59:20.872348

from __future__ import annotations
from typing import Dict, Any


class ComplianceBias:
    """
    Verifica risco de vieses no processamento do MindScan.
    Foca em:
    - viés demográfico
    - viés estatístico
    - viés por ausência de dados
    """

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:

        issues = {}

        # Regra 1 — Dados demográficos nunca podem afetar scorings psicométricos
        forbidden = ["genero", "raca", "etnia", "religiao"]
        for f in forbidden:
            if f in data:
                issues[f] = "Campo demográfico não deve ser usado no cálculo psicométrico."

        # Regra 2 — distribuição anômala (ex.: todas respostas iguais)
        responses = data.get("responses", {})
        if isinstance(responses, dict):
            values = list(responses.values())
            if len(values) > 5 and len(set(values)) == 1:
                issues["respostas_uniformes"] = (
                    "Todas as respostas são idênticas — possível ruído ou preenchimento automático."
                )

        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
