"""
MindScan — Advanced Psychological Algorithm (Level 2)
Direção Técnica: Leo Vinci — Inovexa

Este módulo implementa heurísticas avançadas que operam
sobre os sinais cognitivos extraídos pelo BaseAlgorithm.

Objetivo:
    - detectar padrões compostos
    - avaliar relações entre sinais
    - identificar divergências estruturais
    - fornecer índices cognitivos mais profundos
"""

from typing import Dict, Any
from statistics import mean
from core import corelog


# ------------------------------------------------------------
# Auxiliares
# ------------------------------------------------------------

def _safe(val):
    """Normaliza e protege contra valores inválidos."""
    try:
        val = float(val)
        return max(0.0, min(1.0, val))
    except:
        return 0.0


# ------------------------------------------------------------
# Funções internas para padrões compostos
# ------------------------------------------------------------

def _coherence(signals: Dict[str, float]) -> float:
    """Coerência interna entre sinais psicológicos."""
    if len(signals) < 2:
        return 1.0
    vals = list(signals.values())
    amplitude = max(vals) - min(vals)
    return 1.0 - amplitude


def _divergence(signals: Dict[str, float]) -> float:
    """Divergência entre sinais (quanto diferem entre si)."""
    if len(signals) < 2:
        return 0.0
    vals = list(signals.values())
    amplitude = max(vals) - min(vals)
    return amplitude


def _hyperactivation(signals: Dict[str, float]) -> float:
    """
    Mede estado geral de hiperativação emocional:
    média dos valores acima de 0.75.
    """
    highs = [v for v in signals.values() if v > 0.75]
    if not highs:
        return 0.0
    return mean(highs)


# ------------------------------------------------------------
# Algoritmo principal (nível avançado)
# ------------------------------------------------------------

def run_advanced(signals: Dict[str, float]) -> Dict[str, float]:
    """
    Calcula índices psicológicos avançados.
    Requer os sinais gerados pelo BaseAlgorithm.
    """

    corelog("Executando AdvancedAlgorithm...")

    if not signals or not isinstance(signals, dict):
        corelog("[WARN] Sinais inválidos para algoritmo avançado.")
        return {
            "coherence": 0.5,
            "divergence": 0.5,
            "hyperactivation": 0.0
        }

    try:
        adv = {
            "coherence": _safe(_coherence(signals)),
            "divergence": _safe(_divergence(signals)),
            "hyperactivation": _safe(_hyperactivation(signals)),
        }

        corelog(f"Algoritmo avançado gerou: {adv}")
        return adv

    except Exception as e:
        corelog(f"[ERRO] AdvancedAlgorithm: {e}")
        return {
            "coherence": 0.5,
            "divergence": 0.5,
            "hyperactivation": 0.0
        }
