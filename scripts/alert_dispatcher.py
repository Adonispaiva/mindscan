import datetime, json
from pathlib import Path

BASE = Path("D:/projetos-inovexa/mindscan")
ALERT_DIR = BASE / "alerts"
LOG_DIR = BASE / "logs"

def dispatch(message, level="warning"):
    ALERT_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "level": level.upper(),
        "message": message
    }
    alert_file = ALERT_DIR / f"alert_{timestamp}.json"
    with open(alert_file, "w", encoding="utf-8") as f:
        json.dump(entry, f, indent=4, ensure_ascii=False)
    print(f"[ALERT-{level.upper()}] {message}")

if __name__ == "__main__":
    dispatch("Teste de alerta MindScan.", "info")
