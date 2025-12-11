# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\recommendation_item.py
# Última atualização: 2025-12-11T09:59:20.980027

"""
recommendation_item.py
----------------------

Item de recomendação avançada do MindScan.

Cada recomendação é composta por:
- Contexto da recomendação
- Insight que originou
- Texto final
- Peso/força da recomendação
- Categoria
- Impacto comportamental
- Criticidade
- Horizonte temporal
- Etiquetas auxiliares
"""

from __future__ import annotations
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, model_validator


class RecommendationItem(BaseModel):
    """
    Estrutura ULTRA SUPERIOR para recomendações do MindScan.
    """

    rec_id: str = Field(..., description="ID único da recomendação.")
    title: str = Field(..., description="Título sintetizado da recomendação.")
    description: str = Field(..., description="Descrição completa e orientada a ação.")

    insight_origin: Optional[str] = Field(
        None,
        description="Insight, matriz ou cálculo que deu origem a esta recomendação."
    )

    category: str = Field(
        default="geral",
        description="Categoria da recomendação (ex.: cognitiva, emocional, social, técnica)."
    )

    impact: str = Field(
        default="moderado",
        description="Impacto comportamental esperado."
    )

    weight: float = Field(
        default=1.0,
        description="Peso relativo da recomendação, para priorização."
    )

    criticality: str = Field(
        default="média",
        description="Criticidade atribuída."
    )

    timeframe: Optional[str] = Field(
        None,
        description="Horizonte temporal para implementação (curto, médio, longo prazo)."
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Etiquetas auxiliares, contexto técnico, flags internas."
    )

    # ------------------------------------------------------
    # VALIDAÇÃO
    # ------------------------------------------------------
    @model_validator(mode="after")
    def validate_item(self):
        if self.weight < 0:
            raise ValueError("O peso da recomendação não pode ser negativo.")
        return self

    # ------------------------------------------------------
    # REPRESENTAÇÃO PARA RENDERIZAÇÃO
    # ------------------------------------------------------
    def to_render_dict(self) -> Dict[str, Any]:
        """
        Exporta o item para uso em motores de relatório ou PDF.
        """
        return {
            "rec_id": self.rec_id,
            "title": self.title,
            "description": self.description,
            "insight_origin": self.insight_origin,
            "category": self.category,
            "impact": self.impact,
            "weight": self.weight,
            "criticality": self.criticality,
            "timeframe": self.timeframe,
            "metadata": self.metadata,
        }

    def brief(self) -> str:
        """
        Resumo técnico de debug.
        """
        return f"[Recommendation] {self.rec_id} | {self.title} ({self.category})"
