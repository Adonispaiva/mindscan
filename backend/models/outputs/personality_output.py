# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\personality_output.py
# Última atualização: 2025-12-11T09:59:21.026903

from __future__ __ import annotations

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class PersonalityOutput(BaseModel):
    """
    Resultado de instrumentos de personalidade fora do Big Five,
    como HEXACO, DISC adaptado, ou modelos proprietários.

    Quando presentes, complementam os cruzamentos da MI.
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    traits: Dict[str, float] = Field(
        default_factory=dict,
        description="Mapa de traços adicionais."
    )

    narrative: Optional[str] = Field(
        default=None,
        description="Resumo interpretativo dos traços adicionais."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_report_payload(self) -> Dict[str, Any]:
        return self.dict()
