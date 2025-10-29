import sys
import platform
import shutil
import socket
import logging
from pathlib import Path
from datetime import datetime

# --- Configurações ---
BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = LOG_DIR / f"verif_env_{TIMESTAMP}.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logging.info("=== Início verificação de ambiente ===")

# Versão mínima do Python
if sys.version_info.major < 3 or (sys.version_info.major == 3 and sys.version_info.minor < 10):
    logging.critical("Python < 3.10 detectado.")
    sys.exit("❌ Requer Python 3.10+")

logging.info(f"Versão Python: {platform.python_version()}")

# Verificar pacotes básicos
pacotes = ["os", "zipfile", "subprocess", "logging", "pathlib"]
for p in pacotes:
    try:
        __import__(p)
        logging.info(f"Pacote presente: {p}")
    except ImportError:
        logging.critical(f"Pacote ausente: {p}")
        sys.exit(f"❌ Pacote ausente: {p}")

# Verificar permissão de escrita
teste = BASE_DIR / "__teste__.tmp"
try:
    teste.write_text("ok")
    teste.unlink()
    logging.info("Permissões de escrita OK")
except Exception as e:
    logging.critical(f"Sem permissão de escrita: {e}")
    sys.exit("❌ Permissão de escrita insuficiente")

# Verificar disco livre
du = shutil.disk_usage(BASE_DIR)
livre_gb = du.free / (1024**3)
logging.info(f"Espaço livre: {livre_gb:.2f} GB")

if livre_gb < 1.0:
    logging.warning("Espaço livre menor que 1GB — risco de falha")

# Verificar conectividade básica
try:
    socket.create_connection(("1.1.1.1", 53), timeout=3)
    logging.info("Conectividade com internet OK (DNS)")
except Exception:
    logging.warning("Sem conexão de rede detectada — pode ser OK para execução local")

logging.info("=== Fim verificação de ambiente ===")
print(f"✔ Verificação concluída. Log em: {LOG_FILE}")
