# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\scoring\scoring_big5.py
# Última atualização: 2025-12-11T09:59:21.042587

from __future__ import annotations

from typing import Dict, Any
from pydantic import BaseModel, Field


class ScoringBig5(BaseModel):
    """
    Estrutura intermediária de scoring do Big Five.
    Consumida por:
    - scoring_engine
    - pipelines de síntese
    - MI
    """

    raw_scores: Dict[str, int] = Field(default_factory=dict)
    normalized_scores: Dict[str, float] = Field(default_factory=dict)
    factors: Dict[str, float] = Field(default_factory=dict)

    metadata: Dict[str, Any] = Field(default_factory=dict)
