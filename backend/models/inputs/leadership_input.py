# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\leadership_input.py
# Última atualização: 2025-12-11T09:59:20.995650

from __future__ import annotations

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class LeadershipInput(BaseModel):
    """
    Payload de entrada para análise de Estilo de Liderança.

    O MindScan pode trabalhar com diferentes matrizes (transformacional,
    situacional, comportamental, competências), por isso o modelo é flexível.
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    # item_id → resposta Likert ou valor contínuo
    responses: Dict[str, float] = Field(
        default_factory=dict,
        description="Respostas aos itens de liderança."
    )

    framework: Optional[str] = Field(
        default=None,
        description="Nome do modelo utilizado (ex.: 'transformacional', 'situacional')."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_algorithm_payload(self) -> Dict[str, Any]:
        """
        Usado por:
        - backend/algorithms/leadership/*
        - backend/engine/leadership_engine.py
        """
        return self.dict()
