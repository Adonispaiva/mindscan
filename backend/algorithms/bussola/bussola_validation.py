# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\bussola\bussola_validation.py
# Última atualização: 2025-12-11T09:59:20.620871

from __future__ import annotations
from typing import Dict, Any


class BussolaValidation:
    """
    Valida coerência interna dos dados da Bússola.
    Regras:
    - Todos os eixos devem estar entre 0 e 5
    - Diferenças extremas entre eixos podem indicar ruído
    """

    def validate(self, dims: Dict[str, float]) -> Dict[str, Any]:

        problems = {}
        values = list(dims.values())

        # Regra 1 — faixa válida
        for key, val in dims.items():
            if val < 0 or val > 5:
                problems[key] = f"Valor fora da faixa permitida: {val}"

        # Regra 2 — incoerência (variação extrema)
        if max(values) - min(values) > 4.5:
            problems["incoerencia"] = "Variação extrema entre eixos detectada."

        return {
            "valid": len(problems) == 0,
            "issues": problems
        }
