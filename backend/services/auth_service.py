from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt

# ==========================================================
#  Serviço de Autenticação — MindScan 2.0
# ==========================================================
# A versão superior do AuthService unifica:
# - geração de tokens
# - validação de tokens
# - extração de usuário
# - política de expiração
# ==========================================================


class AuthService:
    SECRET_KEY = "INOVEXA_SYN_MIND_SCAN_KEY_2025"  # Ajustável no futuro
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    @staticmethod
    def create_access_token(data: Dict[str, Any]) -> str:
        """
        Cria um token JWT com expiração definida.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=AuthService.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            AuthService.SECRET_KEY,
            algorithm=AuthService.ALGORITHM
        )

        return encoded_jwt

    @staticmethod
    def validate_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Valida um token JWT. Retorna o payload do usuário se válido.
        """
        try:
            payload = jwt.decode(
                token,
                AuthService.SECRET_KEY,
                algorithms=[AuthService.ALGORITHM]
            )
            return payload
        except Exception:
            return None

    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Método fictício até integração com o banco real.
        Aqui podemos validar admins, usuários e permissões.
        """

        # Exemplo temporário — substituir pelo banco real
        FAKE_USERS = {
            "admin": {"password": "123", "role": "admin", "name": "Milena"},
            "user": {"password": "123", "role": "user", "name": "João"}
        }

        user = FAKE_USERS.get(username)

        if not user or user["password"] != password:
            return None

        return {
            "username": username,
            "role": user["role"],
            "name": user["name"]
        }
