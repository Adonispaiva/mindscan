import time
import threading
import requests
import subprocess
import psutil
from datetime import datetime
import sys
import os

# ============================================
# MindScan System Manager — v3.8
# Controle global de ciclo de vida e heartbeat
# ============================================

SERVICES = {
    "launcher": {"port": 8090, "process": None, "path": "D:\\MindScan\\core\\mindscan_launcher_service.py"},
    "monitor": {"port": None, "process": None, "path": "D:\\MindScan\\core\\module_monitor.py"},
    "loghandler": {"port": 8091, "process": None, "path": "D:\\MindScan\\core\\log_handler.py"},
}

HEARTBEAT_INTERVAL = 5
HEALTH_TIMEOUT = 10
running = True


def now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")


def log(msg):
    print(f"[{now()}] [SYSTEM] {msg}")
    sys.stdout.flush()
    try:
        requests.post(
            "http://127.0.0.1:8091/logs",
            json={"origin": "SYSTEM", "message": msg, "level": "INFO"},
            timeout=1,
        )
    except Exception:
        pass


def start_service(name):
    service = SERVICES[name]
    if service["process"] and psutil.pid_exists(service["process"].pid):
        log(f"{name} já está em execução.")
        return

    try:
        log(f"Iniciando serviço {name}...")
        proc = subprocess.Popen(
            ["python", service["path"]],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )
        SERVICES[name]["process"] = proc
        log(f"Serviço {name} iniciado (PID {proc.pid}).")
    except Exception as e:
        log(f"Erro ao iniciar {name}: {e}")


def stop_service(name):
    service = SERVICES[name]
    proc = service.get("process")
    if proc and psutil.pid_exists(proc.pid):
        try:
            psutil.Process(proc.pid).terminate()
            log(f"Serviço {name} encerrado (PID {proc.pid}).")
        except Exception as e:
            log(f"Erro ao encerrar {name}: {e}")
    else:
        log(f"Serviço {name} já estava inativo.")


def check_health():
    for name, svc in SERVICES.items():
        port = svc["port"]
        if not port:
            continue
        try:
            response = requests.get(f"http://127.0.0.1:{port}/status", timeout=2)
            if response.status_code == 200:
                log(f"{name} saudável.")
            else:
                log(f"⚠️ {name} respondeu com status {response.status_code}.")
        except Exception:
            log(f"❌ {name} inativo. Tentando reiniciar...")
            restart_service(name)


def restart_service(name):
    stop_service(name)
    time.sleep(1)
    start_service(name)


def heartbeat_loop():
    log("Heartbeat iniciado.")
    while running:
        try:
            check_health()
        except Exception as e:
            log(f"Erro no heartbeat: {e}")
        time.sleep(HEARTBEAT_INTERVAL)
    log("Heartbeat encerrado.")


def shutdown_all():
    global running
    running = False
    log("Encerrando todos os serviços...")
    for name in SERVICES:
        stop_service(name)
    log("MindScan encerrado com sucesso.")


def restart_all():
    log("Reiniciando todos os serviços...")
    for name in SERVICES:
        restart_service(name)
    log("Reinicialização completa.")


def main():
    log("System Manager iniciado.")
    for name in SERVICES:
        start_service(name)

    threading.Thread(target=heartbeat_loop, daemon=True).start()

    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown_all()


if __name__ == "__main__":
    main()
