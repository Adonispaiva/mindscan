# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\routes\health_check_router.py
# Última atualização: 2025-12-11T09:59:20.745854

from fastapi import APIRouter
from backend.analytics.metrics.metrics_service import MetricsService

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/")
async def get_health():
    return {
        "status": "online",
        "service": "MindScan Enterprise",
        "metrics": MetricsService.get_snapshot()
    }
