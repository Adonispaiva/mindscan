# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\dass_output.py
# Última atualização: 2025-12-11T09:59:21.026903

from __future__ import annotations

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class DASSOutput(BaseModel):
    """
    Resultado do DASS-21 após cálculo:
    - escore bruto
    - escore normalizado
    - classificação
    - narrativa emocional
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    raw_scores: Dict[str, int] = Field(
        default_factory=dict,
        description="Pontuações brutas (depressão, ansiedade, estresse)."
    )

    normalized: Dict[str, float] = Field(
        default_factory=dict,
        description="Scores normalizados para a escala interna do MindScan."
    )

    classification: Dict[str, str] = Field(
        default_factory=dict,
        description="Classificação dos níveis de cada dimensão."
    )

    narrative: Optional[str] = Field(
        default=None,
        description="Interpretação emocional integrada."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_report_payload(self) -> Dict[str, Any]:
        return self.dict()
