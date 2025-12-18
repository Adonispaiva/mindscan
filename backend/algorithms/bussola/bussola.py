"""
Algoritmo Bússola
Direcionamento comportamental e decisório.
Contrato:
- run_bussola(payload: dict) -> dict
"""

from typing import Dict, Any


def run_bussola(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Payload da Bússola deve ser um dicionário")

    return {
        "module": "BUSSOLA",
        "orientation": payload,
        "summary": {
            "keys_analyzed": list(payload.keys())
        },
    }
