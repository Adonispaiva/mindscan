"""
MindScan MI Utilities

Funções auxiliares para o MindScan MI (Persona, Compliance, Prompts).
"""

from typing import Dict


def normalize_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normaliza os resultados psicométricos para formato esperado pelo sistema.

    :param results: resultados brutos.
    :return: resultados normalizados.
    """
    return {key: value for key, value in results.items() if value is not None}
