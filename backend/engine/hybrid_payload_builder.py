# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\hybrid_payload_builder.py
# Última atualização: 2025-12-11T09:59:20.792728

# ============================================================
# MindScan — Hybrid Payload Builder
# ============================================================
# Consolida:
# - narrative
# - summary
# - scores
# - persona
# - insights
# - normalized blocks
#
# Finalidade:
# → Entregar um payload definitivo ao ReportService
#   compatível com os 4 templates oficiais.
# ============================================================

from typing import Dict, Any, List


class HybridPayloadBuilder:

    def __init__(self):
        pass

    def assemble(
        self,
        engine_used: str,
        normalized: Dict[str, Any],
        insights: Dict[str, Any],
        narrative: List[str],
        summary: Dict[str, Any],
        scores: Dict[str, Any],
        persona: Dict[str, Any]
    ) -> Dict[str, Any]:

        return {
            "engine_used": engine_used,
            "persona": persona,
            "normalized": normalized,
            "insights": insights,
            "narrative": narrative,
            "summary": summary,
            "scores": scores,
            "metadata": {
                "payload_version": "hybrid.1.0"
            }
        }
