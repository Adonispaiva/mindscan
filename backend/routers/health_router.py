# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\routers\health_router.py
# Última atualização: 2025-12-11T09:59:21.089476

# Caminho: backend/routers/health_router.py
# MindScan Backend — Health Check Router
# Diretor Técnico: Leo Vinci — Inovexa Software
# Versão Final — MindScan v2.0

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/", summary="Health Check")
def health_status():
    return {
        "service": "MindScan Backend API v2.0",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }