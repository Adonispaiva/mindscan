# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\scoring\scoring_performance.py
# Última atualização: 2025-12-11T09:59:21.042587

from __future__ import annotations

from typing import Dict, Any
from pydantic import BaseModel, Field


class ScoringPerformance(BaseModel):
    """
    Estrutura intermediária de scoring de performance longitudinal.

    Produz:
    - curva normalizada,
    - coeficientes estatísticos,
    - índice geral interno.
    """

    semesters: Dict[str, float] = Field(default_factory=dict)
    trend_coefficients: Dict[str, float] = Field(default_factory=dict)
    global_index: float | None = Field(default=None)

    metadata: Dict[str, Any] = Field(default_factory=dict)
