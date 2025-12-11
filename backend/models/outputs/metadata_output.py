# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\metadata_output.py
# Última atualização: 2025-12-11T09:59:21.026903

from __future__ import annotations

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class MetadataOutput(BaseModel):
    """
    Estrutura padrão para metadados consolidados do diagnóstico.

    Inclui:
    - versão do modelo,
    - informações técnicas,
    - tempos de execução,
    - flags internas das engines.
    """

    candidate_id: str = Field(..., description="ID único do candidato.")
    session_id: Optional[str] = Field(default=None)

    engine_metadata: Dict[str, Any] = Field(default_factory=dict)
    runtime_metadata: Dict[str, Any] = Field(default_factory=dict)
    model_versions: Dict[str, str] = Field(default_factory=dict)

    notes: Optional[str] = Field(default=None)

    def to_report_payload(self) -> Dict[str, Any]:
        return self.dict()
