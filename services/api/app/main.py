from fastapi import FastAPI
from app.routers import health, quiz  # talentgpt removido

app = FastAPI(title="MindScan API")

app.include_router(health.router, tags=["Health"])
app.include_router(quiz.router, prefix="/quiz", tags=["Quiz"])
