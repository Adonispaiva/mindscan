# MindScan Backend — API Router Central
# Arquitetura oficial MindScan v2.0 — Inovexa Software

from fastapi import APIRouter

# ============================================================
# IMPORTS SEGUROS (compatíveis com sua estrutura real)
# ============================================================

try:
    from routers.health_router import router as health_router
except Exception:
    health_router = None

try:
    from routers.users_router import router as users_router
except Exception:
    users_router = None

try:
    from routers.candidates_router import router as candidates_router
except Exception:
    candidates_router = None

try:
    from routers.tests_router import router as tests_router
except Exception:
    tests_router = None

try:
    from routers.diagnostic_router import router as diagnostic_router
except Exception:
    diagnostic_router = None

try:
    from routers.dashboard_router import router as dashboard_router
except Exception:
    dashboard_router = None

# ============================================================
# API Router Principal
# ============================================================

api_router = APIRouter(prefix="/api", tags=["MindScan API v2.0"])

# Registro seguro dos subrouters

if health_router:
    api_router.include_router(health_router, prefix="/health", tags=["Health"])

if users_router:
    api_router.include_router(users_router, prefix="/users", tags=["Users"])

if candidates_router:
    api_router.include_router(candidates_router, prefix="/candidates", tags=["Candidates"])

if tests_router:
    api_router.include_router(tests_router, prefix="/tests", tags=["Tests"])

if diagnostic_router:
    api_router.include_router(diagnostic_router, prefix="/diagnostic", tags=["Diagnostic"])

if dashboard_router:
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
