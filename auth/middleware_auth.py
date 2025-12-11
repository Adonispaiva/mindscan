# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\auth\middleware_auth.py
# Última atualização: 2025-12-11T09:59:20.558303

# ============================================================
# MindScan — Auth Middleware
# ============================================================

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .auth_service import AuthService

auth = AuthService()

PROTECTED_ENDPOINTS = [
    "/mindscan/mi-hybrid"   # proteger MI híbrido
]


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        # Se a rota não é protegida → segue
        if not any(request.url.path.startswith(ep) for ep in PROTECTED_ENDPOINTS):
            return await call_next(request)

        # Verificar header Authorization: Bearer <token>
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse({"detail": "Auth token ausente"}, status_code=401)

        try:
            scheme, token = auth_header.split()
        except ValueError:
            return JSONResponse({"detail": "Token malformatado"}, status_code=401)

        if scheme.lower() != "bearer":
            return JSONResponse({"detail": "Esquema inválido"}, status_code=401)

        try:
            auth.decode_access(token)
        except Exception:
            return JSONResponse({"detail": "Token inválido ou expirado"}, status_code=401)

        return await call_next(request)
