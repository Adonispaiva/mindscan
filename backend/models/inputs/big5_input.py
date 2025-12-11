# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\big5_input.py
# Última atualização: 2025-12-11T09:59:20.980027

from __future__ import annotations

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Big5ItemResponse(BaseModel):
    """
    Resposta individual a um item do inventário Big Five utilizado pelo MindScan.

    O backend pode trabalhar com diferentes versões de questionário, por isso
    usamos `item_id` em vez de índice fixo.
    """

    item_id: str = Field(
        ...,
        description="Identificador único do item no questionário Big5.",
    )
    value: int = Field(
        ...,
        ge=1,
        le=5,
        description="Resposta em escala Likert (tipicamente 1–5).",
    )
    reverse_scored: bool = Field(
        default=False,
        description="Indica se o item é invertido na matriz de correção.",
    )


class Big5Input(BaseModel):
    """
    Payload de entrada de dados do inventário de personalidade Big Five.

    Este modelo é o ponto único de verdade para ingestão Big5 no MindScan.
    As engines de normalização e scoring devem preferir este payload em vez
    de estruturas ad hoc.
    """

    candidate_id: str = Field(
        ...,
        description="Identificador único do candidato no ecossistema SynMind.",
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Sessão/rodada de aplicação do Big5.",
    )
    language: str = Field(
        default="pt-BR",
        description="Código de idioma do questionário respondido.",
    )
    version: Optional[str] = Field(
        default=None,
        description="Versão do formulário Big5 (quando houver múltiplas variações).",
    )
    responses: List[Big5ItemResponse] = Field(
        default_factory=list,
        description="Lista de respostas item a item.",
    )
    already_scored: bool = Field(
        default=False,
        description=(
            "Se True, indica que os escores fatoriais já foram calculados "
            "por um sistema externo; neste caso, `raw_scores` pode ser usado."
        ),
    )
    raw_scores: Optional[Dict[str, float]] = Field(
        default=None,
        description=(
            "Mapa opcional de escores fatoriais pré-calculados "
            "(ex.: {'O': 0.61, 'C': 0.44, 'E': ...})."
        ),
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados auxiliares (dispositivo, origem da coleta, etc.).",
    )

    def to_algorithm_payload(self) -> Dict[str, Any]:
        """
        Converte o input em um dicionário amigável para os módulos:

        - backend/algorithms/big5/*
        - backend/engine/scoring_engine.py
        - backend/pipelines/big5_pipeline.py
        """
        return self.dict()
