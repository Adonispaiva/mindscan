# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\web\web_app.py
# Última atualização: 2025-12-11T09:59:27.824087

from fastapi import FastAPI
from backend.api.routes.health_check_router import router as health_router

def create_web_app():
    app = FastAPI(title="MindScan Web Enterprise", version="4.0")
    app.include_router(health_router)
    return app
