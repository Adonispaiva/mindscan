# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\tools\automator\main.py
# Última atualização: 2025-12-11T09:59:27.808460

import os
import argparse
from datetime import datetime

from core_manager import CoreManager
from audit_manager import AuditManager
from backend_manager import BackendManager
from cleanup_manager import CleanupManager
from data_validator import DataValidator
from release_manager import ReleaseManager
from report_manager import ReportManager
from github_manager import GitHubManager
from fix_paths_manager import FixPathsManager

ROOT_PATH = r"D:\projetos-inovexa\mindscan"   # <- Ajuste para o nome final da pasta

LOG_DIR = os.path.join(ROOT_PATH, "logs", "automator")
os.makedirs(LOG_DIR, exist_ok=True)

def log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[INFO] {timestamp}: {message}")

AVAILABLE_TASKS = {
    "fix_paths": lambda: FixPathsManager(ROOT_PATH).run(),
    "core":      lambda: CoreManager(ROOT_PATH).run(),
    "audit":     lambda: AuditManager(ROOT_PATH).run(),
    "backend":   lambda: BackendManager(ROOT_PATH).run(),
    "validate":  lambda: DataValidator(ROOT_PATH).run(),
    "cleanup":   lambda: CleanupManager(ROOT_PATH).run(),
    "report":    lambda: ReportManager(ROOT_PATH).run(),
    "release":   lambda: ReleaseManager(ROOT_PATH).run(),
    "sync":      lambda: GitHubManager(ROOT_PATH).run()
}

def run_task(task_name):
    if task_name not in AVAILABLE_TASKS:
        log(f"Task desconhecida: {task_name}")
        return
    log(f"Executando task: {task_name}")
    AVAILABLE_TASKS[task_name]()

def run_all_tasks():
    for task in [
        "fix_paths",
        "core",
        "audit",
        "backend",
        "validate",
        "cleanup",
        "report",
        "release"
    ]:
        run_task(task)

def load_tasks_from_json():
    import json
    tasks_file = os.path.join(ROOT_PATH, "tools", "automator", "tasks.json")

    if not os.path.exists(tasks_file):
        log("Arquivo tasks.json não encontrado. Rodando tasks padrão.")
        return None

    try:
        with open(tasks_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("tasks", [])
    except Exception as e:
        log(f"Erro ao ler tasks.json: {e}")
        return None

def run_from_json():
    tasks = load_tasks_from_json()
    if not tasks:
        run_all_tasks()
        return

    for task in tasks:
        name = task.get("name")
        enabled = task.get("enabled", False)
        if enabled:
            run_task(name)

def main():
    parser = argparse.ArgumentParser(description="MindScan Automator Tool")
    parser.add_argument("--all", action="store_true", help="Executa todas as tasks automaticamente")
    parser.add_argument("--task", type=str, help="Executa uma task específica")
    args = parser.parse_args()

    log("===== MINDScan Automator Inovexa =====")

    if args.all:
        run_all_tasks()
    elif args.task:
        run_task(args.task)
    else:
        run_from_json()

    log("===== PIPELINE CONCLUÍDO COM SUCESSO =====")

if __name__ == "__main__":
    main()
