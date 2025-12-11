# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\integrations\whatsapp_utils.py
# Última atualização: 2025-12-11T09:59:20.841083

# Caminho: D:\projetos-inovexa\mindscan\backend\integrations\whatsapp_utils.py
"""
Utilidades oficiais para o módulo WhatsApp do MindScan
Inovexa Software | SynMind | MindScan®

Funções incluídas:
- Sanitização de números internacionais
- Formatação de mensagens
- Validação Twilio
- Logging padronizado
- Controle de erros e fallback
- Normalização semântica para IA leve
"""

import logging

logger = logging.getLogger("whatsapp_utils")
logger.setLevel(logging.INFO)

# ---------------------------------------------------------
# Sanitização de número
# ---------------------------------------------------------
def sanitize_phone(number: str) -> str:
    """
    Normaliza o número para o formato internacional aceito pelo WhatsApp/Twilio.
    """
    if not isinstance(number, str):
        raise ValueError("Número inválido: esperado string.")

    original = number
    number = number.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    number = number.replace("+", "")

    if not number.isdigit():
        raise ValueError(f"Número inválido: {original}")

    return f"whatsapp:+{number}"

# ---------------------------------------------------------
# Formatação de mensagens
# ---------------------------------------------------------
def format_message(text: str) -> str:
    """
    Remove espaços desnecessários e caracteres estranhos.
    """
    if not text:
        return ""
    return text.strip()

# ---------------------------------------------------------
# Normalização semântica (IA leve)
# ---------------------------------------------------------
def normalize(text: str) -> str:
    """
    Normaliza texto para análise determinística da IA leve.
    """
    if not isinstance(text, str):
        return ""
    return text.lower().strip()

# ---------------------------------------------------------
# Fallback para envio (em testes locais)
# ---------------------------------------------------------
def fallback_send(to: str, message: str):
    """
    Usado quando o módulo whatsapp não está ativo.
    """
    logger.warning(f"[FALLBACK] Envio desativado. Destino: {to} | Msg: {message}")
    return {"sid": "fallback"}

# ---------------------------------------------------------
# Validação Twilio (básica)
# ---------------------------------------------------------
def validate_twilio_credentials(account_sid: str, token: str) -> bool:
    """
    Validação simples das credenciais.
    """
    if not account_sid or not token:
        return False
    if " " in account_sid or " " in token:
        return False
    return True