# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\teique_input.py
# Última atualização: 2025-12-11T09:59:21.011277

from __future__ import annotations
from typing import Dict, Any
from pydantic import BaseModel, Field


class TEIQueInput(BaseModel):
    """
    Entrada bruta das respostas do TEIQue.
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    responses: Dict[str, int] = Field(
        ..., description="Mapa de respostas do TEIQue (ex.: bem_estar_1 → 5)."
    )
    metadata: Dict[str, Any] = Field(default_factory=dict)
