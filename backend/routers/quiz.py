# D:\projetos-inovexa\mindscan\backend\routers\quiz.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import List

from .. import models, database
from ..services.analyzer import Analyzer

router = APIRouter(prefix="/quiz", tags=["Quiz"])

class QuizRequest(BaseModel):
    user_id: int
    respostas: List[str]

class QuizResponse(BaseModel):
    diagnostico: str
    nivel: str
    dicas: List[str]

@router.post("", response_model=QuizResponse)
def analisar_quiz(payload: QuizRequest, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Grava quiz
    quiz = models.Quiz(user_id=payload.user_id, created_at=datetime.utcnow())
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    # Grava respostas
    for r in payload.respostas:
        resp = models.Response(user_id=payload.user_id, quiz_id=quiz.id, content=r, created_at=datetime.utcnow())
        db.add(resp)
    db.commit()

    # Executa análise
    resultado = Analyzer(payload.respostas).diagnosticar()

    return {
        "diagnostico": f"Risco {resultado['nivel']}",
        "nivel": resultado['nivel'],
        "dicas": resultado['dicas']
    }
