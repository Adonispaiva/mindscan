# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\personality_input.py
# Última atualização: 2025-12-11T09:59:21.011277

from __future__ import annotations

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class PersonalityInput(BaseModel):
    """
    Payload genérico para dados de personalidade que não pertencem ao Big5.

    O MindScan pode aceitar instrumentos alternativos (HEXACO, DISC adaptado,
    inventários proprietários), então esta estrutura permite inserir fatores
    complementares para enriquecer a MI e os cruzamentos.
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    # fator → score (ex.: 'assertividade': 0.74)
    traits: Dict[str, float] = Field(
        default_factory=dict,
        description="Mapa de traços de personalidade não pertencentes ao Big5."
    )

    source: Optional[str] = Field(
        default=None,
        description="Origem do instrumento."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_algorithm_payload(self) -> Dict[str, Any]:
        return self.dict()
