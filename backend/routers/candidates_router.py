# Caminho: backend/routers/candidates_router.py
# MindScan Backend — Candidates Router
# Diretor Técnico: Leo Vinci — Inovexa Software
# Versão Final — MindScan v2.0

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from backend.database import get_db
from backend.models import Candidate

router = APIRouter()

# ============================================================
# ROTAS DE CANDIDATOS
# ============================================================

@router.post("/create", summary="Criar candidato")
def create_candidate(full_name: str, age: int = None, email: str = None, phone: str = None,
                     db: Session = Depends(get_db)):
    candidate = Candidate(
        full_name=full_name,
        age=age,
        email=email,
        phone=phone,
        created_at=datetime.utcnow(),
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return {
        "status": "created",
        "candidate_id": candidate.id,
        "full_name": candidate.full_name,
    }


@router.get("/", summary="Listar candidatos")
def list_candidates(db: Session = Depends(get_db)):
    rows = db.query(Candidate).all()
    return [
        {
            "id": c.id,
            "full_name": c.full_name,
            "age": c.age,
            "email": c.email,
            "phone": c.phone,
            "created_at": c.created_at.isoformat() + "Z",
        }
        for c in rows
    ]


@router.get("/{candidate_id}", summary="Obter candidato por ID")
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidato não encontrado.")

    return {
        "id": candidate.id,
        "full_name": candidate.full_name,
        "age": candidate.age,
        "email": candidate.email,
        "phone": candidate.phone,
        "created_at": candidate.created_at.isoformat() + "Z",
    }