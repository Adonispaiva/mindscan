import os
import json
import threading
from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import glob

# ============================================
# MindScan Log Handler — v3.7
# Central de registro e auditoria
# ============================================

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
RETENTION_DAYS = 7
lock = threading.Lock()

app = FastAPI(title="MindScan Log API", version="3.7")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")


def _current_log_file():
    os.makedirs(LOG_DIR, exist_ok=True)
    return os.path.join(LOG_DIR, f"mindscan_log_{datetime.now().strftime('%Y-%m-%d')}.jsonl")


def log_event(origin: str, message: str, level: str = "INFO"):
    """Registra evento thread-safe em formato JSONL."""
    entry = {
        "time": now(),
        "origin": origin,
        "level": level.upper(),
        "message": message.strip(),
    }

    line = json.dumps(entry, ensure_ascii=False)
    with lock:
        with open(_current_log_file(), "a", encoding="utf-8") as f:
            f.write(line + "\n")
    print(f"[{entry['time']}] [{origin}] [{level}] {message}")


def read_logs(limit: int = 200, level: str | None = None):
    """Lê os logs recentes, com filtro opcional de severidade."""
    files = sorted(glob.glob(os.path.join(LOG_DIR, "mindscan_log_*.jsonl")), reverse=True)
    logs = []
    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                for line in reversed(f.readlines()):
                    if len(logs) >= limit:
                        break
                    entry = json.loads(line)
                    if not level or entry["level"] == level.upper():
                        logs.append(entry)
        except Exception:
            continue
    return logs


def rotate_logs():
    """Apaga logs antigos (retenção de 7 dias)."""
    cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)
    for file in glob.glob(os.path.join(LOG_DIR, "mindscan_log_*.jsonl")):
        try:
            file_date = datetime.strptime(os.path.basename(file)[13:23], "%Y-%m-%d")
            if file_date < cutoff:
                os.remove(file)
                print(f"🧹 Log antigo removido: {file}")
        except Exception:
            continue


@app.get("/logs")
def get_logs(limit: int = 100, level: str | None = None):
    """Endpoint para visualização dos logs no painel web."""
    rotate_logs()
    return {"count": limit, "logs": read_logs(limit=limit, level=level)}


if __name__ == "__main__":
    import uvicorn
    log_event("SYSTEM", "MindScan LogHandler iniciado.", "INFO")
    uvicorn.run(app, host="127.0.0.1", port=8091)
