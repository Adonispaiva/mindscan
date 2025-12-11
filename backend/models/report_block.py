# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\report_block.py
# Última atualização: 2025-12-11T09:59:20.980027

# D:\backend\models\report_block.py
# Arquivo definitivo — Estrutura completa do ReportBlock para o MindScan

from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field, validator


class ReportBlock(BaseModel):
    """
    Representa um bloco dentro de uma seção do relatório.
    Um bloco pode conter:
      - título
      - texto
      - lista de itens
      - dados estruturados (scores, dicts complexos)
      - estilo específico
      - instruções para renderização
    """

    id: str = Field(..., description="Identificador único do bloco.")
    title: Optional[str] = Field(
        None,
        description="Título do bloco. Opcional dependendo do template."
    )
    content: Optional[str] = Field(
        None,
        description="Conteúdo textual principal do bloco."
    )
    items: Optional[List[str]] = Field(
        None,
        description="Lista de itens (usada em resumos, recomendações, pontos fortes)."
    )
    data: Optional[Dict[str, Any]] = Field(
        None,
        description="Dados estruturados: pontuações, mapas, insights, tabelas, etc."
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configurações personalizadas: peso, alinhamento, categorias."
    )
    style: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configurações visuais para o bloco."
    )

    visible_in: List[str] = Field(
        default_factory=lambda: ["technical", "executive", "psychodynamic", "premium"],
        description="Templates nos quais o bloco deve ser renderizado."
    )

    @validator("id")
    def validate_id(cls, value):
        if " " in value:
            raise ValueError("O campo 'id' não pode conter espaços.")
        return value

    @validator("items", pre=True)
    def convert_single_item_to_list(cls, value):
        """Permite que o usuário envie string ao invés de lista."""
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

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o bloco inteiro em um dicionário 100% serializável,
        pronto para ser consumido pelos renderers.
        """
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "items": self.items,
            "data": self.data,
            "metadata": self.metadata,
            "style": self.style,
            "visible_in": self.visible_in,
        }

    def is_visible_for(self, template: str) -> bool:
        """Define se o bloco aparece no template selecionado."""
        return template in self.visible_in
