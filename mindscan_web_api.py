# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\mindscan_web_api.py
# Última atualização: 2025-12-11T09:59:20.424839

# ============================================================
# MindScan — Web API (MI Original / Advanced / Hybrid + PDF)
# + Autenticação JWT
# + Middleware de proteção
# + Admin Logs
# + Analytics
# + Live Metrics (SSE)
# ============================================================

from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Dict, Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# --------------------------
# AUTH
# --------------------------
from auth.auth_router import router as auth_router
from auth.middleware_auth import AuthMiddleware

# --------------------------
# ADMIN + LOGGING
# --------------------------
from admin.admin_router import router as admin_router
from logging.logging_service import LoggingService

# --------------------------
# ANALYTICS
# --------------------------
from analytics.analytics_router import router as analytics_router

# --------------------------
# LIVE METRICS (SSE)
# --------------------------
from analytics.live_metrics_router import router as live_metrics_router

# --------------------------
# MI Engines
# --------------------------
from backend.engine.mi_engine import MIEngine
from backend.engine.mi_engine_advanced import MIEngineAdvanced
from backend.engine.mi_formatter import mi_formatter

# PDF Builder
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# ============================================================
# CONFIGURAÇÃO BASE
# ============================================================

OUTPUT_DIR = os.getenv("MINDSCAN_REPORT_OUTPUT", "generated_reports")
os.makedirs(OUTPUT_DIR, exist_ok=True)

logger = LoggingService()

app = FastAPI(
    title="MindScan MI Hybrid Web API",
    version="1.4.0",
    description=(
        "API Web completa do MindScan: MI Original, Advanced e Hybrid, "
        "com Autenticação, Logging, Admin Console, Analytics e Métricas em Tempo Real."
    ),
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Segurança
app.add_middleware(AuthMiddleware)

# Rotas externas
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(analytics_router)
app.include_router(live_metrics_router)

# Pasta de PDFs
app.mount("/files", StaticFiles(directory=OUTPUT_DIR), name="files")


# ============================================================
# MODELOS DE REQUEST/RESPONSE
# ============================================================

class MIRequest(BaseModel):
    subject_id: str
    raw_scores: Dict[str, float]
    mi_mode: Literal["original", "advanced", "hybrid"] = "hybrid"
    report_type: Literal["technical", "executive", "psychodynamic", "premium"] = "technical"


class MIResponse(BaseModel):
    subject_id: str
    mi_mode: str
    report_type: str
    mi_package: Dict[str, Any]
    formatted_blocks: Dict[str, str]
    pdf_url: str


# ============================================================
# MI PIPELINE CONSOLIDADO
# ============================================================

def _run_mi_pipeline(req: MIRequest) -> Dict[str, Any]:
    """
    Pipeline MI unificado — original, advanced e hybrid.
    """

    if not req.raw_scores:
        raise ValueError("raw_scores não pode ser vazio.")

    # ORIGINAL
    if req.mi_mode == "original":
        base = MIEngine().compute_mi(req.raw_scores)
        return {
            "mode": "original",
            "mi_score": base.get("mi_score"),
            "package": base,
        }

    # ADVANCED
    if req.mi_mode == "advanced":
        adv = MIEngineAdvanced().compute(req.raw_scores)
        return {
            "mode": "advanced",
            "mi_score": adv.get("mi_advanced_score"),
            "package": adv,
        }

    # HYBRID
    engine_o = MIEngine()
    engine_a = MIEngineAdvanced()

    original = engine_o.compute_mi(req.raw_scores)
    advanced = engine_a.compute(req.raw_scores)

    o_score = float(original.get("mi_score", 0))
    a_score = float(advanced.get("mi_advanced_score", o_score))
    hybrid_score = (o_score + a_score) / 2

    return {
        "mode": "hybrid",
        "mi_score": hybrid_score,
        "package": {
            "quadrant": original.get("quadrant"),
            "coordinates": original.get("coordinates"),
            "style": original.get("style") or advanced.get("style"),
            "risk_level": original.get("risk_level") or advanced.get("risk_level"),
            "talents": original.get("talents", []),
            "risks": original.get("risks", []),
            "contradictions": original.get("contradictions", []),
            "recommendations": original.get("recommendations", []),
        },
    }


# ============================================================
# PDF BUILDER
# ============================================================

def _build_pdf(subject_id: str, mi_mode: str, report_type: str, mi_result: Dict[str, Any]) -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"mindscan_{subject_id}_{mi_mode}_{report_type}_{timestamp}.pdf"
    path = os.path.join(OUTPUT_DIR, filename)

    package = mi_result["package"]
    formatted = mi_formatter.format_package(package)

    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    y = height - 50

    def line(text: str, step: int = 16):
        nonlocal y
        c.drawString(40, y, text)
        y -= step

    line("MindScan — MI Hybrid Report", 20)
    line(f"Sujeito: {subject_id}")
    line(f"Modo MI: {mi_mode}")
    line(f"Relatório: {report_type}")
    line(f"Score MI: {mi_result.get('mi_score'):.3f}", 18)
    line("-" * 80, 18)

    for block_name, block_text in formatted.items():
        line("")
        line(f"[{block_name.upper()}]", 18)
        for l in block_text.split("\n"):
            if y < 80:
                c.showPage()
                y = height - 50
            line(l)

    c.showPage()
    c.save()
    return filename


# ============================================================
# ENDPOINT PRINCIPAL (PROTEGIDO)
# ============================================================

@app.post("/mindscan/mi-hybrid", response_model=MIResponse)
def generate_mindscan_report(req: MIRequest) -> MIResponse:

    try:
        mi_result = _run_mi_pipeline(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no pipeline MI: {e}")

    formatted = mi_formatter.format_package(mi_result["package"])

    filename = _build_pdf(
        subject_id=req.subject_id,
        mi_mode=mi_result["mode"],
        report_type=req.report_type,
        mi_result=mi_result,
    )

    pdf_url = f"/files/{filename}"

    # Auditoria
    logger.record({
        "subject_id": req.subject_id,
        "mi_mode": mi_result["mode"],
        "mi_score": mi_result.get("mi_score"),
        "report_type": req.report_type,
        "pdf_url": pdf_url,
        "raw_count": len(req.raw_scores),
    })

    return MIResponse(
        subject_id=req.subject_id,
        mi_mode=mi_result["mode"],
        report_type=req.report_type,
        mi_package=mi_result["package"],
        formatted_blocks=formatted,
        pdf_url=pdf_url,
    )


# ============================================================
# HEALTHCHECK
# ============================================================

@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "service": "mindscan-web-api",
        "auth": "enabled",
        "admin": "enabled",
        "logging": "enabled",
        "analytics": "enabled",
        "live_metrics": "enabled",
    }
