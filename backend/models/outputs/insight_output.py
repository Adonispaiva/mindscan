# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\insight_output.py
# Última atualização: 2025-12-11T09:59:21.026903

from __future__ import annotations

from typing import Dict, Optional, Any, List
from pydantic import BaseModel, Field


class InsightEntry(BaseModel):
    """
    Insight individual consolidado após cruzamentos e MI.
    """

    tag: str = Field(..., description="Nome do insight.")
    weight: float = Field(default=1.0)
    description: Optional[str] = Field(default=None)


class InsightOutput(BaseModel):
    """
    Resultado final dos insights do MindScan.

    Alimenta:
    - resumo executivo
    - narrativa
    - seções interpretativas do relatório.
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    insights: List[InsightEntry] = Field(
        default_factory=list,
        description="Lista de insights derivados."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_report_payload(self) -> Dict[str, Any]:
        return self.dict()
