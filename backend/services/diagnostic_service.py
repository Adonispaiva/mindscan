from __future__ import annotations

from sqlalchemy.orm import Session

from backend.models.mindscan_test import MindscanTest
from backend.models.mindscan_answers import MindscanAnswers
from backend.models.mindscan_result import MindscanResult
from backend.models.mindscan_report import MindscanReport

from backend.services.data_service import build_dataset_from_answers
from backend.services.engine_service import run_mindscan_engine
from backend.services.report_service import generate_report_pdf


def submit_answers_service(payload: dict, db: Session) -> dict:
    test_id = payload.get("test_id")
    answers = payload.get("answers")

    if not test_id or not answers:
        raise ValueError("test_id e answers são obrigatórios")

    if not isinstance(answers, dict):
        raise ValueError("answers deve ser um objeto JSON")

    test = db.query(MindscanTest).filter(MindscanTest.id == test_id).first()
    if not test:
        raise LookupError("Teste não encontrado")

    record = MindscanAnswers(
        test_id=test_id,
        answers=dict(answers),
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {"status": "answers_saved", "test_id": test_id}


def process_results_service(test_id: int, db: Session) -> dict:
    test = db.query(MindscanTest).filter(MindscanTest.id == test_id).first()
    if not test:
        raise LookupError("Teste não encontrado")

    answers = (
        db.query(MindscanAnswers)
        .filter(MindscanAnswers.test_id == test_id)
        .order_by(MindscanAnswers.created_at.desc())
        .first()
    )
    if not answers:
        raise LookupError("Respostas não encontradas")

    dataset = build_dataset_from_answers(answers.answers)

    result_data = run_mindscan_engine(dataset)

    if not isinstance(result_data, (list, dict)):
        raise ValueError("Resultado do engine inválido")

    result = MindscanResult(
        test_id=test_id,
        result=result_data,
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    report_path = generate_report_pdf(test_id=test_id, result=result_data)

    report = MindscanReport(
        test_id=test_id,
        path=report_path,
    )
    db.add(report)

    test.status = "diagnostic_completed"

    db.commit()

    return {
        "status": "completed",
        "test_id": test_id,
        "report_path": report_path,
    }


def get_latest_results_service(test_id: int, db: Session) -> dict:
    result = (
        db.query(MindscanResult)
        .filter(MindscanResult.test_id == test_id)
        .order_by(MindscanResult.created_at.desc())
        .first()
    )
    if not result:
        raise LookupError("Resultado não encontrado")

    return result.result
