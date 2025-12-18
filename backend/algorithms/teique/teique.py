"""
Algoritmo TEIQue
Traço de Inteligência Emocional.
Contrato:
- run_teique(payload: dict) -> dict
"""

from typing import Dict, Any


def run_teique(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Payload do TEIQue deve ser um dicionário")

    return {
        "module": "TEIQUE",
        "emotional_traits": payload,
        "summary": {
            "traits_count": len(payload)
        },
    }
