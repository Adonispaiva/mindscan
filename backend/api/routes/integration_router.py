# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\routes\integration_router.py
# Última atualização: 2025-12-11T09:59:20.745854

from fastapi import APIRouter
from backend.integrations.webhooks.webhook_engine import WebhookEngine

router = APIRouter(prefix="/integrations", tags=["Integrations"])

@router.post("/webhook-test")
async def test_webhook(url: str):
    payload = {"message": "Webhook ativo", "status": "success"}
    ok = WebhookEngine.trigger(url, payload)
    return {"sent": ok}
