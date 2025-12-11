# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\integrations\whatsapp\whatsapp_gateway.py
# Última atualização: 2025-12-11T09:59:20.856706

import json
import requests

class WhatsAppGateway:
    """
    Camada oficial de envio de mensagens WhatsApp pelo MindScan.
    """

    @staticmethod
    def send_message(phone: str, text: str, token: str, api_url: str) -> bool:
        payload = {
            "phone": phone,
            "message": text
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(api_url, headers=headers, data=json.dumps(payload))
            return response.status_code in [200, 201]
        except Exception:
            return False
