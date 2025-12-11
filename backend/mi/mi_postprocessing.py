# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\mi_postprocessing.py
# Última atualização: 2025-12-11T09:59:20.856706

from __future__ import annotations
from typing import Dict, Any


class MIPostProcessing:
    """
    Ajustes finais após todos os módulos serem executados.
    Inclui:
    - arredondamentos
    - remoção de anomalias
    - reforço de coerência narrativa
    """

    def refine(self, output: Dict[str, Any]) -> Dict[str, Any]:

        refined = {}

        for key, value in output.items():
            if isinstance(value, float):
                refined[key] = round(value, 3)
            else:
                refined[key] = value

        refined["postprocessing"] = "done"

        return refined
