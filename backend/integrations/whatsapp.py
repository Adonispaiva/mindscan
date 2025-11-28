"""
Módulo Oficial de Integração WhatsApp (Twilio API)
MindScan® — Inovexa Software | SynMind

Funções incluídas:
- Envio de mensagens WhatsApp
- Envio de mensagens com mídia
- Envio automatizado do relatório MindScan em PDF
- Atendimento básico (FAQ + orientações de preenchimento)
- Fallback seguro
- Logging integrado
"""

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from twilio.rest import Client
import os
import logging

# ---------------------------------------------------------
# Configurações (chaves devem ser armazenadas em variáveis de ambiente)
# ---------------------------------------------------------

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "CHAVE_AQUI")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "TOKEN_AQUI")
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Número padrão Twilio Sandbox

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Inicialização do router
router = APIRouter(prefix="/whatsapp", tags=["WhatsApp Integration"])

# Logger
logger = logging.getLogger("whatsapp")
logger.setLevel(logging.INFO)


# ---------------------------------------------------------
# MODELOS
# ---------------------------------------------------------
class WhatsAppMessage(BaseModel):
    to: str
    message: str


class WhatsAppMediaMessage(BaseModel):
    to: str
    media_url: str
    caption: str | None = None


class AutoSendReport(BaseModel):
    to: str
    pdf_url: str  # PDF precisa estar hospedado publicamente


class BasicQuestion(BaseModel):
    to: str
    question: str


# ---------------------------------------------------------
# FUNÇÕES INTERNAS
# ---------------------------------------------------------
def _sanitize(phone: str):
    """Garante padrão internacional."""
    phone = phone.replace("+", "").replace(" ", "").replace("-", "")
    return f"whatsapp:+{phone}"


def _send_text(to: str, message: str):
    """Função interna de envio de texto."""
    final_number = _sanitize(to)
    logger.info(f"Enviando mensagem WhatsApp para {final_number}")

    return client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body=message,
        to=final_number
    )


def _send_media(to: str, media_url: str, caption: str = ""):
    """Função interna de envio de mídia."""
    final_number = _sanitize(to)
    logger.info(f"Enviando mídia WhatsApp para {final_number}")

    return client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        media_url=[media_url],
        body=caption,
        to=final_number
    )


# ---------------------------------------------------------
# ENDPOINTS OFICIAIS
# ---------------------------------------------------------

@router.post("/send")
def send_whatsapp_message(payload: WhatsAppMessage):
    try:
        result = _send_text(payload.to, payload.message)
        return {"status": "success", "sid": result.sid}
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-media")
def send_media(payload: WhatsAppMediaMessage):
    try:
        result = _send_media(payload.to, payload.media_url, payload.caption or "")
        return {"status": "success", "sid": result.sid}
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-report")
def send_report(payload: AutoSendReport):
    """
    Envia automaticamente o relatório MindScan via WhatsApp.
    OBS: Twilio exige URL pública para mídia.
    """
    try:
        result = _send_media(payload.to, payload.pdf_url, "Seu relatório MindScan está disponível.")
        return {"status": "success", "sid": result.sid}
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------
# ATENDIMENTO BÁSICO (FAQ)
# ---------------------------------------------------------
BASIC_RESPONSES = {
    "ola": "Olá! 👋 Aqui é o canal oficial do MindScan. Como posso ajudar?",
    "bom dia": "Bom dia! 😊 Como posso te orientar sobre o MindScan?",
    "como funciona": "O MindScan é um diagnóstico psicoprofissional. Você receberá perguntas objetivas — basta responder com sinceridade.",
    "como preencher": "Reserve um ambiente calmo. Leia cada pergunta com atenção e responda de forma autêntica.",
    "demora": "O preenchimento leva de 5 a 10 minutos.",
    "duvidas": "Posso te ajudar com dúvidas sobre: preenchimento, acesso e orientações gerais.",
    "relatorio": "Seu relatório é gerado automaticamente ao final do processo.",
    "link": "Você receberá o link de preenchimento diretamente pelo RH/consultor responsável.",
}


def _faq_answer(question: str) -> str:
    q = question.lower().strip()

    for key in BASIC_RESPONSES:
        if key in q:
            return BASIC_RESPONSES[key]

    return (
        "Posso te ajudar com dúvidas simples sobre o MindScan. "
        "Pergunte por: 'como funciona', 'como preencher', 'relatório', 'tempo', etc."
    )


@router.post("/faq")
def whatsapp_faq(payload: BasicQuestion):
    """Responde dúvidas simples."""
    try:
        reply = _faq_answer(payload.question)
        result = _send_text(payload.to, reply)
        return {"status": "success", "sid": result.sid, "reply": reply}
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))
