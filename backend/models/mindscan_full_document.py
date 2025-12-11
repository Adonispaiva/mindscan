# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\mindscan_full_document.py
# Última atualização: 2025-12-11T09:59:20.964461

"""
MindScan Full Document Model
----------------------------
Documento total do MindScan, contendo toda a estrutura hierárquica,
metadados, blocos, seções, e mecanismos necessários para renderização
posterior em PDF, geração de payloads avançados, navegação interna e
interação com o ecossistema MindScan.

Este módulo é o núcleo da arquitetura de relatórios.
"""

from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, model_validator
from datetime import datetime

# Interfaces externas (outros modelos da pasta)
from .report_section import ReportSection
from .report_block import ReportBlock
from .pdf_render_payload import PDFRenderPayload


class DocumentMetadata(BaseModel):
    """
    Metadados completos do documento MindScan.
    """

    document_id: str = Field(..., description="ID único do relatório.")
    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Data e hora de geração do documento."
    )
    version: str = Field(
        default="1.0.0",
        description="Versão lógica do documento."
    )
    language: str = Field(
        default="pt-BR",
        description="Idioma base do relatório."
    )
    owner_name: Optional[str] = Field(
        default=None,
        description="Nome da pessoa avaliada."
    )
    owner_role: Optional[str] = Field(
        default=None,
        description="Cargo/função do avaliado (quando aplicável)."
    )
    evaluator_name: Optional[str] = Field(
        default=None,
        description="Avaliador que conduziu a análise."
    )


class DocumentNavigationIndex(BaseModel):
    """
    Estrutura que representa a árvore de navegação interna do documento.

    Permite:
    - Hyperlinks internos
    - Sumário automático
    - Referências cruzadas
    """

    index_map: Dict[str, str] = Field(
        default_factory=dict,
        description="Mapa: ID da seção → âncora no PDF."
    )

    def register_section(self, section_id: str, anchor: str):
        self.index_map[section_id] = anchor

    def get_anchor(self, section_id: str) -> Optional[str]:
        return self.index_map.get(section_id)


class MindScanFullDocument(BaseModel):
    """
    Estrutura principal do relatório final.

    Contém:
    - Metadados
    - Seções ordenadas
    - Blocos auxiliares
    - Navegação hierárquica
    - Mecanismos de geração de payload para PDF
    """

    metadata: DocumentMetadata = Field(..., description="Metadados do documento.")
    title: str = Field(..., description="Título do relatório.")
    subtitle: Optional[str] = Field(None, description="Subtítulo do relatório.")
    sections: List[ReportSection] = Field(
        default_factory=list,
        description="Lista ordenada das seções do documento."
    )
    global_blocks: List[ReportBlock] = Field(
        default_factory=list,
        description="Blocos que não pertencem a uma seção específica."
    )
    navigation_index: DocumentNavigationIndex = Field(
        default_factory=DocumentNavigationIndex,
        description="Índice para navegação interna do documento."
    )
    style_config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configurações de estilo e layout global."
    )
    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Contexto técnico usado pelos engines internos."
    )

    # -----------------------------
    #   VALIDAÇÃO & REGRAS
    # -----------------------------

    @model_validator(mode="after")
    def validate_sections(self):
        """
        Garante consistência na estrutura das seções e blocos.
        """
        identifiers = set()
        order_values = []

        for section in self.sections:
            if section.section_id in identifiers:
                raise ValueError(f"Seção duplicada: {section.section_id}")
            identifiers.add(section.section_id)
            order_values.append(section.order)

        if sorted(order_values) != order_values:
            raise ValueError(
                "A lista de seções deve estar ordenada por 'order'. "
                "Use .sort_sections() para corrigir."
            )

        return self

    # -----------------------------
    #   FUNÇÕES AVANÇADAS
    # -----------------------------

    def sort_sections(self):
        """
        Garante ordenação por ordem lógica.
        """
        self.sections = sorted(self.sections, key=lambda x: x.order)

    def add_section(self, section: ReportSection):
        """
        Adiciona uma nova seção ao documento.
        """
        self.sections.append(section)
        self.sort_sections()

    def add_global_block(self, block: ReportBlock):
        """
        Adiciona um bloco global (capa, disclaimer, etc.).
        """
        self.global_blocks.append(block)

    def build_navigation_index(self):
        """
        Gera o mapa de navegação interna com âncoras para PDF.
        """
        for idx, section in enumerate(self.sections):
            anchor = f"sec_{idx}_{section.section_id}"
            self.navigation_index.register_section(section.section_id, anchor)

    # -----------------------------
    #   RENDERIZAÇÃO PARA PDF
    # -----------------------------

    def to_pdf_payload(self) -> PDFRenderPayload:
        """
        Constrói o payload completo para renderização PDF.

        Esta função é chamada pelo motor de PDF e deve retornar
        toda a estrutura hierárquica pronta para renderização.
        """
        self.build_navigation_index()

        return PDFRenderPayload(
            metadata=self.metadata.model_dump(),
            title=self.title,
            subtitle=self.subtitle,
            sections=[sec.to_render_dict() for sec in self.sections],
            global_blocks=[blk.to_render_dict() for blk in self.global_blocks],
            navigation_index=self.navigation_index.index_map,
            style_config=self.style_config,
        )

    # -----------------------------
    #   OUTPUTS UTILITÁRIOS
    # -----------------------------

    def summary(self) -> Dict[str, Any]:
        """
        Retorna uma visão geral do documento para debug.
        """
        return {
            "title": self.title,
            "sections": [s.section_id for s in self.sections],
            "total_sections": len(self.sections),
            "total_blocks": sum(len(s.blocks) for s in self.sections),
            "global_blocks": len(self.global_blocks),
        }
