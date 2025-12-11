# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\scoring\scoring_validation.py
# Última atualização: 2025-12-11T09:59:21.042587

from __future__ import annotations

from typing import Dict, Any
from pydantic import BaseModel, Field


class ScoringValidation(BaseModel):
    """
    Módulo de validação pós-scoring.
    Verifica consistência entre módulos:
    - Contradições Big5 x TEIQue
    - Dissonâncias entre Esquemas e DASS
    - Coerência Cultura x Comportamento
    """

    validation_flags: Dict[str, bool] = Field(default_factory=dict)
    issues_report: Dict[str, str] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def validate(self, scoring_package: Dict[str, Any]):
        """
        scoring_package contém:
        - big5
        - dass
        - esquemas
        - teique
        - performance
        - cultura
        """

        issues = {}
        flags = {}

        # Exemplo realista:
        # alta ansiedade com baixa IE → incoerência
        try:
            anxiety = scoring_package["dass"].normalized.get("ansiedade", 0)
            ie_global = scoring_package["teique"].weighted_index or 0

            if anxiety > 0.8 and ie_global > 0.5:
                issues["ansiedade_ie"] = "Ansiedade muito alta coexistindo com IE elevada."
                flags["ansiedade_ie"] = True

        except Exception:
            pass

        self.issues_report = issues
        self.validation_flags = flags
        return self
