# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\compliance\compliance_fairness.py
# Última atualização: 2025-12-11T09:59:20.872348

from __future__ import annotations
from typing import Dict, Any
import numpy as np


class ComplianceFairness:
    """
    Avalia equilíbrio e justiça dos resultados.
    Considera:
    - outliers extremos
    - distribuição irregular entre dimensões
    """

    def evaluate(self, scores: Dict[str, float]) -> Dict[str, Any]:

        issues = {}
        values = np.array(list(scores.values()), dtype=float)

        # Regra 1 — outlier extremo
        if np.max(values) - np.min(values) > 50:
            issues["outliers"] = (
                "Diferença extrema entre dimensões — possível distorção estatística."
            )

        # Regra 2 — variância muito baixa → perfil artificial
        if len(values) > 3 and np.var(values) < 1e-3:
            issues["variancia_baixa"] = (
                "Variância mínima detectada — respostas possivelmente artificiais."
            )

        return {
            "fair": len(issues) == 0,
            "issues": issues
        }
