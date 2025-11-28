"""
MindScan — Profiler
Direção Técnica: Leo Vinci

Gera um perfil psicológico interpretável a partir:
    - score unificado
    - métricas internas
    - padrões gerados pelos algoritmos psicológicos
"""

from typing import Dict, Any
from core import corelog


# ------------------------------------------------------------
# Tabela inicial de perfis (versão simplificada)
# ------------------------------------------------------------

PROFILE_TABLE = [
    (0.00, 0.20, "Extrema Instabilidade", "Alto risco psicológico, forte dispersão emocional."),
    (0.20, 0.40, "Instabilidade", "Oscilações internas relevantes, atenção necessária."),
    (0.40, 0.60, "Neutro", "Estado emocional balanceado, sem sinais fortes."),
    (0.60, 0.80, "Estabilidade", "Boa regulação emocional, foco e coerência presentes."),
    (0.80, 1.00, "Alta Estabilidade", "Consistência excepcional, alta clareza mental."),
]


# ------------------------------------------------------------
# Função principal utilizada pelo Engine
# ------------------------------------------------------------

def generate_profile(score: float, metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converte o score num perfil psicológico interpretável.
    """

    corelog("Gerando perfil psicológico...")

    if not isinstance(score, (int, float)):
        corelog("[WARN] Score inválido, perfil neutro.")
        return _neutral_profile()

    score = float(max(0.0, min(1.0, score)))

    # Seleção do perfil adequado na tabela
    selected = None
    for low, high, name, desc in PROFILE_TABLE:
        if low <= score <= high:
            selected = (name, desc)
            break

    if not selected:
        selected = ("Indeterminado", "Não foi possível determinar um perfil.")

    profile_name, description = selected

    profile_data = {
        "profile_name": profile_name,
        "description": description,
        "score": score,
        "metrics": metrics,
    }

    corelog(f"Perfil gerado: {profile_name} (score={score:.4f})")
    return profile_data


# ------------------------------------------------------------
# Perfil neutro (fallback)
# ------------------------------------------------------------

def _neutral_profile() -> Dict[str, Any]:
    return {
        "profile_name": "Neutro",
        "description": "Estado emocional não identificado.",
        "score": 0.5,
        "metrics": {},
    }
