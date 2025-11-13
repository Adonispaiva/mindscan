import os
import sys
import subprocess
import requests
from datetime import datetime
import time
import shutil

# ============================================
# 🧠 Inovexa MindScan Web — Service Installer v4.3 (Python Edition)
# ============================================
# Autor: Leo Vinci (GPT Inovexa)
# Data: 12/11/2025
# Função: Registrar e gerenciar serviços persistentes MindScan Web no Windows
# ============================================

NSSM_PATH = r"C:\nssm\nssm.exe"
PYTHON_EXE = "python"
BASE_PATH = r"D:\MindScan\core"
LOG_DIR = r"D:\MindScan\logs"

SERVICES = [
    {"name": "MindScan_SystemManager", "script": os.path.join(BASE_PATH, "system_manager.py")},
    {"name": "MindScan_AutoSync", "script": os.path.join(BASE_PATH, "supervisao_diretor_auto_sync.py")},
    {"name": "MindScan_CommandCenter", "script": os.path.join(BASE_PATH, "command_center_integration.py")},
]

LOG_API = "http://127.0.0.1:8091/logs"


# ------------------------- UTILITÁRIOS -------------------------
def now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")


def log(msg, level="INFO"):
    line = f"[{now()}] [Installer] [{level}] {msg}"
    print(line)
    try:
        requests.post(LOG_API, json={"origin": "Installer", "message": msg, "level": level}, timeout=1)
    except Exception:
        pass


def check_dependencies():
    if not shutil.which(PYTHON_EXE):
        log("Python não encontrado no PATH.", "ERROR")
        sys.exit(1)

    if not os.path.exists(NSSM_PATH):
        log(f"NSSM não encontrado em {NSSM_PATH}.", "ERROR")
        log("Baixe em: https://nssm.cc/download e extraia para C:\\nssm", "WARN")
        sys.exit(1)

    os.makedirs(LOG_DIR, exist_ok=True)


def run_nssm_command(args):
    try:
        subprocess.run([NSSM_PATH] + args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        log(f"Erro NSSM: {e}", "ERROR")
        return False


# ------------------------- OPERAÇÕES PRINCIPAIS -------------------------
def install_service(name, script):
    log(f"Instalando serviço {name}...")
    run_nssm_command(["install", name, PYTHON_EXE, script])
    run_nssm_command(["set", name, "AppDirectory", BASE_PATH])
    run_nssm_command(["set", name, "Start", "SERVICE_AUTO_START"])
    run_nssm_command(["set", name, "AppStdout", os.path.join(LOG_DIR, f"{name}.out.log")])
    run_nssm_command(["set", name, "AppStderr", os.path.join(LOG_DIR, f"{name}.err.log")])
    run_nssm_command(["set", name, "Description", f"Inovexa MindScan Service — {name}"])
    log(f"Serviço {name} instalado com sucesso.")


def remove_service(name):
    log(f"Removendo serviço {name}...")
    run_nssm_command(["remove", name, "confirm"])
    log(f"Serviço {name} removido.")


def start_service(name):
    log(f"Iniciando serviço {name}...")
    run_nssm_command(["start", name])
    log(f"{name} iniciado.")


def stop_service(name):
    log(f"Parando serviço {name}...")
    run_nssm_command(["stop", name])
    log(f"{name} parado.")


def status_service(name):
    try:
        output = subprocess.check_output(["sc", "query", name], text=True)
        if "RUNNING" in output:
            state = "🟢 Em execução"
        elif "STOPPED" in output:
            state = "🔴 Parado"
        else:
            state = "⚪ Desconhecido"
        log(f"{name}: {state}")
    except subprocess.CalledProcessError:
        log(f"{name}: não registrado no sistema.", "WARN")


# ------------------------- MAIN -------------------------
def main():
    if len(sys.argv) < 2:
        print("Uso: MindScan_ServiceInstaller.py [install|remove|start|stop|status]")
        sys.exit(0)

    action = sys.argv[1].lower()
    check_dependencies()

    if action == "install":
        for svc in SERVICES:
            install_service(svc["name"], svc["script"])
        log("Todos os serviços MindScan foram instalados.", "INFO")

    elif action == "remove":
        for svc in SERVICES:
            remove_service(svc["name"])
        log("Todos os serviços MindScan foram removidos.", "INFO")

    elif action == "start":
        for svc in SERVICES:
            start_service(svc["name"])
        log("Todos os serviços MindScan foram iniciados.", "INFO")

    elif action == "stop":
        for svc in SERVICES:
            stop_service(svc["name"])
        log("Todos os serviços MindScan foram parados.", "INFO")

    elif action == "status":
        for svc in SERVICES:
            status_service(svc["name"])

    else:
        log(f"Ação inválida: {action}", "ERROR")


if __name__ == "__main__":
    main()
