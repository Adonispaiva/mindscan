# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\dass_input.py
# Última atualização: 2025-12-11T09:59:20.995650

from __future__ import annotations

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class DASSInput(BaseModel):
    """
    Payload de entrada do inventário DASS-21 (Depressão, Ansiedade, Estresse).

    O MindScan utiliza o DASS como um dos vetores emocionais de análise,
    que posteriormente será cruzado com personalidade, esquemas e MI.
    """

    candidate_id: str = Field(
        ...,
        description="Identificador único do candidato."
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Sessão/rodada de aplicação do DASS-21."
    )

    # Respostas 1–4 Likert mapeadas por item_id: "d1", "a2", "s3", etc.
    responses: Dict[str, int] = Field(
        default_factory=dict,
        description="Mapa item_id → resposta (1–4)."
    )

    language: str = Field(
        default="pt-BR",
        description="Idioma da aplicação."
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados auxiliares."
    )

    def to_algorithm_payload(self) -> Dict[str, Any]:
        """
        Formato usado por:
        - backend/algorithms/dass21/dass_scoring.py
        - backend/engine/emotional_engine.py
        """
        return self.dict()
