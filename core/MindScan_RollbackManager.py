import os
import json
import zipfile
import shutil
import subprocess
import hashlib
import requests
from datetime import datetime
from pathlib import Path

# ============================================
# 🧠 MindScan Rollback Manager — v4.6
# ============================================
# Autor: Leo Vinci (GPT Inovexa)
# Data: 12/11/2025
# Função: Reversão automática de versão em caso de falha
# ============================================

MANIFEST_PATH = Path(r"D:\MindScan\update_manifest.json")
BACKUP_DIR = Path(r"D:\MindScan\backups")
INSTALL_DIR = Path(r"D:\MindScan")
SERVICE_INSTALLER = Path(r"D:\MindScan\core\MindScan_ServiceInstaller.py")
LOG_API = "http://127.0.0.1:8091/logs"


# ----------------------- UTILITÁRIOS -----------------------
def now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")

def log(message, level="INFO"):
    print(f"[{now()}] [{level}] {message}")
    try:
        requests.post(LOG_API, json={"origin": "RollbackManager", "message": message, "level": level}, timeout=1)
    except Exception:
        pass


def sha256sum(file_path):
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest():
    if not MANIFEST_PATH.exists():
        log("Manifesto de atualização não encontrado.", "ERROR")
        return None
    try:
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log(f"Erro ao ler manifesto: {e}", "ERROR")
        return None


# ----------------------- ROLLBACK -----------------------
def restore_backup(backup_path):
    if not Path(backup_path).exists():
        log(f"Backup não encontrado: {backup_path}", "ERROR")
        return False

    log(f"Iniciando restauração a partir de {backup_path}...")
    try:
        # Limpa diretório atual
        for item in INSTALL_DIR.iterdir():
            if item.name not in ("backups", "logs", "updates"):
                if item.is_file():
                    item.unlink()
                else:
                    shutil.rmtree(item)
        # Extrai backup
        with zipfile.ZipFile(backup_path, "r") as zf:
            zf.extractall(INSTALL_DIR)
        log("Backup restaurado com sucesso.")
        return True
    except Exception as e:
        log(f"Erro durante restauração: {e}", "ERROR")
        return False


def update_manifest(rollback_info):
    try:
        manifest = load_manifest()
        if not manifest:
            return
        manifest["rollback"]["last_action"] = rollback_info
        manifest["current_build"]["version_tag"] = rollback_info["reverted_to"]
        manifest["verification"]["last_result"] = "rollback"
        with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        log("Manifesto atualizado após rollback.")
    except Exception as e:
        log(f"Erro ao atualizar manifesto: {e}", "ERROR")


def restart_services():
    log("Reiniciando serviços MindScan após rollback...")
    try:
        subprocess.run(["python", str(SERVICE_INSTALLER), "stop"], check=True)
        subprocess.run(["python", str(SERVICE_INSTALLER), "start"], check=True)
        log("Serviços reiniciados com sucesso.")
    except Exception as e:
        log(f"Erro ao reiniciar serviços: {e}", "ERROR")


# ----------------------- MONITORAMENTO -----------------------
def verify_integrity(manifest):
    try:
        current_hash = manifest["current_build"]["integrity_hash"]
        ref_file = BACKUP_DIR / f"{manifest['current_build']['version_tag']}.zip"
        if not ref_file.exists():
            log("Arquivo de referência de integridade não encontrado.", "WARN")
            return True  # Sem referência — ignora
        calculated = sha256sum(ref_file)
        return calculated == current_hash
    except Exception as e:
        log(f"Erro ao verificar integridade: {e}", "ERROR")
        return False


def main():
    log("Rollback Manager iniciado.")
    manifest = load_manifest()
    if not manifest:
        return

    integrity_ok = verify_integrity(manifest)
    if integrity_ok:
        log("Integridade validada. Nenhuma ação necessária.", "INFO")
        return

    log("⚠️ Integridade comprometida. Iniciando rollback...", "WARN")
    backup_info = manifest.get("rollback", {}).get("previous_build")
    if not backup_info:
        log("Nenhum backup registrado no manifesto.", "ERROR")
        return

    success = restore_backup(backup_info["backup_path"])
    if success:
        rollback_record = {
            "timestamp": now(),
            "reverted_to": backup_info["version_tag"],
            "reason": "integrity failure",
            "result": "success"
        }
        update_manifest(rollback_record)
        restart_services()
        log(f"Rollback para {backup_info['version_tag']} concluído com sucesso.", "INFO")
    else:
        log("Rollback falhou. Sistema requer intervenção manual.", "ERROR")


if __name__ == "__main__":
    main()
