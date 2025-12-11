# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\core\reporting\report_generator.py
# Última atualização: 2025-12-11T09:59:27.558489

"""
MindScan — Reporting Module
Direção Técnica: Leo Vinci — Inovexa

Responsável por:
    - consolidar score, métricas, perfil e diagnóstico
    - produzir a estrutura final de relatório
    - fornecer base para futuras exportações (PDF/JSON)
"""

from typing import Dict, Any
from datetime import datetime
from core import corelog


def generate_report(
    input_data: Dict[str, Any],
    algorithms: Dict[str, float],
    metrics: Dict[str, float],
    score: float,
    profile: Dict[str, Any],
    diagnosis: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Gera um relatório psicológico consolidado.
    Este é o formato final consumido pelo sistema.
    """

    corelog("Gerando relatório cognitivo final...")

    try:
        report = {
            "timestamp": datetime.now().isoformat(),
            "input": input_data,
            "algorithms": algorithms,
            "metrics": metrics,
            "score": score,
            "profile": profile,
            "diagnosis": diagnosis,
            "summary": _build_summary(profile, diagnosis),
        }

        corelog("Relatório gerado com sucesso.")
        return report

    except Exception as e:
        corelog(f"[ERRO] Falha ao gerar relatório: {e}")
        return {"error": True, "details": str(e)}


# ----------------------------------------------------------------------
# Construção do Sumário Psicológico
# ----------------------------------------------------------------------

def _build_summary(profile: Dict[str, Any], diagnosis: Dict[str, Any]) -> str:
    """
    Cria uma narrativa psicológica curta:
    baseada no perfil e diagnóstico.
    """

    profile_name = profile.get("profile_name", "Desconhecido")
    desc = profile.get("description", "")
    severity = diagnosis.get("severity", 0.0)
    alerts = diagnosis.get("alerts", [])

    summary = f"Perfil: {profile_name}. {desc}"

    if severity > 0:
        summary += f" Severidade: {severity:.2f}. "
        if alerts:
            summary += "Alertas: " + "; ".join(alerts) + "."

    return summary
