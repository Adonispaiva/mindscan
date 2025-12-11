# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\strengths_report.py
# Última atualização: 2025-12-11T09:59:21.042587

from __future__ import annotations

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class StrengthEntry(BaseModel):
    """
    Representa uma força identificada no perfil do candidato.
    """

    name: str = Field(..., description="Nome da força.")
    description: Optional[str] = Field(default=None)
    weight: float = Field(default=1.0)


class StrengthsReport(BaseModel):
    """
    Relatório consolidado de forças psicológicas e comportamentais.

    Utiliza inputs provenientes de:
    - Big Five
    - Performance
    - Bússola
    - MI
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    strengths: List[StrengthEntry] = Field(
        default_factory=list,
        description="Lista de forças identificadas."
    )

    summary: Optional[str] = Field(
        default=None,
        description="Resumo interpretativo das forças."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        return self.dict()
