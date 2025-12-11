# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\bussola_output.py
# Última atualização: 2025-12-11T09:59:21.011277

from __future__ import annotations

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class BussolaOutput(BaseModel):
    """
    Resultado final da Bússola de Talentos após processamento.

    Inclui:
    - scores dimensionais
    - posicionamento vetorial
    - quadrante final
    - narrativa interpretativa
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    dimensions: Dict[str, float] = Field(
        default_factory=dict,
        description="Mapa de pontuação por dimensão."
    )

    vector_position: Dict[str, float] = Field(
        default_factory=dict,
        description="Coordenadas vetoriais internas da Bússola."
    )

    quadrant: Optional[str] = Field(
        default=None,
        description="Quadrante final do candidato."
    )

    narrative: Optional[str] = Field(default=None)

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_report_payload(self) -> Dict[str, Any]:
        return self.dict()
