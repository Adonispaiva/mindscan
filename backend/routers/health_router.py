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