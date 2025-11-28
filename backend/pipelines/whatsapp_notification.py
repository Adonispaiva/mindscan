# Caminho: D:\projetos-inovexa\mindscan\backend\pipelines\whatsapp_notification.py
"""
Integração WhatsApp ao Pipeline do MindScan
Inovexa Software | SynMind | MindScan®

Objetivo:
- Permitir que, após gerar o PDF do MindScan, o sistema notifique automaticamente
  o usuário via WhatsApp utilizando a Twilio API.

Este módulo NÃO interfere na lógica psicométrica.
Ele apenas consome o resultado final do MindScan (PDF) e executa a notificação.

Fluxo:
1. Pipeline gera PDF
2. Pipeline publica PDF (URL pública)
3. Pipeline chama notify_user_via_whatsapp()
4. WhatsApp envia o link ao usuário

"""

import logging
import requests
from pydantic import BaseModel

logger = logging.getLogger("whatsapp_pipeline")
logger.setLevel(logging.INFO)

# ---------------------------------------------------------
# MODELO DE NOTIFICAÇÃO
# ---------------------------------------------------------
class NotificationPayload(BaseModel):
    phone: str
    pdf_url: str

# ---------------------------------------------------------
# CONFIGURAÇÃO DO ENDPOINT WHATSAPP
# ---------------------------------------------------------
WHATSAPP_ENDPOINT = "http://localhost:8000/whatsapp/send-report"  # ajustar em produção

# ---------------------------------------------------------
# FUNÇÃO PRINCIPAL
# ---------------------------------------------------------
def notify_user_via_whatsapp(phone: str, pdf_url: str) -> dict:
    """
    Envia notificação automática ao usuário após o MindScan gerar o relatório.
    """
    logger.info(f"[Pipeline] Notificando usuário {phone} via WhatsApp...")

    payload = NotificationPayload(phone=phone, pdf_url=pdf_url)

    try:
        response = requests.post(WHATSAPP_ENDPOINT, json={
            "to": payload.phone,
            "pdf_url": payload.pdf_url
        })

        if response.status_code == 200:
            logger.info(f"[Pipeline] Envio concluído com sucesso → {phone}")
        else:
            logger.error(f"[Pipeline] Falha no envio WhatsApp: {response.text}")

        return {
            "status": response.status_code,
            "response": response.json() if response.content else {}
        }

    except Exception as e:
        logger.error(f"[Pipeline] Erro crítico no envio WhatsApp → {e}")
        return {"status": "error", "detail": str(e)}

# ---------------------------------------------------------
# FUNÇÃO AUXILIAR (HOOK DO PIPELINE)
# ---------------------------------------------------------
def mindscan_postprocess_hook(user_phone: str, pdf_url: str):
    """
    Deve ser chamada automaticamente logo após a geração do relatório MindScan.
    """
    logger.info("[Pipeline] Executando hook pós-processamento MindScan...")
    return notify_user_via_whatsapp(user_phone, pdf_url)
