"""
MindScan Log Archiver v1.0
Autor: Inovexa Software
Diretor Técnico: Leo Vinci
Descrição:
Automatiza o arquivamento e compressão dos logs antigos do MindScan,
preservando os registros recentes e otimizando o uso de espaço em disco.
"""

import os
import json
import time
import zipfile
from datetime import datetime, timedelta

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOGS_DIR = os.path.join(ROOT_DIR, "maintenance", "logs")
ARCHIVE_DIR = os.path.join(LOGS_DIR, "archives")
RETENTION_DAYS = 3  # mantém logs dos últimos 3 dias

def list_log_files():
    """Lista arquivos de log candidatos a arquivamento."""
    return [
        os.path.join(LOGS_DIR, f)
        for f in os.listdir(LOGS_DIR)
        if f.endswith(".json") or f.endswith(".log")
    ]

def archive_logs():
    """Compacta logs antigos em um arquivo ZIP datado."""
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    archive_name = datetime.utcnow().strftime("archive_%Y%m%d_%H%M%S.zip")
    archive_path = os.path.join(ARCHIVE_DIR, archive_name)

    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for log_file in list_log_files():
            if should_archive(log_file):
                zipf.write(log_file, os.path.basename(log_file))
                os.remove(log_file)
                print(f"[ARCHIVER] Log arquivado: {log_file}")

    print(f"[ARCHIVER] Arquivo criado: {archive_path}")

def should_archive(filepath):
    """Verifica se o log deve ser arquivado com base na data de modificação."""
    mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
    return datetime.utcnow() - mod_time > timedelta(days=RETENTION_DAYS)

def clean_old_archives():
    """Remove arquivos ZIP muito antigos (mais de 30 dias)."""
    cutoff = datetime.utcnow() - timedelta(days=30)
    for f in os.listdir(ARCHIVE_DIR):
        if f.endswith(".zip"):
            path = os.path.join(ARCHIVE_DIR, f)
            mod_time = datetime.fromtimestamp(os.path.getmtime(path))
            if mod_time < cutoff:
                os.remove(path)
                print(f"[ARCHIVER] Arquivo antigo removido: {path}")

def run_archiver():
    """Rotina principal do Archiver."""
    print(f"[ARCHIVER] Iniciado — {datetime.utcnow().isoformat()} UTC")
    archive_logs()
    clean_old_archives()
    print(f"[ARCHIVER] Concluído — logs arquivados e limpos.")

if __name__ == "__main__":
    run_archiver()
