# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\routes\routes_results.py
# Última atualização: 2025-12-11T09:59:20.761538

from fastapi import APIRouter, HTTPException
from backend.api.services.result_gateway import ResultGateway

router = APIRouter(prefix="/mindscan/results", tags=["MindScan Results"])


@router.get("/{test_id}")
async def get_results(test_id: str):

    try:
        results = ResultGateway.load(test_id)

        if not results:
            raise HTTPException(status_code=404, detail="Resultados não encontrados")

        summarized = ResultGateway.summarize(results)

        return {
            "status": "success",
            "test_id": test_id,
            "results": summarized
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
