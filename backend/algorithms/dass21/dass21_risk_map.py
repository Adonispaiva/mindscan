# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\dass21\dass21_risk_map.py
# Última atualização: 2025-12-11T09:59:20.667799

"""
DASS21 Risk Map — Versão ULTRA SUPERIOR
--------------------------------------------------------------

Concentra todos os fatores de risco derivados do DASS21:

- risco emocional total
- risco de retração
- risco de hiperativação
- risco de burnout
"""

from typing import Dict, Any


class DASS21RiskMap:
    def __init__(self):
        self.version = "2.0-ultra"

    def risk_total(self, d: float, a: float, s: float) -> float:
        return round((d * 0.4 + a * 0.3 + s * 0.3), 2)

    def define_level(self, value: float) -> str:
        if value < 30:
            return "baixo"
        if value < 60:
            return "moderado"
        return "alto"

    def run(self, scores: Dict[str, float]) -> Dict[str, Any]:
        d = scores.get("depressao", 0)
        a = scores.get("ansiedade", 0)
        s = scores.get("stress", 0)

        total = self.risk_total(d, a, s)

        return {
            "module": "dass21_risk_map",
            "version": self.version,
            "risk_total": total,
            "risk_level": self.define_level(total),
            "subrisks": {
                "retraimento": round(d * 0.6, 2),
                "hiperativacao": round(a * 0.7, 2),
                "sobrecarga": round(s * 0.75, 2),
            },
        }
