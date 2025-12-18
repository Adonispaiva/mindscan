from fastapi import APIRouter
from mindscan.router import load_router

router = APIRouter()

ROUTERS = [
    "mindscan.backend.routers.health_router",
    "mindscan.backend.routers.api_router",
    "mindscan.backend.routers.mindscan_router",
    "mindscan.backend.routers.report_router",

    # 🔥 NOVO: WebApp
    "mindscan.web.router",
]

for router_path in ROUTERS:
    load_router(router, router_path)
