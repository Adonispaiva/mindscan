# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\risk_map_engine.py
# Última atualização: 2025-12-11T09:59:20.829001

"""
MindScan — Risk Map Engine (ULTRA)
Inovexa Software — Engenharia Ultra Superior

Função:
- Criar mapa de risco organizado em clusters lógicos
- Atribuir riscos a domínios comportamentais
"""

from typing import Dict, Any, List
from datetime import datetime


class RiskMapEngine:
    CLUSTERS = {
        "emocional": ["dass21_stress", "dass21_anxiety", "big5_neuroticism"],
        "social": ["tei_emotionality", "tei_selfcontrol"],
        "comportamental": ["impulsivity", "disinhibition"]
    }

    def _cluster(self, factor: str) -> str:
        for cname, flist in self.CLUSTERS.items():
            if factor in flist:
                return cname
        return "geral"

    def execute(self, block: Dict[str, Any]) -> Dict[str, Any]:
        risks = block.get("risks", [])
        mapping = {k: [] for k in self.CLUSTERS}
        mapping["geral"] = []

        for r in risks:
            factor = r.get("factor")
            cname = self._cluster(factor)
            mapping[cname].append(r)

        return {
            "risk_map": mapping,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "engine": "RiskMapEngine(ULTRA)"
        }
