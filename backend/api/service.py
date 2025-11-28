import subprocess
import os

REPORTS_DIR = "D:/backend/reports"

def run_mindscan():
    """
    Executa o script Python que gera os relatórios.
    """
    script_path = os.path.abspath("run_e2e.py")

    subprocess.run(["python", script_path], check=True)

    files = os.listdir(REPORTS_DIR)
    files = [f"{REPORTS_DIR}/{f}" for f in files if f.endswith(".pdf")]

    return files
