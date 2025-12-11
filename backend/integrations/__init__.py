# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\integrations\__init__.py
# Última atualização: 2025-12-11T09:59:20.841083

"""
Pacote de Integração WhatsApp do MindScan®
Inovexa Software | SynMind

Exposição pública dos módulos:

- whatsapp          → Envio real via Twilio
- whatsapp_ai       → IA leve operacional
- whatsapp_utils    → Utilidades e saneamento
- whatsapp_handler  → Orquestração e gateway
"""

from .whatsapp import (
    send_whatsapp_message,
    send_media,
    send_report,
    whatsapp_faq,
)

from .whatsapp_ai import ai_whatsapp, ai_answer

from .whatsapp_utils import (
    sanitize_phone,
    format_message,
    normalize,
    fallback_send,
    validate_twilio_credentials,
)

from .whatsapp_handler import (
    handle_text_message,
    handle_media_message,
    handle_unknown,
)

__all__ = [
    # whatsapp
    "send_whatsapp_message",
    "send_media",
    "send_report",
    "whatsapp_faq",

    # ai
    "ai_whatsapp",
    "ai_answer",

    # utils
    "sanitize_phone",
    "format_message",
    "normalize",
    "fallback_send",
    "validate_twilio_credentials",

    # handler
    "handle_text_message",
    "handle_media_message",
    "handle_unknown",
]
