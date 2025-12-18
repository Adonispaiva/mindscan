"""
Compliance Service — MindScan

Serviço de validação de conformidade.
Integra com o ComplianceEngine.
"""

from backend.mi.compliance.compliance_engine import ComplianceEngine


class ComplianceService:
    def __init__(self):
        self.engine = ComplianceEngine()

    def validate_compliance(self, results: dict) -> bool:
        return self.engine.validate(results)
