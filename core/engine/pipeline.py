from typing import Dict, Any

from core.algorithms.big5 import run_big5
from core.algorithms.dass21 import run_dass21
from core.algorithms.bussola import run_bussola
from core.algorithms.esquemas import run_esquemas
from core.algorithms.ocai import run_ocai
from core.algorithms.performance import run_performance
from core.algorithms.teique import run_teique
from core.algorithms.cruzamentos import run_cruzamentos


class DiagnosticPipeline:
    """
    Executa todos os algoritmos e consolida respostas.
    """

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        scores = payload["raw_scores"]

        results = {
            "big5": run_big5(scores),
            "dass21": run_dass21(scores),
            "bussola": run_bussola(scores),
            "esquemas": run_esquemas(scores),
            "ocai": run_ocai(scores),
            "performance": run_performance(scores),
            "teique": run_teique(scores),
        }

        results["cruzamentos"] = run_cruzamentos(results)
        return results
