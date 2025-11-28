# Caminho: backend/main.py
# MindScan Backend — Execução Oficial (API + Worker)
# Diretor Técnico: Leo Vinci — Inovexa Software
#
# Versão Final e Definitiva para MindScan v2.0 (SynMind)
# Compatível com:
#   - Execução via "python -m backend.main"
#   - API FastAPI integrada a app.py
#   - Worker interno
#   - pysettings (sistema oficial de configuração)

import threading
import time
from datetime import datetime
from pathlib import Path

from pysettings import settings
from backend.app import app


# ============================================================
# 1) LOG E RUNTIME
# ============================================================

ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / "runtime"
RUNTIME.mkdir(parents=True, exist_ok=True)

LOGFILE = RUNTIME / "backend_runtime.log"


def blog(msg: str):
    """Log estruturado para execução do backend."""
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[Backend {ts}] {msg}"
    print(line)
    with LOGFILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


# ============================================================
# 2) WORKER INTERNO
# ============================================================

def worker_loop():
    blog("Worker iniciado.")
    interval = settings.WORKER_INTERVAL

    while True:
        time.sleep(interval)
        blog("Worker ativo...")


def iniciar_worker():
    thread = threading.Thread(target=worker_loop, daemon=True)
    thread.start()
    blog("Thread do worker foi iniciada.")


# ============================================================
# 3) API VIA UVICORN (THREAD)
# ============================================================

def iniciar_api():
    """Executa a API em thread separada."""
    try:
        import uvicorn
    except Exception:
        blog("FastAPI/Uvicorn não instalados. API desativada.")
        return

    def run():
        blog(f"API iniciando em {settings.API_HOST}:{settings.API_PORT}...")
        uvicorn.run(
            app,
            host=settings.API_HOST,
            port=settings.API_PORT,
            log_level="warning",
        )

    th = threading.Thread(target=run, daemon=True)
    th.start()
    blog("Thread da API foi iniciada.")


# ============================================================
# 4) BOOT GERAL DO BACKEND
# ============================================================

def start_backend():
    blog("Inicializando Backend (API + Worker)...")

    if settings.WORKER_ENABLED:
        iniciar_worker()
    else:
        blog("Worker desativado pelo settings.")

    if settings.API_ENABLED:
        iniciar_api()
    else:
        blog("API desativada pelo settings.")

    blog("Backend inicializado com sucesso.")


# ============================================================
# 5) EXECUÇÃO DIRETA
# ============================================================

if __name__ == "__main__":
    blog("Execução direta detectada.")
    start_backend()

    # Mantém o processo rodando
    while True:
        time.sleep(1)
