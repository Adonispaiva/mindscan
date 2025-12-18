from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.mindscan_store import get_db, MindscanTest, Answer, Result

router = APIRouter(prefix="/dashboard", tags=["ms_dashboard"])


@router.get("/summary", summary="Resumo operacional (store isolado)")
def summary(db: Session = Depends(get_db)) -> Dict[str, Any]:
    return {
        "tests": db.query(MindscanTest).count(),
        "answers": db.query(Answer).count(),
        "results": db.query(Result).count(),
        "status": "ok",
    }
