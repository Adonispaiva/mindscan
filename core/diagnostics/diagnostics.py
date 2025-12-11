# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\core\diagnostics\diagnostics.py
# Última atualização: 2025-12-11T09:59:27.558489

"""
MindScan — Diagnostics Module
Direção Técnica: Leo Vinci — Inovexa

Este módulo executa diagnósticos cognitivos e detecta
anomalias psicológicas nos resultados intermediários do CORE.

É utilizado pelo Engine, mas pode ser acionado manualmente
por módulos avançados ou pelo backend.
"""

from typing import Dict, Any
from core import corelog


# ------------------------------------------------------------
# Detectores de anomalia
# ------------------------------------------------------------

def detect_hyperactivation(metrics: Dict[str, float]) -> bool:
    """Detecta hiperativação emocional."""
    val = metrics.get("intensity", 0)
    return val >= 0.85


def detect_inconsistency(metrics: Dict[str, float]) -> bool:
    """Detecta inconsistência interna nos sinais."""
    return metrics.get("consistency", 1) <= 0.25


def detect_instability(metrics: Dict[str, float]) -> bool:
    """Detecta instabilidade emocional."""
    return metrics.get("stability", 1) <= 0.30


# ------------------------------------------------------------
# Diagnóstico Geral
# ------------------------------------------------------------

def run_diagnostics(algorithm_output: Dict[str, Any],
                    metric_output: Dict[str, float]) -> Dict[str, Any]:
    """
    Executa um diagnóstico completo da situação cognitiva.
    """

    corelog("Executando diagnósticos cognitivos...")

    if not metric_output or not isinstance(metric_output, dict):
        corelog("[WARN] Métricas inválidas, diagnóstico neutro.")
        return {"alerts": [], "severity": 0.0}

    alerts = []

    # Hiperativação
    if detect_hyperactivation(metric_output):
        alerts.append("Hiperativação emocional detectada.")

    # Inconsistência
    if detect_inconsistency(metric_output):
        alerts.append("Alta inconsistência interna.")

    # Instabilidade
    if detect_instability(metric_output):
        alerts.append("Instabilidade emocional relevante.")

    if not alerts:
        result = {"alerts": [], "severity": 0.0}
        corelog("Nenhuma anomalia identificada.")
        return result

    # Severidade simples: número de alertas / 3
    severity = min(1.0, len(alerts) / 3)

    result = {
        "alerts": alerts,
        "severity": severity,
    }

    corelog(f"Diagnóstico gerado: {result}")
    return result
