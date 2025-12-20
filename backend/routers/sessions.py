from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime

# Importações Absolutas Orion
from backend.database import get_db
from backend.models.user import User
from backend.algorithms.mindscan_engine import MindScanEngine
from backend.services.report_service import report_manager

router = APIRouter(
    prefix="/sessions",
    tags=["MindScan Sessions"]
)

@router.post("/process-dass21", status_code=status.HTTP_200_OK)
def process_dass21_session(
    user_email: str, 
    answers: List[int], 
    report_type: str = "technical",
    db: Session = Depends(get_db)
):
    """
    Endpoint de Fechamento Funcional: Recebe respostas, calcula DASS-21 e gera o Relatório.
    """
    # 1. Validação do Usuário/Candidato
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Candidato não encontrado na base SynMind.")

    # 2. Execução do Motor Determinístico (Cálculo Lovibond)
    engine = MindScanEngine()
    results = engine.calculate_dass21(answers)
    
    if "error" in results:
        raise HTTPException(status_code=400, detail=results["error"])

    # 3. Preparação de dados para o Relatório
    candidate_info = {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }

    # 4. Geração do Relatório PDF (v2.0 Architecture)
    report_path = report_manager.generate_report(
        candidate_data=candidate_info,
        results=results,
        report_type=report_type
    )

    return {
        "status": "Success",
        "candidate": user.name,
        "scores": results["scores"],
        "classification": results["classification"],
        "report_generated": os.path.basename(report_path) if report_path else "Falha na geração",
        "message": "Diagnóstico concluído e processado pela MI SynMind."
    }

@router.get("/active")
def get_active_summary():
    return {"status": "Aguardando novas entradas de diagnóstico"}