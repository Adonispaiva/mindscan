from fastapi import APIRouter

router = APIRouter(prefix="/diagnostic", tags=["diagnostic"])

@router.get("/ping")
def ping():
    return {"status": "diagnostic ok"}
