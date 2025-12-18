from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/users", tags=["users"])


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: Optional[str] = None


@router.get("/ping", summary="Ping users")
def ping_users() -> Dict[str, Any]:
    return {"ok": True, "service": "users"}


@router.post("", summary="Cria usuário (stub)")
def create_user(payload: UserCreate) -> Dict[str, Any]:
    # Stub proposital: sem modelo/DB ainda (evita regressão estrutural)
    return {"user_id": "stub-1", "name": payload.name, "email": payload.email, "status": "created_stub"}


@router.get("/{user_id}", summary="Obtém usuário (stub)")
def get_user(user_id: str) -> Dict[str, Any]:
    return {"user_id": user_id, "status": "stub", "message": "User model not wired yet"}
