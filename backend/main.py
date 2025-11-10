from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from config import DATABASE_URL, ALLOWED_ORIGINS
from database import engine, Base, init_db  # ✅ banco desacoplado
from routers import quiz, auth, admin, health, user, response  # ✅ uso do diretório real
from routes import diagnostic_router  # 🧠 nova rota de diagnóstico MI

# -------------------------------------------------------------------------
# LOGGING
# -------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------------
# APLICAÇÃO FASTAPI
# -------------------------------------------------------------------------
app = FastAPI(
    title="MindScan API",
    version="2.1.0",
    description="API do sistema MindScan - Inovexa"
)

# -------------------------------------------------------------------------
# CORS CONFIGURATION
# -------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------------------
# EVENTOS DE STARTUP E SHUTDOWN
# -------------------------------------------------------------------------
@app.on_event("startup")
async def on_startup():
    """Inicializa banco e valida conexão."""
    try:
        await init_db()
        logger.info("✅ Banco inicializado e tabelas validadas com sucesso.")
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar o banco de dados: {e}")


@app.on_event("shutdown")
async def on_shutdown():
    """Evento de desligamento do app."""
    logger.info("🛑 Encerrando MindScan API...")

# -------------------------------------------------------------------------
# ROTAS PRINCIPAIS
# -------------------------------------------------------------------------
app.include_router(quiz.router, prefix="/quiz", tags=["Quiz"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(response.router, prefix="/response", tags=["Response"])
app.include_router(diagnostic_router.router, prefix="/diagnostic", tags=["Diagnóstico"])

# -------------------------------------------------------------------------
# ENDPOINT RAIZ (INFORMATIVO)
# -------------------------------------------------------------------------
@app.get("/")
async def root():
    """Endpoint de boas-vindas da API."""
    return {
        "message": "MindScan API operacional com backend assíncrono.",
        "database": DATABASE_URL.split('/')[-1],
        "version": "2.1.0"
    }

# -------------------------------------------------------------------------
# EXECUÇÃO DIRETA (LOCAL)
# -------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)