import os
import shutil
import json
from datetime import datetime

ROOT_PATH = r"D:\projetos-inovexa\mindscan"
BACKUP_ROOT = os.path.join(ROOT_PATH, "backup")
LOG_FILE = os.path.join(ROOT_PATH, "logs", f"rollback_guardian_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

def list_backups():
    backups = [b for b in os.listdir(BACKUP_ROOT) if os.path.isdir(os.path.join(BACKUP_ROOT, b))]
    backups.sort(reverse=True)
    return backups

def choose_backup():
    backups = list_backups()
    if not backups:
        print("⚠️ Nenhum backup encontrado.")
        return None
    print("📦 Backups disponíveis:")
    for i, b in enumerate(backups, 1):
        print(f"{i}. {b}")
    choice = input("Escolha o número do backup a restaurar (ou pressione Enter para cancelar): ")
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(backups):
        return None
    return os.path.join(BACKUP_ROOT, backups[int(choice) - 1])

def restore_backup(backup_path):
    log_data = {"start_time": str(datetime.now()), "restored_files": []}
    for root, _, files in os.walk(backup_path):
        for file in files:
            src_file = os.path.join(root, file)
            rel_path = os.path.relpath(src_file, backup_path)
            dest_file = os.path.join(ROOT_PATH, rel_path)
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            shutil.copy2(src_file, dest_file)
            log_data["restored_files"].append(dest_file)
    log_data["end_time"] = str(datetime.now())
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=4, ensure_ascii=False)
    print(f"♻️ Rollback concluído. Log salvo em: {LOG_FILE}")

if __name__ == "__main__":
    print("Iniciando Rollback Guardian — MindScan Recovery System...")
    selected_backup = choose_backup()
    if selected_backup:
        print(f"🔁 Restaurando backup: {selected_backup}")
        restore_backup(selected_backup)
    else:
        print("Rollback cancelado.")
