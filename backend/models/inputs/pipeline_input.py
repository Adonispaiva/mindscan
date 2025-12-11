# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\pipeline_input.py
# Última atualização: 2025-12-11T09:59:21.011277

from __future__ import annotations
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class PipelineInput(BaseModel):
    """
    Entrada usada pelos pipelines do MindScan.
    """

    candidate_id: str = Field(..., description="ID único do candidato.")
    session_id: Optional[str] = Field(None)
    raw_data: Dict[str, Any] = Field(default_factory=dict, description="Dados brutos capturados.")
    modules_to_run: Optional[Dict[str, bool]] = Field(
        default=None,
        description="Permite ativar ou desativar módulos específicos."
    )
    metadata: Optional[Dict[str, Any]] = Field(default=None)
