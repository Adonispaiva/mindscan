# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\router.py
# Última atualização: 2025-12-11T09:59:20.745854

from fastapi import APIRouter

# Importações dos módulos oficiais
from backend.api.routes.routes_report import router as report_router
from backend.api.routes.routes_mindscan_integration import router as mindscan_router
from backend.api.routes.routes_auth import router as auth_router if 'routes_auth' in globals() else None
from backend.api.routes.routes_admin import router as admin_router if 'routes_admin' in globals() else None
from backend.api.routes.routes_analytics import router as analytics_router if 'routes_analytics' in globals() else None

api_router = APIRouter()


# ----------------------------------------------------------
# REGISTRO OFICIAL DAS ROTAS DO MINDSCAN ENTERPRISE
# ----------------------------------------------------------

# Rota do Sistema de Relatórios (templates, PDF, etc.)
api_router.include_router(report_router)

# Rota oficial de integração MindScan Web → Engine
api_router.include_router(mindscan_router)

# Rotas opcionais (caso o projeto as possua)
if auth_router:
    api_router.include_router(auth_router)

if admin_router:
    api_router.include_router(admin_router)

if analytics_router:
    api_router.include_router(analytics_router)


# ----------------------------------------------------------
# ROTA RAIZ PARA TESTE E MONITORAMENTO
# ----------------------------------------------------------
@api_router.get("/")
async def root():
    return {
        "status": "online",
        "service": "MindScan Enterprise API",
        "version": "3.0",
        "message": "Backend ativo e integrado."
    }
