from backend.core.normalizer import normalize_payload
from backend.core.scoring import calculate_scores
from backend.algorithms.big5 import run as run_big5
from backend.algorithms.dass21 import run as run_dass21
from backend.algorithms.bussola import run as run_bussola
from backend.algorithms.ocai import run as run_ocai
from backend.algorithms.performance import run as run_performance
from backend.algorithms.teique import run as run_teique
from backend.algorithms.esquemas import run as run_esquemas
from backend.algorithms.matcher import run as run_matcher
from backend.algorithms.cruzamentos import run as run_cruzamentos


class DiagnosticEngine:
    def run(self, payload: dict) -> dict:
        payload = normalize_payload(payload)

        results = {}

        results["big5"] = run_big5(payload)
        results["dass21"] = run_dass21(payload)
        results["bussola"] = run_bussola(payload)
        results["ocai"] = run_ocai(payload)
        results["performance"] = run_performance(payload)
        results["teique"] = run_teique(payload)
        results["esquemas"] = run_esquemas(payload)
        results["matcher"] = run_matcher(payload)
        results["cruzamentos"] = run_cruzamentos(payload)

        results["scores"] = calculate_scores(results)

        return results
