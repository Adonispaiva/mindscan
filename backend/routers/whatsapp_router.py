"""
Router Oficial do WhatsApp para o MindScan
Inovexa Software | SynMind | MindScan®

Funções expostas:
- /whatsapp/send          → Envio de mensagens simples
- /whatsapp/send-media    → Envio de mídia
- /whatsapp/send-report   → Envio automático de relatório MindScan
- /whatsapp/faq           → Atendimento básico
- /whatsapp/ai/ask        → IA Leve para dúvidas operacionais

Este router centraliza todas as rotas relacionadas ao WhatsApp
e delega lógica para os módulos:
- integrations.whatsapp
- integrations.whatsapp_ai
"""

from fastapi import APIRouter
from backend.integrations.whatsapp import (
    send_whatsapp_message,
    send_media,
    send_report,
    whatsapp_faq
)
from backend.integrations.whatsapp_ai import ai_whatsapp

router = APIRouter(prefix="/whatsapp", tags=["WhatsApp"])


# ---------------------------------------------------------
# Delegações diretas
# ---------------------------------------------------------

@router.post("/send")
def route_send(payload: dict):
    """
    Envio de mensagem simples (delegado ao módulo whatsapp).
    """
    return send_whatsapp_message(payload)


@router.post("/send-media")
def route_media(payload: dict):
    """
    Envio de mídia (delegado ao módulo whatsapp).
    """
    return send_media(payload)


@router.post("/send-report")
def route_report(payload: dict):
    """
    Envio do relatório MindScan (PDF via URL).
    """
    return send_report(payload)


@router.post("/faq")
def route_faq(payload: dict):
    """
    Atendimento básico pré-definido (concierge fixo).
    """
    return whatsapp_faq(payload)


@router.post("/ai")
def route_ai(payload: dict):
    """
    IA leve: responde dúvidas simples sobre o processo MindScan.
    """
    return ai_whatsapp(payload)
