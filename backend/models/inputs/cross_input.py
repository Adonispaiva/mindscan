# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\cross_input.py
# Última atualização: 2025-12-11T09:59:20.980027

from __future__ import annotations

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class CrossInput(BaseModel):
    """
    Payload usado pelos módulos de cruzamento do MindScan.

    Os cruzamentos ocorrem entre:
    - Big5
    - TEIQue
    - DASS-21
    - Esquemas
    - Performance
    - Bússola
    - Dados cognitivos
    - Comportamento
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    # Cada chave representa o módulo de origem
    # Ex.: {"big5": {"O": 0.62, "C": 0.40}, "dass": {"stress": 12}}
    modules: Dict[str, Any] = Field(
        default_factory=dict,
        description="Pacote consolidado de todos os resultados a serem cruzados."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_algorithm_payload(self) -> Dict[str, Any]:
        """
        Necessário para:
        - backend/algorithms/cruzamentos/*
        - backend/engine/cross_engine.py
        """
        return self.dict()
