# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\algorithms_ocai.py
# Última atualização: 2025-12-11T09:59:20.573935

from __future__ import annotations
import numpy as np
from typing import Dict, Any


class OCAIAlgorithm:
    """
    Algoritmo do modelo OCAI (Cameron & Quinn).

    Cálculos implementados:
    - normalização percentual dos 6 blocos
    - distribuição por cultura:
        * Clã
        * Adocracia
        * Mercado
        * Hierarquia
    - índice de alinhamento cultural
    """

    FACTORS = ["cla", "adocracia", "mercado", "hierarquia"]

    def compute(self, responses: Dict[str, int]) -> Dict[str, Any]:

        total = sum(responses.values()) or 1
        normalized = {k: (v / total) * 100 for k, v in responses.items()}

        # índice de polarização (diferença entre maior e menor)
        values = list(normalized.values())
        polarization = max(values) - min(values)

        # índice de equilíbrio cultural
        balance = 1 - (polarization / 100)

        return {
            "normalized": normalized,
            "polarization": round(polarization, 2),
            "balance_index": round(balance, 3),
        }
