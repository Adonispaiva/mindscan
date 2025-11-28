# Caminho: D:\projetos-inovexa\mindscan\backend\integrations\whatsapp_handler.py
"""
Handler oficial do WhatsApp para o MindScan
Inovexa Software | SynMind | MindScan®

Funções incluídas:
- Orquestração entre utils, IA e envio real
- Registros de auditoria
- Gateway unificado para o WhatsApp
- Tratamento de exceções
- Segurança e fallback
"""

import logging
from backend.integrations.whatsapp_utils import (
    sanitize_phone,
    format_message,
    normalize,
    fallback_send,
)
from backend.integrations.whatsapp import _send_text, _send_media
from backend.integrations.whatsapp_ai import ai_answer

logger = logging.getLogger("whatsapp_handler")
logger.setLevel(logging.INFO)

# ---------------------------------------------------------
# Handler principal
# ---------------------------------------------------------
def handle_text_message(to: str, message: str):
    """
    Processa uma mensagem de texto recebida do usuário
    e decide qual ação tomar.
    """
    try:
        phone = sanitize_phone(to)
        clean = format_message(message)
        norm = normalize(clean)

        logger.info(f"[Handler] Mensagem recebida de {phone}: {clean}")

        # IA leve
        reply = ai_answer(norm)

        result = _safe_send(phone, reply)
        return {"status": "success", "reply": reply, "sid": result.get("sid")}

    except Exception as e:
        logger.error(str(e))
        fallback_send(to, "Ocorreu um erro temporário. Tente novamente em instantes.")
        return {"status": "error", "detail": str(e)}


# ---------------------------------------------------------
# Envio seguro com fallback
# ---------------------------------------------------------
def _safe_send(to: str, message: str):
    try:
        return _send_text(to, message)
    except Exception as e:
        logger.error(f"Erro no Twilio: {e}")
        return fallback_send(to, message)


# ---------------------------------------------------------
# Envio de mídia seguro
# ---------------------------------------------------------
def handle_media_message(to: str, media_url: str, caption: str = ""):
    try:
        phone = sanitize_phone(to)
        result = _send_media(phone, media_url, caption)
        return {"status": "success", "sid": result.sid}
    except Exception as e:
        logger.error(str(e))
        return fallback_send(to, caption or "Arquivo enviado.")


# ---------------------------------------------------------
# Resposta padrão para mensagens fora do escopo
# ---------------------------------------------------------
def handle_unknown(to: str):
    msg = (
        "Não consegui entender totalmente sua pergunta. "
        "Posso te ajudar com dúvidas como: 'como preencher', 'tempo', 'relatório', 'acesso'."
    )
    return _safe_send(to, msg)
