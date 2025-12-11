# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\schemas_input.py
# Última atualização: 2025-12-11T09:59:21.011277

from __future__ import annotations

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class SchemasInput(BaseModel):
    """
    Payload unificado para ingestão dos Esquemas Adaptativos (Young)
    quando utilizados fora do inventário tradicional.

    Esta estrutura complementa `EsquemasInput`, permitindo inputs
    derivados de sistemas externos, MI intermediária ou análises qualitativas.
    """

    candidate_id: str = Field(..., description="ID único do candidato.")
    session_id: Optional[str] = Field(default=None)

    # esquema → score (ex.: 'abandono': 0.63)
    schema_scores: Dict[str, float] = Field(
        default_factory=dict,
        description="Mapa de escores dos esquemas adaptativos."
    )

    source: Optional[str] = Field(
        default=None, description="Origem dos dados (manual, algoritmo, derivação)."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_algorithm_payload(self) -> Dict[str, Any]:
        return self.dict()
