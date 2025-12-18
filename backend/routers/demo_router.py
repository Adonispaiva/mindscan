from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import MindscanTest, Answer, Result
from backend.services.engine_service import MindScanEngine
from backend.services.report_service import ReportService

router = APIRouter(prefix="/demo", tags=["demo"])


class DemoAnswer(BaseModel):
    question_id: int = Field(..., ge=1)
    answer: Any


class DemoRunRequest(BaseModel):
    test_name: Optional[str] = Field(default="MindScan Demo")
    answers: List[DemoAnswer] = Field(default_factory=list)


def _to_storable(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


@router.get("/ping", summary="Ping demo")
def ping_demo() -> Dict[str, Any]:
    return {"ok": True, "service": "demo"}


@router.post("/run", summary="One-shot: cria teste → salva respostas → processa → gera PDF")
def run_demo(payload: DemoRunRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    if not payload.answers:
        raise HTTPException(status_code=400, detail="answers cannot be empty for demo")

    # 1) cria teste
    test = MindscanTest(name=payload.test_name or "MindScan Demo")
    db.add(test)
    db.commit()
    db.refresh(test)

    # 2) persiste respostas
    answer_rows: list[Answer] = []
    for a in payload.answers:
        row = Answer(test_id=test.id, question_id=a.question_id, answer=_to_storable(a.answer))
        db.add(row)
        answer_rows.append(row)
    db.commit()

    # 3) engine
    dataset_builder = getattr(MindScanEngine, "dataset_from_answers", None)
    dataset = dataset_builder(answer_rows) if callable(dataset_builder) else {"answers": []}
    results = MindScanEngine.process(dataset)

    # 4) persiste resultado (JSON string)
    results_json = json.dumps(results, ensure_ascii=False)
    result_row = Result(test_id=test.id, results=results_json)
    db.add(result_row)
    db.commit()
    db.refresh(result_row)

    # 5) gera relatório (contrato canônico: tuple)
    pdf_path, metadata = ReportService.generate_pdf(test.id, results)

    return {
        "message": "demo_complete",
        "test_id": test.id,
        "result_id": result_row.id,
        "pdf_path": pdf_path,
        "report_metadata": metadata,
    }
