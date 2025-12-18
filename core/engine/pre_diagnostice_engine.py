from typing import Dict, Any


class PreDiagnosticEngine:
    """
    Normaliza e prepara os dados antes do pipeline.
    """

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "subject_id": payload.get("subject_id"),
            "raw_scores": payload.get("raw_scores", {}),
            "metadata": payload.get("metadata", {})
        }
