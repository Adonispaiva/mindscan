# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\outputs\pdf_output.py
# Última atualização: 2025-12-11T09:59:21.026903

from __future__ import annotations

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class PDFOutput(BaseModel):
    """
    Estrutura final gerada antes da construção do PDF.

    Cada chave representa uma seção processada em `pdf_sections/*`,
    já com o texto final formatado.
    """

    candidate_id: str = Field(..., description="ID do candidato.")
    session_id: Optional[str] = Field(default=None)

    sections: Dict[str, str] = Field(
        default_factory=dict,
        description="Texto final de cada seção do relatório."
    )

    assets: Dict[str, Any] = Field(
        default_factory=dict,
        description="Imagens, gráficos ou artefatos gerados para o PDF."
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_pdf_payload(self) -> Dict[str, Any]:
        return self.dict()
