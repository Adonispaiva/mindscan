import os, json, datetime
from pathlib import Path

BASE = Path("D:/projetos-inovexa/mindscan")
LOG_DIR = BASE / "logs"
OUT = LOG_DIR / f"maintenance_summary_{datetime.date.today()}.json"

def collect():
    report = {"timestamp": datetime.datetime.now().isoformat(), "files": []}
    for f in LOG_DIR.glob("*.json"):
        with open(f, "r", encoding="utf-8") as h:
            try:
                data = json.load(h)
                report["files"].append({"name": f.name, "lines": len(json.dumps(data).splitlines())})
            except Exception as e:
                report["files"].append({"name": f.name, "error": str(e)})
    with open(OUT, "w", encoding="utf-8") as o:
        json.dump(report, o, indent=4)
    print(f"[REPORT] Relatório consolidado salvo em {OUT}")

if __name__ == "__main__":
    collect()
