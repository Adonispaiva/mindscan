from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.mindscan_store import get_db, MindscanTest, Answer, Result
from backend.services.engine_service import MindScanEngine
from backend.services.report_service import ReportService

router = APIRouter(prefix="/demo", tags=["ms_demo"])


class DemoAnswer(BaseModel):
    question_id: int = Field(..., ge=1)
    answer: Any


class DemoRunRequest(BaseModel):
    test_name: Optional[str] = Field(default="MindScan Demo Milena")
    answers: List[DemoAnswer] = Field(default_factory=list)


def _to_str(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False)
    return str(v)


@router.post("/run", summary="One-shot: cria teste → salva respostas → processa → gera PDF")
def run_demo(payload: DemoRunRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    if not payload.answers:
        raise HTTPException(status_code=400, detail="answers cannot be empty")

    t = MindscanTest(name=payload.test_name or "MindScan Demo Milena")
    db.add(t)
    db.commit()
    db.refresh(t)

    answer_rows: List[Answer] = []
    for a in payload.answers:
        row = Answer(test_id=t.id, question_id=a.question_id, answer=_to_str(a.answer))
        db.add(row)
        answer_rows.append(row)
    db.commit()

    dataset_builder = getattr(MindScanEngine, "dataset_from_answers", None)
    dataset = dataset_builder(answer_rows) if callable(dataset_builder) else {"answers": []}
    results = MindScanEngine.process(dataset)

    r = Result(test_id=t.id, results_json=json.dumps(results, ensure_ascii=False))
    db.add(r)
    db.commit()
    db.refresh(r)

    pdf_path, metadata = ReportService.generate_pdf(t.id, results)

    return {
        "message": "demo_complete",
        "test_id": t.id,
        "result_id": r.id,
        "pdf_path": pdf_path,
        "report_metadata": metadata,
    }
