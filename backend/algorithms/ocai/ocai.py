"""
Algoritmo OCAI
Cultura Organizacional.
Contrato:
- run_ocai(payload: dict) -> dict
"""

from typing import Dict, Any


def run_ocai(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Payload do OCAI deve ser um dicionário")

    return {
        "module": "OCAI",
        "culture_profile": payload,
        "summary": {
            "dimensions": list(payload.keys())
        },
    }
