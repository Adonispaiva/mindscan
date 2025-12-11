# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\performance_input.py
# Última atualização: 2025-12-11T09:59:20.995650

from __future__ import annotations

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class PerformanceInput(BaseModel):
    """
    Payload de entrada para dados de performance longitudinal do candidato.

    O MindScan utiliza até 5 semestres de indicadores para gerar:
    - curva de evolução
    - tendência
    - variação relativa
    - estabilidade/inconsistência
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    # semestre → indicador numérico (ex.: 0.72, 0.81, 0.55)
    performance: Dict[str, float] = Field(
        default_factory=dict,
        description="Mapa de indicadores por semestre."
    )

    source: Optional[str] = Field(
        default=None,
        description="Origem (ex.: HR system, LMS, gestor, autoavaliação)."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_algorithm_payload(self) -> Dict[str, Any]:
        """
        Alimenta:
        - backend/algorithms/performance/*
        - backend/engine/performance_engine.py
        """
        return self.dict()
