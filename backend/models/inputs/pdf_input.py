# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\inputs\pdf_input.py
# Última atualização: 2025-12-11T09:59:20.995650

from __future__ import annotations
from typing import Dict, Optional
from pydantic import BaseModel, Field


class PDFInput(BaseModel):
    """
    Entrada para geração de PDF final.
    """

    candidate_id: str = Field(..., description="ID único do candidato.")
    session_id: Optional[str] = Field(None)
    report_type: str = Field(..., description="Tipo de relatório: executivo, completo, lite, etc.")
    theme: Optional[str] = Field("default", description="Tema visual do relatório.")
    extra_data: Optional[Dict[str, str]] = Field(default=None)
