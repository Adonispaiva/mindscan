# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\user_output.py
# Última atualização: 2025-12-11T09:59:21.042587

# -*- coding: utf-8 -*-
"""
MindScan – User Output (Final Version)
--------------------------------------
Objeto final de saída do sistema MindScan, responsável por:

- Consolidar todas as seções do relatório
- Armazenar o resumo global/executivo
- Transportar dados para o BaseRenderer
- Organizar contexto diagnósticos
- Servir como saída oficial para API, WhatsApp e Dashboard

Inovexa Software — Arquitetura oficial do MindScan.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, validator


class ReportPayload(BaseModel):
    """
    Payload final montado pelo ReportEngine.

    Estrutura:

    - test_id: ID único do teste
    - context: contexto global (ReportContext serializado)
    - sections: lista de seções (cada uma gerada por ReportSection.to_dict())
    - summary: resumo executivo (ReportSummary.to_dict())
    - metadata: dados adicionais
    """

    test_id: str = Field(..., description="Identificador único do teste.")
    context: Dict[str, Any] = Field(
        ..., description="Contexto global do relatório (dict)."
    )
    sections: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Lista completa de seções estruturadas."
    )
    summary: Optional[Dict[str, Any]] = Field(
        None,
        description="Resumo global/executivo."
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadados globais do relatório."
    )

    @validator("test_id")
    def validate_test_id(cls, value):
        if not value or not isinstance(value, str):
            raise ValueError("test_id deve ser uma string válida e não vazia.")
        return value

    @validator("context")
    def validate_context(cls, value):
        if not isinstance(value, dict):
            raise ValueError("context deve ser um dict (ReportContext serializado).")
        return value

    @validator("sections", each_item=True)
    def validate_each_section(cls, value):
        if not isinstance(value, dict):
            raise ValueError("Cada seção deve ser um dict válido.")
        if "id" not in value:
            raise ValueError("Cada seção deve conter um campo 'id'.")
        return value

    def get_section(self, section_id: str) -> Optional[Dict[str, Any]]:
        """
        Retorna uma seção específica pelo ID.
        """
        for sec in self.sections:
            if sec.get("id") == section_id:
                return sec
        return None

    def has_section(self, section_id: str) -> bool:
        """
        Verifica se uma seção existe.
        """
        return any(sec.get("id") == section_id for sec in self.sections)

    def to_render_dict(self) -> Dict[str, Any]:
        """
        Estrutura final usada pelos renderizadores.

        {  
          "test_id": str,
          "context": {...},
          "sections": [...],
          "summary": {...},
          "metadata": {...}
        }
        """
        return {
            "test_id": self.test_id,
            "context": self.context,
            "sections": self.sections,
            "summary": self.summary,
            "metadata": self.metadata,
        }

    def add_section(self, section_dict: Dict[str, Any]):
        """
        Adiciona uma nova seção ao payload.
        """
        if not isinstance(section_dict, dict):
            raise ValueError("section_dict deve ser um dict válido.")
        self.sections.append(section_dict)

    def set_summary(self, summary_dict: Dict[str, Any]):
        """
        Define o resumo executivo.
        """
        if not isinstance(summary_dict, dict):
            raise ValueError("summary_dict deve ser um dict válido.")
        self.summary = summary_dict
