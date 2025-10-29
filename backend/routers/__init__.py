# routers/__init__.py
# Importa rotas para facilitar registro no FastAPI

from .health import router as health_router
from .user import router as user_router
from .response import router as response_router
