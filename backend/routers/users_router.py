# Caminho: backend/routers/users_router.py
# MindScan Backend — Users Router (Autenticação e Gestão de Usuários)
# Diretor Técnico: Leo Vinci — Inovexa Software
# Versão Final — MindScan v2.0

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import hashlib

from backend.database import get_db
from backend.models import User

router = APIRouter()

# ============================================================
# UTILITÁRIOS
# ============================================================

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed


# ============================================================
# ROTAS DE USUÁRIO
# ============================================================

@router.post("/create", summary="Criar usuário")
def create_user(full_name: str, email: str, password: str, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="E-mail já registrado.")

    user = User(
        full_name=full_name,
        email=email,
        password_hash=hash_password(password),
        created_at=datetime.utcnow(),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "status": "created",
        "user_id": user.id,
        "email": user.email,
    }


@router.post("/login", summary="Login e validação básica")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha incorreta.")

    return {
        "status": "authenticated",
        "user": user.email,
        "user_id": user.id,
    }


@router.get("/", summary="Listar usuários")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "full_name": u.full_name,
            "email": u.email,
            "created_at": u.created_at.isoformat() + "Z",
        }
        for u in users
    ]