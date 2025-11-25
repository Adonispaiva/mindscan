# ============================================================
# MindScan — Email Provider
# ============================================================
# Responsável por envio de emails internos:
# - notificações
# - logs críticos
# - entrega de relatórios (versões futuras)
#
# O envio real pode ser feito por:
# - SMTP
# - SendGrid
# - AWS SES
# - Qualquer outro backend configurável
#
# Esta versão implementa a base completa e extensível.
# ============================================================

import smtplib
from email.mime.text import MIMEText
from typing import Optional


class EmailProvider:
    """
    Provedor de envio de emails do MindScan.
    """

    def __init__(
        self,
        smtp_server: str = "smtp.gmail.com",
        smtp_port: int = 587,
        username: Optional[str] = None,
        password: Optional[str] = None,
        default_sender: Optional[str] = None
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.default_sender = default_sender

    # ------------------------------------------------------------
    # ENVIAR EMAIL
    # ------------------------------------------------------------
    def send_email(
        self,
        to: str,
        subject: str,
        message: str,
        sender: Optional[str] = None
    ) -> bool:

        sender_email = sender or self.default_sender

        if not sender_email:
            raise ValueError("Endereço de remetente não definido.")

        msg = MIMEText(message, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = to

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                if self.username and self.password:
                    server.login(self.username, self.password)
                server.sendmail(sender_email, [to], msg.as_string())
            return True

        except Exception as e:
            print(f"[EmailProvider] Erro ao enviar email: {e}")
            return False
