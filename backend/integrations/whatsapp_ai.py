# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\integrations\whatsapp_ai.py
# Última atualização: 2025-12-11T09:59:20.841083

# Caminho recomendado: D:\projetos-inovexa\mindscan\backend\integrations\whatsapp_ai.py
"""
Módulo IA de Atendimento Básico via WhatsApp
MindScan® / Inovexa Software / SynMind

Função:
- Atender o usuário via WhatsApp com respostas simples e administrativas.
- Não interfere no núcleo psicométrico.
- IA leve (NLP) com heurística + instruções estáveis.

Depende da integração Twilio do arquivo whatsapp.py.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

router = APIRouter(prefix="/whatsapp/ai", tags=["WhatsApp AI"])

logger = logging.getLogger("whatsapp_ai")
logger.setLevel(logging.INFO)

# ---------------------------------------------------------
# Modelo de entrada do usuário
# ---------------------------------------------------------
class AIQuery(BaseModel):
    to: str
    message: str

# ---------------------------------------------------------
# Base de respostas IA leve (concierge)
# ---------------------------------------------------------
IA_KNOWLEDGE = {
    "como funciona": "O MindScan é um diagnóstico psicoprofissional. Você responde perguntas objetivas e recebe um relatório completo.",
    "como preencher": "Procure um ambiente calmo, leia com atenção e responda com sinceridade. Leva de 5 a 10 minutos.",
    "tempo": "O MindScan leva em média de 5 a 10 minutos para ser preenchido.",
    "relatorio": "Seu relatório é gerado automaticamente ao final do processo e enviado pelo RH ou consultor.",
    "link": "O link de acesso é enviado diretamente pelo RH ou consultor responsável.",
    "duvida": "Posso te ajudar com dúvidas simples sobre preenchimento, acesso e etapas do processo.",
    "acesso": "Se tiver dificuldade no link, tente abrir no modo anônimo ou verifique a internet.",
    "finalizei": "Ao finalizar, uma tela de confirmação aparece. Depois disso, o relatório é processado.",
    "erro": "Se aparecer algum erro, tente atualizar a página ou abrir no navegador Chrome.",
}

# fallback universal
DEFAULT_RESPONSE = (
    "Posso te ajudar com dúvidas básicas sobre o MindScan:"
    " digite por exemplo 'como preencher', 'tempo', 'relatório', 'acesso'."
)

# ---------------------------------------------------------
# IA Leve – heurística determinística
# ---------------------------------------------------------
def ai_answer(text: str) -> str:
    text = text.lower().strip()

    for key in IA_KNOWLEDGE:
        if key in text:
            return IA_KNOWLEDGE[key]

    return DEFAULT_RESPONSE

# ---------------------------------------------------------
# Envio via módulo whatsapp.py (chamada indireta)
# ---------------------------------------------------------
try:
    from backend.integrations.whatsapp import _send_text
except Exception:
    # fallback seguro caso import inicial falhe
    def _send_text(to: str, message: str):
        logger.warning("[AI] Envio WhatsApp desativado em ambiente atual.")
        return {"sid": "disabled"}

# ---------------------------------------------------------
# Endpoint oficial da IA
# ---------------------------------------------------------
@router.post("/ask")
def ai_whatsapp(payload: AIQuery):
    """
    IA leve de atendimento ao usuário pelo WhatsApp.
    Não gera insights, não analisa perfil, não interfere no MindScan.
    Apenas fornece orientações operacionais simples.
    """
    try:
        reply = ai_answer(payload.message)
        result = _send_text(payload.to, reply)
        return {"status": "success", "reply": reply, "sid": result.get("sid")}
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))

