# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\algorithms_esquemas.py
# Última atualização: 2025-12-11T09:59:20.573935

from __future__ import annotations
import numpy as np
from typing import Dict, Any


class EsquemasAlgorithm:
    """
    Algoritmo dos Esquemas Adaptativos (Young).
    Inclui:
    - soma por domínio
    - cálculo de severidade relativa
    - índice de vulnerabilidade emocional
    """

    DOMAIN_MAP = {
        "desconfianca": ["d1", "d2", "d3", "d4", "d5"],
        "abandono":     ["a1", "a2", "a3", "a4", "a5"],
        "dependencia":  ["dep1", "dep2", "dep3", "dep4"],
        "privacao":     ["p1", "p2", "p3", "p4"],
        "autocritic":   ["ac1", "ac2", "ac3", "ac4"],
    }

    def compute(self, responses: Dict[str, int]) -> Dict[str, Any]:

        # 1 — Soma por domínio
        domain_scores = {
            domain: sum(responses.get(i, 0) for i in items)
            for domain, items in self.DOMAIN_MAP.items()
        }

        # 2 — Normalização (z-score)
        values = list(domain_scores.values())
        mean = np.mean(values)
        std = np.std(values) or 1
        severity_index = {d: (v - mean) / std for d, v in domain_scores.items()}

        # 3 — índice global de vulnerabilidade
        vulnerability_index = np.mean(list(severity_index.values()))

        return {
            "domain_scores": domain_scores,
            "severity": severity_index,
            "vulnerability": vulnerability_index
        }
