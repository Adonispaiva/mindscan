# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\routes\session_auth_router.py
# Última atualização: 2025-12-11T09:59:27.855343

from fastapi import APIRouter

router = APIRouter(prefix="/session", tags=["Session/Auth"])

@router.get("/check")
async def check():
    return {"session": "valid"}
