from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yaml
import os

router = APIRouter()

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "../../../packages/prompts/prompts.yml")

class AdviceRequest(BaseModel):
    territory: str
    context: str

class AdviceResponse(BaseModel):
    advice: str

def load_prompts():
    try:
        with open(PROMPT_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar prompts: {e}")

@router.post("/talentgpt/advice", response_model=AdviceResponse)
async def get_advice(payload: AdviceRequest):
    prompts = load_prompts()

    if payload.territory not in prompts:
        raise HTTPException(status_code=404, detail="Território não encontrado")

    prompt_template = prompts[payload.territory]
    context = payload.context

    # Aqui a IA será chamada futuramente – por enquanto, mock
    advice = f"{prompt_template.strip()} CONTEXTO: {context}"

    return {"advice": advice}
