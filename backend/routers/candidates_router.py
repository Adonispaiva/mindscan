from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/candidates", tags=["candidates"])


class CandidateCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: Optional[str] = None
    role: Optional[str] = None


@router.get("/ping", summary="Ping candidates")
def ping_candidates() -> Dict[str, Any]:
    return {"ok": True, "service": "candidates"}


@router.post("", summary="Cria candidato (stub)")
def create_candidate(payload: CandidateCreate) -> Dict[str, Any]:
    return {
        "candidate_id": "stub-1",
        "name": payload.name,
        "email": payload.email,
        "role": payload.role,
        "status": "created_stub",
    }


@router.get("/{candidate_id}", summary="Obtém candidato (stub)")
def get_candidate(candidate_id: str) -> Dict[str, Any]:
    return {"candidate_id": candidate_id, "status": "stub", "message": "Candidate model not wired yet"}
