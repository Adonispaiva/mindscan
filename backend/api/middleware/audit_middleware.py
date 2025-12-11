# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\middleware\audit_middleware.py
# Última atualização: 2025-12-11T09:59:20.745854

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time

class AuditMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start = time.time()

        response = await call_next(request)

        duration = round(time.time() - start, 3)
        method = request.method
        path = request.url.path
        status = response.status_code

        print(f"[AUDIT] {method} {path} → {status} | {duration}s")

        return response
