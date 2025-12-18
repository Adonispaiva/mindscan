"""
Algoritmo DASS-21
Depressão, Ansiedade e Estresse.

Contrato público obrigatório:
- run_dass21(payload: dict) -> dict
"""

from typing import Dict, Any


DASS21_DIMENSIONS = ["depression", "anxiety", "stress"]


def _validate_payload(payload: Dict[str, Any]) -> Dict[str, float]:
    if not isinstance(payload, dict):
        raise ValueError("Payload do DASS21 deve ser um dicionário")

    scores = payload.get("scores")
    if not isinstance(scores, dict):
        raise ValueError("Payload DASS21 deve conter a chave 'scores'")

    normalized = {}
    for dim in DASS21_DIMENSIONS:
        value = scores.get(dim)
        if value is None:
            raise ValueError(f"Dimensão ausente no DASS21: {dim}")
        if not isinstance(value, (int, float)):
            raise ValueError(f"Valor inválido para {dim}: {value}")
        normalized[dim] = float(value)

    return normalized


def _severity(value: float) -> str:
    if value < 10:
        return "normal"
    if value < 20:
        return "moderado"
    return "severo"


def run_dass21(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executa o algoritmo DASS-21.

    Espera:
    {
        "scores": {
            "depression": float,
            "anxiety": float,
            "stress": float
        }
    }
    """

    scores = _validate_payload(payload)

    severity = {dim: _severity(value) for dim, value in scores.items()}

    return {
        "module": "DASS21",
        "scores": scores,
        "severity": severity,
        "summary": {
            "critical": any(v == "severo" for v in severity.values())
        },
    }
