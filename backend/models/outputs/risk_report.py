# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\risk_report.py
# Última atualização: 2025-12-11T09:59:21.026903

from __future__ import annotations

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class RiskReport(BaseModel):
    """
    Relatório consolidado de riscos psicossociais e organizacionais.

    Baseado em:
    - DASS
    - Esquemas
    - MI
    - Performance
    - Cruzamentos emocionais
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    risk_factors: Dict[str, float] = Field(
        default_factory=dict,
        description="Mapa de fatores de risco e seus pesos."
    )

    classification: Optional[str] = Field(
        default=None,
        description="Nível de risco geral."
    )

    narrative: Optional[str] = Field(
        default=None,
        description="Descrição interpretativa dos riscos identificados."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_report_payload(self) -> Dict[str, Any]:
        return self.dict()
