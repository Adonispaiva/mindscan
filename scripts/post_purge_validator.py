from alert_dispatcher import dispatch
from policy_loader import load_policy
import psutil, json, datetime, os
from pathlib import Path

BASE = Path("D:/projetos-inovexa/mindscan")
LOG = BASE / "logs" / f"post_purge_validator_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

def run():
    policy = load_policy()
    usage = psutil.disk_usage("D:/")
    free_percent = usage.free / usage.total * 100
    critical = free_percent < policy["disk_min_free_percent"]

    result = {
        "timestamp": datetime.datetime.now().isoformat(),
        "disk_free_percent": round(free_percent, 2),
        "critical": critical
    }

    if critical:
        dispatch(policy["alerts"]["disk_critical"], "critical")
    else:
        print(f"[Validator] Espaço livre OK: {free_percent:.2f}%")

    with open(LOG, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)
    print(f"[Validator] Log salvo: {LOG}")

if __name__ == "__main__":
    run()
