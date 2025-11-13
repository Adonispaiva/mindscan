import asyncio
import subprocess
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import threading

# ===========================================
# MindScan Web — FastAPI Backend (v3.1)
# ===========================================

app = FastAPI(title="MindScan Web API", version="3.1")

# ---------------------- CONFIGURAÇÕES ----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = []
executor = ThreadPoolExecutor(max_workers=4)
loop = asyncio.get_event_loop()

# Ajuste de encoding
sys.stdout.reconfigure(encoding="utf-8")

# Timezone local
def now():
    return datetime.now().astimezone().strftime("%H:%M:%S")

# ---------------------- FUNÇÕES INTERNAS ----------------------
def log(message: str):
    timestamp = now()
    line = f"[{timestamp}] {message}"
    print(line)
    for ws in clients:
        loop.create_task(ws.send_text(line))

def run_launcher():
    """Executa o orquestrador principal MindScan."""
    try:
        log("Inicializando módulos do MindScan...")
        process = subprocess.Popen(
            ["python", "D:\\MindScan\\core\\mindscan_launcher_service.py"],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )
        for line in process.stdout:
            log(line.strip())
        process.wait()
        log("Processo do MindScan finalizado.")
    except Exception as e:
        log(f"Erro ao executar MindScan: {e}")

def stop_mindscan():
    """Encerra todos os processos MindScan em execução."""
    try:
        subprocess.run(
            'taskkill /F /IM python.exe /T',
            shell=True,
            capture_output=True,
            text=True
        )
        log("MindScan encerrado com sucesso.")
    except Exception as e:
        log(f"Erro ao encerrar MindScan: {e}")

# ---------------------- ROTAS HTTP ----------------------
@app.get("/")
async def root():
    return {"status": "MindScan Web ativo", "time": now()}

@app.post("/start")
async def start_mindscan():
    """Aciona o botão Iniciar via navegador."""
    loop.run_in_executor(executor, run_launcher)
    return {"status": "Iniciando módulos MindScan", "time": now()}

@app.post("/stop")
async def stop():
    """Aciona o botão Encerrar via navegador."""
    loop.run_in_executor(executor, stop_mindscan)
    return {"status": "Encerrando MindScan", "time": now()}

@app.get("/logs")
async def get_logs_placeholder():
    """Endpoint temporário para o painel de logs."""
    return {"logs": "Em desenvolvimento — Fase 3", "time": now()}

# ---------------------- WEBSOCKET ----------------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    log("Novo cliente conectado ao WebSocket.")
    try:
        while True:
            data = await websocket.receive_text()
            log(f"Comando recebido: {data}")
    except WebSocketDisconnect:
        clients.remove(websocket)
        log("Cliente desconectado do WebSocket.")

# ---------------------- INICIALIZAÇÃO ----------------------
if __name__ == "__main__":
    import uvicorn
    log("Servidor MindScan Web iniciado.")
    uvicorn.run(app, host="127.0.0.1", port=8080)
