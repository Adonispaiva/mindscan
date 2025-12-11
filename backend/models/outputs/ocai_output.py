# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\ocai_output.py
# Última atualização: 2025-12-11T09:59:21.026903

from __future__ import annotations

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class OCAIOutput(BaseModel):
    """
    Resultado final do instrumento OCAI após processamento e normalização.

    Inclui:
    - pontuações por quadrante cultural,
    - classificação dominante,
    - narrativa cultural,
    - metadados de versão e processo.
    """

    candidate_id: str = Field(..., description="ID único do candidato.")
    session_id: Optional[str] = Field(default=None)

    quadrant_scores: Dict[str, float] = Field(
        default_factory=dict,
        description="Pontuação dos quatro quadrantes culturais."
    )

    dominant_quadrant: Optional[str] = Field(
        default=None,
        description="Quadrante predominante segundo o OCAI."
    )

    narrative: Optional[str] = Field(
        default=None,
        description="Descrição interpretativa da cultura identificada."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_report_payload(self) -> Dict[str, Any]:
        return self.dict()
