import os
import subprocess
import requests
import psutil
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
from pathlib import Path

# ============================================
# 🧠 MindScan Remote Console — v4.9
# ============================================
# Autor: Leo Vinci (GPT Inovexa)
# Data: 12/11/2025
# Função: Console administrativa segura via API REST
# ============================================

LOG_API = "http://127.0.0.1:8091/logs"
SERVICE_INSTALLER = Path(r"D:\MindScan\core\MindScan_ServiceInstaller.py")
ROLLBACK_MANAGER = Path(r"D:\MindScan\core\MindScan_RollbackManager.py")
SYNC_AGENT = Path(r"D:\MindScan\core\supervisao_diretor_auto_sync.py")
CONSOLE_KEY = os.getenv("INOVEXA_CONSOLE_KEY", "DEV-LOCAL-KEY")

app = FastAPI(title="MindScan Remote Console", version="4.9")
auth_scheme = HTTPBearer()

# ---------------------- UTILITÁRIOS ----------------------
def now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")

def log(msg, level="INFO"):
    print(f"[{now()}] [Console] [{level}] {msg}")
    try:
        requests.post(LOG_API, json={"origin": "RemoteConsole", "message": msg, "level": level}, timeout=1)
    except Exception:
        pass

def require_auth(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    if credentials.credentials != CONSOLE_KEY:
        log(f"Acesso negado com token inválido.", "WARN")
        raise HTTPException(status_code=403, detail="Token inválido.")
    return True

# ---------------------- ENDPOINTS ----------------------
@app.get("/status", dependencies=[Depends(require_auth)])
def get_status():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    procs = len(psutil.pids())
    log("Consulta de status executada.")
    return {"time": now(), "cpu": cpu, "memory": mem, "processes": procs, "status": "OK"}

@app.post("/restart", dependencies=[Depends(require_auth)])
def restart_services():
    log("Reiniciando serviços MindScan via RemoteConsole.")
    subprocess.run(["python", str(SERVICE_INSTALLER), "stop"])
    subprocess.run(["python", str(SERVICE_INSTALLER), "start"])
    return {"result": "success", "message": "Serviços reiniciados com sucesso."}

@app.post("/sync", dependencies=[Depends(require_auth)])
def sync_supervisao():
    log("Sincronização manual solicitada via RemoteConsole.")
    subprocess.run(["python", str(SYNC_AGENT)])
    return {"result": "success", "message": "Sincronização concluída."}

@app.post("/rollback", dependencies=[Depends(require_auth)])
def rollback_version():
    log("Rollback remoto solicitado via RemoteConsole.")
    subprocess.run(["python", str(ROLLBACK_MANAGER)])
    return {"result": "success", "message": "Rollback executado com sucesso."}

@app.delete("/logs/clear", dependencies=[Depends(require_auth)])
def clear_logs():
    log_dir = Path(r"D:\MindScan\logs")
    count = 0
    for file in log_dir.glob("*.jsonl"):
        file.unlink(missing_ok=True)
        count += 1
    log(f"Logs apagados via RemoteConsole ({count} arquivos).", "WARN")
    return {"result": "success", "deleted": count}

# ---------------------- PROTEÇÃO ADICIONAL ----------------------
@app.middleware("http")
async def block_unauthorized(request: Request, call_next):
    if request.url.path == "/docs":
        raise HTTPException(status_code=403, detail="Documentação desativada por segurança.")
    return await call_next(request)

# ---------------------- EXECUÇÃO ----------------------
if __name__ == "__main__":
    import uvicorn
    print(f"[{now()}] 🧠 Remote Console iniciado em http://127.0.0.1:8093")
    log("MindScan Remote Console iniciada com sucesso.", "INFO")
    uvicorn.run(app, host="127.0.0.1", port=8093)
