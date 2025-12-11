# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\scoring\scoring_esquemas.py
# Última atualização: 2025-12-11T09:59:21.042587

from __future__ import annotations

from typing import Dict, Any
from pydantic import BaseModel, Field


class ScoringEsquemas(BaseModel):
    """
    Estrutura intermediária para Esquemas Adaptativos de Young.
    """

    schema_scores: Dict[str, float] = Field(default_factory=dict)
    severity_index: Dict[str, float] = Field(default_factory=dict)

    metadata: Dict[str, Any] = Field(default_factory=dict)
