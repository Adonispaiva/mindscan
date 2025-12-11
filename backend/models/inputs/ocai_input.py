# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\ocai_input.py
# Última atualização: 2025-12-11T09:59:20.995650

from __future__ import annotations

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class OCAIInput(BaseModel):
    """
    Payload de entrada do instrumento OCAI (Organizational Culture Assessment Instrument).

    O OCAI é um dos frameworks utilizados pelo MindScan para mapear o modelo cultural
    dominante percebido pelo candidato ou pela organização.
    """

    candidate_id: str = Field(..., description="ID único do candidato.")
    session_id: Optional[str] = Field(default=None)

    # item_id → valor percentual ou Likert, dependendo do formato adotado
    responses: Dict[str, float] = Field(
        default_factory=dict,
        description="Mapa de respostas aos itens do OCAI."
    )

    version: Optional[str] = Field(
        default=None,
        description="Versão do OCAI (ex.: 'standard', 'adapted')."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_algorithm_payload(self) -> Dict[str, Any]:
        """
        Consumido pelos módulos internos:
        - backend/algorithms/ocai/*
        - backend/engine/culture_engine.py
        """
        return self.dict()
