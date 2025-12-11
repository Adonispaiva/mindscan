# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\hybrid_summary_builder.py
# Última atualização: 2025-12-11T09:59:20.809000

# ============================================================
# MindScan — Hybrid Summary Builder
# ============================================================
# Gera resumo executivo híbrido para:
# - Relatórios técnicos
# - Relatórios executivos
# - Relatórios premium
# ============================================================

from typing import Dict, Any, List


class HybridSummaryBuilder:

    def __init__(self):
        pass

    def build(self, insights: Dict[str, Any], narrative: List[str]) -> Dict[str, Any]:
        """
        Constrói resumo executivo com base em insights + narrativa estruturada.
        """

        top_points = list(insights.values())[:3]

        executive_summary = {
            "highlights": top_points,
            "narrative_overview": narrative[:2],
            "strategic_note": (
                "A leitura híbrida combina evidências múltiplas para revelar "
                "padrões dominantes e riscos potenciais."
            )
        }

        return executive_summary
