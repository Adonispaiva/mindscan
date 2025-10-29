from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from pydantic import BaseModel
from models.response import Response
from models.base import Base
from sqlalchemy.orm import sessionmaker
from main import AsyncSessionLocal

router = APIRouter()

# Função de dependência do banco
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Pydantic para entrada
class ResponseCreate(BaseModel):
    user_id: int
    question_id: int
    answer: str

# Pydantic para saída
class ResponseRead(BaseModel):
    id: int
    user_id: int
    question_id: int
    answer: str

    class Config:
        orm_mode = True

# Criar nova resposta
@router.post("/responses", response_model=ResponseRead)
async def create_response(data: ResponseCreate, db: AsyncSession = Depends(get_db)):
    response = Response(**data.dict())
    db.add(response)
    await db.commit()
    await db.refresh(response)
    return response

# Listar respostas (opcionalmente por usuário)
@router.get("/responses", response_model=List[ResponseRead])
async def list_responses(user_id: Optional[int] = Query(None), db: AsyncSession = Depends(get_db)):
    stmt = select(Response)
    if user_id is not None:
        stmt = stmt.where(Response.user_id == user_id)
    results = await db.execute(stmt)
    return results.scalars().all()
