import os
import shutil
import json
from datetime import datetime

# Caminhos principais
ROOT_PATH = r"D:\projetos-inovexa\mindscan"
BACKUP_DIR = os.path.join(ROOT_PATH, "backup")
ARCHIVE_DIR = os.path.join(BACKUP_DIR, "_archive")
LOG_FILE = os.path.join(ROOT_PATH, "logs", f"backup_cleaner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

# Configurações de retenção
MAX_BACKUPS_TO_KEEP = 2  # mantém apenas os dois mais recentes
VALID_EXTENSIONS = (".zip", ".tar.gz", ".rar")

def list_backups():
    backups = []
    for item in os.listdir(BACKUP_DIR):
        item_path = os.path.join(BACKUP_DIR, item)
        if os.path.isdir(item_path) and not item.startswith("_"):
            backups.append((item, os.path.getmtime(item_path)))
        elif os.path.isfile(item_path) and item.endswith(VALID_EXTENSIONS):
            backups.append((item, os.path.getmtime(item_path)))
    backups.sort(key=lambda x: x[1], reverse=True)
    return backups

def move_to_archive(item_name):
    src = os.path.join(BACKUP_DIR, item_name)
    dst = os.path.join(ARCHIVE_DIR, item_name)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    try:
        shutil.move(src, dst)
        return True
    except Exception as e:
        return str(e)

def cleanup_backups():
    print("🧹 Iniciando limpeza de backups antigos...")
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    backups = list_backups()
    log_data = {
        "executed_at": str(datetime.now()),
        "kept_backups": [],
        "archived_backups": [],
        "errors": []
    }

    if len(backups) <= MAX_BACKUPS_TO_KEEP:
        print(f"✅ Apenas {len(backups)} backups encontrados. Nenhuma ação necessária.")
        return

    to_keep = backups[:MAX_BACKUPS_TO_KEEP]
    to_archive = backups[MAX_BACKUPS_TO_KEEP:]

    print(f"📦 Mantendo {len(to_keep)} backups mais recentes.")
    for item, ts in to_keep:
        log_data["kept_backups"].append({"name": item, "timestamp": datetime.fromtimestamp(ts).isoformat()})

    print(f"📦 Movendo {len(to_archive)} backups antigos para _archive...")
    for item, ts in to_archive:
        result = move_to_archive(item)
        if result is True:
            log_data["archived_backups"].append({"name": item, "timestamp": datetime.fromtimestamp(ts).isoformat()})
            print(f"   🔸 {item} movido com sucesso.")
        else:
            log_data["errors"].append({"name": item, "error": result})
            print(f"   ⚠️ Falha ao mover {item}: {result}")

    with open(LOG_FILE, "w", encoding="utf-8") as logf:
        json.dump(log_data, logf, indent=4, ensure_ascii=False)

    print(f"\n✅ Limpeza concluída. Log salvo em: {LOG_FILE}")
    print(f"🗃️ Backups mantidos: {[b[0] for b in to_keep]}")
    print(f"📁 Backups movidos para: {ARCHIVE_DIR}")

if __name__ == "__main__":
    cleanup_backups()
