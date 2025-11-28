from fastapi import APIRouter
from .service import run_mindscan

router = APIRouter(prefix="/mindscan", tags=["MindScan"])

@router.post("/run")
async def run():
    """
    Executa o MindScan E2E e retorna os caminhos dos relatórios.
    """
    result = run_mindscan()
    return {"status": "OK", "reports": result}
