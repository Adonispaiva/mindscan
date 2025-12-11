# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\summary_output.py
# Última atualização: 2025-12-11T09:59:21.042587

from __future__ import annotations

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class SummaryOutput(BaseModel):
    """
    Resumo executivo final do MindScan.

    Este módulo consolida:
    - insights principais
    - elementos de personalidade
    - pontos críticos
    - forças
    - narrativa curta
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    headline: Optional[str] = Field(default=None)
    summary_text: Optional[str] = Field(default=None)

    highlights: Dict[str, str] = Field(
        default_factory=dict,
        description="Destaques chave sintetizados."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        return self.dict()
