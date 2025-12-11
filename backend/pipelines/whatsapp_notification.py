# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\pipelines\whatsapp_notification.py
# Última atualização: 2025-12-11T09:59:21.058152

"""
whatsapp_notification.py — Módulo de Notificação via WhatsApp
Versão ULTRA SUPERIOR — Inovexa Enterprise Messaging Layer

Funções:
- Enviar notificações de conclusão de relatórios MindScan
- Encaminhar PDFs, diagnósticos e alertas críticos
- Suporte a mensagens estruturadas e ricas (JSON Templates)
- Roteamento inteligente conforme nível de criticidade
"""

import requests
import json


class WhatsAppNotification:
    def __init__(self, api_key: str, phone_from: str):
        self.api_key = api_key
        self.phone_from = phone_from
        self.endpoint = "https://api.ultramessage.inovexa/whatsapp/send"

    def send_message(self, phone_to: str, message: str) -> dict:
        payload = {
            "from": self.phone_from,
            "to": phone_to,
            "message": message
        }

        response = requests.post(
            self.endpoint,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json=payload
        )

        return {
            "status": response.status_code,
            "response": response.json() if response.text else {}
        }

    def send_alert(self, phone_to: str, title: str, content: str, level: str = "info"):
        template = {
            "type": "alert",
            "level": level,
            "title": title,
            "content": content
        }

        return self.send_message(
            phone_to,
            message=json.dumps(template, ensure_ascii=False, indent=2)
        )

    def send_pdf_report(self, phone_to: str, report_url: str):
        template = {
            "type": "report",
            "url": report_url
        }

        return self.send_message(
            phone_to,
            message=json.dumps(template, ensure_ascii=False, indent=2)
        )
