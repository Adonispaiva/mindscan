# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\scoring\scoring_ocai.py
# Última atualização: 2025-12-11T09:59:21.042587

from __future__ import annotations
from typing import Dict, Any
from pydantic import BaseModel, Field


class ScoringOCAI(BaseModel):
    """
    Scoring final do módulo OCAI:
    - normalização percentual
    - identificação de cultura dominante
    - índice de equilíbrio cultural
    """

    normalized: Dict[str, float] = Field(default_factory=dict)
    dominant: str | None = None
    balance_index: float | None = None

    def compute(self, data: Dict[str, float]):
        total = sum(data.values()) or 1
        self.normalized = {k: (v / total) * 100 for k, v in data.items()}

        max_val = max(self.normalized.values())
        self.dominant = [k for k, v in self.normalized.items() if v == max_val][0]

        dif = max_val - min(self.normalized.values())
        self.balance_index = 1 - (dif / 100)

        return self
