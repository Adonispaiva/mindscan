"""
MindScan — Scoring Core
Responsável por calcular scores psicológicos e técnicos
a partir do payload normalizado.
"""

from typing import Dict, Any


def score(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função principal de scoring do sistema.

    Recebe um payload normalizado e retorna
    os scores calculados por dimensão.
    """

    if not isinstance(payload, dict):
        raise ValueError("Payload inválido para scoring")

    scores = {}

    for key, value in payload.items():
        # Regra básica de exemplo (mantém extensibilidade)
        try:
            scores[key] = float(value)
        except (TypeError, ValueError):
            scores[key] = 0.0

    return scores


# =====================================================
# ALIAS DE COMPATIBILIDADE — CONTRATO OFICIAL
# =====================================================

def calculate_scores(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Alias esperado pelo DiagnosticEngine.

    NÃO REMOVER.
    """
    return score(payload)
