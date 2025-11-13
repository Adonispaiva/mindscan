"""
↩️ MindScan Rollback Manager — Template v5.8
Autor: Inovexa Software
Função: Reverte o sistema para o último build estável do MindScan.
"""

import os, json, zipfile, shutil, datetime

TARGET_DIR = r"D:\MindScan"
BACKUP_DIR = os.path.join(TARGET_DIR, "backups")
LOG_PATH = os.path.join(TARGET_DIR, "logs", "rollback.log")

def log(msg):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")

def create_backup():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    backup_name = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(TARGET_DIR):
            for file in files:
                if "backups" not in root and "logs" not in root:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, TARGET_DIR)
                    z.write(full_path, rel_path)
    log(f"Backup criado: {backup_path}")
    return backup_path

def restore_latest_backup():
    backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.endswith(".zip")])
    if not backups:
        log("Nenhum backup encontrado.")
        return False
    last = os.path.join(BACKUP_DIR, backups[-1])
    with zipfile.ZipFile(last, "r") as z:
        z.extractall(TARGET_DIR)
    log(f"Backup restaurado: {last}")
    return True

if __name__ == "__main__":
    create_backup()
