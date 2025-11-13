"""
MindScan Task Watcher Auto v2.0 — Inteligência Supervisora
Agora com suporte a políticas dinâmicas via supervisor_rules.json
"""

import os
import time
import json
import subprocess
from datetime import datetime
from rich.console import Console

console = Console()

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONFIG_PATH = os.path.join(ROOT_DIR, "maintenance", "configs", "supervisor_rules.json")
LOG_PATH = os.path.join(ROOT_DIR, "maintenance", "logs", "watchdog_mindscan.json")
SCRIPTS_DIR = os.path.join(ROOT_DIR, "scripts")

def load_policies():
    """Carrega políticas de supervisão."""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[red]Falha ao carregar políticas: {e}[/red]")
        return {}

def log_event(event, status="OK"):
    """Registra evento JSON no log do Watchdog."""
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event,
        "status": status
    }
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    try:
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
        data.append(entry)
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(data[-200:], f, indent=2)
    except Exception as e:
        console.print(f"[red]Erro ao gravar log: {e}[/red]")

def execute_script(script, cooldown):
    """Executa script e aplica cooldown."""
    try:
        log_event(f"Iniciando script: {script}")
        subprocess.run(["python", os.path.join(SCRIPTS_DIR, script)], check=True)
        log_event(f"Concluído: {script}")
        time.sleep(cooldown)
    except subprocess.CalledProcessError as e:
        log_event(f"Falha em {script}: {e}", status="ERRO")

def main():
    policies = load_policies()
    watchdog = policies.get("watchdog_policies", {})
    interval = watchdog.get("scan_interval_seconds", 5)
    cooldown = watchdog.get("restart_cooldown_seconds", 10)
    max_retries = watchdog.get("max_retries", 3)
    retries = {}

    console.print(f"[cyan]MindScan Watchdog iniciado com política dinâmica (intervalo {interval}s)[/cyan]")

    while True:
        for script in watchdog.get("priority_scripts", []):
            path = os.path.join(SCRIPTS_DIR, script)
            if os.path.exists(path):
                try:
                    execute_script(script, cooldown)
                except Exception as e:
                    retries[script] = retries.get(script, 0) + 1
                    if retries[script] <= max_retries:
                        log_event(f"Tentando reiniciar {script} (tentativa {retries[script]})", status="RETRY")
                    else:
                        log_event(f"Máx. tentativas atingido para {script}", status="FAIL")
            else:
                log_event(f"Script ausente: {script}", status="WARNING")
        time.sleep(interval)

if __name__ == "__main__":
    main()
