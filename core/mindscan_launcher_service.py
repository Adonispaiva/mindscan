import asyncio
import psutil
import time
import json
import subprocess
import threading
from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# ============================================
# MindScan Launcher Service — v3.5
# Núcleo orquestrador com telemetria
# ============================================

app = FastAPI(title="MindScan Launcher Service", version="3.5")

# ---------------------- CONFIGURAÇÕES ----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

modules = {
    "watchdog": {"status": "idle", "pid": None},
    "safe": {"status": "idle", "pid": None},
    "recovery": {"status": "idle", "pid": None},
}

telemetry = {
    "cpu": 0,
    "memory": 0,
    "uptime": "00:00:00",
    "start_time": datetime.now().astimezone().strftime("%H:%M:%S"),
}

shutdown_event = threading.Event()
start_time = time.time()

# ---------------------- FUNÇÕES AUXILIARES ----------------------
def now():
    return datetime.now().astimezone().strftime("%H:%M:%S")

def log(msg: str):
    line = f"[{now()}] {msg}"
    print(line)
    sys.stdout.flush()

def start_module(name: str, path: str):
    try:
        log(f"Iniciando módulo {name}...")
        proc = subprocess.Popen(
            ["python", path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )
        modules[name]["status"] = "running"
        modules[name]["pid"] = proc.pid
        log(f"{name} iniciado (PID {proc.pid}).")
        return proc
    except Exception as e:
        log(f"Erro ao iniciar {name}: {e}")
        modules[name]["status"] = "error"
        return None

def stop_all_modules():
    for name, info in modules.items():
        if info["pid"]:
            try:
                psutil.Process(info["pid"]).terminate()
                log(f"Módulo {name} encerrado (PID {info['pid']}).")
                modules[name]["status"] = "stopped"
            except Exception:
                log(f"Falha ao encerrar módulo {name}.")
    shutdown_event.set()

def update_telemetry():
    telemetry["cpu"] = psutil.cpu_percent(interval=1)
    telemetry["memory"] = psutil.virtual_memory().percent
    uptime_seconds = int(time.time() - start_time)
    telemetry["uptime"] = str(timedelta(seconds=uptime_seconds))

# ---------------------- LOOP DE EXECUÇÃO ----------------------
async def monitor_loop():
    while not shutdown_event.is_set():
        update_telemetry()
        await asyncio.sleep(2)

# ---------------------- ROTAS HTTP ----------------------
@app.get("/status")
def get_status():
    update_telemetry()
    return {
        "time": now(),
        "cpu": telemetry["cpu"],
        "memory": telemetry["memory"],
        "uptime": telemetry["uptime"],
    }

@app.get("/modules")
def get_modules():
    return modules

@app.post("/start")
def start_all():
    if any(m["status"] == "running" for m in modules.values()):
        return {"status": "already_running", "time": now()}

    base_path = os.path.dirname(__file__)
    paths = {
        "watchdog": os.path.join(base_path, "..", "modules", "watchdog", "main.py"),
        "safe": os.path.join(base_path, "..", "modules", "safe", "main.py"),
        "recovery": os.path.join(base_path, "..", "modules", "recovery", "main.py"),
    }

    for name, path in paths.items():
        start_module(name, os.path.abspath(path))

    return {"status": "started", "modules": list(modules.keys()), "time": now()}

@app.post("/stop")
def stop_all():
    stop_all_modules()
    return {"status": "stopped", "time": now()}

# ---------------------- INICIALIZAÇÃO ----------------------
def main():
    log("MindScan Launcher iniciado.")
    loop = asyncio.get_event_loop()
    loop.create_task(monitor_loop())

    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8090)

if __name__ == "__main__":
    main()
