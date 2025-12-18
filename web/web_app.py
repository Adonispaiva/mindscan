from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from mindscan.web.services.demo_service import executar_demo
from mindscan.web.services.demo_payload import build_demo_payload

BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "ui"))

router = APIRouter(tags=["WebApp"])

@router.get("/app", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/app/questionario", response_class=HTMLResponse)
async def questionario(request: Request):
    return templates.TemplateResponse("questionario.html", {"request": request})

@router.post("/app/questionario")
async def processar_questionario(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...)
):
    payload = build_demo_payload(nome, email)
    result = executar_demo(payload)

    test_id = result.get("test_id")

    return RedirectResponse(
        url=f"/app/resultado?test_id={test_id}",
        status_code=303
    )

@router.get("/app/resultado", response_class=HTMLResponse)
async def resultado(request: Request, test_id: str):
    return templates.TemplateResponse(
        "resultado.html",
        {
            "request": request,
            "test_id": test_id,
            "pdf_url": f"/report/{test_id}/pdf"
        }
    )
