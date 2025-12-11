# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\mi_input.py
# Última atualização: 2025-12-11T09:59:20.995650

from __future__ import annotations

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class MIInput(BaseModel):
    """
    Payload utilizado pelo módulo de MI (Mente Interpretativa) do MindScan.

    A MI consolida:
    - resultados psicométricos
    - emoções
    - padrões de comportamento
    - cultura
    - esquemas
    - cruzamentos
    - perfil cognitivo
    - performance
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    # Pacote consolidado: módulo → dados agregados
    bundle: Dict[str, Any] = Field(
        default_factory=dict,
        description="Conjunto de dados que serão reinterpretados pela MI."
    )

    version: Optional[str] = Field(
        default=None,
        description="Versão da MI utilizada (permite evolução futura controlada)."
    )

    flags: Dict[str, Any] = Field(
        default_factory=dict,
        description="Sinais/alertas internos (ex.: padrões emocionais críticos)."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_algorithm_payload(self) -> Dict[str, Any]:
        """
        Consumido por:
        - backend/mi/persona/*
        - backend/mi/compliance/*
        - backend/engine/mi_engine.py
        """
        return self.dict()
