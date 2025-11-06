from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from pydantic import BaseModel

from models.user import User
from database import AsyncSessionLocal  # ✅ desacoplado de main.py

router = APIRouter(tags=["Admin"])

# ── Dependência de sessão ───────────────────────────────────────────────
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# ── Schemas ─────────────────────────────────────────────────────────────
class UserRead(BaseModel):
    id: int
    name: str | None = None
    email: str

    class Config:
        orm_mode = True

# ── Endpoints administrativos ───────────────────────────────────────────
@router.get("/admin/users", response_model=List[UserRead])
async def list_all_users(db: AsyncSession = Depends(get_db)):
    """Lista todos os usuários do sistema (apenas para administradores)."""
    result = await db.execute(select(User))
    return result.scalars().all()

@router.get("/admin/users/{user_id}", response_model=UserRead)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    """Obtém informações detalhadas de um usuário específico."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return user

@router.delete("/admin/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Remove um usuário do sistema (somente administradores)."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    await db.delete(user)
    await db.commit()
