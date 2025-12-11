# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\pdi_item.py
# Última atualização: 2025-12-11T09:59:20.964461

"""
pdi_item.py
-----------

Modelo ULTRA SUPERIOR para itens de Plano de Desenvolvimento Individual (PDI)
dentro do MindScan.

Cada PDI contém:
- Competência alvo
- Nível atual
- Meta desejada
- Ações comportamentais concretas
- Indicadores observáveis
- Descrição de impacto
- Horizonte temporal
- Categoria
- Peso e prioridade
"""

from __future__ import annotations
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, model_validator


class PDIItem(BaseModel):
    """
    Representa um item do Plano de Desenvolvimento Individual.
    """

    pdi_id: str = Field(..., description="Identificador único do item de PDI.")
    competency: str = Field(..., description="Competência alvo do desenvolvimento.")
    current_level: Optional[str] = Field(
        None, description="Nível atual do avaliado em relação à competência."
    )
    target_level: Optional[str] = Field(
        None, description="Nível desejado para evolução."
    )

    actions: List[str] = Field(
        default_factory=list,
        description="Ações concretas recomendadas."
    )

    indicators: List[str] = Field(
        default_factory=list,
        description="Indicadores observáveis que mostram progresso."
    )

    impact_description: Optional[str] = Field(
        None,
        description="Descrição do impacto esperado ao desenvolver a competência."
    )

    timeframe: Optional[str] = Field(
        None,
        description="Prazo sugerido (ex.: curto/médio/longo)."
    )

    category: str = Field(
        default="geral",
        description="Categoria do PDI (comportamental, técnico, emocional, social)."
    )

    weight: float = Field(
        default=1.0,
        description="Peso ou prioridade relativa deste item de desenvolvimento."
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Tags auxiliares, contexto técnico, anotações internas."
    )

    # ------------------------------------------------------
    # VALIDAÇÃO
    # ------------------------------------------------------
    @model_validator(mode="after")
    def validate_item(self):
        if self.weight < 0:
            raise ValueError("O peso não pode ser negativo.")
        if not self.competency.strip():
            raise ValueError("A competência alvo não pode ser vazia.")
        return self

    # ------------------------------------------------------
    # REPRESENTAÇÃO PARA PDF / RELATÓRIO
    # ------------------------------------------------------
    def to_render_dict(self) -> Dict[str, Any]:
        """
        Converte o PDI em formato apropriado para motores de relatório.
        """
        return {
            "pdi_id": self.pdi_id,
            "competency": self.competency,
            "current_level": self.current_level,
            "target_level": self.target_level,
            "actions": self.actions,
            "indicators": self.indicators,
            "impact_description": self.impact_description,
            "timeframe": self.timeframe,
            "category": self.category,
            "weight": self.weight,
            "metadata": self.metadata,
        }

    def brief(self) -> str:
        """
        Resumo técnico para logs/debug.
        """
        return (
            f"[PDIItem] {self.pdi_id} | {self.competency} "
            f"(weight={self.weight}, category={self.category})"
        )
