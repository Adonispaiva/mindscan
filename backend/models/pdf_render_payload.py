# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\pdf_render_payload.py
# Última atualização: 2025-12-11T09:59:20.964461

"""
pdf_render_payload.py
---------------------

Payload ULTRA SUPERIOR de renderização PDF do MindScan.

Este módulo reúne:
- Estrutura hierárquica do documento
- Dados de seções
- Blocos pré-renderizados
- Configurações de estilo
- Índice de navegação
- Metadados completos
- Layout final para o motor PDF

O PDF Engine consome diretamente esta estrutura.
"""

from __future__ import annotations
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, model_validator


class PDFRenderPayload(BaseModel):
    """
    Estrutura final entregue ao motor de renderização PDF.
    """

    metadata: Dict[str, Any] = Field(
        ...,
        description="Metadados completos do documento (autor, data, versão, etc.)."
    )
    title: str = Field(..., description="Título do documento.")
    subtitle: Optional[str] = Field(None, description="Subtítulo do documento.")
    sections: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Todas as seções do documento, já convertidas para formato renderizável."
    )
    global_blocks: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Blocos globais (capa, notas, disclaimers)."
    )
    navigation_index: Dict[str, str] = Field(
        default_factory=dict,
        description="Mapa de navegação interna: section_id → anchor."
    )
    style_config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configurações globais de estilo (fontes, cores, margens)."
    )

    layout_engine_version: str = Field(
        default="1.0.0",
        description="Versão lógica do layout engine para compatibilidade futura."
    )

    render_tokens: Dict[str, Any] = Field(
        default_factory=dict,
        description="Tokens técnicos usados pelo motor de PDF interno."
    )

    # -----------------------------
    # VALIDAÇÃO
    # -----------------------------
    @model_validator(mode="after")
    def validate_payload(self):
        if not self.title.strip():
            raise ValueError("O payload deve conter um título válido para o relatório.")

        if not isinstance(self.sections, list):
            raise ValueError("Campo 'sections' deve ser uma lista de seções renderizáveis.")

        return self

    # -----------------------------
    # FUNÇÕES
    # -----------------------------
    def get_toc(self) -> List[Dict[str, Any]]:
        """
        Gera o sumário automático com base no navigation_index.
        """
        toc = []
        for sec in self.sections:
            sec_id = sec.get("id")
            toc.append({
                "title": sec.get("title"),
                "anchor": self.navigation_index.get(sec_id),
                "order": sec.get("order"),
            })
        return sorted(toc, key=lambda x: x["order"])

    def as_render_object(self) -> Dict[str, Any]:
        """
        Retorna a estrutura final que o PDF Engine utiliza.
        """
        return {
            "metadata": self.metadata,
            "title": self.title,
            "subtitle": self.subtitle,
            "sections": self.sections,
            "global_blocks": self.global_blocks,
            "navigation_index": self.navigation_index,
            "style": self.style_config,
            "toc": self.get_toc(),
            "layout_engine_version": self.layout_engine_version,
            "render_tokens": self.render_tokens,
        }

    def debug_summary(self) -> Dict[str, Any]:
        """
        Resumo técnico para inspeção.
        """
        return {
            "total_sections": len(self.sections),
            "total_blocks": sum(len(s.get("blocks", [])) for s in self.sections),
            "global_blocks": len(self.global_blocks),
            "toc_entries": len(self.navigation_index),
        }
