# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\report_summary.py
# Última atualização: 2025-12-11T09:59:20.980027

# D:\backend\models\report_summary.py
# Estrutura completa do resumo do relatório MindScan — Versão Inovexa Ultra

from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field, validator


class ReportSummary(BaseModel):
    """
    O resumo é uma entidade especial do relatório:
      - aparece em todos os templates (com conteúdo diferente)
      - contém sínteses estruturadas das seções
      - alimenta o Executive Renderer e o Premium Renderer
      - organiza insights globais, forças, riscos e indicadores
    """

    id: str = Field(..., description="Identificador único do resumo dentro do relatório.")
    headline: Optional[str] = Field(
        None,
        description="Frase-chave ou título resumido do relatório."
    )
    overview: Optional[str] = Field(
        None,
        description="Descrição panorâmica do perfil e do diagnóstico."
    )
    key_points: List[str] = Field(
        default_factory=list,
        description="Lista dos principais pontos (forças, riscos, indicadores)."
    )
    indicators: Dict[str, Any] = Field(
        default_factory=dict,
        description="Indicadores numéricos agregados (ex.: estabilidade, coerência, EQ global)."
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados adicionais para renderização e priorização."
    )
    style: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configurações visuais específicas do resumo."
    )
    visible_in: List[str] = Field(
        default_factory=lambda: ["executive", "premium"],
        description="Por padrão, o resumo aparece no executivo e no premium."
    )

    @validator("id")
    def validate_id(cls, value):
        if " " in value:
            raise ValueError("O campo 'id' não pode conter espaços.")
        return value

    @validator("key_points", pre=True)
    def convert_single_point(cls, value):
        """Permite inserir apenas uma string em vez de lista."""
        if isinstance(value, str):
            return [value]
        return value

    @validator("visible_in", each_item=True)
    def validate_template(cls, value):
        allowed = {"technical", "executive", "psychodynamic", "premium"}
        if value not in allowed:
            raise ValueError(
                f"Template inválido: {value}. Deve ser um de {allowed}"
            )
        return value

    def add_point(self, point: str):
        """Adiciona um ponto-chave ao resumo."""
        if not isinstance(point, str):
            raise ValueError("O ponto-chave deve ser uma string.")
        self.key_points.append(point)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o resumo em um dicionário padronizado, pronto para
        renderização em qualquer template.
        """
        return {
            "id": self.id,
            "headline": self.headline,
            "overview": self.overview,
            "key_points": self.key_points,
            "indicators": self.indicators,
            "metadata": self.metadata,
            "style": self.style,
            "visible_in": self.visible_in,
        }

    def is_visible_for(self, template: str) -> bool:
        """
        Define se o resumo aparece no template atual.
        """
        return template in self.visible_in
