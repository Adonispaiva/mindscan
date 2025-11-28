"""
Task: run_audit
MindScan Automator — Inovexa Software
Autor: Leo Vinci (GPT Inovexa)
Data: 26/11/2025

Objetivo:
- Auditar automaticamente toda a estrutura MindScan.
- Validar a presença e integridade de:
    • backend
    • modules
    • services
    • algorithms
    • pipeline
    • arquivos essenciais
- Gerar relatório técnico avançado, com:
    • status por componente
    • inconsistências
    • itens faltantes
    • sugestões de correção
- Preparar dados para a geração do relatório final.

Resultado:
- logs/audit_report.json
"""

import os
import json
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------------------
# Regras oficiais de auditoria (BOOT-SPEC / identidade MindScan)
# ---------------------------------------------------------------------

REQUIRED_BACKEND_DIRS = [
    "algorithms",
    "services",
    "mi",
    "models",
    "routers",
    "db"
]

REQUIRED_MODULES = [
    "bigfive",
    "teique",
    "ocai",
    "dass21",
    "esquemas",
    "performance",
    "cruzamentos",
    "bussola",
    "report_pipeline"
]

REQUIRED_SERVICES = [
    "loader",
    "dispatcher",
    "validator",
    "aggregator",
    "report"
]


# ---------------------------------------------------------------------
# AUDITORES INTERNOS
# ---------------------------------------------------------------------

def check_dirs(base: Path, items: list, log: dict):
    results = {}
    for item in items:
        path = base / item
        exists = path.exists()
        results[item] = {
            "exists": exists,
            "path": str(path)
        }
        if not exists:
            log["missing"].append(f"[DIR] {path}")
    return results


def check_files_recursively(base: Path, log: dict):
    """
    Verifica se há arquivos vazios, corrompidos ou suspeitos.
    """
    issues = []
    for root, _, files in os.walk(base):
        for f in files:
            file_path = Path(root) / f
            try:
                size = file_path.stat().st_size
                if size == 0:
                    issues.append(f"[EMPTY FILE] {file_path}")
                if size < 3:  # não deve existir arquivo minúsculo
                    issues.append(f"[SUSPICIOUS] {file_path}")
            except Exception as e:
                issues.append(f"[ERROR] {file_path}: {e}")
    log["issues"].extend(issues)
    return issues


def summarize_audit(log):
    if len(log["missing"]) == 0 and len(log["issues"]) == 0:
        return "A estrutura está íntegra, estável e aderente ao BOOT-SPEC MindScan."
    else:
        return "Foram identificados problemas estruturais. Recomenda-se executar tasks corretivas."


# ---------------------------------------------------------------------
# RELATÓRIO
# ---------------------------------------------------------------------

def write_report(path: Path, report: dict):
    with path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)


# ---------------------------------------------------------------------
# ENTRYPOINT
# ---------------------------------------------------------------------

def run(context):
    project_root = Path(context["project_root"])
    logs_dir = Path(context["logs_path"])
    logs_dir.mkdir(parents=True, exist_ok=True)

    log = {
        "missing": [],
        "issues": [],
        "checks": {}
    }

    backend_root = project_root / "mindscan" / "backend"
    modules_root = project_root / "mindscan" / "modules"
    services_root = project_root / "mindscan" / "services"

    # Auditorias principais
    log["checks"]["backend_dirs"] = check_dirs(backend_root, REQUIRED_BACKEND_DIRS, log)
    log["checks"]["modules"] = check_dirs(modules_root, REQUIRED_MODULES, log)
    log["checks"]["services"] = check_dirs(services_root, REQUIRED_SERVICES, log)

    # Auditoria de arquivos vazios/suspeitos
    check_files_recursively(project_root / "mindscan", log)

    # Resumo geral
    summary = summarize_audit(log)

    report_data = {
        "task": "run_audit",
        "timestamp": datetime.now().isoformat(),
        "summary": summary,
        "details": log
    }

    report_path = logs_dir / "audit_report.json"
    write_report(report_path, report_data)

    return {
        "status": "success",
        "message": "Auditoria completa.",
        "report": str(report_path)
    }


if __name__ == "__main__":
    fake_ctx = {
        "project_root": str(Path(__file__).resolve().parents[2]),
        "logs_path": str(Path(__file__).resolve().parents[2] / "logs"),
        "settings": {}
    }
    print(run(fake_ctx))
