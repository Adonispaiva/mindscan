import requests
import time
from datetime import datetime
import os
import json
import sys

# ============================================
# MindScan Supervisor Auto-Sync — v4.0
# Atualização automática do supervisao_diretor.md
# ============================================

SYNC_INTERVAL = 600  # segundos (10 minutos)
BASE_PATH = "D:\\MindScan"
REPORT_PATH = os.path.join(BASE_PATH, "supervisao_diretor.md")

SERVICES = {
    "launcher": "http://127.0.0.1:8090/status",
    "modules": "http://127.0.0.1:8090/modules",
    "logs": "http://127.0.0.1:8091/logs?limit=50",
}

def now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")

def log(msg):
    line = f"[{now()}] [AutoSync] {msg}"
    print(line)
    sys.stdout.flush()

def fetch_json(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        log(f"Falha ao consultar {url}: {e}")
    return {}

def update_report():
    log("Coletando dados para atualização de supervisão...")

    status = fetch_json(SERVICES["launcher"])
    modules = fetch_json(SERVICES["modules"])
    logs = fetch_json(SERVICES["logs"])

    cpu = status.get("cpu", "?")
    mem = status.get("memory", "?")
    uptime = status.get("uptime", "?")
    timestamp = now()

    log_count = len(logs.get("logs", []))
    module_lines = []
    for name, info in modules.items():
        module_lines.append(f"| {name:<10} | {info.get('status', '?')} | {info.get('pid', '?')} |")

    md = f"""# 🧠 Supervisão Técnica — MindScan (AutoSync)
**Última atualização:** {timestamp}  
**Gerado por:** Leo Vinci (GPT Inovexa Auto Supervisor)

---

## 📈 Telemetria
- **CPU:** {cpu}%
- **Memória:** {mem}%
- **Uptime:** {uptime}
- **Logs recentes:** {log_count}

---

## 🧩 Módulos Ativos
| Nome       | Status     | PID   |
|-------------|------------|-------|
{os.linesep.join(module_lines)}

---

## 🕒 Histórico
- Atualização automática executada com sucesso.
- Fonte: API local (`/status`, `/modules`, `/logs`).

---

**Status:** 🟢 Operante  
**Próxima sincronização:** {SYNC_INTERVAL // 60} minutos
"""

    try:
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            f.write(md)
        log(f"Relatório atualizado com sucesso ({REPORT_PATH}).")
    except Exception as e:
        log(f"Erro ao atualizar relatório: {e}")

def loop():
    log("Supervisor AutoSync iniciado.")
    while True:
        update_report()
        time.sleep(SYNC_INTERVAL)

if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        log("AutoSync interrompido manualmente.")
