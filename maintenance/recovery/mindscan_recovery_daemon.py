"""
MindScan Recovery Daemon v1.1 — Com políticas dinâmicas
Integração completa com supervisor_rules.json
"""

import os
import time
import json
import psutil
import subprocess
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONFIG_PATH = os.path.join(ROOT_DIR, "maintenance", "configs", "supervisor_rules.json")
LOG_PATH = os.path.join(ROOT_DIR, "maintenance", "logs", "recovery_daemon.log")

WATCHDOG_PATH = os.path.join(ROOT_DIR, "maintenance", "watchdog", "mindscan_task_watcher_auto.py")
PANEL_PATH = os.path.join(ROOT_DIR, "command_center", "command_center_interface.py")

def load_policies():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log(f"Erro ao carregar políticas: {e}")
        return {}

def log(message):
    timestamp = datetime.utcnow().isoformat()
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def is_process_running(target_path: str) -> bool:
    for proc in psutil.process_iter(attrs=["cmdline"]):
        try:
            cmd = " ".join(proc.info["cmdline"]).lower()
            if target_path.lower() in cmd and "python" in cmd:
                return True
        except Exception:
            continue
    return False

def start_process(path, name):
    try:
        subprocess.Popen(["python", path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        log(f"Processo iniciado: {name}")
    except Exception as e:
        log(f"Falha ao iniciar {name}: {e}")

def recovery_loop():
    policies = load_policies()
    recovery = policies.get("recovery_policies", {})
    heartbeat = recovery.get("heartbeat_interval_minutes", 5) * 60
    max_restarts = recovery.get("max_restarts_per_day", 10)
    restarts = {"watchdog": 0, "panel": 0}

    log("MindScan Recovery Daemon com políticas dinâmicas iniciado.")

    while True:
        if not is_process_running(WATCHDOG_PATH):
            if restarts["watchdog"] < max_restarts:
                restarts["watchdog"] += 1
                start_process(WATCHDOG_PATH, "Watchdog MindScan")
            else:
                log("Limite diário de reinícios do Watchdog atingido.")

        if not is_process_running(PANEL_PATH):
            if restarts["panel"] < max_restarts:
                restarts["panel"] += 1
                start_process(PANEL_PATH, "Painel Command Center")
            else:
                log("Limite diário de reinícios do Painel atingido.")

        log("Heartbeat ativo — sistemas supervisionados em operação.")
        time.sleep(heartbeat)

if __name__ == "__main__":
    recovery_loop()
