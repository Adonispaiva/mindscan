# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\behavioral_input.py
# Última atualização: 2025-12-11T09:59:20.980027

from __future__ import annotations

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class BehavioralEvent(BaseModel):
    """
    Representa um evento observável do comportamento do candidato
    em contexto profissional ou de avaliação.

    Esta estrutura é intencionalmente genérica para permitir que a SynMind
    injete eventos vindos de diferentes fontes (entrevista, assessment center,
    feedback 360°, etc.).
    """

    timestamp: Optional[str] = Field(
        default=None,
        description="Marca temporal livre (ISO 8601, data/hora local ou rótulo semiformatado).",
    )
    context: Optional[str] = Field(
        default=None,
        description="Contexto do evento (ex.: 'entrevista técnica', 'dinâmica de grupo').",
    )
    description: str = Field(
        ...,
        description="Descrição objetiva do comportamento observado.",
    )
    source: Optional[str] = Field(
        default=None,
        description="Origem da informação (ex.: avaliador, gestor, sistema externo).",
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Marcadores livres para facilitar buscas e análises posteriores.",
    )


class BehavioralInput(BaseModel):
    """
    Payload de entrada de dados comportamentais para o MindScan.

    Esta estrutura NÃO faz inferência; apenas organiza o material que será
    consumido pelos algoritmos de análise comportamental, módulos de MI ou
    pipelines de enriquecimento.

    Integração típica:
    - backend/pipelines/*_pipeline.py
    - backend/engine/normalization_engine.py
    - backend/engine/insight_engine.py
    """

    candidate_id: str = Field(
        ...,
        description="Identificador único do candidato no ecossistema SynMind.",
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Identificador da sessão/rodada de avaliação (quando existir).",
    )
    events: List[BehavioralEvent] = Field(
        default_factory=list,
        description="Lista de eventos comportamentais observados.",
    )
    free_notes: Optional[str] = Field(
        default=None,
        description="Campo textual livre para observações adicionais relevantes.",
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados auxiliares (ex.: origem do formulário, versão do protocolo).",
    )

    def to_algorithm_payload(self) -> Dict[str, Any]:
        """
        Converte o modelo em um dicionário pronto para consumo
        pelos algoritmos internos do MindScan.

        Mantém a superfície de API estável mesmo que os detalhes
        internos mudem futuramente.
        """
        return self.dict()
