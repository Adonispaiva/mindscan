# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\controllers\report_controller.py
# Última atualização: 2025-12-11T09:59:20.745854

# -*- coding: utf-8 -*-
"""
Report Controller — MindScan Corporate
-------------------------------------

Recebe payloads via API e dispara a geração de relatórios.
"""

from fastapi import APIRouter, HTTPException
from api.schemas.report_schema import ReportPayload, ReportResponse
from services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/generate", response_model=ReportResponse)
def generate_report(payload: ReportPayload):
    """
    Gera relatório MindScan Corporate (HTML + PDF).
    """
    try:
        service = ReportService()
        result = service.generate_report(payload.dict())
        return ReportResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar relatório: {e}")
