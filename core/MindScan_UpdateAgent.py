import os
import sys
import time
import json
import requests
import hashlib
import zipfile
import subprocess
from datetime import datetime
from pathlib import Path

# ============================================
# 🧠 MindScan Update Agent — v4.4
# ============================================
# Autor: Leo Vinci (GPT Inovexa)
# Data: 12/11/2025
# Função: Atualização automática e segura via GitHub API
# ============================================

REPO_OWNER = "InovexaSoftware"
REPO_NAME = "MindScan"
API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
DOWNLOAD_DIR = Path(r"D:\MindScan\updates")
INSTALL_DIR = Path(r"D:\MindScan")
LOG_API = "http://127.0.0.1:8091/logs"

# ---------------------- UTILITÁRIOS ----------------------
def now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")

def log(message, level="INFO"):
    print(f"[{now()}] [{level}] {message}")
    try:
        requests.post(LOG_API, json={"origin": "UpdateAgent", "message": message, "level": level}, timeout=1)
    except Exception:
        pass

def sha256sum(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def restart_services():
    log("Reiniciando serviços MindScan...")
    subprocess.run(["python", "D:\\MindScan\\core\\MindScan_ServiceInstaller.py", "stop"])
    time.sleep(2)
    subprocess.run(["python", "D:\\MindScan\\core\\MindScan_ServiceInstaller.py", "start"])
    log("Serviços reiniciados com sucesso.")

# ---------------------- ATUALIZAÇÃO ----------------------
def get_latest_release():
    log("Consultando GitHub API para nova versão...")
    try:
        r = requests.get(API_URL, timeout=10)
        if r.status_code != 200:
            log(f"Erro ao consultar API: {r.status_code}", "ERROR")
            return None
        return r.json()
    except Exception as e:
        log(f"Falha ao acessar API GitHub: {e}", "ERROR")
        return None

def download_asset(url, filename):
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    log(f"Baixando atualização: {filename}")
    try:
        r = requests.get(url, stream=True, timeout=30)
        if r.status_code == 200:
            with open(DOWNLOAD_DIR / filename, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
            log(f"Download concluído: {filename}")
            return DOWNLOAD_DIR / filename
        else:
            log(f"Erro no download ({r.status_code})", "ERROR")
    except Exception as e:
        log(f"Erro no download: {e}", "ERROR")
    return None

def apply_update(zip_path):
    log("Aplicando atualização...")
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(INSTALL_DIR)
        log("Arquivos extraídos com sucesso.")
        restart_services()
        return True
    except Exception as e:
        log(f"Erro ao aplicar atualização: {e}", "ERROR")
        return False

# ---------------------- CICLO PRINCIPAL ----------------------
def update_cycle():
    release = get_latest_release()
    if not release:
        return

    tag = release.get("tag_name", "unknown")
    assets = release.get("assets", [])
    if not assets:
        log("Nenhum pacote disponível na release.", "WARN")
        return

    latest_asset = assets[0]
    asset_url = latest_asset["browser_download_url"]
    filename = latest_asset["name"]

    # Baixar e validar
    file_path = download_asset(asset_url, filename)
    if not file_path:
        return

    # Verificar integridade se disponível
    checksum = latest_asset.get("sha256", "")
    if checksum:
        calc = sha256sum(file_path)
        if calc != checksum:
            log("Hash inválido! Atualização abortada.", "ERROR")
            return

    # Aplicar atualização
    if apply_update(file_path):
        log(f"Atualização para {tag} concluída com sucesso.", "INFO")
    else:
        log("Atualização falhou. Verifique logs.", "ERROR")

def main():
    log("MindScan UpdateAgent iniciado.")
    while True:
        try:
            update_cycle()
            log("Aguardando próxima verificação (6h)...")
            time.sleep(21600)  # 6 horas
        except KeyboardInterrupt:
            log("Agente encerrado manualmente.", "WARN")
            sys.exit(0)
        except Exception as e:
            log(f"Erro inesperado no ciclo: {e}", "ERROR")
            time.sleep(300)

if __name__ == "__main__":
    main()
