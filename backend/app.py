# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\app.py
# Última atualização: 2025-12-11T09:59:20.558303

# app.py
# MindScan Backend - Arquitetura Oficial Inovexa
# Carrega todos os routers reais do diretório /routers
# NÃO ALTERAR A ESTRUTURA DE IMPORTS

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers reais do backend
from routers.api_router import router as api_router
from routers.candidates_router import router as candidates_router
from routers.diagnostic_router import router as diagnostic_router
from routers.health_router import router as health_router
from routers.mindscan_api import router as mindscan_router
from routers.tests_router import router as tests_router
from routers.users_router import router as users_router
from routers.whatsapp_router import router as whatsapp_router

# Configurações
from config import settings


# ============================================================
# Inicialização da API
# ============================================================

app = FastAPI(
    title="MindScan API",
    description="API oficial MindScan - Inovexa Intelligence",
    version="2.0",
)


# ============================================================
# Configuração de CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Registro dos routers reais
# ============================================================

app.include_router(api_router, prefix="/api", tags=["API Root"])
app.include_router(candidates_router, prefix="/candidates", tags=["Candidatos"])
app.include_router(diagnostic_router, prefix="/diagnostic", tags=["Diagnóstico Psicométrico"])
app.include_router(health_router, prefix="/health", tags=["Health Check"])
app.include_router(mindscan_router, prefix="/mindscan", tags=["Engine Psicométrico"])
app.include_router(tests_router, prefix="/tests", tags=["Testes e Blocos Psicométricos"])
app.include_router(users_router, prefix="/users", tags=["Usuários"])
app.include_router(whatsapp_router, prefix="/whatsapp", tags=["Integração WhatsApp"])


# ============================================================
# Rota raiz
# ============================================================

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "MindScan Backend",
        "version": "2.0",
        "environment": settings.ENV
    }


# ============================================================
# Execução local
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
