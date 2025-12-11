# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\compliance\compliance_privacy.py
# Última atualização: 2025-12-11T09:59:20.887954

from __future__ import annotations
from typing import Dict, Any


class CompliancePrivacy:
    """
    Regras gerais de privacidade:
    - Dados sensíveis devem ser minimizados
    - IDs devem ser pseudonimizados
    """

    def validate(self, session: Dict[str, Any]) -> Dict[str, Any]:

        issues = {}

        # Regra 1 — dados sensíveis proibidos
        forbidden = ["senha", "token_interno", "endereco_residencial"]
        for key in forbidden:
            if key in session:
                issues[key] = "Informação sensível não deve ser armazenada no sistema."

        # Regra 2 — ID do candidato não pode ser e-mail
        cid = session.get("candidate_id", "")
        if "@" in cid:
            issues["candidate_id"] = "O ID do candidato não pode conter e-mail. Use um ID pseudonimizado."

        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
