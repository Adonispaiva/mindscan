# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\workers\main_worker.py
# Última atualização: 2025-12-11T09:59:27.542857

"""
MindScan Backend — Worker Interno
Diretor Técnico: Leo Vinci

Responsável por:
    - Executar tarefas contínuas do backend (workers)
    - Preparado para futuras integrações do Core psicométrico
    - Operar em thread daemon sem bloquear o servidor
"""

import time
import threading
from datetime import datetime
from pathlib import Path

# Configuração de diretórios
ROOT = Path(__file__).resolve().parents[1]  # /backend
RUNTIME = ROOT / "runtime"
RUNTIME.mkdir(parents=True, exist_ok=True)

LOGFILE = RUNTIME / "worker_runtime.log"


def wlog(msg: str):
    """Log interno do Worker."""
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[Worker {ts}] {msg}"
    print(line)

    with LOGFILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


# ----------------------------------------------------------------------
# Loop de Trabalho (executado em thread)
# ----------------------------------------------------------------------
def worker_loop():
    wlog("Worker iniciado.")

    while True:
        time.sleep(2)
        wlog("Worker ativo...")

        # ------------------------------------------------------------------
        # ÁREA PARA LÓGICA FUTURA (Fase 2)
        # ------------------------------------------------------------------
        # cálculos psicométricos
        # pré-processamento de dados
        # chamadas ao Core
        # telemetria interna
        # previsões de comportamento
        # ------------------------------------------------------------------


# ----------------------------------------------------------------------
# Inicializador público
# ----------------------------------------------------------------------
def start_worker():
    """Cria e inicia a thread worker."""
    th = threading.Thread(target=worker_loop, daemon=True)
    th.start()
    wlog("Thread do worker foi iniciada.")
    return th


# ----------------------------------------------------------------------
# Execução direta (modo teste)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    wlog("Execução direta detectada.")
    start_worker()

    while True:
        time.sleep(1)
