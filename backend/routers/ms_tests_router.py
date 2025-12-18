from __future__ import annotations

from typing import Any, Dict, Optional, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.mindscan_store import get_db, MindscanTest

router = APIRouter(prefix="/tests", tags=["ms_tests"])


class TestCreate(BaseModel):
    name: Optional[str] = Field(default="MindScan Test")


@router.post("", summary="Cria um teste MindScan (isolado)")
def create_test(payload: TestCreate, db: Session = Depends(get_db)) -> Dict[str, Any]:
    t = MindscanTest(name=payload.name or "MindScan Test")
    db.add(t)
    db.commit()
    db.refresh(t)
    return {"test_id": t.id, "name": t.name}


@router.get("/{test_id}", summary="Obtém um teste por id")
def get_test(test_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    t = db.query(MindscanTest).filter(MindscanTest.id == test_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"test_id": t.id, "name": t.name, "created_at": t.created_at.isoformat() + "Z"}


@router.get("", summary="Lista testes")
def list_tests(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)) -> Dict[str, Any]:
    q = db.query(MindscanTest).order_by(MindscanTest.id.desc())
    total = q.count()
    items: List[MindscanTest] = q.offset(offset).limit(limit).all()
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": [{"test_id": x.id, "name": x.name} for x in items],
    }
