# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\controllers\mindscan_controller.py
# Última atualização: 2025-12-11T09:59:20.745854

from fastapi import HTTPException
from backend.api.schemas.mindscan_models import (
    MindScanRunRequest,
    MindScanRunResponse
)
from backend.api.services.mindscan_service import MindScanService
from backend.api.services.session_gateway import SessionGateway


class MindScanController:

    @staticmethod
    def run(payload: MindScanRunRequest) -> MindScanRunResponse:

        try:
            session_id = payload.session_id or SessionGateway.start_session()

            result = MindScanService.run(
                user_id=payload.user_id,
                form_data=payload.form_data,
                report_type=payload.report_type
            )

            return MindScanRunResponse(
                status="success",
                message="Diagnóstico executado via controller",
                test_id=result["test_id"],
                session_id=session_id,
                report_url=result["report_url"],
                results=result["results"]
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
