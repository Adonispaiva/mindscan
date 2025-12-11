# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\auth\auth_router.py
# Última atualização: 2025-12-11T09:59:20.558303

# ============================================================
# MindScan — Auth Router (FastAPI)
# ============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

auth = AuthService()

# Usuário fixo para ambiente de demonstração
DEMO_USER = {
    "username": "admin",
    "password_hash": auth.hash_password("admin123")
}


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest):
    if req.username != DEMO_USER["username"]:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    if not auth.verify_password(req.password, DEMO_USER["password_hash"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access = auth.create_access_token({"sub": req.username})
    refresh = auth.create_refresh_token({"sub": req.username})

    return TokenResponse(access_token=access, refresh_token=refresh)


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/refresh", response_model=TokenResponse)
def refresh(req: RefreshRequest):
    try:
        payload = auth.decode_refresh(req.refresh_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Refresh token inválido")

    username = payload.get("sub")

    access = auth.create_access_token({"sub": username})
    refresh = auth.create_refresh_token({"sub": username})

    return TokenResponse(access_token=access, refresh_token=refresh)
