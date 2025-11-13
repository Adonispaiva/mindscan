import json, time
from pathlib import Path

ALERT_DIR = Path("D:/projetos-inovexa/mindscan/alerts")

def watch():
    if not ALERT_DIR.exists():
        print("Nenhum alerta ativo."); return
    files = sorted(ALERT_DIR.glob("*.json"))
    if not files:
        print("Nenhum alerta registrado.")
        return
    print(f"=== ALERTAS ATIVOS ({len(files)}) ===")
    for f in files[-10:]:
        with open(f, "r", encoding="utf-8") as h:
            data = json.load(h)
        print(f"[{data['level']}] {data['message']} @ {data['timestamp']}")

if __name__ == "__main__":
    watch()
