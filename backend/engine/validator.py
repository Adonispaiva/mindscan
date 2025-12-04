"""
MindScan — Validator Wrapper (ULTRA)
Inovexa Software — Engenharia Ultra Superior

Função:
- Wrapper compatível com versões antigas
- Encapsula ValidationEngine(ULTRA)
- Mantém assinatura validate()/report()
"""

from typing import Dict, Any
from .validation_engine import ValidationEngine


class Validator:
    def __init__(self):
        self.engine = ValidationEngine()

    def validate(self, block: Dict[str, Any], label: str) -> bool:
        return self.engine.validate(block, label)

    def report(self) -> Dict[str, Any]:
        return self.engine.report()
