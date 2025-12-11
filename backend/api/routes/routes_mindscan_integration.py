# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\routes\routes_mindscan_integration.py
# Última atualização: 2025-12-11T09:59:20.745854

from fastapi import APIRouter, HTTPException
from backend.api.schemas.mindscan_models import MindScanRunRequest, MindScanRunResponse
from backend.api.services.mindscan_service import MindScanService
from backend.api.services.session_gateway import SessionGateway

router = APIRouter(prefix="/mindscan", tags=["MindScan Integration"])


@router.post("/run", response_model=MindScanRunResponse)
async def run(payload: MindScanRunRequest):

    try:
        # Criar sessão nova se não existir
        session_id = payload.session_id or SessionGateway.start_session()

        result = MindScanService.run(
            user_id=payload.user_id,
            form_data=payload.form_data,
            report_type=payload.report_type
        )

        return MindScanRunResponse(
            status="success",
            message="Diagnóstico executado com sucesso",
            test_id=result["test_id"],
            session_id=session_id,
            report_url=result["report_url"],
            results=result["results"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
