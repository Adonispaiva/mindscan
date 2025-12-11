# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\insight_engine.py
# Última atualização: 2025-12-11T09:59:20.811999

"""
MindScan — Insight Engine (ULTRA)
Inovexa Software — Engenharia Ultra Superior

Gera insights avançados a partir de:
- Scores normalizados
- Riscos classificados
- Traços comportamentais
- Padrões psicométricos combinados

Camadas:
1) Insights por score
2) Insights por risco
3) Insights por traços
4) Insights compostos
"""

from typing import Dict, Any, List
from datetime import datetime


class InsightEngine:
    def __init__(self):
        self.threshold_high = 0.85
        self.threshold_low = 0.15

    # ----------------------------------------------------
    # Utilidades
    # ----------------------------------------------------
    def _is_num(self, v): return isinstance(v, (int, float))

    def _fmt(self, src: str, text: str, weight: float):
        return {
            "source": src,
            "text": text,
            "weight": round(weight, 4),
            "ts": datetime.utcnow().isoformat() + "Z"
        }

    # ----------------------------------------------------
    # Insights com base em scores
    # ----------------------------------------------------
    def _insights_from_scores(self, scores: Dict[str, float]):
        out = []

        for key, value in scores.items():
            if not self._is_num(value):
                continue

            if value >= self.threshold_high:
                out.append(self._fmt("score", f"Nível elevado em {key}.", value))

            if value <= self.threshold_low:
                out.append(self._fmt("score", f"Nível reduzido em {key}.", 1 - value))

        return out

    # ----------------------------------------------------
    # Insights com base em riscos
    # ----------------------------------------------------
    def _insights_from_risks(self, risks: List[Dict[str, Any]]):
        out = []
        for r in risks:
            level = r.get("level")
            desc = r.get("description", "Risco detectado.")

            weight = 0.9 if level == "high" else 0.7
            out.append(self._fmt("risk", desc, weight))

        return out

    # ----------------------------------------------------
    # Insights com base em traços (strings qualitativas)
    # ----------------------------------------------------
    def _insights_from_traits(self, traits: Dict[str, Any]):
        out = []
        for t, v in traits.items():
            if isinstance(v, str):
                out.append(self._fmt("trait", f"{t}: {v}", 0.6))
        return out

    # ----------------------------------------------------
    # Execução completa
    # ----------------------------------------------------
    def execute(self, block: Dict[str, Any]) -> Dict[str, Any]:
        scores = block.get("scores", {})
        risks = block.get("risks", [])
        traits = block.get("traits", {})

        insights = []
        insights.extend(self._insights_from_scores(scores))
        insights.extend(self._insights_from_risks(risks))
        insights.extend(self._insights_from_traits(traits))

        return {
            "insights": insights,
            "total_insights": len(insights),
            "engine": "InsightEngine(ULTRA)"
        }
