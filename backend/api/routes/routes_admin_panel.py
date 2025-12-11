# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\routes\routes_admin_panel.py
# Última atualização: 2025-12-11T09:59:20.745854

from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["Admin Panel"])

@router.get("/status")
async def get_status():
    return {
        "status": "online",
        "service": "MindScan Admin Panel",
        "version": "1.0"
    }
