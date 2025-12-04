"""
MindScan — Risk Aggregator (ULTRA)
Inovexa Software — Engenharia Ultra Superior

Objetivo:
- Consolidar riscos provenientes de múltiplos módulos:
    - DASS / DASS-21
    - Big Five (risk flags)
    - TEIQue (instabilidade emocional)
    - Módulo de Cruzamentos
- Classificar densidade, severidade e origem
- Detectar padrões compostos de risco
"""

from typing import Dict, Any, List
from datetime import datetime


class RiskAggregator:
    def __init__(self):
        self._risks: List[Dict[str, Any]] = []

    # -----------------------------------------------------
    # Adiciona riscos de qualquer módulo
    # -----------------------------------------------------
    def add_risks(self, block: Dict[str, Any], source: str):
        risks = block.get("risks", [])
        for r in risks:
            enriched = {
                "source": source,
                "factor": r.get("factor"),
                "level": r.get("level"),
                "description": r.get("description"),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            self._risks.append(enriched)

    # -----------------------------------------------------
    # Inferência: densidade global
    # -----------------------------------------------------
    def _risk_density(self) -> float:
        return len(self._risks) / 10.0 if self._risks else 0.0

    # -----------------------------------------------------
    # Inferência: riscos críticos
    # -----------------------------------------------------
    def _critical_risks(self) -> List[Dict[str, Any]]:
        return [r for r in self._risks if r.get("level") == "high"]

    # -----------------------------------------------------
    # Consolidação final
    # -----------------------------------------------------
    def consolidate(self) -> Dict[str, Any]:
        return {
            "risks": self._risks,
            "critical": self._critical_risks(),
            "risk_density": round(self._risk_density(), 4),
            "total_risks": len(self._risks),
            "engine": "RiskAggregator(ULTRA)"
        }
