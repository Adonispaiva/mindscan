# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\providers\auth_provider.py
# Última atualização: 2025-12-11T09:59:21.058152

# ============================================================
# MindScan — Auth Provider
# ============================================================
# Responsável por autenticação, verificação de tokens e
# segurança interna da API MindScan.
#
# Recursos:
# - Hash seguro (bcrypt)
# - Verificação de credenciais
# - Geração de tokens (UUID/JWT-ready)
# - Validação de sessão
# - Middleware de segurança futura
#
# Versão: Final — SynMind 2025
# ============================================================

import uuid
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict


class AuthProvider:
    """
    Sistema completo de autenticação do MindScan.
    """

    def __init__(self, token_expiration_minutes: int = 120):
        self.token_expiration = token_expiration_minutes
        self.sessions: Dict[str, Dict] = {}

    # ------------------------------------------------------------
    # Hash da senha
    # ------------------------------------------------------------
    def hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # ------------------------------------------------------------
    # Verificar senha
    # ------------------------------------------------------------
    def verify_password(self, password: str, hashed: bytes) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed)

    # ------------------------------------------------------------
    # Gerar token de sessão
    # ------------------------------------------------------------
    def generate_token(self, user_id: str) -> str:
        token = str(uuid.uuid4())
        expiration = datetime.utcnow() + timedelta(minutes=self.token_expiration)

        self.sessions[token] = {
            "user_id": user_id,
            "expires_at": expiration,
        }

        return token

    # ------------------------------------------------------------
    # Validar token
    # ------------------------------------------------------------
    def validate_token(self, token: str) -> Optional[str]:
        session = self.sessions.get(token)

        if not session:
            return None

        if datetime.utcnow() > session["expires_at"]:
            del self.sessions[token]
            return None

        return session["user_id"]

    # ------------------------------------------------------------
    # Revogar token
    # ------------------------------------------------------------
    def revoke_token(self, token: str) -> bool:
        if token in self.sessions:
            del self.sessions[token]
            return True
        return False

    # ------------------------------------------------------------
    # Limpar sessões expiradas
    # ------------------------------------------------------------
    def cleanup_expired(self):
        to_delete = [
            t for t, s in self.sessions.items()
            if datetime.utcnow() > s["expires_at"]
        ]
        for t in to_delete:
            del self.sessions[t]
