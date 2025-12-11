# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\middleware\web_auth_middleware.py
# Última atualização: 2025-12-11T09:59:27.839711

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException, Request

class WebAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware simples de autenticação Web para o portal.
    """

    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("X-MIND-AUTH")
        if not token:
            raise HTTPException(status_code=401, detail="Auth Token Missing")
        return await call_next(request)
