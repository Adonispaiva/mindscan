# ===============================================================
#  ROTEADOR: INOVEXA ADMIN CONTROL
#  Projeto: MindScan — SynMind MI v2.0
#  Autor: Leo Vinci (GPT Inovexa)
#  Data: 07/11/2025
#  Função: Fornecer controle técnico reservado à Inovexa
# ===============================================================

from fastapi import APIRouter, HTTPException, Request
import os, subprocess, json, platform, datetime

router = APIRouter(prefix="/inovexa-admin", tags=["Inovexa Control"])

# ---------------------------------------------------------------
# Função utilitária — valida token interno da Inovexa
# ---------------------------------------------------------------
def validar_token(request: Request):
    token_header = request.headers.get("X-Inovexa-Token")
    token_env = os.getenv("INOVEXA_ADMIN_TOKEN")
    if not token_header or token_header != token_env:
        raise HTTPException(status_code=403, detail="Acesso negado à área técnica Inovexa.")

# ---------------------------------------------------------------
# Endpoint: Status geral do sistema
# ---------------------------------------------------------------
@router.get("/status")
async def obter_status(request: Request):
    validar_token(request)

    data = {
        "status": "operational",
        "sistema": "MindScan SynMind",
        "versao": "2.0",
        "ambiente": platform.system(),
        "data_hora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "modulos": {
            "diagnostic_engine": os.path.exists("backend/modules/diagnostic_engine.py"),
            "mi_engine": os.path.exists("backend/modules/mi_engine.py"),
            "performance_matcher": os.path.exists("backend/modules/performance_matcher.py"),
            "report_generator": os.path.exists("backend/modules/report_generator.py")
        }
    }
    return data

# ---------------------------------------------------------------
# Endpoint: Execução de comandos internos (restrito)
# ---------------------------------------------------------------
@router.post("/exec")
async def executar_comando(request: Request):
    validar_token(request)
    body = await request.json()
    comando = body.get("cmd")

    if not comando:
        raise HTTPException(status_code=400, detail="Campo 'cmd' obrigatório.")

    try:
        saida = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT, text=True, timeout=20)
        return {"status": "executado", "saida": saida}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Erro na execução: {e.output}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------------------
# Endpoint: Logs resumidos do sistema
# ---------------------------------------------------------------
@router.get("/logs")
async def obter_logs(request: Request):
    validar_token(request)
    log_path = "backend/logs/mi_logs.enc"
    if not os.path.exists(log_path):
        return {"status": "sem logs", "mensagem": "Nenhum log de MI encontrado."}

    try:
        tamanho = os.path.getsize(log_path)
        data_mod = datetime.datetime.fromtimestamp(os.path.getmtime(log_path))
        return {
            "arquivo": log_path,
            "tamanho_bytes": tamanho,
            "ultima_modificacao": data_mod.strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
