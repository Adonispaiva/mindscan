# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\esquemas_output.py
# Última atualização: 2025-12-11T09:59:21.026903

from __future__ import annotations

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class EsquemasOutput(BaseModel):
    """
    Resultado final dos Esquemas Adaptativos de Young.

    Inclui:
    - scores por esquema
    - índice de severidade
    - narrativa interpretativa
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    schema_scores: Dict[str, float] = Field(
        default_factory=dict,
        description="Scores por esquema."
    )

    severity_index: Dict[str, float] = Field(
        default_factory=dict,
        description="Índice de severidade por fator."
    )

    narrative: Optional[str] = Field(default=None)

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_report_payload(self) -> Dict[str, Any]:
        return self.dict()
