# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\risk_engine.py
# Última atualização: 2025-12-11T09:59:20.828001

"""
MindScan — Risk Engine (ULTRA)
Inovexa Software — Engenharia Ultra Superior

Função:
- Detectar riscos psicométricos fundamentais
- Classificar em níveis (high / moderate / low)
- Analisar padrões cruzados em módulos psicométricos
"""

from typing import Dict, Any, List
from datetime import datetime


class RiskEngine:
    RULES = {
        "dass21_stress": 0.80,
        "big5_neuroticism": 0.75,
        "tei_emotionality_low": 0.25,
    }

    def _detect(self, key: str, value: float) -> List[Dict[str, Any]]:
        out = []
        if key in self.RULES and value >= self.RULES[key]:
            out.append({
                "factor": key,
                "level": "high",
                "description": f"Nível elevado em {key}.",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
        if "emotionality" in key and value <= self.RULES["tei_emotionality_low"]:
            out.append({
                "factor": key,
                "level": "moderate",
                "description": f"Baixa emocionalidade detectada.",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
        return out

    def execute(self, block: Dict[str, Any]) -> Dict[str, Any]:
        scores = block.get("scores", {})
        risks = []
        for key, val in scores.items():
            if isinstance(val, (int, float)):
                risks.extend(self._detect(key, val))

        return {
            "risks": risks,
            "total_risks": len(risks),
            "engine": "RiskEngine(ULTRA)"
        }
