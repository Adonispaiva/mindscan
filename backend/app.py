# app.py
# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Arquitetura oficial Inovexa
# Carrega todos os routers reais do diretório backend/routers

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers (imports absolutos – padrão produção)
from backend.routers.api_router import router as api_router
from backend.routers.candidates_router import router as candidates_router
from backend.routers.diagnostic_router import router as diagnostic_router
from backend.routers.health_router import router as health_router
from backend.routers.mindscan_api import router as mindscan_router
from backend.routers.tests_router import router as tests_router
from backend.routers.users_router import router as users_router
from backend.routers.whatsapp_router import router as whatsapp_router

# Configurações
from backend.config import settings


# =========================================================
# Inicialização da API
# =========================================================

app = FastAPI(
    title="MindScan API",
    description="API oficial MindScan - Inovexa Intelligence",
    version="2.0",
)


# =========================================================
# Configuração de CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# Registro dos routers
# =========================================================

app.include_router(api_router)
app.include_router(candidates_router)
app.include_router(diagnostic_router)
app.include_router(health_router)
app.include_router(mindscan_router)
app.include_router(tests_router)
app.include_router(users_router)
app.include_router(whatsapp_router)


# =========================================================
# Healthcheck raiz
# =========================================================

@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "MindScan API",
        "version": "2.0"
    }
