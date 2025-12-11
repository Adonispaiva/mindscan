# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\decision_output.py
# Última atualização: 2025-12-11T09:59:21.026903

from __future__ import annotations

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class DecisionOutput(BaseModel):
    """
    Resultado consolidado das decisões psicométricas e interpretativas do MindScan.

    Este módulo é utilizado para:
    - indicar direções gerais do perfil,
    - embasar recomendações,
    - registrar decisões internas tomadas por engines e MI.
    """

    candidate_id: str = Field(..., description="ID único do candidato.")
    session_id: Optional[str] = Field(default=None)

    decisions: Dict[str, Any] = Field(
        default_factory=dict,
        description="Mapa de decisões interpretativas por módulo."
    )

    rationale: Optional[str] = Field(
        default=None,
        description="Justificativa central das decisões tomadas."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_report_payload(self) -> Dict[str, Any]:
        return self.dict()
