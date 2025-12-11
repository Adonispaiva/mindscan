# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\pdf_section_context.py
# Última atualização: 2025-12-11T09:59:20.964461

"""
pdf_section_context.py
----------------------

Contexto de renderização para cada seção do relatório MindScan.

Fornece:
- Estilos locais
- Configurações de fonte
- Regras de espaçamento
- Margens
- Layouts específicos para tipo de seção
- Tokens de renderização para o PDF Engine
- Herança de estilos globais
"""

from __future__ import annotations
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class PDFSectionContext(BaseModel):
    """
    Contexto detalhado de renderização PDF para uma seção específica.
    """

    section_id: str = Field(..., description="ID único da seção.")
    title_style: Dict[str, Any] = Field(
        default_factory=lambda: {
            "font": "Helvetica-Bold",
            "size": 18,
            "color": "#000000",
        },
        description="Estilo aplicado ao título da seção."
    )
    subtitle_style: Dict[str, Any] = Field(
        default_factory=lambda: {
            "font": "Helvetica",
            "size": 14,
            "color": "#444444",
        },
        description="Estilo aplicado ao subtítulo."
    )
    paragraph_style: Dict[str, Any] = Field(
        default_factory=lambda: {
            "font": "Helvetica",
            "size": 11,
            "leading": 15,
            "color": "#222222",
        },
        description="Estilo do corpo do texto."
    )
    margins: Dict[str, int] = Field(
        default_factory=lambda: {
            "top": 40,
            "bottom": 40,
            "left": 50,
            "right": 50
        },
        description="Margens da seção."
    )
    spacing: Dict[str, int] = Field(
        default_factory=lambda: {
            "between_blocks": 16,
            "after_title": 10,
            "after_subtitle": 6,
        },
        description="Regras de espaçamento local."
    )
    tokens: Dict[str, Any] = Field(
        default_factory=dict,
        description="Tokens livres utilizados por renderizadores personalizados."
    )

    # ------------------------------------------------------
    # FUNÇÕES UTILITÁRIAS
    # ------------------------------------------------------

    def merge_with_global(self, global_style: Dict[str, Any]) -> Dict[str, Any]:
        """
        Combina estilos locais com o estilo global do documento.
        Estilos locais têm prioridade.
        """
        merged = {**global_style}
        merged.update({
            "title_style": {**global_style.get("title_style", {}), **self.title_style},
            "subtitle_style": {**global_style.get("subtitle_style", {}), **self.subtitle_style},
            "paragraph_style": {**global_style.get("paragraph_style", {}), **self.paragraph_style},
            "margins": {**global_style.get("margins", {}), **self.margins},
            "spacing": {**global_style.get("spacing", {}), **self.spacing},
        })
        return merged

    def to_render_dict(self) -> Dict[str, Any]:
        """
        Exporta o contexto para o motor PDF.
        """
        return {
            "section_id": self.section_id,
            "title_style": self.title_style,
            "subtitle_style": self.subtitle_style,
            "paragraph_style": self.paragraph_style,
            "margins": self.margins,
            "spacing": self.spacing,
            "tokens": self.tokens,
        }

    def brief(self) -> str:
        """
        Resumo técnico.
        """
        return (
            f"[PDFSectionContext] {self.section_id} | "
            f"Margins={self.margins} Spacing={self.spacing}"
        )
