import os
import datetime
import subprocess
import logging

# Configurar logging
logging.basicConfig(
    filename='logs/backup_mindscan.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Diretórios e arquivos
backup_dir = "backup"
rclone_path = "rclone"  # Certifique-se de que rclone está no PATH
drive_remote = "mindscan-drive:/backups"

# Timestamp para nome do arquivo
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
zip_name = f"mindscan_backup_{timestamp}.zip"
zip_path = os.path.join(backup_dir, zip_name)

# Criar diretório de backup, se não existir
os.makedirs(backup_dir, exist_ok=True)

# Compactar os diretórios principais do projeto
try:
    logging.info("Iniciando compressão do projeto...")
    subprocess.run([
        "powershell", "Compress-Archive",
        "-Path", "backend", "frontend", "services", "scripts",
        "-DestinationPath", zip_path
    ], check=True)
    logging.info(f"Arquivo compactado com sucesso: {zip_path}")
except subprocess.CalledProcessError as e:
    logging.error(f"Erro ao compactar arquivos: {e}")
    raise

# Enviar o arquivo ao Google Drive com rclone
try:
    logging.info("Iniciando envio com rclone...")
    subprocess.run([
        rclone_path, "copy", zip_path, drive_remote, "--progress"
    ], check=True)
    logging.info("Backup enviado com sucesso para o Google Drive.")
except subprocess.CalledProcessError as e:
    logging.error(f"Erro ao enviar com rclone: {e}")
    raise
