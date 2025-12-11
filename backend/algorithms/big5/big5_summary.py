# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\big5\big5_summary.py
# Última atualização: 2025-12-11T09:59:20.609842

"""
Big5 Summary — Versão Ultra Superior
------------------------------------

Gera o RESUMO EXECUTIVO da personalidade com:
- fator dominante
- padrões de equilíbrio
- riscos e forças integradas
- leitura global da personalidade
- insights estratégicos para relatório master
"""

from typing import Dict, Any


class Big5Summary:
    def __init__(self):
        self.version = "2.0-ultra"

    def build(
        self,
        dims: Dict[str, float],
        strengths: Dict[str, str],
        risks: Dict[str, str],
        needs: Dict[str, str],
        enrichment: Dict[str, Any],
    ) -> Dict[str, Any]:

        if not dims:
            return {"summary": "Dados insuficientes para análise."}

        top = max(dims, key=dims.get)
        lowest = min(dims, key=dims.get)

        balance_range = max(dims.values()) - min(dims.values())

        if balance_range <= 25:
            balance = "perfil equilibrado"
        elif balance_range <= 45:
            balance = "perfil moderadamente heterogêneo"
        else:
            balance = "perfil altamente assimétrico"

        return {
            "module": "Big5",
            "version": self.version,
            "top_dimension": top,
            "lower_dimension": lowest,
            "balance_type": balance,
            "strengths": strengths,
            "risks": risks,
            "needs": needs,
            "enrichment": enrichment,
        }
