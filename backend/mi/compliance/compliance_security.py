# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\compliance\compliance_security.py
# Última atualização: 2025-12-11T09:59:20.887954

from __future__ import annotations
from typing import Dict, Any


class ComplianceSecurity:
    """
    Verifica condições básicas de segurança:
    - ausência de chaves internas
    - ausência de logs verbosos contendo dados pessoais
    """

    def validate(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        issues = {}

        # Regra 1 — chaves internas não podem aparecer
        internal_keys = ["api_key", "internal_secret", "encryption_seed"]
        for k in internal_keys:
            if k in payload:
                issues[k] = "Chave interna detectada — remover imediatamente."

        # Regra 2 — logs excessivos contendo dados de candidatos
        logs = payload.get("logs", [])
        if any("candidate" in str(item).lower() for item in logs):
            issues["logs"] = "Logs contêm informações de candidatos — reduzir verbosidade."

        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
