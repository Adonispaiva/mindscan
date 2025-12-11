# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\context_input.py
# Última atualização: 2025-12-11T09:59:20.980027

from __future__ import annotations

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class ContextInput(BaseModel):
    """
    Payload de contexto de aplicação do MindScan.

    Relevante para:
    - auditoria técnica
    - confiabilidade da coleta
    - análise situacional
    - MI contextual (narrativa e interpretação)
    """

    candidate_id: str = Field(..., description="ID único do candidato.")
    session_id: Optional[str] = Field(default=None)

    environment: Optional[str] = Field(
        default=None,
        description="Ambiente de aplicação (home, empresa, remoto, presencial)."
    )

    channel: Optional[str] = Field(
        default=None,
        description="Canal de acesso (web app, mobile, cliente corporativo)."
    )

    timestamp: Optional[str] = Field(
        default=None,
        description="Momento da aplicação (ISO 8601 ou padrão livre)."
    )

    extra_context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Informações adicionais relevantes ao contexto."
    )

    def to_algorithm_payload(self) -> Dict[str, Any]:
        return self.dict()
