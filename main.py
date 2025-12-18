from fastapi import FastAPI
from core.run_mindscan import run_mindscan
from models import MindScanInput

app = FastAPI(
    title="MindScan API",
    version="MVP-1.0",
    description="API principal do sistema MindScan"
)


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


@app.post("/mindscan/run")
def mindscan_run(payload: MindScanInput):
    """
    Endpoint principal do MindScan
    """
    return run_mindscan(payload.dict())
