# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\pipeline_output.py
# Última atualização: 2025-12-11T09:59:21.026903

from __future__ import annotations

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class PipelineOutput(BaseModel):
    """
    Estrutura usada internamente para registrar o status final
    de cada pipeline executado no MindScan.

    Usado principalmente para:
    - auditoria,
    - depuração avançada,
    - monitoramento,
    - geração do relatório de execução.
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    pipeline_status: Dict[str, Any] = Field(
        default_factory=dict,
        description="Informações sobre cada pipeline executado."
    )

    warnings: Dict[str, str] = Field(
        default_factory=dict,
        description="Alertas internos gerados durante o processo."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        return self.dict()
