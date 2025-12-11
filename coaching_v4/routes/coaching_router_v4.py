# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\coaching_v4\routes\coaching_router_v4.py
# Última atualização: 2025-12-11T09:59:27.558489

from fastapi import APIRouter

router = APIRouter(prefix="/coaching-v4", tags=["Coaching AI v4"])

@router.get("/status")
async def status():
    return {"coaching_v4": "online"}
