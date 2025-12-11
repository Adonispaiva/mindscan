# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\scoring\scoring_dass.py
# Última atualização: 2025-12-11T09:59:21.042587

from __future__ import annotations

from typing import Dict, Any
from pydantic import BaseModel, Field


class ScoringDASS(BaseModel):
    """
    Escores intermediários do DASS-21:
    - depressão
    - ansiedade
    - estresse

    Alimenta classificações internas e normalizações do relatório.
    """

    raw: Dict[str, int] = Field(default_factory=dict)
    normalized: Dict[str, float] = Field(default_factory=dict)
    severity: Dict[str, str] = Field(default_factory=dict)

    metadata: Dict[str, Any] = Field(default_factory=dict)
