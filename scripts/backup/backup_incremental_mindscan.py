# D:\projetos-inovexa\mindscan\scripts\backup\backup_incremental_mindscan.py

import os
import shutil
import zipfile
import datetime
import subprocess
from pathlib import Path

# === Configurações ===
PROJETO_DIR = Path("D:/projetos-inovexa/mindscan")
BACKUP_DIR = PROJETO_DIR / "scripts/backup"
LOG_DIR = PROJETO_DIR / "scripts/logs"
RETENCAO_MAXIMA = 5
REMOTE_RCLONE = "gdrive:MindScan_Backups"

# === Inicialização ===
BACKUP_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
agora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
nome_backup = f"mindscan_backup_{agora}.zip"
caminho_backup = BACKUP_DIR / nome_backup
caminho_log_execucao = LOG_DIR / f"automacao_log_{agora}.txt"
caminho_log_upload = LOG_DIR / f"upload_rclone_{agora}.log"

# === 1. Criar Backup ===
with zipfile.ZipFile(caminho_backup, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for foldername, subfolders, filenames in os.walk(PROJETO_DIR):
        folder_path = Path(foldername)
        if any(p in folder_path.parts for p in ['backup', 'logs']):
            continue  # Ignora pastas internas de backup e log
        for filename in filenames:
            filepath = folder_path / filename
            arcname = filepath.relative_to(PROJETO_DIR)
            zipf.write(filepath, arcname)

# === 2. Aplicar Política de Retenção ===
backups_existentes = sorted(BACKUP_DIR.glob("mindscan_backup_*.zip"))
if len(backups_existentes) > RETENCAO_MAXIMA:
    for b in backups_existentes[:-RETENCAO_MAXIMA]:
        b.unlink()

# === 3. Upload para Google Drive com rclone ===
comando = [
    "rclone", "copy", str(caminho_backup), REMOTE_RCLONE,
    f"--log-file={caminho_log_upload}", "--log-level=INFO"
]
resultado = subprocess.run(comando, capture_output=True, text=True)

# === 4. Log Final da Execução ===
with open(caminho_log_execucao, 'w', encoding='utf-8') as log:
    log.write(f"[INFO] Backup criado em: {caminho_backup}\n")
    log.write(f"[INFO] Upload para Google Drive iniciado...\n")
    if resultado.returncode == 0:
        log.write("[SUCESSO] Upload concluído com sucesso.\n")
    else:
        log.write("[ERRO] Falha no upload via rclone.\n")
        log.write(resultado.stderr + "\n")

print(f"Backup completo: {caminho_backup}")
print(f"Log: {caminho_log_execucao}")
