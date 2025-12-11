# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\report_section.py
# Última atualização: 2025-12-11T09:59:20.980027

# D:\backend\models\report_section.py
# Modelo estrutural completo do MindScan — versão definitiva Inovexa Ultra

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, validator


class ReportSection(BaseModel):
    """
    Representa uma seção principal do relatório MindScan.
    Cada seção contém:
    - título
    - descrição opcional
    - blocos (subpartes)
    - metadados
    - instruções de renderização
    """

    id: str = Field(..., description="Identificador único da seção dentro do relatório.")
    title: str = Field(..., description="Título textual da seção.")
    description: Optional[str] = Field(
        None,
        description="Descrição geral da seção, usada em templates executivo e premium."
    )
    blocks: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Lista de blocos estruturados (ReportBlock transformado em dict)."
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados específicos, como peso, ordem, estilo, visibilidade."
    )
    style: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configurações de estilo aplicáveis ao renderer."
    )

    render_priority: int = Field(
        10,
        description="Quanto menor o número, mais cedo a seção aparece no PDF."
    )

    visible_in: List[str] = Field(
        default_factory=lambda: ["technical", "executive", "psychodynamic", "premium"],
        description="Define em quais templates a seção será usada."
    )

    @validator("id")
    def validate_id(cls, value):
        if " " in value:
            raise ValueError("O campo 'id' não pode conter espaços.")
        return value

    @validator("visible_in", each_item=True)
    def validate_template(cls, value):
        allowed = {"technical", "executive", "psychodynamic", "premium"}
        if value not in allowed:
            raise ValueError(
                f"Template inválido: {value}. Deve ser um de {allowed}"
            )
        return value

    def add_block(self, block_dict: Dict[str, Any]):
        """
        Adiciona um bloco à seção. O bloco deve vir formatado como dict
        (normalmente vindo de ReportBlock.to_dict()).
        """
        if not isinstance(block_dict, dict):
            raise ValueError("Blocks devem ser dicts derivados de ReportBlock.to_dict().")

        self.blocks.append(block_dict)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte a seção em um dicionário totalmente serializável,
        compatível com renderers e com o pipeline do ReportService.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "blocks": self.blocks,
            "metadata": self.metadata,
            "style": self.style,
            "render_priority": self.render_priority,
            "visible_in": self.visible_in,
        }

    def is_visible_for(self, template: str) -> bool:
        """
        Utilizado pelos renderers para determinar se uma seção deve
        ou não ser incluída no relatório.
        """
        return template in self.visible_in
