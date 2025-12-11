# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\diagnostic_report_output.py
# Última atualização: 2025-12-11T09:59:21.026903

from __future__ import annotations

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class DiagnosticReportOutput(BaseModel):
    """
    Estrutura que consolida o diagnóstico final no formato utilizado
    especificamente pelo gerador de PDF.

    Ela recebe os outputs consolidados (DiagnosticOutput) e expande com:
    - blocos prontos de narrativa
    - seções formatadas
    - estruturas finais consumidas por pdf_sections/*
    """

    candidate_id: str = Field(..., description="ID único do candidato.")
    session_id: Optional[str] = Field(default=None)

    sections: Dict[str, str] = Field(
        default_factory=dict,
        description="Texto final de cada seção do relatório."
    )

    insights: Dict[str, Any] = Field(
        default_factory=dict,
        description="Conjunto de insights destacados para o relatório."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_pdf_payload(self) -> Dict[str, Any]:
        return self.dict()
