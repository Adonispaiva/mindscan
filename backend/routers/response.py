from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from pydantic import BaseModel

from models.response import Response
from database import AsyncSessionLocal  # ✅ desacoplado de main.py

router = APIRouter(tags=["Response"])

# Dependência de sessão assíncrona
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# ── Schemas ──────────────────────────────────────────────────────────────────
class ResponseCreate(BaseModel):
    user_id: int
    question_id: int
    answer: str

class ResponseRead(BaseModel):
    id: int
    user_id: int
    question_id: int
    answer: str

    class Config:
        orm_mode = True

# ── Endpoints ────────────────────────────────────────────────────────────────
@router.post("/responses", response_model=ResponseRead)
async def create_response(data: ResponseCreate, db: AsyncSession = Depends(get_db)):
    """Cria uma nova resposta associada a um usuário/questão."""
    entity = Response(**data.dict())
    db.add(entity)
    await db.commit()
    await db.refresh(entity)
    return entity

@router.get("/responses", response_model=List[ResponseRead])
async def list_responses(
    user_id: Optional[int] = Query(None, description="Filtra por usuário"),
    db: AsyncSession = Depends(get_db),
):
    """Lista respostas; opcionalmente filtra por user_id."""
    stmt = select(Response)
    if user_id is not None:
        stmt = stmt.where(Response.user_id == user_id)
    results = await db.execute(stmt)
    return results.scalars().all()
