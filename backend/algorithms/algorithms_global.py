# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\algorithms_global.py
# Última atualização: 2025-12-11T09:59:20.573935

from __future__ import_annotations
import numpy as np
from typing import Dict, Any


class GlobalMindScanAlgorithm:
    """
    Algoritmo global de integração dos módulos MindScan.
    Integra:
    - Big Five
    - DASS
    - TEIQue
    - Esquemas
    - Bússola
    - Performance

    Produz:
    - índice composto global
    - mapa de coerências
    - pesos dinâmicos
    """

    WEIGHTS = {
        "big5": 0.22,
        "dass": 0.18,
        "teique": 0.20,
        "esquemas": 0.15,
        "bussola": 0.15,
        "performance": 0.10,
    }

    def compute(self, modules: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:

        scores = {}

        # Extração de índices
        try: scores["big5"] = modules["big5"]["composite_index"]
        except: scores["big5"] = 0

        try: scores["dass"] = modules["dass"]["integrated_index"] * -1
        except: scores["dass"] = 0

        try: scores["teique"] = modules["teique"]["weighted_index"]
        except: scores["teique"] = 0

        try: scores["esquemas"] = modules["esquemas"]["vulnerability"] * -1
        except: scores["esquemas"] = 0

        try: scores["bussola"] = modules["bussola"]["vector"]["magnitude"]
        except: scores["bussola"] = 0

        try: scores["performance"] = modules["performance"]["global_index"]
        except: scores["performance"] = 0

        # índice global ponderado
        global_index = sum(scores[m] * self.WEIGHTS[m] for m in scores)

        # coerência (variância inversa)
        variance = np.var(list(scores.values()))
        coherence = 1 / (1 + variance)

        return {
            "module_scores": scores,
            "global_index": global_index,
            "coherence": coherence
        }
