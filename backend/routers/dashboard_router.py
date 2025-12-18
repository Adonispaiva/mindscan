from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import MindscanTest, Answer, Result

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", summary="Resumo operacional do MindScan (contagens)")
def dashboard_summary(db: Session = Depends(get_db)) -> Dict[str, Any]:
    tests = db.query(MindscanTest).count()
    answers = db.query(Answer).count()
    results = db.query(Result).count()
    return {"tests": tests, "answers": answers, "results": results, "status": "ok"}
