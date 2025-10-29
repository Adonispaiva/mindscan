# D:\projetos-inovexa\mindscan\backend\routers\admin.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import csv
import io

from .. import models, database
from .auth import get_current_user

router = APIRouter(prefix="", tags=["Admin"])

@router.get("/metrics")
def get_metrics(db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    users = db.query(models.User).count()
    quizzes = db.query(models.Quiz).count()
    responses = db.query(models.Response).count()
    return {
        "total_users": users,
        "total_quizzes": quizzes,
        "total_responses": responses,
    }

@router.get("/export")
def export_responses_csv(db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "user_id", "quiz_id", "content", "created_at"])

    responses = db.query(models.Response).all()
    for r in responses:
        writer.writerow([r.id, r.user_id, r.quiz_id, r.content, r.created_at])

    output.seek(0)
    return StreamingResponse(iter([output.read()]), media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=respostas_mindscan.csv"
    })
