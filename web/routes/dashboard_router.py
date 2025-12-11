# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\routes\dashboard_router.py
# Última atualização: 2025-12-11T09:59:27.839711

from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/overview")
async def overview():
    return {"status": "ok", "message": "Dashboard Online"}
