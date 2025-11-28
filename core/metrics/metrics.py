"""
MindScan — Metrics Module
Direção Técnica: Leo Vinci

Fornece métricas internas utilizadas pelo sistema cognitivo:
    - consistência
    - intensidade emocional
    - estabilidade do padrão

As métricas operam sobre os resultados gerados pelos algoritmos psicológicos.
"""

from typing import Dict, Any
from statistics import mean
from core import corelog


# ------------------------------------------------------------
# Funções internas de cálculo de métricas
# ------------------------------------------------------------

def metric_consistency(values: Dict[str, float]) -> float:
    """Avalia a consistência geral das respostas."""
    if not values:
        return 0.0

    spread = max(values.values()) - min(values.values())
    return 1.0 - (spread / (max(values.values()) or 1))


def metric_intensity(values: Dict[str, float]) -> float:
    """Avalia intensidade emocional média."""
    if not values:
        return 0.0
    return mean(values.values())


def metric_stability(values: Dict[str, float]) -> float:
    """Avalia estabilidade (baixa variação interna)."""
    if not values:
        return 0.0

    vals = list(values.values())
    if len(vals) < 2:
        return 1.0

    return 1.0 - (abs(vals[-1] - vals[0]) / (max(vals) or 1))


# ------------------------------------------------------------
# Interface principal utilizada pelo Engine
# ------------------------------------------------------------

def evaluate(algorithm_output: Dict[str, Any]) -> Dict[str, float]:
    """
    Avalia métricas a partir da saída dos algoritmos psicológicos.

    O algoritmo deve retornar um dicionário numérico, ex:
        {
            "anxiety": 0.72,
            "focus": 0.83,
            "stress": 0.44
        }
    """

    corelog("Calculando métricas internas...")

    if not algorithm_output or not isinstance(algorithm_output, dict):
        corelog("[WARN] Saída do algoritmo inválida para métricas.")
        return {
            "consistency": 0.0,
            "intensity": 0.0,
            "stability": 0.0,
        }

    try:
        metrics = {
            "consistency": metric_consistency(algorithm_output),
            "intensity": metric_intensity(algorithm_output),
            "stability": metric_stability(algorithm_output),
        }

        corelog(f"Métricas calculadas: {metrics}")
        return metrics

    except Exception as e:
        corelog(f"[ERRO] Falha ao calcular métricas: {e}")
        return {
            "consistency": 0.0,
            "intensity": 0.0,
            "stability": 0.0,
        }
