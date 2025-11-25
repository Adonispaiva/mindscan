# ============================================================
# MindScan — Notification Provider
# ============================================================
# Sistema centralizado de notificações internas.
#
# Responsável por:
# - enviar alertas críticos
# - registrar notificações internas
# - integrar com EmailProvider
# - abstrair futuras integrações (SMS, Push, WhatsApp, Telegram...)
#
# Arquitetura completa e extensível.
# ============================================================

from typing import List, Dict, Optional
from datetime import datetime

from backend.providers.email_provider import EmailProvider


class NotificationProvider:
    """
    Provedor unificado de notificações internas do MindScan.
    """

    def __init__(self):
        self.history: List[Dict] = []
        self.channels = {
            "email": None,   # será vinculado externamente pelo ProviderManager
        }

    # ------------------------------------------------------------
    # Registrar canal
    # ------------------------------------------------------------
    def register_channel(self, name: str, provider):
        self.channels[name] = provider

    # ------------------------------------------------------------
    # Registrar log interno
    # ------------------------------------------------------------
    def _log(self, message: str, channel: str, status: str):
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "channel": channel,
            "status": status
        })

    # ------------------------------------------------------------
    # Enviar notificação por email
    # ------------------------------------------------------------
    def notify_email(self, to: str, subject: str, message: str) -> bool:
        email_provider: EmailProvider = self.channels.get("email")

        if not email_provider:
            self._log(message, "email", "NO_PROVIDER")
            return False

        ok = email_provider.send_email(to, subject, message)

        self._log(
            message,
            "email",
            "SENT" if ok else "FAILED"
        )

        return ok

    # ------------------------------------------------------------
    # Métodos futuros (push, sms, whatsapp...)
    # ------------------------------------------------------------
    def notify(self, channel: str, *args, **kwargs) -> bool:
        if channel == "email":
            return self.notify_email(*args, **kwargs)

        self._log("Canal não implementado", channel, "NOT_IMPLEMENTED")
        return False

    # ------------------------------------------------------------
    # Histórico de notificações
    # ------------------------------------------------------------
    def get_history(self):
        return self.history
