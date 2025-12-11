# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\integrations\webhooks\webhook_engine.py
# Última atualização: 2025-12-11T09:59:20.856706

import json
import requests

class WebhookEngine:
    """
    Envia notificações para URLs externas (mindscan_web, Slack, serviços terceiros).
    """

    @staticmethod
    def trigger(url: str, payload: dict) -> bool:
        try:
            response = requests.post(url, json=payload, timeout=5)
            return response.status_code in [200, 201, 202]
        except Exception:
            return False
