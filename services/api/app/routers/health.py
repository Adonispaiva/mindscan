from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def health_check():
    return {"status": "API do MindScan operando normalmente."}
