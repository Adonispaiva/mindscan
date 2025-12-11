# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\cross_output.py
# Última atualização: 2025-12-11T09:59:21.026903

from __future__ import annotations

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class CrossOutput(BaseModel):
    """
    Estrutura de saída para os módulos de cruzamento interno.
    Esses cruzamentos integram dados entre:
    - Big5
    - TEIQue
    - DASS
    - Performance
    - Esquemas
    - Cultura
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    cross_maps: Dict[str, Any] = Field(
        default_factory=dict,
        description="Mapeamento de cruzamentos entre módulos."
    )

    narrative: Optional[str] = Field(
        default=None,
        description="Resumo interpretativo dos cruzamentos."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        return self.dict()
