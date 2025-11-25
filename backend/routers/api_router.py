from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Sub-routers existentes
from backend.routers.health_router import router as health_router
from backend.routers.users_router import router as users_router
from backend.routers.candidates_router import router as candidates_router
from backend.routers.tests_router import router as tests_router

# Serviços principais
from backend.services.auth_service import AuthService
from backend.services.data_service import DataService
from backend.services.report_service import ReportService

# Engine unificado
from backend.core.engine import MindScanEngine

# Modelos pendentes (serão criados na sequência)
# DiagnosticRequest
# DiagnosticResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# API ROOT
api_router = APIRouter(prefix="/api", tags=["MindScan API v2.0"])

# ==================================================
#  Dependência: Usuário atual (token JWT)
# ==================================================
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = AuthService.validate_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado."
        )
    return user

# ==================================================
#  Registro de sub-routers oficiais
# ==================================================
api_router.include_router(health_router)
api_router.include_router(users_router)
api_router.include_router(candidates_router)
api_router.include_router(tests_router)

# ==================================================
#  Endpoint Central do Diagnóstico
# ==================================================
@api_router.post("/diagnostic")
async def run_diagnostic(payload: dict, current_user: dict = Depends(get_current_user)):
    """
    Endpoint principal do MindScan.
    Versão superior — aguardando modelos definitivos (DiagnosticRequest / Response).
    """

    # 1. Preparar dataset do candidato
    dataset = DataService.prepare_dataset(payload)

    # 2. Processar via Engine
    engine = MindScanEngine()
    results = engine.process(dataset)

    # 3. Gerar PDF final do laudo
    pdf_path = ReportService.generate_pdf(
        user=current_user,
        diagnostic_data=results
    )

    # 4. Resposta temporária até os modelos formais
    return {
        "status": "ok",
        "report_url": pdf_path,
        "insights": results.get("insights"),
        "profile": results.get("profile"),
        "scores": results.get("scores")
    }

# ==================================================
#  Painel Administrativo (Milena)
# ==================================================
@api_router.get("/dashboard")
async def dashboard(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito ao painel administrativo."
        )

    settings = DataService.get_system_settings()

    return {
        "status": "ok",
        "settings": settings,
        "message": "Bem-vinda ao painel administrativo do MindScan, Milena."
    }
