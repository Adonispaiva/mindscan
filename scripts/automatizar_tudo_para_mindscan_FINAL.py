import sys
import platform
import subprocess
import logging
from pathlib import Path
from datetime import datetime

# --- Configurações básicas ---
BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
BACKUP_DIR = BASE_DIR / "backup"
BACKUP_DIR.mkdir(exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = LOG_DIR / f"automacao_log_{TIMESTAMP}.txt"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logging.info("=== Início da Automação MindScan FINAL ===")

# --- Execução do verificador de ambiente ---
verificador = BASE_DIR / "verificar_ambiente_mindscan.py"
if not verificador.exists():
    logging.critical("Verificador de ambiente ausente.")
    sys.exit("❌ Verificador não encontrado")
try:
    subprocess.run([sys.executable, str(verificador)], check=True)
    logging.info("Verificação de ambiente finalizada com sucesso.")
except subprocess.CalledProcessError as e:
    logging.critical(f"Erro no verificador: {e}")
    sys.exit(1)

# --- Checagem de arquivos auxiliares ---
def verificar_arquivo(nome: str) -> Path:
    p = BASE_DIR / nome
    if not p.exists():
        logging.error(f"Arquivo ausente: {p}")
        raise FileNotFoundError(f"Arquivo ausente: {p}")
    logging.info(f"Arquivo presente: {p}")
    return p

try:
    script_amb = verificar_arquivo("automatizar_ambiente.py")
    script_back = verificar_arquivo("backup_mindscan_rclone.py")
    dados = verificar_arquivo("dados_entrada.csv")
except Exception as e:
    logging.critical(str(e))
    sys.exit(1)

# --- Executar scripts auxiliares ---
def executar(script_path: Path):
    logging.info(f"Executando: {script_path.name}")
    try:
        subprocess.run([sys.executable, str(script_path)], check=True)
        logging.info(f"✅ Concluído: {script_path.name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Erro ao executar {script_path.name}: {e}")

executar(script_amb)
executar(script_back)

logging.info("=== Fim da Automação MindScan FINAL ===")
print(f"\n✔ Automação executada. Log em: {LOG_FILE}")
