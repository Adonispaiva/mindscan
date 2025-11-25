# ============================================================
# MindScan — Health Router
# ============================================================
# Rotas básicas para verificação de vida, integridade e status
# do servidor/backend/banco de dados.
# ------------------------------------------------------------

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from backend.database import get_session

router = APIRouter()


# ------------------------------------------------------------
# 1) STATUS DO SERVIDOR
# ------------------------------------------------------------
@router.get("/ping")
async def ping():
    """
    Verifica se a API está respondendo.
    """
    return {"status": "alive", "service": "MindScan Backend"}


# ------------------------------------------------------------
# 2) STATUS DO BANCO DE DADOS
# ------------------------------------------------------------
@router.get("/db")
async def db_status(session: AsyncSession = Depends(get_session)):
    """
    Verifica se o banco está online executando um SELECT simples.
    """
    try:
        result = await session.execute(text("SELECT 1"))
        _ = result.scalar()
        return {"database": "OK"}
    except Exception as e:
        return {"database": "ERROR", "detail": str(e)}


# ------------------------------------------------------------
# 3) STATUS COMPLETO DO SISTEMA
# ------------------------------------------------------------
@router.get("/full")
async def full_status(session: AsyncSession = Depends(get_session)):
    """
    Verifica backend + DB e retorna estado consolidado.
    """
    # Teste DB
    try:
        result = await session.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    return {
        "mindscan_api": "online",
        "version": "2.0.1",
        "database_online": db_ok,
    }
