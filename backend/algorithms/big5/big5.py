"""
Algoritmo BIG FIVE (OCEAN)
Responsável por calcular traços de personalidade a partir de escores brutos.

Contrato público obrigatório:
- run_big5(payload: dict) -> dict
"""

from typing import Dict, Any


BIG5_DIMENSIONS = [
    "openness",
    "conscientiousness",
    "extraversion",
    "agreeableness",
    "neuroticism",
]


def _validate_payload(payload: Dict[str, Any]) -> Dict[str, float]:
    if not isinstance(payload, dict):
        raise ValueError("Payload do BIG5 deve ser um dicionário")

    scores = payload.get("scores")
    if not isinstance(scores, dict):
        raise ValueError("Payload BIG5 deve conter a chave 'scores' como dict")

    normalized = {}
    for dim in BIG5_DIMENSIONS:
        value = scores.get(dim)
        if value is None:
            raise ValueError(f"Dimensão ausente no BIG5: {dim}")
        if not isinstance(value, (int, float)):
            raise ValueError(f"Valor inválido para {dim}: {value}")
        normalized[dim] = float(value)

    return normalized


def _classify(value: float) -> str:
    if value < 0.33:
        return "baixo"
    if value < 0.66:
        return "medio"
    return "alto"


def run_big5(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executa o algoritmo BIG5.

    Espera:
    {
        "scores": {
            "openness": float,
            "conscientiousness": float,
            "extraversion": float,
            "agreeableness": float,
            "neuroticism": float
        }
    }
    """

    scores = _validate_payload(payload)

    classifications = {
        dim: _classify(value) for dim, value in scores.items()
    }

    return {
        "module": "BIG5",
        "model": "OCEAN",
        "scores": scores,
        "classifications": classifications,
        "summary": {
            "dominant_trait": max(scores, key=scores.get),
            "balanced": all(0.33 <= v <= 0.66 for v in scores.values()),
        },
    }
