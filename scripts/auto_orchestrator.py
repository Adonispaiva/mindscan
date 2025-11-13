import subprocess
import os
from datetime import datetime

ROOT_PATH = r"D:\projetos-inovexa\mindscan"
SCRIPTS = [
    "env_validator.py",
    "structure_manager.py",
    "audit_cleaner.py",
    "deploy_saver.py",
    "deploy_integrity_checker.py",
    "post_deploy_reporter.py"
]
LOG_FILE = os.path.join(ROOT_PATH, "logs", f"auto_orchestrator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

def run_script(script_name):
    script_path = os.path.join(ROOT_PATH, "scripts", script_name)
    print(f"▶️ Executando {script_name}...")
    try:
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        stdout = result.stdout or ""
        stderr = result.stderr or ""
    except Exception as e:
        stdout = ""
        stderr = f"[ERRO] Falha ao executar {script_name}: {e}"
        result = type("Result", (), {"returncode": 1})()
    return {
        "script": script_name,
        "returncode": result.returncode,
        "stdout": stdout,
        "stderr": stderr
    }

def orchestrate():
    print("🚀 Iniciando pipeline completo do MindScan...")
    logs = []
    for script in SCRIPTS:
        logs.append(run_script(script))

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "w", encoding="utf-8") as logf:
        for entry in logs:
            logf.write(f"\n=== {entry['script']} ===\n")
            logf.write(entry['stdout'])
            if entry['stderr']:
                logf.write(f"\n[ERROS]\n{entry['stderr']}\n")
            logf.write("\n" + "-" * 80 + "\n")

    print(f"🧩 Pipeline completo executado. Log salvo em: {LOG_FILE}")

if __name__ == "__main__":
    orchestrate()
