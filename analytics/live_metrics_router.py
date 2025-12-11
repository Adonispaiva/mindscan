# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\analytics\live_metrics_router.py
# Última atualização: 2025-12-11T09:59:20.542656

# ============================================================
# MindScan — Live Metrics Router (SSE)
# ============================================================

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from analytics.live_metrics_service import LiveMetricsService

router = APIRouter(prefix="/live", tags=["Live Metrics"])

service = LiveMetricsService()


@router.get("/stream")
def stream_metrics():
    """
    Stream contínuo (SSE) de métricas em tempo real.
    """
    return StreamingResponse(
        service.stream(),
        media_type="text/event-stream"
    )
