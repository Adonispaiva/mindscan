# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\performance_output.py
# Última atualização: 2025-12-11T09:59:21.026903

from __future__ import annotations

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class PerformanceOutput(BaseModel):
    """
    Resultado final da análise de performance longitudinal.

    Inclui:
    - curva de evolução,
    - índice global,
    - tendência,
    - narrativa interpretativa.
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    semesters: Dict[str, float] = Field(
        default_factory=dict,
        description="Valores normalizados por semestre."
    )

    global_index: Optional[float] = Field(
        default=None,
        description="Índice geral de performance."
    )

    trend: Optional[str] = Field(
        default=None,
        description="Descrição qualitativa da tendência: ascendente, estável, descendente."
    )

    narrative: Optional[str] = Field(default=None)

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_report_payload(self) -> Dict[str, Any]:
        return self.dict()
