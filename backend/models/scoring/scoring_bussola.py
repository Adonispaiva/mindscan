# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\scoring\scoring_bussola.py
# Última atualização: 2025-12-11T09:59:21.042587

from __future__ import annotations

from typing import Dict, Any
from pydantic import BaseModel, Field


class ScoringBussola(BaseModel):
    """
    Estrutura intermediária da Bússola de Talentos.

    Inclui:
    - normalizações
    - vetorização
    - pesos dimensionais
    """

    dimension_scores: Dict[str, float] = Field(default_factory=dict)
    vector: Dict[str, float] = Field(default_factory=dict)
    weights: Dict[str, float] = Field(default_factory=dict)

    metadata: Dict[str, Any] = Field(default_factory=dict)
