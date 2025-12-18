# Arquivo: backend/routers/export_router.py
# MindScan Backend — Export Router (CSV/JSON)
# Diretor Técnico: Leo Vinci — Inovexa Software
# Versão: 1.0.0

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.services.export_service import ExportService

router = APIRouter(prefix="/export", tags=["export"])

_export = ExportService()


@router.get("/{test_id}/json", summary="Exporta resultados em JSON")
def export_results_json(test_id: int, db: Session = Depends(get_db)):
    payload = _export.export_json(db, test_id)
    if not payload.get("results"):
        raise HTTPException(status_code=404, detail="No results found for this test_id")
    return JSONResponse(content=payload)


@router.get("/{test_id}/csv", summary="Exporta resultados em CSV (download)")
def export_results_csv(test_id: int, db: Session = Depends(get_db)):
    path = _export.export_csv(db, test_id)
    return FileResponse(
        path,
        media_type="text/csv",
        filename=f"mindscan_results_{test_id}.csv",
    )
