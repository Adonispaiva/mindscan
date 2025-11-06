from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import platform, datetime

from database import AsyncSessionLocal  # ✅ desacoplado do main

router = APIRouter(tags=["Health"])

# ── Dependência de sessão ──────────────────────────────────────────────
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# ── Endpoint de verificação ────────────────────────────────────────────
@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Verifica o status do banco e retorna informações do sistema.
    Compatível com CI/CD e monitoramento externo.
    """
    try:
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {e}"

    return {
        "status": "ok",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "database": db_status,
        "system": platform.system(),
        "release": platform.release(),
        "python_version": platform.python_version()
    }
