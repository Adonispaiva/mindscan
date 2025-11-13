import os
import platform
import sys
import shutil
from datetime import datetime

ROOT_PATH = r"D:\projetos-inovexa\mindscan"
LOG_FILE = os.path.join(ROOT_PATH, "logs", f"env_validator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

REQUIRED_DIRS = ["backend", "frontend", "MI", "scripts", "logs", "docs"]
REQUIRED_EXECUTABLES = ["python", "git"]

def check_directories():
    missing = [d for d in REQUIRED_DIRS if not os.path.exists(os.path.join(ROOT_PATH, d))]
    return missing

def check_executables():
    missing_execs = []
    for exe in REQUIRED_EXECUTABLES:
        if not shutil.which(exe):
            missing_execs.append(exe)
    return missing_execs

def validate_environment():
    print("🔍 Validando ambiente MindScan...")
    with open(LOG_FILE, "w", encoding="utf-8") as log:
        log.write(f"Validação iniciada: {datetime.now()}\n")
        log.write(f"Sistema: {platform.system()} {platform.release()}\n")
        log.write(f"Python: {sys.version}\n\n")

        missing_dirs = check_directories()
        missing_execs = check_executables()

        if missing_dirs:
            log.write(f"[FALHA] Pastas ausentes: {', '.join(missing_dirs)}\n")
        if missing_execs:
            log.write(f"[FALHA] Executáveis ausentes: {', '.join(missing_execs)}\n")

        if not missing_dirs and not missing_execs:
            log.write("[SUCESSO] Ambiente completo e validado.\n")

    print(f"Validação concluída. Log salvo em: {LOG_FILE}")

if __name__ == "__main__":
    validate_environment()
