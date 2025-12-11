# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\routes\analytics_router.py
# Última atualização: 2025-12-11T09:59:27.839711

from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/overview")
async def analytics_overview():
    return {"analytics": "online"}
