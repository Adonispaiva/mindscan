# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\analytics\analytics_router.py
# Última atualização: 2025-12-11T09:59:20.542656

# ============================================================
# MindScan — Analytics Router
# ============================================================

from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from analytics.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])
analytics = AnalyticsService()


@router.get("/summary", response_model=Dict[str, Any])
def get_summary():
    try:
        return analytics.summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar analytics: {e}")
