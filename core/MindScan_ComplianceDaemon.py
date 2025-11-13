import os
import time
import threading
import subprocess
import json
import requests
from datetime import datetime
from pathlib import Path
from watchfiles import watch

# ============================================
# ⚖️ MindScan ComplianceDaemon — v5.2
# ============================================
# Autor: Leo Vinci (GPT Inovexa)
# Data: 12/11/2025
# Função: Executor contínuo do ComplianceKit + vigilância ética autônoma
# ============================================

BASE_DIR = Path(r"D:\MindScan")
CORE_DIR = BASE_DIR / "core"
LOG_DIR = BASE_DIR / "logs"
MANIFEST_PATH = BASE_DIR / "update_manifest.json"
COMPLIANCE_KIT = CORE_DIR / "MindScan_ComplianceKit.py"
LOG_API = "http://127.0.0.1:8091/logs"

SCAN_INTERVAL = 6 * 3600  # 6 horas
WATCHED_DIRS = [LOG_DIR, BASE_DIR / "datasets", BASE_DIR / "cache"]


# ---------------------- UTILITÁRIOS ----------------------
def now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")

def log(message, level="INFO"):
    print(f"[{now()}] [ComplianceDaemon] [{level}] {message}")
    try:
        requests.post(LOG_API, json={"origin": "ComplianceDaemon", "message": message, "level": level}, timeout=1)
    except Exception:
        pass


def run_compliance_kit(reason="scheduled"):
    """Executa o ComplianceKit com subprocess e registra o motivo."""
    log(f"Execução do ComplianceKit iniciada (motivo: {reason}).")
    try:
        subprocess.run(["python", str(COMPLIANCE_KIT)], check=True)
        log("ComplianceKit concluído com sucesso.")
    except subprocess.CalledProcessError as e:
        log(f"Erro ao executar ComplianceKit: {e}", "ERROR")
    except Exception as e:
        log(f"Exceção inesperada: {e}", "ERROR")


# ---------------------- WATCHERS ----------------------
def watch_directories():
    """Monitora diretórios e executa anonimização quando arquivos novos aparecem."""
    log("Monitorando diretórios sensíveis para anonimização automática.")
    for changes in watch(*WATCHED_DIRS, stop_event=None):
        for change_type, path in changes:
            if any(path.endswith(ext) for ext in [".log", ".txt", ".json", ".csv"]):
                log(f"Arquivo detectado: {path} → disparando ComplianceKit.")
                run_compliance_kit(reason=f"file_event: {path}")


def watch_manifest():
    """Monitora o manifesto de updates para reagir a eventos críticos."""
    last_hash = None
    while True:
        if MANIFEST_PATH.exists():
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                content = f.read()
                new_hash = hash(content)
                if last_hash and new_hash != last_hash:
                    log("Alteração detectada no update_manifest.json → Compliance reativo.")
                    run_compliance_kit(reason="manifest_change")
                last_hash = new_hash
        time.sleep(120)


# ---------------------- LOOP PRINCIPAL ----------------------
def periodic_scan():
    """Executa varreduras periódicas a cada 6 horas."""
    while True:
        run_compliance_kit(reason="periodic")
        time.sleep(SCAN_INTERVAL)


def main():
    log("ComplianceDaemon iniciado. Modo contínuo ativo.")
    # Threads paralelas: agendamento, diretórios, manifesto
    threads = [
        threading.Thread(target=periodic_scan, daemon=True),
        threading.Thread(target=watch_directories, daemon=True),
        threading.Thread(target=watch_manifest, daemon=True)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("ComplianceDaemon encerrado manualmente.", "WARN")
