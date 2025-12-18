from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from backend.core.diagnostic_engine import DiagnosticEngine

router = APIRouter(prefix="/mindscan", tags=["MindScan"])


@router.post("/run")
def run_mindscan(payload: Dict[str, Any]):
    try:
        result = DiagnosticEngine.run_diagnostic(payload)
        return {
            "status": "success",
            "diagnostic_id": result["diagnostic_id"],
            "reports": result["reports"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
