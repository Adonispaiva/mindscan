# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\routers\diagnostic_router.py
# Última atualização: 2025-12-11T09:59:21.073776

# Caminho: backend/routers/diagnostic_router.py
# MindScan Backend — Diagnostic Router (Motor Central)
# Diretor Técnico: Leo Vinci — Inovexa Software
# Versão Final — MindScan v2.0

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from backend.database import get_db
from backend.models import (
    MindscanTest,
    MindscanAnswers,
    MindscanResult,
    MindscanReport,
)

# Serviços (placeholders — devem existir no backend/services)
try:
    from backend.services.data_service import DataService
    from backend.services.engine_service import MindScanEngine
    from backend.services.report_service import ReportService
except Exception:
    DataService = None
    MindScanEngine = None
    ReportService = None

router = APIRouter()

# ============================================================
# RECEBER RESPOSTAS DO TESTE
# ============================================================
@router.post("/answers", summary="Enviar respostas brutas do teste")
def submit_answers(test_id: int, answers: dict, db: Session = Depends(get_db)):
    test = db.query(MindscanTest).filter(MindscanTest.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Teste não encontrado.")

    entry = MindscanAnswers(
        test_id=test_id,
        answers_json=answers,
        created_at=datetime.utcnow(),
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return {"status": "answers_received", "test_id": test_id}


# ============================================================
# PROCESSAR DIAGNÓSTICO COMPLETO
# ============================================================
@router.post("/process", summary="Processar diagnóstico completo do MindScan")
def process_diagnostic(test_id: int, db: Session = Depends(get_db)):
    # ---- Validação ----
    test = db.query(MindscanTest).filter(MindscanTest.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Teste não encontrado.")

    if DataService is None or MindScanEngine is None or ReportService is None:
        raise HTTPException(status_code=500, detail="Serviços não encontrados no backend.")

    # ---- 1) Carregar respostas ----
    answers_entry = db.query(MindscanAnswers).filter(MindscanAnswers.test_id == test_id).first()
    if not answers_entry:
        raise HTTPException(status_code=400, detail="Nenhuma resposta enviada para este teste.")

    raw_answers = answers_entry.answers_json

    # ---- 2) Normalização e preparação dos dados ----
    prepared_data = DataService.prepare_dataset(raw_answers)

    # ---- 3) Execução do motor MindScan ----
    engine_output = MindScanEngine.process(prepared_data)

    # ---- 4) Salvar resultados intermediários ----
    results = []
    for item in engine_output:
        result = MindscanResult(
            test_id=test_id,
            dimension=item.get("dimension"),
            score=item.get("score"),
            descriptor=item.get("descriptor"),
            metadata=item.get("metadata"),
            created_at=datetime.utcnow(),
        )
        db.add(result)
        results.append(result)

    db.commit()

    # ---- 5) Gerar relatório final ----
    pdf_path, metadata = ReportService.generate_pdf(test_id, results)

    report_entry = MindscanReport(
        test_id=test_id,
        pdf_path=pdf_path,
        metadata=metadata,
        created_at=datetime.utcnow(),
    )

    db.add(report_entry)
    test.status = "completed"
    test.completed_at = datetime.utcnow()
    db.commit()

    return {
        "status": "diagnostic_completed",
        "test_id": test_id,
        "pdf_path": pdf_path,
        "results_count": len(results),
    }


# ============================================================
# CONSULTAR RELATÓRIO FINAL
# ============================================================
@router.get("/report/{test_id}", summary="Obter relatório final do MindScan")
def get_report(test_id: int, db: Session = Depends(get_db)):
    report = db.query(MindscanReport).filter(MindscanReport.test_id == test_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Relatório não encontrado.")

    return {
        "test_id": test_id,
        "pdf_path": report.pdf_path,
        "metadata": report.metadata,
        "created_at": report.created_at.isoformat() + "Z",
    }
