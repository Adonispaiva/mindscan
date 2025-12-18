from typing import Dict, Any


class ValidationEngine:
    """
    Validação mínima do payload.
    """

    def validate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if "raw_scores" not in payload:
            raise ValueError("raw_scores ausente no payload")
        return payload
