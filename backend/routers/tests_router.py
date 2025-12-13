from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from backend.db.session import get_db
from backend.models import MindscanTest, User, Candidate

router = APIRouter(
    prefix="/tests",
    tags=["Tests"]
)

# ============================================================
# HEALTH CHECK
# ============================================================

@router.get("/health", summary="Health check do módulo de testes")
def tests_health():
    return {
        "status": "ok",
        "module": "tests_router",
        "models_loaded": ["User", "Candidate", "MindscanTest"]
    }

# ============================================================
# CRIAR NOVA SESSÃO MINDSCAN
# ============================================================

@router.post("/create", summary="Criar nova sessão MindScan")
def create_test(
    user_id: int,
    candidate_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidato não encontrado.")

    test = MindscanTest(
        user_id=user_id,
        candidate_id=candidate_id,
        status="pending",
        started_at=datetime.utcnow()
    )

    db.add(test)
    db.commit()
    db.refresh(test)

    return {
        "status": "created",
        "test_id": test.id,
        "user_id": test.user_id,
        "candidate_id": test.candidate_id,
        "started_at": test.started_at.isoformat() + "Z"
    }

# ============================================================
# LISTAR SESSÕES
# ============================================================

@router.get("/", summary="Listar sessões MindScan")
def list_tests(db: Session = Depends(get_db)):
    tests = db.query(MindscanTest).all()
    return [
        {
            "id": t.id,
            "user_id": t.user_id,
            "candidate_id": t.candidate_id,
            "status": t.status,
            "started_at": t.started_at.isoformat() + "Z",
            "completed_at": t.completed_at.isoformat() + "Z"
            if t.completed_at else None
        }
        for t in tests
    ]

# ============================================================
# OBTER SESSÃO POR ID
# ============================================================

@router.get("/{test_id}", summary="Obter sessão MindScan por ID")
def get_test(test_id: int, db: Session = Depends(get_db)):
    test = (
        db.query(MindscanTest)
        .filter(MindscanTest.id == test_id)
        .first()
    )

    if not test:
        raise HTTPException(status_code=404, detail="Sessão não encontrada.")

    return {
        "id": test.id,
        "user_id": test.user_id,
        "candidate_id": test.candidate_id,
        "status": test.status,
        "started_at": test.started_at.isoformat() + "Z",
        "completed_at": test.completed_at.isoformat() + "Z"
        if test.completed_at else None
    }
