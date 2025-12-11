# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\system_input.py
# Última atualização: 2025-12-11T09:59:21.011277

from __future__ import annotations

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class SystemInput(BaseModel):
    """
    Payload técnico para transmissão de informações internas do sistema
    durante o fluxo de diagnóstico.

    Inclui parâmetros que podem alterar:
    - comportamento das engines
    - modo de depuração
    - configurações de normalização
    - flags de auditoria
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    flags: Dict[str, Any] = Field(
        default_factory=dict,
        description="Sinalizadores internos (debug, auditoria, validação)."
    )

    runtime_config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configurações aplicadas a engines e pipelines."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_algorithm_payload(self) -> Dict[str, Any]:
        return self.dict()
