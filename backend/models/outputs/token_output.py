# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\token_output.py
# Última atualização: 2025-12-11T09:59:21.042587

from __future__ import annotations

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class TokenOutput(BaseModel):
    """
    Estrutura que registra tokens internos utilizados para rastreamento
    e auditoria de execução do diagnóstico.

    NÃO é parte da análise psicométrica, mas integra a camada técnica.
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    tokens: Dict[str, Any] = Field(
        default_factory=dict,
        description="Tokens e marcadores gerados pela execução."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        return self.dict()
