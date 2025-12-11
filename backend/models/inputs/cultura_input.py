# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\cultura_input.py
# Última atualização: 2025-12-11T09:59:20.995650

from __future__ import annotations

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class CulturaInput(BaseModel):
    """
    Payload de entrada para o módulo de Cultura Organizacional do MindScan,
    baseado no OCAI (Organizational Culture Assessment Instrument) e modelos derivados.

    O objetivo é permitir flexibilidade no formato dos itens e nas versões do instrumento.
    """

    candidate_id: str = Field(..., description="ID único do candidato.")
    session_id: Optional[str] = Field(default=None)

    # item_id → pontuação Likert ou percentual (dependendo do protocolo usado)
    responses: Dict[str, float] = Field(
        default_factory=dict,
        description="Mapa de respostas do OCAI ou equivalente."
    )

    version: Optional[str] = Field(
        default=None,
        description="Versão do instrumento cultural (ex.: OCAI v1, OCAI adaptado)."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_algorithm_payload(self) -> Dict[str, Any]:
        """
        Usado pelos módulos:
        - backend/algorithms/ocai/*
        - backend/engine/culture_engine.py
        """
        return self.dict()
