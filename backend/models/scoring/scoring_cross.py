# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\scoring\scoring_cross.py
# Última atualização: 2025-12-11T09:59:21.042587

from __future__ import annotations

from typing import Dict, Any
from pydantic import BaseModel, Field


class ScoringCross(BaseModel):
    """
    Estrutura intermediária de cruzamentos psicométricos.

    Integra dados de:
    - Big Five
    - TEIQue
    - DASS
    - Performance
    - Esquemas
    - Cultura / OCAI

    É consumida principalmente pela MI e engines de interpretação cruzada.
    """

    cross_maps: Dict[str, Any] = Field(default_factory=dict)
    weights: Dict[str, float] = Field(default_factory=dict)

    metadata: Dict[str, Any] = Field(default_factory=dict)
