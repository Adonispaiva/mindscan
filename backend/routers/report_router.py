# ===============================================================
#  ROTEADOR: REPORT ROUTER
#  Projeto: MindScan — SynMind MI v2.0
#  Autor: Leo Vinci (GPT Inovexa)
#  Data: 07/11/2025
#  Função: Endpoint REST para geração e entrega de relatório PDF
# ===============================================================

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from backend.modules.report_generator import gerar_relatorio_pdf
import io

router = APIRouter(prefix="/report", tags=["Report Generator"])

# ---------------------------------------------------------------
# Modelo de entrada
# ---------------------------------------------------------------
class ReportRequest(BaseModel):
    nome: str = Field(..., description="Nome do usuário")
    scores: dict = Field(..., description="Pontuações DASS-21")
    quadrante: str = Field(..., description="Quadrante da Bússola SynMind")
    score_performance: float = Field(..., description="Score de performance global (%)")
    relatorio_mi: str = Field(..., description="Texto interpretativo gerado pela MI")

# ---------------------------------------------------------------
# Endpoint principal: POST /report/generate
# ---------------------------------------------------------------
@router.post("/generate")
async def generate_report(payload: ReportRequest):
    """
    Gera e retorna o relatório PDF completo do MindScan SynMind v2.0.
    """
    try:
        pdf_bytes = gerar_relatorio_pdf(payload.dict())
        pdf_stream = io.BytesIO(pdf_bytes)

        filename = f"Relatorio_MindScan_{payload.nome.replace(' ', '_')}.pdf"

        return StreamingResponse(
            pdf_stream,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar relatório PDF: {str(e)}")
