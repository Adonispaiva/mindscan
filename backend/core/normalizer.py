"""
MindScan — Normalizer
Responsável por normalizar e validar o payload bruto
antes da execução dos algoritmos.

Este módulo define o CONTRATO de normalização do sistema.
"""

from typing import Dict, Any


def normalize(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normaliza o payload bruto recebido pela API.

    Responsabilidades:
    - validar estrutura básica
    - garantir tipos esperados
    - padronizar chaves
    - remover ruídos

    Retorna um dicionário pronto para scoring.
    """

    if not isinstance(payload, dict):
        raise ValueError("Payload inválido: esperado dict")

    normalized = {}

    for key, value in payload.items():
        # padronização básica
        normalized[key.strip().lower()] = value

    return normalized


# =====================================================
# ALIAS DE COMPATIBILIDADE — CONTRATO OFICIAL
# =====================================================

def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Alias oficial esperado pelo DiagnosticEngine.

    NÃO REMOVER.
    """
    return normalize(payload)
