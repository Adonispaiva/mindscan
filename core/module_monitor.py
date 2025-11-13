import psutil
import time
import json
import threading
import requests
from datetime import datetime
import os
import sys

# ============================================
# MindScan Module Monitor — v3.6
# Monitoramento ativo + Auto-recovery
# ============================================

MONITOR_INTERVAL = 3  # segundos
LAUNCHER_URL = "http://127.0.0.1:8090/modules"
LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "logs", "module_monitor.json")

lock = threading.Lock()
running = True


def now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")


def log_event(message: str, level: str = "INFO"):
    entry = {"time": now(), "level": level, "message": message}
    print(f"[{entry['time']}] [{level}] {message}")
    sys.stdout.flush()

    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"[{now()}] [ERROR] Falha ao registrar log: {e}")


def get_modules_status():
    try:
        response = requests.get(LAUNCHER_URL, timeout=2)
        if response.status_code == 200:
            return response.json()
        else:
            log_event(f"Erro HTTP {response.status_code} ao consultar módulos", "WARN")
    except Exception as e:
        log_event(f"Erro ao acessar launcher: {e}", "ERROR")
    return {}


def check_process(pid):
    try:
        p = psutil.Process(pid)
        return p.is_running() and p.status() != psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return False
    except Exception as e:
        log_event(f"Erro ao verificar PID {pid}: {e}", "ERROR")
        return False


def restart_module(name):
    try:
        log_event(f"Tentando reiniciar módulo {name}...", "WARN")
        requests.post(f"http://127.0.0.1:8090/start")
        log_event(f"Módulo {name} reiniciado com sucesso.", "INFO")
    except Exception as e:
        log_event(f"Falha ao reiniciar {name}: {e}", "ERROR")


def monitor_loop():
    log_event("Monitor de módulos iniciado.")
    while running:
        with lock:
            modules = get_modules_status()
            if not modules:
                log_event("Sem resposta do launcher. Tentando novamente...", "WARN")
                time.sleep(MONITOR_INTERVAL)
                continue

            for name, info in modules.items():
                pid = info.get("pid")
                status = info.get("status")
                if status == "running" and not check_process(pid):
                    log_event(f"⚠️ Módulo {name} inativo (PID {pid}).", "WARN")
                    restart_module(name)
                elif status == "running":
                    log_event(f"Módulo {name} OK (PID {pid}).", "INFO")
                else:
                    log_event(f"Módulo {name} estado: {status}.", "INFO")

        time.sleep(MONITOR_INTERVAL)

    log_event("Monitor de módulos encerrado.")


def start_monitor():
    thread = threading.Thread(target=monitor_loop, daemon=True)
    thread.start()
    return thread


if __name__ == "__main__":
    try:
        t = start_monitor()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        running = False
        log_event("Encerrando monitor por interrupção manual.", "WARN")
