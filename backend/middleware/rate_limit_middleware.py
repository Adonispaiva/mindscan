# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\middleware\rate_limit_middleware.py
# Última atualização: 2025-12-11T09:59:20.948776

import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware de proteção contra abuso:
    Limita requisições por IP.
    """

    window_seconds = 10
    max_requests = 20
    access_log = {}

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        current_time = time.time()

        # Inicializa janela
        if ip not in self.access_log:
            self.access_log[ip] = []

        # Remove requisições antigas
        self.access_log[ip] = [
            t for t in self.access_log[ip]
            if current_time - t < self.window_seconds
        ]

        # Verifica limite
        if len(self.access_log[ip]) >= self.max_requests:
            raise HTTPException(
                status_code=429,
                detail="Limite de requisições excedido. Tente novamente mais tarde."
            )

        # Registra requisição atual
        self.access_log[ip].append(current_time)

        response = await call_next(request)
        return response
