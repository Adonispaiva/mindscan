import hashlib, json, datetime
from pathlib import Path

BASE = Path("D:/projetos-inovexa/mindscan")
LOG = BASE / "logs" / f"integrity_scan_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
MANIFEST = BASE / "config" / "integrity_manifest.json"

def sha256(file):
    h = hashlib.sha256()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def scan():
    results = {}
    for p in BASE.glob("**/*.py"):
        if "venv" in str(p): continue
        results[str(p)] = sha256(p)
    with open(LOG, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    with open(MANIFEST, "w", encoding="utf-8") as m:
        json.dump(results, m, indent=2)
    print(f"[Integrity] Scan completo -> {LOG}")

if __name__ == "__main__":
    scan()
