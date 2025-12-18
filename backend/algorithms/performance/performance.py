"""
Algoritmo de Performance
Indicadores de desempenho.
Contrato:
- run_performance(payload: dict) -> dict
"""

from typing import Dict, Any


def run_performance(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Payload de Performance deve ser um dicionário")

    return {
        "module": "PERFORMANCE",
        "metrics": payload,
        "summary": {
            "metrics_count": len(payload)
        },
    }
