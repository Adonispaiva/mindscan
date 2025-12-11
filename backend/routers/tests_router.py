# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\routers\tests_router.py
# Última atualização: 2025-12-11T09:59:21.089476

# Caminho: backend/routers/tests_router.py
# MindScan Backend — Tests Router (Sessões de Teste)
# Diretor Técnico: Leo Vinci — Inovexa Software
# Versão Final — MindScan v2.0

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from backend.database import get_db
from backend.models import MindscanTest, Candidate, User

router = APIRouter()

# ============================================================
# CRIAÇÃO DE UMA NOVA SESSÃO DO MINDSCAN
# ============================================================

@router.post("/create", summary="Criar uma nova sessão de teste MindScan")
def create_test(user_id: int, candidate_id: int, db: Session = Depends(get_db)):
    # Verifica se o usuário existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    # Verifica se o candidato existe
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidato não encontrado.")

    test = MindscanTest(
        user_id=user_id,
        candidate_id=candidate_id,
        started_at=datetime.utcnow(),
        status="pending",
    )

    db.add(test)
    db.commit()
    db.refresh(test)

    return {
        "status": "created",
        "test_id": test.id,
        "user_id": test.user_id,
        "candidate_id": test.candidate_id,
    }


# ============================================================
# LISTAR SESSÕES
# ============================================================

@router.get("/", summary="Listar sessões de teste")
def list_tests(db: Session = Depends(get_db)):
    rows = db.query(MindscanTest).all()
    return [
        {
            "id": t.id,
            "user_id": t.user_id,
            "candidate_id": t.candidate_id,
            "status": t.status,
            "started_at": t.started_at.isoformat() + "Z",
            "completed_at": t.completed_at.isoformat() + "Z" if t.completed_at else None,
        }
        for t in rows
    ]


# ============================================================
# OBTER UMA SESSÃO PELO ID
# ============================================================

@router.get("/{test_id}", summary="Obter sessão por ID")
def get_test(test_id: int, db: Session = Depends(get_db)):
    test = db.query(MindscanTest).filter(MindscanTest.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Sessão não encontrada.")

    return {
        "id": test.id,
        "user_id": test.user_id,
        "candidate_id": test.candidate_id,
        "status": test.status,
        "started_at": test.started_at.isoformat() + "Z",
        "completed_at": test.completed_at.isoformat() + "Z" if test.completed_at else None,
    }