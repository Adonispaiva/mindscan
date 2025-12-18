from __future__ import annotations

import json
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.mindscan_store import get_db, MindscanTest, Answer, Result
from backend.services.engine_service import MindScanEngine
from backend.services.report_service import ReportService

router = APIRouter(prefix="/diagnostic", tags=["ms_diagnostic"])


class AnswerItem(BaseModel):
    question_id: int = Field(..., ge=1)
    answer: Any


class AnswerRequest(BaseModel):
    test_id: int = Field(..., ge=1)
    answers: List[AnswerItem] = Field(default_factory=list)


def _to_str(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False)
    return str(v)


@router.post("/answers", summary="Salva respostas no store isolado")
def submit_answers(payload: AnswerRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    t = db.query(MindscanTest).filter(MindscanTest.id == payload.test_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Test not found")
    if not payload.answers:
        raise HTTPException(status_code=400, detail="answers cannot be empty")

    for a in payload.answers:
        row = (
            db.query(Answer)
            .filter(Answer.test_id == payload.test_id, Answer.question_id == a.question_id)
            .first()
        )
        if row:
            row.answer = _to_str(a.answer)
        else:
            db.add(Answer(test_id=payload.test_id, question_id=a.question_id, answer=_to_str(a.answer)))

    db.commit()
    return {"ok": True, "test_id": payload.test_id, "count": len(payload.answers)}


@router.post("/process", summary="Processa e gera PDF (store isolado)")
def process_results(test_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    t = db.query(MindscanTest).filter(MindscanTest.id == test_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Test not found")

    answers = db.query(Answer).filter(Answer.test_id == test_id).all()
    if not answers:
        raise HTTPException(status_code=400, detail="No answers found for this test_id")

    dataset_builder = getattr(MindScanEngine, "dataset_from_answers", None)
    dataset = dataset_builder(answers) if callable(dataset_builder) else {"answers": []}

    results = MindScanEngine.process(dataset)
    results_json = json.dumps(results, ensure_ascii=False)

    r = Result(test_id=test_id, results_json=results_json)
    db.add(r)
    db.commit()
    db.refresh(r)

    pdf_path, metadata = ReportService.generate_pdf(test_id, results)

    return {
        "message": "processing_complete",
        "test_id": test_id,
        "result_id": r.id,
        "pdf_path": pdf_path,
        "report_metadata": metadata,
    }


@router.get("/results/latest/{test_id}", summary="Último resultado salvo")
def latest_results(test_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    last = (
        db.query(Result)
        .filter(Result.test_id == test_id)
        .order_by(desc(Result.id))
        .first()
    )
    if not last:
        raise HTTPException(status_code=404, detail="No results found")

    try:
        payload = json.loads(last.results_json or "[]")
    except Exception:
        payload = last.results_json

    return {"test_id": test_id, "result_id": last.id, "results": payload}
