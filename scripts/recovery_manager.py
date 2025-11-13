# D:\projetos-inovexa\mindscan\scripts\recovery_manager.py
"""
Gerencia a recuperação automática de estrutura e scripts do MindScan.
"""
import os
import json
import datetime
from pathlib import Path
from policy_loader import load_policy

LOG_PATH = Path("D:/projetos-inovexa/mindscan/logs/recovery_manager_{}.json".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))

def recover():
    policy = load_policy()
    created_dirs = []
    recreated_scripts = []

    for d in policy["directories_required"]:
        p = Path(d)
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)
            created_dirs.append(str(p))

    for s in policy["scripts_required"]:
        path = Path("D:/projetos-inovexa/mindscan/scripts") / s
        if not path.exists():
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"# {s} recriado automaticamente em {datetime.datetime.now().isoformat()}\n")
            recreated_scripts.append(s)

    log = {
        "timestamp": datetime.datetime.now().isoformat(),
        "created_dirs": created_dirs,
        "recreated_scripts": recreated_scripts,
        "status": "ok"
    }

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=4)
    print(f"[Recovery] Execução concluída. Log salvo em {LOG_PATH}")

if __name__ == "__main__":
    recover()
