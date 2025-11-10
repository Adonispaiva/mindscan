from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()  # carrega .env

app = FastAPI()

# CORS (libera frontend local e domínios do Render)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # em produção, troque por ["https://SEU-DOMINIO-WEB.onrender.com"]
    allow_methods=["*"],
    allow_headers=["*"],
)

default_prompt = (
    "Você é um assistente de RH. Analise a descrição de um candidato e ofereça "
    "orientação útil baseada em suas metas."
)

class OrientationRequest(BaseModel):
    prompt: str

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY não definido no .env")

client = OpenAI(api_key=api_key)

@app.post("/api/orientacao")
async def gerar_orientacao(req: OrientationRequest):
    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": default_prompt},
                {"role": "user", "content": req.prompt},
            ],
        )
        return {"resposta": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# (opcional) healthcheck simples
@app.get("/health")
def health():
    return {"ok": True}
