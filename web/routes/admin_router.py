# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\routes\admin_router.py
# Última atualização: 2025-12-11T09:59:27.839711

from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/status")
async def admin_status():
    return {"admin": "online"}
