from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.mindscan_store import get_db, Result
from backend.services.report_service import ReportService

router = APIRouter(prefix="/pdf", tags=["ms_pdf"])


@router.get("/{test_id}", summary="Gera e retorna PDF do relatório")
def download_pdf(test_id: int, db: Session = Depends(get_db)):
    last = (
        db.query(Result)
        .filter(Result.test_id == test_id)
        .order_by(desc(Result.id))
        .first()
    )
    if not last or not last.results_json:
        raise HTTPException(status_code=404, detail="No results found for this test_id")

    try:
        payload = json.loads(last.results_json)
    except Exception:
        payload = last.results_json

    pdf_path, _ = ReportService.generate_pdf(test_id, payload)
    p = Path(pdf_path)
    if not p.exists():
        raise HTTPException(status_code=500, detail=f"PDF not found at {pdf_path}")

    return FileResponse(str(p), media_type="application/pdf", filename=p.name)
