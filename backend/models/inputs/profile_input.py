# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\profile_input.py
# Última atualização: 2025-12-11T09:59:21.011277

from __future__ import annotations

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class ProfileInput(BaseModel):
    """
    Payload consolidado para informações cadastrais e funcionais do candidato,
    utilizadas pela MI, pipelines e relatório final.

    NÃO contém dados psicométricos — apenas dados de perfil.
    """

    candidate_id: str = Field(..., description="ID do candidato.")

    name: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)
    gender: Optional[str] = Field(default=None)

    role: Optional[str] = Field(default=None, description="Cargo atual.")
    department: Optional[str] = Field(default=None)
    seniority: Optional[str] = Field(default=None)

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_algorithm_payload(self) -> Dict[str, Any]:
        """
        Usado por:
        - backend/engine/profile_engine.py
        - backend/pipelines/summary_pipeline.py
        """
        return self.dict()
