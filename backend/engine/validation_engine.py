"""
MindScan — Validation Engine (ULTRA)
Inovexa Software — Engenharia Ultra Superior

Função:
- Validar estrutura de blocos psicométricos
- Checar campos obrigatórios
- Detectar incoerências e falhas graves
"""

from typing import Dict, Any, List


class ValidationEngine:
    REQUIRED = ["scores", "traits", "risks", "insights"]

    def __init__(self):
        self.issues: List[Dict[str, Any]] = []

    def validate(self, block: Dict[str, Any], label: str) -> bool:
        ok = True

        for field in self.REQUIRED:
            if field not in block:
                ok = False
                self.issues.append({
                    "issue": "missing_field",
                    "field": field,
                    "block": label
                })

        if "scores" in block and not isinstance(block["scores"], dict):
            ok = False
            self.issues.append({
                "issue": "invalid_score_format",
                "block": label
            })

        return ok

    def report(self):
        return {
            "issues": self.issues,
            "total": len(self.issues),
            "engine": "ValidationEngine(ULTRA)"
        }
