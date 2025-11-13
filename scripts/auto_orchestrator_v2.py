import os, subprocess
from datetime import datetime

ROOT = r"D:\projetos-inovexa\mindscan"
SCRIPTS = [
    "env_validator.py",
    "structure_manager.py",
    "audit_cleaner.py",
    "backup_manager.py",
    "deploy_saver.py",
    "deploy_integrity_checker.py",
    "post_deploy_reporter.py"
]
LOG = os.path.join(ROOT, "logs", f"auto_orchestrator_v2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

def run(script):
    path = os.path.join(ROOT, "scripts", script)
    result = subprocess.run(["python", path], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return result.stdout, result.stderr

def main():
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "w", encoding="utf-8") as log:
        for script in SCRIPTS:
            out, err = run(script)
            log.write(f"\n=== {script} ===\n{out}\n")
            if err: log.write(f"[ERROS]\n{err}\n")
    print(f"🧠 MindScan orchestrator v2 completo. Log: {LOG}")

if __name__ == "__main__":
    main()
