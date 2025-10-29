from fastapi import APIRouter
from pydantic import BaseModel

class QuizPayload(BaseModel):
    performance: list[int]
    matcher: list[int]

router = APIRouter()

@router.post("/submit")
def submit(data: QuizPayload):
    p = round(sum(data.performance) / max(len(data.performance), 1), 2)
    m = round(sum(data.matcher) / max(len(data.matcher), 1), 2)
    cutoff = 80
    if p > cutoff and m > cutoff:
        t = "inspiradores"
    elif p > cutoff:
        t = "especialistas"
    elif m > cutoff:
        t = "promissores"
    else:
        t = "buscadores"
    return {"performance": p, "matcher": m, "territory": t, "insights": []}
