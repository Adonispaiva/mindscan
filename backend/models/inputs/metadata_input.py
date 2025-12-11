# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\metadata_input.py
# Última atualização: 2025-12-11T09:59:20.995650

from __future__ import annotations
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class MetadataInput(BaseModel):
    """
    Entrada de metadados suplementares para enriquecer análises.
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(None)
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Conjunto de metadados complementares (idade, área, senioridade, etc.)."
    )
