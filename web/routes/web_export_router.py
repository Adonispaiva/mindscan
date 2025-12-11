# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\routes\web_export_router.py
# Última atualização: 2025-12-11T09:59:27.855343

from fastapi import APIRouter

router = APIRouter(prefix="/export", tags=["Export"])

@router.get("/health")
async def export_health():
    return {"export": "active"}
