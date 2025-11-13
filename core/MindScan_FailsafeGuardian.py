import os
import time
import json
import psutil
import requests
import subprocess
from datetime import datetime
from pathlib import Path
import hashlib

# ============================================
# 🧠 MindScan Failsafe Guardian — v4.7
# ============================================
# Autor: Leo Vinci (GPT Inovexa)
# Data: 12/11/2025
# Função: Vigia persistente — integridade, disponibilidade e rollback automático
# ============================================

MANIFEST_PATH = Path(r"D:\MindScan\update_manifest.json")
ROLLBACK_MANAGER = Path(r"D:\MindScan\core\MindScan_RollbackManager.py")
SERVICE_INSTALLER = Path(r"D:\MindScan\core\MindScan_ServiceInstaller.py")
LOG_API = "http://127.0.0.1:8091/logs"
CHECK_INTERVAL = 60  # segundos
CPU_THRESHOLD = 90.0
MEM_THRESHOLD = 85.0


def now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")


def log(msg, level="INFO"):
    print(f"[{now()}] [Guardian] [{level}] {msg}")
    try:
        requests.post(LOG_API, json={"origin": "FailsafeGuardian", "message": msg, "level": level}, timeout=1)
    except Exception:
        pass


def load_manifest():
    if not MANIFEST_PATH.exists():
        log("Manifesto não encontrado. Abortando.", "ERROR")
        return None
    try:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log(f"Erro ao ler manifesto: {e}", "ERROR")
        return None


def sha256sum(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_integrity(manifest):
    try:
        current_hash = manifest["current_build"]["integrity_hash"]
        tag = manifest["current_build"]["version_tag"]
        backup_path = Path(rf"D:\MindScan\backups\{tag}.zip")
        if not backup_path.exists():
            return True  # ignora se sem backup
        calc = sha256sum(backup_path)
        if calc != current_hash:
            log("❌ Integridade corrompida detectada!", "ERROR")
            return False
        return True
    except Exception as e:
        log(f"Erro ao verificar integridade: {e}", "ERROR")
        return True


def check_services():
    """Verifica se os principais serviços estão rodando e saudáveis."""
    expected = ["MindScan_SystemManager", "MindScan_AutoSync", "MindScan_CommandCenter"]
    active = {p.name(): p for p in psutil.process_iter(['name'])}
    for svc in expected:
        found = any(svc.lower() in p.name().lower() for p in psutil.process_iter(['name']))
        if not found:
            log(f"⚠️ Serviço ausente: {svc}. Tentando reiniciar...", "WARN")
            subprocess.run(["python", str(SERVICE_INSTALLER), "start"])
            time.sleep(5)
            if not any(svc.lower() in p.name().lower() for p in psutil.process_iter(['name'])):
                log(f"Falha crítica: {svc} não pôde ser reiniciado.", "ERROR")
                trigger_rollback(f"Serviço {svc} inativo")
        else:
            log(f"Serviço {svc} operacional.", "INFO")


def check_resource_usage():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    if cpu > CPU_THRESHOLD:
        log(f"CPU alta detectada: {cpu}%", "WARN")
    if mem > MEM_THRESHOLD:
        log(f"Uso de memória elevado: {mem}%", "WARN")
    if cpu > 98 or mem > 95:
        log("⚠️ Potencial loop ou sobrecarga detectado. Preparando rollback...", "ERROR")
        trigger_rollback("resource overload")


def trigger_rollback(reason):
    """Executa rollback imediato e registra o evento."""
    log(f"Iniciando rollback automático devido a: {reason}", "WARN")
    try:
        subprocess.run(["python", str(ROLLBACK_MANAGER)], check=True)
        log("Rollback executado com sucesso.", "INFO")
    except Exception as e:
        log(f"Erro ao acionar rollback: {e}", "ERROR")


def main():
    log("Failsafe Guardian iniciado.")
    while True:
        manifest = load_manifest()
        if not manifest:
            log("Manifesto inválido. Nova tentativa em 1 minuto.", "WARN")
            time.sleep(CHECK_INTERVAL)
            continue

        integrity = verify_integrity(manifest)
        if not integrity:
            trigger_rollback("integrity failure")
            time.sleep(CHECK_INTERVAL)
            continue

        check_services()
        check_resource_usage()
        log("Ciclo de verificação concluído.", "INFO")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("Failsafe Guardian encerrado manualmente.", "WARN")
