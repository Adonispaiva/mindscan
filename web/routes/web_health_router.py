# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\routes\web_health_router.py
# Última atualização: 2025-12-11T09:59:27.855343

from fastapi import APIRouter

router = APIRouter(prefix="/web-health", tags=["Health"])

@router.get("/")
async def health():
    return {"web": "online", "uptime": "stable"}
