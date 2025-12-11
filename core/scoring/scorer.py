# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\core\scoring\scorer.py
# Última atualização: 2025-12-11T09:59:27.558489

"""
MindScan — Scoring Module
Direção Técnica: Leo Vinci

Converte métricas internas em uma pontuação psicológica unificada.
A pontuação alimenta o módulo de perfis.
"""

from typing import Dict, Any
from core import corelog


# ------------------------------------------------------------
# Configuração de pesos utilizados no cálculo do score
# ------------------------------------------------------------

class ScoreWeights:
    """Pesos internos para o cálculo do score global."""
    consistency: float = 0.35
    intensity: float = 0.40
    stability: float = 0.25


# ------------------------------------------------------------
# Funções internas de cálculo
# ------------------------------------------------------------

def _safe(val: float) -> float:
    """Garante que valores inválidos não quebrem o cálculo."""
    if val is None or not isinstance(val, (int, float)):
        return 0.0
    return max(0.0, min(1.0, float(val)))


# ------------------------------------------------------------
# Interface principal utilizada pelo Engine
# ------------------------------------------------------------

def compute_score(algorithm_output: Dict[str, Any],
                  metric_output: Dict[str, Any]) -> float:
    """
    Produz o score psicológico principal do MindScan.
    Score é normalizado entre 0.0 e 1.0.
    """

    corelog("Calculando score psicológico...")

    if not metric_output or not isinstance(metric_output, dict):
        corelog("[WARN] Métricas inválidas, score = 0.0")
        return 0.0

    try:
        c = _safe(metric_output.get("consistency"))
        i = _safe(metric_output.get("intensity"))
        s = _safe(metric_output.get("stability"))

        score = (
            c * ScoreWeights.consistency +
            i * ScoreWeights.intensity +
            s * ScoreWeights.stability
        )

        # Normalização final
        score = _safe(score)

        corelog(f"Score calculado: {score:.4f}")
        return score

    except Exception as e:
        corelog(f"[ERRO] Score: {e}")
        return 0.0
