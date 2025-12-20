from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from services.engine import MindScanEngine
from services.report_service import ReportService
import logging

router = APIRouter(prefix="/api/v1/diagnostic", tags=["MindScan-Diagnostic"])
report_service = ReportService()
engine = MindScanEngine()

@router.post("/generate-report")
async def generate_diagnostic_report(payload: dict):
    """
    Endpoint Principal para a reunião das 16h.
    Recebe os dados do candidato e devolve o PDF oficial SynMind.
    """
    try:
        # 1. Validação de integridade dos dados
        if not payload.get("responses") or not payload.get("name"):
            raise HTTPException(status_code=400, detail="Dados incompletos para diagnóstico.")

        # 2. Execução do motor de relatório (Cálculo + Narrativa + PDF)
        # O ReportService já utiliza o MindScanEngine internamente
        pdf_path = report_service.build_report(payload)
        
        if pdf_path and os.path.exists(pdf_path):
            return FileResponse(
                path=pdf_path, 
                filename=f"MindScan_Relatorio_{payload['name']}.pdf",
                media_type='application/pdf'
            )
        else:
            raise HTTPException(status_code=500, detail="Erro na geração do artefato PDF.")

    except Exception as e:
        logging.error(f"Falha crítica no router de diagnóstico: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/status")
async def get_router_status():
    """Verificação de prontidão do módulo."""
    return {
        "module": "diagnostic_router",
        "status": "active",
        "engine_connected": True,
        "pdf_service": "ready"
    }