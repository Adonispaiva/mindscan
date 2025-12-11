# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\admin\admin_router.py
# Última atualização: 2025-12-11T09:59:20.542656

# ============================================================
# MindScan — Admin Router (Histórico + Auditoria)
# ============================================================

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from logging.logging_service import LoggingService

router = APIRouter(prefix="/admin", tags=["Admin"])

logs = LoggingService()


@router.get("/reports", response_model=List[Dict[str, Any]])
def list_reports(limit: int = 50):
    """
    Lista os relatórios gerados recentemente.
    """
    try:
        return logs.list_entries(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler logs: {e}")
