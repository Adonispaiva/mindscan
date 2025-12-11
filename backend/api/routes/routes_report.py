# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\routes\routes_report.py
# Última atualização: 2025-12-11T09:59:20.761538

# -*- coding: utf-8 -*-
"""
Rotas Report — MindScan Corporate
---------------------------------
Registra o controller de relatórios no router principal.
"""

from fastapi import APIRouter
from api.controllers.report_controller import router as report_router

report_routes = APIRouter()
report_routes.include_router(report_router)
