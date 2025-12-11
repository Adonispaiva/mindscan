# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\scoring_input.py
# Última atualização: 2025-12-11T09:59:21.011277

from __future__ import annotations

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class ScoringInput(BaseModel):
    """
    Estrutura genérica para envio de escores pré-processados ao MindScan.

    Usado quando:
    - instrumentos externos calculam seus próprios fatores;
    - pipelines intermediários da SynMind fornecem escores compostos;
    - motores independentes realizam normalizações antes do MindScan.
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    # nome_do_modulo → mapa de escores
    # ex.: {"big5": {"O": 0.61}, "dass": {"stress": 14}}
    modules: Dict[str, Dict[str, float]] = Field(
        default_factory=dict,
        description="Pacote de escores já processados."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_algorithm_payload(self) -> Dict[str, Any]:
        return self.dict()
