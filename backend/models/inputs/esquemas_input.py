# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\esquemas_input.py
# Última atualização: 2025-12-11T09:59:20.995650

from __future__ import annotations

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class EsquemasInput(BaseModel):
    """
    Payload de entrada para o módulo de Esquemas Adaptativos de Young.

    O MindScan utiliza versões reduzidas e expandidas do inventário,
    por isso a estrutura é flexível.
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    # item_id → resposta Likert (1–6)
    responses: Dict[str, int] = Field(
        default_factory=dict,
        description="Respostas aos itens do inventário de esquemas."
    )

    version: Optional[str] = Field(
        default=None,
        description="Versão utilizada do inventário (reduzida/expandida)."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_algorithm_payload(self) -> Dict[str, Any]:
        """
        Consumo interno:
        - backend/algorithms/esquemas/*
        - backend/engine/schema_engine.py
        """
        return self.dict()
