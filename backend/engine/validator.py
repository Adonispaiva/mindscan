# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\engine\validator.py
# Última atualização: 2025-12-11T09:59:20.841083

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
