# MindScan Backend — API Router Central
# Arquitetura oficial MindScan v2.0 — Inovexa Software

from fastapi import APIRouter

# ============================================================
# IMPORTS ABSOLUTOS CORRETOS (Docker / Render safe)
# ============================================================

from backend.routers.health_router import router as health_router
from backend.routers.users_router import router as users_router
from backend.routers.candidates_router import router as candidates_router
from backend.routers.tests_router import router as tests_router
from backend.routers.diagnostic_router import router as diagnostic_router
from backend.routers.dashboard_router import router as dashboard_router

# ============================================================
# API Router Principal
# ============================================================

api_router = APIRouter(prefix="/api", tags=["MindScan API v2.0"])

# Registro dos subrouters

api_router.include_router(health_router, prefix="/health", tags=["Health"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(candidates_router, prefix="/candidates", tags=["Candidates"])
api_router.include_router(tests_router, prefix="/tests", tags=["Tests"])
api_router.include_router(diagnostic_router, prefix="/diagnostic", tags=["Diagnostic"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])

# ============================================================
# Rota Raiz da API
# ============================================================

@api_router.get("/", summary="API Root", tags=["Root"])
def api_root():
    return {
        "name": "MindScan Backend API v2.0",
        "status": "online",
        "routers": [
            "health",
            "users",
            "candidates",
            "tests",
            "diagnostic",
            "dashboard",
        ],
    }
