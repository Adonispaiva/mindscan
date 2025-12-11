# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\compliance\compliance_apa.py
# Última atualização: 2025-12-11T09:59:20.872348

from __future__ import annotations
from typing import Dict, Any


class ComplianceAPA:
    """
    Valida conformidade com diretrizes gerais de boas práticas psicológicas.
    Este módulo NÃO substitui regulamentações profissionais — apenas orienta o sistema.
    """

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        issues = {}

        # Regra 1 — ausência de dados pessoais sensíveis excessivos
        sensitive_keys = ["cpf", "rg", "salario"]
        for key in sensitive_keys:
            if key in data:
                issues[key] = "Informação sensível desnecessária detectada."

        # Regra 2 — volume de dados reduzido
        if len(data) > 300:
            issues["excesso_dados"] = "Dataset muito extenso para o propósito do relatório."

        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
