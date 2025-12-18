from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.database import get_db
from backend.models import Result
from backend.services.report_service import ReportService

router = APIRouter(prefix="/report", tags=["report"])


@router.get("/{test_id}", summary="Gera (se necessário) e retorna paths + metadata do relatório")
def report_status(test_id: int, db: Session = Depends(get_db)):
    last = (
        db.query(Result)
        .filter(Result.test_id == test_id)
        .order_by(desc(Result.id))
        .first()
    )
    if not last or not last.results:
        raise HTTPException(status_code=404, detail="No results found for this test_id")

    try:
        payload = json.loads(last.results)
    except Exception:
        payload = last.results

    pdf_path, metadata = ReportService.generate_pdf(test_id, payload)
    return JSONResponse(content={"test_id": test_id, "pdf_path": pdf_path, "metadata": metadata})


@router.get("/{test_id}/pdf", summary="Download do PDF do relatório (atalho)")
def report_pdf(test_id: int, db: Session = Depends(get_db)):
    last = (
        db.query(Result)
        .filter(Result.test_id == test_id)
        .order_by(desc(Result.id))
        .first()
    )
    if not last or not last.results:
        raise HTTPException(status_code=404, detail="No results found for this test_id")

    try:
        payload = json.loads(last.results)
    except Exception:
        payload = last.results

    pdf_path, _ = ReportService.generate_pdf(test_id, payload)
    p = Path(pdf_path)
    if not p.exists():
        raise HTTPException(status_code=500, detail=f"PDF file not found at {pdf_path}")

    return FileResponse(str(p), media_type="application/pdf", filename=p.name)
