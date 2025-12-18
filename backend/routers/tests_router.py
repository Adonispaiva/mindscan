from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import MindscanTest

router = APIRouter(prefix="/tests", tags=["tests"])


class TestCreate(BaseModel):
    name: Optional[str] = Field(default="MindScan Test")


@router.post("", summary="Cria um MindscanTest e retorna o id")
def create_test(payload: TestCreate, db: Session = Depends(get_db)) -> Dict[str, Any]:
    test = MindscanTest(name=payload.name or "MindScan Test")
    db.add(test)
    db.commit()
    db.refresh(test)
    return {"test_id": test.id, "name": test.name}


@router.get("/{test_id}", summary="Obtém um MindscanTest por id")
def get_test(test_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    test = db.query(MindscanTest).filter(MindscanTest.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return {"test_id": test.id, "name": test.name}
