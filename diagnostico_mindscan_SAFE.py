"""
MindScan Diagnóstico SAFE v1.0
Autor: Inovexa Software
Diretor Técnico: Leo Vinci
Descrição:
Executa verificações automáticas de integridade, desempenho e estabilidade
do ecossistema MindScan. Gera relatórios para o Command Center e logs locais.
"""

import os
import json
import time
import psutil
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, "maintenance", "configs", "supervisor_rules.json")
LOG_PATH = os.path.join(ROOT_DIR, "maintenance", "logs", "diagnostico_safe.json")
EVENTS_PATH = os.path.join(ROOT_DIR, "command_center", "notifier_events.json")

def load_policies():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def write_log(entry):
    """Salva resultados no log do diagnóstico e no painel de eventos."""
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    timestamp = datetime.utcnow().isoformat()
    entry["timestamp"] = timestamp

    # Atualiza log local
    try:
        data = []
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        data.append(entry)
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(data[-100:], f, indent=2)
    except Exception:
        pass

    # Atualiza painel
    try:
        if os.path.exists(EVENTS_PATH):
            with open(EVENTS_PATH, "r", encoding="utf-8") as f:
                events = json.load(f)
        else:
            events = []
        events.append({
            "timestamp": timestamp,
            "event": f"Diagnóstico SAFE — {entry['summary']}",
            "status": entry["status"]
        })
        with open(EVENTS_PATH, "w", encoding="utf-8") as f:
            json.dump(events[-200:], f, indent=2)
    except Exception:
        pass

def check_system_health(policies):
    """Executa verificações de recursos e integridade."""
    recovery = policies.get("recovery_policies", {}).get("self_check_rules", {})
    cpu_threshold = recovery.get("cpu_threshold_percent", 90)
    mem_threshold = recovery.get("memory_threshold_percent", 85)
    disk_min_gb = recovery.get("disk_space_min_gb", 2)

    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").free / (1024 ** 3)

    status = "OK"
    summary = "Todos os parâmetros dentro do normal"
    alerts = []

    if cpu > cpu_threshold:
        status, summary = "⚠️", "CPU acima do limite"
        alerts.append("cpu_threshold_exceeded")
    if mem > mem_threshold:
        status, summary = "⚠️", "Memória acima do limite"
        alerts.append("memory_threshold_exceeded")
    if disk < disk_min_gb:
        status, summary = "⚠️", "Espaço em disco crítico"
        alerts.append("low_disk_space")

    return {
        "summary": summary,
        "status": status,
        "metrics": {
            "cpu_usage_percent": cpu,
            "memory_usage_percent": mem,
            "disk_free_gb": round(disk, 2)
        },
        "alerts": alerts
    }

def main():
    policies = load_policies()
    interval = policies.get("diagnostics_policies", {}).get("safe_check_interval_minutes", 30) * 60

    while True:
        report = check_system_health(policies)
        write_log(report)
        print(f"[SAFE] {report['summary']} | CPU: {report['metrics']['cpu_usage_percent']}% | MEM: {report['metrics']['memory_usage_percent']}% | DISK: {report['metrics']['disk_free_gb']} GB")
        time.sleep(interval)

if __name__ == "__main__":
    main()
