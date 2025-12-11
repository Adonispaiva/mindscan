# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\bussola_input.py
# Última atualização: 2025-12-11T09:59:20.980027

from __future__ import annotations

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class BussolaDimensionScore(BaseModel):
    """
    Representa o score em uma dimensão da Bússola de Talentos MindScan.

    Exemplo de dimensões (meramente ilustrativas):
    - 'exploracao'
    - 'estabilidade'
    - 'relacoes'
    - 'resultado'
    """

    dimension: str = Field(
        ...,
        description="Nome/slug da dimensão da Bússola.",
    )
    score: float = Field(
        ...,
        description="Score numérico já normalizado para a escala interna da Bússola.",
    )


class BussolaInput(BaseModel):
    """
    Payload de entrada para o módulo Bússola de Talentos.

    Pode receber:
    - respostas brutas a itens específicos da Bússola; e/ou
    - escores dimensionais já calculados (ex.: quando derivados de outros instrumentos).
    """

    candidate_id: str = Field(
        ...,
        description="Identificador único do candidato no ecossistema SynMind.",
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Sessão/rodada associada à avaliação de Bússola.",
    )
    raw_answers: Optional[Dict[str, int]] = Field(
        default=None,
        description=(
            "Mapa opcional item_id → resposta em escala (quando o protocolo "
            "usa itens próprios de Bússola)."
        ),
    )
    dimension_scores: List[BussolaDimensionScore] = Field(
        default_factory=list,
        description="Lista de escores por dimensão da Bússola.",
    )
    source: Optional[str] = Field(
        default=None,
        description="Origem principal dos dados (formulário próprio, derivação de outros testes etc.).",
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados auxiliares relevantes para rastreio e auditoria.",
    )

    def to_algorithm_payload(self) -> Dict[str, Any]:
        """
        Exporta o payload em formato simples para uso pelos algoritmos
        em `backend/algorithms/bussola/*` e pelas engines de perfil.
        """
        return self.dict()
