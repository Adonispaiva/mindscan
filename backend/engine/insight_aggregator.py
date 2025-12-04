"""
MindScan — Insight Aggregator (ULTRA)
Inovexa Software — Engenharia Ultra Superior

Função:
- Agregar insights provenientes de qualquer módulo
- Enriquecer com metadados e timestamps
- Consolidar visão interpretativa global
"""

from typing import Dict, Any, List
from datetime import datetime


class InsightAggregator:
    def __init__(self):
        self.insights: List[Dict[str, Any]] = []

    def add(self, insight: Dict[str, Any], source: str = "unknown"):
        enriched = dict(insight)
        enriched["source"] = source
        enriched["timestamp"] = datetime.utcnow().isoformat() + "Z"
        self.insights.append(enriched)

    def extend(self, lst: List[Dict[str, Any]], source: str = "unknown"):
        for ins in lst:
            self.add(ins, source)

    def export(self) -> Dict[str, Any]:
        return {
            "insights": self.insights,
            "total_insights": len(self.insights),
            "engine": "InsightAggregator(ULTRA)"
        }
