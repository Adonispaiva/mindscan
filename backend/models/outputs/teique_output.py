# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\teique_output.py
# Última atualização: 2025-12-11T09:59:21.042587

from __future__ import annotations

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class TEIQueOutput(BaseModel):
    """
    Resultado final do TEIQue (Inteligência Emocional Traço).

    Inclui:
    - fatores TEIQue,
    - índices agregados,
    - narrativa emocional,
    - integração com MI.
    """

    candidate_id: str = Field(..., description="ID único do candidato.")
    session_id: Optional[str] = Field(default=None)

    factor_scores: Dict[str, float] = Field(
        default_factory=dict,
        description="Pontuação de cada fator TEIQue."
    )

    global_index: Optional[float] = Field(
        default=None,
        description="Índice global de IE-Traço."
    )

    narrative: Optional[str] = Field(default=None)

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_report_payload(self) -> Dict[str, Any]:
        return self.dict()
