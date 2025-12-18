from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.mindscan_store import get_db, Result
from backend.services.report_service import ReportService

router = APIRouter(prefix="/report", tags=["ms_report"])


def _latest_payload(db: Session, test_id: int) -> Any:
    last = (
        db.query(Result)
        .filter(Result.test_id == test_id)
        .order_by(desc(Result.id))
        .first()
    )
    if not last or not last.results_json:
        raise HTTPException(status_code=404, detail="No results found for this test_id")
    try:
        return json.loads(last.results_json)
    except Exception:
        return last.results_json


@router.get("/{test_id}", summary="Status + metadata do relatório (gera se necessário)")
def report_status(test_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    payload = _latest_payload(db, test_id)
    pdf_path, metadata = ReportService.generate_pdf(test_id, payload)
    return JSONResponse(content={"test_id": test_id, "pdf_path": pdf_path, "metadata": metadata})


@router.get("/{test_id}/pdf", summary="Download do PDF (atalho)")
def report_pdf(test_id: int, db: Session = Depends(get_db)):
    payload = _latest_payload(db, test_id)
    pdf_path, _ = ReportService.generate_pdf(test_id, payload)
    p = Path(pdf_path)
    if not p.exists():
        raise HTTPException(status_code=500, detail=f"PDF not found at {pdf_path}")
    return FileResponse(str(p), media_type="application/pdf", filename=p.name)
