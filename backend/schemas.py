from pydantic import BaseModel, EmailStr
from typing import List, Optional

# ==== USER ====

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

# ==== RESPONSE ====

class ResponseCreate(BaseModel):
    user_id: int
    question: str
    answer: str

class ResponseOut(BaseModel):
    id: int
    user_id: int
    question: str
    answer: str

    class Config:
        orm_mode = True

# ==== QUIZ ====

class QuizInput(BaseModel):
    performance: List[float]
    matcher: List[float]

class QuizResult(BaseModel):
    score: float
    feedback: str
