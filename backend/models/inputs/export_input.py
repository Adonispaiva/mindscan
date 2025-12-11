# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\export_input.py
# Última atualização: 2025-12-11T09:59:20.995650

from __future__ import annotations
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class ExportInput(BaseModel):
    """
    Entrada para exportação de relatórios e resultados.
    """

    candidate_id: str = Field(..., description="ID único do candidato.")
    session_id: Optional[str] = Field(None, description="ID da sessão de avaliação.")
    export_format: str = Field("pdf", description="Formato de exportação: pdf, json.")
    include_sections: Optional[Dict[str, bool]] = Field(
        default=None,
        description="Seções a serem incluídas na exportação."
    )
    metadata: Optional[Dict[str, Any]] = Field(default=None)
