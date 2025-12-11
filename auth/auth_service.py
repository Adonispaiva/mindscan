# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\auth\auth_service.py
# Última atualização: 2025-12-11T09:59:20.558303

# ============================================================
# MindScan — Auth Service (JWT + Refresh)
# ============================================================

from datetime import datetime, timedelta
from typing import Dict

import jwt
from passlib.context import CryptContext


SECRET_KEY = "CHANGE_THIS_SECRET"
REFRESH_SECRET = "CHANGE_THIS_REFRESH_SECRET"
ALGORITHM = "HS256"

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    def __init__(self):
        pass

    # --------------------------------------------------------
    # Senhas
    # --------------------------------------------------------
    def hash_password(self, password: str) -> str:
        return pwd.hash(password)

    def verify_password(self, plain: str, hashed: str) -> bool:
        return pwd.verify(plain, hashed)

    # --------------------------------------------------------
    # JWT
    # --------------------------------------------------------
    def create_access_token(self, data: Dict) -> str:
        payload = data.copy()
        payload["exp"] = datetime.utcnow() + timedelta(minutes=30)
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def create_refresh_token(self, data: Dict) -> str:
        payload = data.copy()
        payload["exp"] = datetime.utcnow() + timedelta(days=7)
        return jwt.encode(payload, REFRESH_SECRET, algorithm=ALGORITHM)

    def decode_access(self, token: str) -> Dict:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    def decode_refresh(self, token: str) -> Dict:
        return jwt.decode(token, REFRESH_SECRET, algorithms=[ALGORITHM])
