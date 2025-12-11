# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\core\algorithms\base_algorithm.py
# Última atualização: 2025-12-11T09:59:27.558489

"""
MindScan — Base Psychological Algorithm
Direção Técnica: Leo Vinci (Inovexa)

Este módulo implementa o algoritmo psicológico básico do MindScan.
Responsável por:
    - extrair sinais cognitivos de entrada
    - normalizar valores
    - gerar vetores psicológicos para o restante do CORE
"""

from typing import Dict, Any
from statistics import mean
from core import corelog


# ------------------------------------------------------------
# Auxiliares internos
# ------------------------------------------------------------

def _norm(x: float) -> float:
    """Normaliza valores entre 0.0 e 1.0."""
    if x is None or not isinstance(x, (int, float)):
        return 0.0
    x = float(x)
    return max(0.0, min(1.0, x))


def _extract_features(inp: Dict[str, Any]) -> Dict[str, float]:
    """
    Extrai sinais psicológicos básicos do input.
    Este método pode ser expandido no futuro.
    """

    features = {}

    # Exemplos simplificados de heurísticas iniciais:
    if "stress" in inp:
        features["stress"] = _norm(inp["stress"])

    if "focus" in inp:
        features["focus"] = _norm(inp["focus"])

    if "anxiety" in inp:
        features["anxiety"] = _norm(inp["anxiety"])

    if "energy" in inp:
        features["energy"] = _norm(inp["energy"])

    # Caso nada seja encontrado, fornecer sinal neutro
    if not features:
        features = {
            "neutral_signal": 0.5
        }

    return features


# ------------------------------------------------------------
# Algoritmo principal
# ------------------------------------------------------------

def run(user_input: Dict[str, Any]) -> Dict[str, float]:
    """
    Entrada → Sinais Cognitivos → Vetor Numérico
    """

    corelog("Executando BaseAlgorithm...")

    if not user_input or not isinstance(user_input, dict):
        corelog("[WARN] Entrada inválida, gerando vetor neutro.")
        return {"neutral_signal": 0.5}

    try:
        features = _extract_features(user_input)

        # Criar score bruto médio
        values = list(features.values())
        features["mean_activation"] = mean(values)

        corelog(f"Sinais extraídos: {features}")
        return features

    except Exception as e:
        corelog(f"[ERRO] BaseAlgorithm: {e}")
        return {"neutral_signal": 0.5}
