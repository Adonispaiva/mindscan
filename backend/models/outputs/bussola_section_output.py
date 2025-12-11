# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\bussola_section_output.py
# Última atualização: 2025-12-11T09:59:21.011277

from __future__ import annotations

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class BussolaSectionOutput(BaseModel):
    """
    Saída da seção da Bússola de Talentos, contendo dimensões,
    interpretação e posição vetorial dentro do modelo da SynMind.
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    # ex.: {"exploracao": 0.71, "estabilidade": 0.44, ...}
    dimension_scores: Dict[str, float] = Field(
        default_factory=dict,
        description="Scores por dimensão da Bússola."
    )

    # narração interpretativa
    narrative: Optional[str] = Field(
        default=None,
        description="Texto interpretativo consolidado da Bússola."
    )

    # posição em quadrantes (quando apropriado)
    positioning: Dict[str, Any] = Field(
        default_factory=dict,
        description="Informações de vetorização e quadrantes."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_report_payload(self) -> Dict[str, Any]:
        return self.dict()
