# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\hybrid_score_engine.py
# Última atualização: 2025-12-11T09:59:20.792728

# ============================================================
# MindScan — Hybrid Score Engine
# ============================================================
# Cria pontuações híbridas para:
# - Indicadores globais MindScan
# - Riscos agregados
# - Forças dominantes
# ============================================================

from typing import Dict, Any


class HybridScoreEngine:

    def __init__(self):
        pass

    def compute_scores(self, normalized: Dict[str, Any], insights: Dict[str, Any]) -> Dict[str, Any]:
        """
        Integra múltiplos blocos para gerar scores híbridos.
        """

        try:
            big5 = normalized.get("big5", {})
            o_score = big5.get("O", {}).get("score", 0)
        except Exception:
            o_score = 0

        creativity_index = min(100, max(0, o_score * 1.2))

        risk_index = 0
        for k, v in insights.items():
            if "instabilidade" in v.lower() or "tensão" in v.lower():
                risk_index += 15

        return {
            "creativity_index": round(creativity_index, 2),
            "hybrid_risk_index": risk_index,
            "insight_count": len(insights)
        }
