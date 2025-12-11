# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\insight_input.py
# Última atualização: 2025-12-11T09:59:20.995650

from __future__ import annotations

from typing import Dict, Optional, Any, List
from pydantic import BaseModel, Field


class InsightTag(BaseModel):
    """
    Representa um marcador semântico identificado ao longo do processo MindScan.
    Pode ser utilizado por pipelines de insights, resumo executivo e narrativa.
    """

    tag: str = Field(..., description="Nome do marcador.")
    weight: float = Field(
        default=1.0,
        description="Peso relativo do insight para agregação posterior."
    )
    source: Optional[str] = Field(
        default=None,
        description="Origem do insight (algoritmo, MI, cruzamento etc.)."
    )


class InsightInput(BaseModel):
    """
    Payload que concentra insights brutos gerados ao longo do diagnóstico.

    Ele não representa dados de entrada do candidato, mas sim resultados intermediários
    que alimentam módulos como:
    - Bússola
    - Resumo Executivo
    - Narrativa Psicodinâmica
    - Recomendações
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    insights: List[InsightTag] = Field(
        default_factory=list,
        description="Lista de insights brutos."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_algorithm_payload(self) -> Dict[str, Any]:
        """
        Formato para módulos internos:
        - backend/engine/insight_engine.py
        - backend/pipelines/summary_pipeline.py
        """
        return self.dict()
