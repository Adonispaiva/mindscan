# MindScan Backend — Health Check Router (compatível com probes)
from __future__ import annotations

from datetime import datetime
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/", summary="Health Check")
@router.get("/health", summary="Health Check")
@router.get("/healthz", summary="Health Check (probe alias)")
def health_status():
    return {
        "service": "MindScan Backend API v2.0",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
