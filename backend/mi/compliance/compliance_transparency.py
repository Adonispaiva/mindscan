# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\compliance\compliance_transparency.py
# Última atualização: 2025-12-11T09:59:20.887954

from __future__ import annotations
from typing import Dict, Any


class ComplianceTransparency:
    """
    Garante transparência mínima do sistema:
    - módulos utilizados
    - pesos e normalizações
    - critérios de interpretação
    """

    def validate(self, report: Dict[str, Any]) -> Dict[str, Any]:

        issues = {}

        if "modules_used" not in report:
            issues["modules_used"] = "Relatório deve informar quais módulos participaram da análise."

        if "scoring_metadata" not in report:
            issues["scoring_metadata"] = "Deve existir metadado explicando critérios de cálculo."

        if "interpretation_rules" not in report:
            issues["interpretation_rules"] = "As regras interpretativas devem ser documentadas."

        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
