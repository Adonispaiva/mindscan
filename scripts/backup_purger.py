import os
import hashlib
import json
import argparse
from datetime import datetime

# Caminhos principais
ROOT_PATH = r"D:\projetos-inovexa\mindscan"
BACKUP_DIR = os.path.join(ROOT_PATH, "backup")
ARCHIVE_DIR = os.path.join(BACKUP_DIR, "_archive")
LOG_DIR = os.path.join(ROOT_PATH, "logs")
LOG_FILE = os.path.join(LOG_DIR, f"backup_purger_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

# ------------------------------------------
# Funções utilitárias
# ------------------------------------------

def calc_hash(file_path):
    """Calcula o hash SHA256 de um arquivo"""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def get_archive_files():
    """Lista todos os arquivos dentro do diretório _archive"""
    if not os.path.exists(ARCHIVE_DIR):
        return []
    return [
        os.path.join(ARCHIVE_DIR, f)
        for f in os.listdir(ARCHIVE_DIR)
        if os.path.isfile(os.path.join(ARCHIVE_DIR, f))
    ]

def purge_files(files, force=False):
    """Exclui definitivamente os arquivos listados"""
    log_data = {
        "executed_at": str(datetime.now()),
        "purged_files": [],
        "errors": [],
        "space_reclaimed_MB": 0.0
    }

    total_size = 0
    for file_path in files:
        try:
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            file_hash = calc_hash(file_path)

            if not force:
                confirm = input(f"⚠️ Deseja realmente apagar '{os.path.basename(file_path)}'? (s/n): ").strip().lower()
                if confirm != "s":
                    print(f"⏩ Ignorado: {file_path}")
                    continue

            os.remove(file_path)
            print(f"✅ Removido: {os.path.basename(file_path)}")

            log_data["purged_files"].append({
                "file": file_path,
                "hash": file_hash,
                "size_MB": round(size_mb, 2)
            })
            total_size += size_mb

        except Exception as e:
            log_data["errors"].append({
                "file": file_path,
                "error": str(e)
            })
            print(f"⚠️ Erro ao remover {file_path}: {e}")

    log_data["space_reclaimed_MB"] = round(total_size, 2)
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, "w", encoding="utf-8") as logf:
        json.dump(log_data, logf, indent=4, ensure_ascii=False)

    print(f"\n📄 Log salvo em: {LOG_FILE}")
    print(f"💾 Espaço total liberado: {log_data['space_reclaimed_MB']} MB")
    print("🧹 Purga concluída.")
    return log_data


# ------------------------------------------
# Execução principal
# ------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Purga definitiva de backups arquivados do MindScan.")
    parser.add_argument("--force", action="store_true", help="Executa sem confirmação (modo automático).")
    args = parser.parse_args()

    print("🧹 Iniciando purga definitiva dos backups arquivados...\n")
    files = get_archive_files()

    if not files:
        print("✅ Nenhum arquivo encontrado em _archive. Nada a fazer.")
        return

    print(f"🔎 {len(files)} arquivos encontrados em _archive:")
    for f in files:
        size_mb = os.path.getsize(f) / (1024 * 1024)
        print(f"   - {os.path.basename(f)} ({round(size_mb,2)} MB)")

    if not args.force:
        confirm = input("\n⚠️ Confirmar purga de todos esses arquivos? (s/n): ").strip().lower()
        if confirm != "s":
            print("❎ Operação cancelada.")
            return

    purge_files(files, force=args.force)


if __name__ == "__main__":
    main()
