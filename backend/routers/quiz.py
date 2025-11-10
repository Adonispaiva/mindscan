from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from pydantic import BaseModel

from models.quiz import Quiz
from database import AsyncSessionLocal  # ✅ desacoplado de main.py

router = APIRouter(tags=["Quiz"])

# ── Dependência de sessão ───────────────────────────────────────────────
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# ── Schemas ─────────────────────────────────────────────────────────────
class QuizCreate(BaseModel):
    title: str
    description: str

class QuizRead(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        orm_mode = True

# ── Endpoints ───────────────────────────────────────────────────────────
@router.post("/quizzes", response_model=QuizRead)
async def create_quiz(data: QuizCreate, db: AsyncSession = Depends(get_db)):
    """Cria um novo quiz."""
    entity = Quiz(**data.dict())
    db.add(entity)
    await db.commit()
    await db.refresh(entity)
    return entity

@router.get("/quizzes", response_model=List[QuizRead])
async def list_quizzes(db: AsyncSession = Depends(get_db)):
    """Retorna todos os quizzes."""
    result = await db.execute(select(Quiz))
    return result.scalars().all()

@router.get("/quizzes/{quiz_id}", response_model=QuizRead)
async def get_quiz(quiz_id: int, db: AsyncSession = Depends(get_db)):
    """Obtém detalhes de um quiz pelo ID."""
    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz não encontrado.")
    return quiz

@router.delete("/quizzes/{quiz_id}", status_code=204)
async def delete_quiz(quiz_id: int, db: AsyncSession = Depends(get_db)):
    """Remove um quiz existente."""
    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalar_one_or_none()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz não encontrado.")
    await db.delete(quiz)
    await db.commit()
