import os
import hashlib
import json
import argparse
import sys
import time
from datetime import datetime

# Caminhos principais
ROOT_PATH = r"D:\projetos-inovexa\mindscan"
BACKUP_DIR = os.path.join(ROOT_PATH, "backup")
ARCHIVE_DIR = os.path.join(BACKUP_DIR, "_archive")
LOG_DIR = os.path.join(ROOT_PATH, "logs")
LOG_FILE = os.path.join(LOG_DIR, f"backup_purger_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

CHUNK_SIZE = 1024 * 1024 * 8  # 8 MB por bloco

# ------------------------------------------
# Barra de progresso
# ------------------------------------------
def progress_bar(progress, total, prefix='', suffix='', length=50):
    percent = f"{100 * (progress / float(total)):.1f}"
    filled_length = int(length * progress // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    if progress >= total:
        sys.stdout.write('\n')


# ------------------------------------------
# Funções utilitárias
# ------------------------------------------
def calc_hash(file_path):
    """Calcula hash SHA256 com barra de progresso"""
    sha256 = hashlib.sha256()
    file_size = os.path.getsize(file_path)
    read_size = 0
    last_update = time.time()

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            sha256.update(chunk)
            read_size += len(chunk)

            # Atualiza barra de progresso a cada 0.5s
            if time.time() - last_update > 0.5:
                progress_bar(read_size, file_size, prefix=f"🔍 Calculando hash de {os.path.basename(file_path)}")
                last_update = time.time()

    progress_bar(file_size, file_size, prefix=f"🔍 Calculando hash de {os.path.basename(file_path)}")
    return sha256.hexdigest()


def get_archive_files():
    if not os.path.exists(ARCHIVE_DIR):
        return []
    return [
        os.path.join(ARCHIVE_DIR, f)
        for f in os.listdir(ARCHIVE_DIR)
        if os.path.isfile(os.path.join(ARCHIVE_DIR, f))
    ]


def purge_files(files, force=False):
    log_data = {
        "executed_at": str(datetime.now()),
        "purged_files": [],
        "errors": [],
        "space_reclaimed_MB": 0.0
    }

    total_size = 0
    start_time = time.time()

    for idx, file_path in enumerate(files, 1):
        try:
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            file_hash = calc_hash(file_path)

            if not force:
                confirm = input(f"\n⚠️ Apagar definitivamente '{os.path.basename(file_path)}'? (s/n): ").strip().lower()
                if confirm != "s":
                    print(f"⏩ Ignorado: {file_path}")
                    continue

            os.remove(file_path)
            print(f"\n✅ Removido: {os.path.basename(file_path)} ({round(file_size_mb, 2)} MB)")

            total_size += file_size_mb
            log_data["purged_files"].append({
                "file": file_path,
                "hash": file_hash,
                "size_MB": round(file_size_mb, 2)
            })

        except Exception as e:
            log_data["errors"].append({
                "file": file_path,
                "error": str(e)
            })
            print(f"⚠️ Erro ao remover {file_path}: {e}")

    duration = time.time() - start_time
    log_data["space_reclaimed_MB"] = round(total_size, 2)
    log_data["execution_time_sec"] = round(duration, 1)

    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, "w", encoding="utf-8") as logf:
        json.dump(log_data, logf, indent=4, ensure_ascii=False)

    print(f"\n📄 Log salvo em: {LOG_FILE}")
    print(f"💾 Espaço total liberado: {round(total_size, 2)} MB")
    print(f"⏱️ Tempo total: {round(duration / 60, 2)} minutos")
    print("🧹 Purga concluída.")
    return log_data


# ------------------------------------------
# Execução principal
# ------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Purga definitiva com barra de progresso dos backups arquivados.")
    parser.add_argument("--force", action="store_true", help="Executa sem confirmação (modo automático).")
    args = parser.parse_args()

    print("🧹 Iniciando purga definitiva dos backups arquivados...\n")
    files = get_archive_files()

    if not files:
        print("✅ Nenhum arquivo encontrado em _archive. Nada a fazer.")
        return

    total_size_gb = sum(os.path.getsize(f) for f in files) / (1024 ** 3)
    print(f"🔎 {len(files)} arquivos encontrados em _archive (total {round(total_size_gb, 2)} GB):")
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
