"""
Task: validate_structure
MindScan Automator — Inovexa Software
Autor: Leo Vinci (GPT Inovexa)
Data: 26/11/2025

Função:
- Validar toda a estrutura oficial do MindScan
- Criar pastas faltantes
- Criar arquivos essenciais vazios quando aplicável
- Registrar correções
- Emitir relatório interno de conformidade
"""

import os
import json
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------
# Estrutura oficial do MindScan (BOOT-SPEC)
# ---------------------------------------------------------------------

REQUIRED_STRUCTURE = {
    "mindscan": {
        "backend": {
            "algorithms": [
                "matcher.py",
                "performance.py",
                "dass21.py",
                "esquemas.py",
                "big5.py",
                "teique.py",
                "ocai.py",
                "cruzamentos.py",
                "bussola.py"
            ],
            "services/pdf": [],
            "mi/persona": [],
            "mi/compliance": [],
            "mi/prompts": [],
            "models": [],
            "routers": [],
            "db": [],
            "config.py": None,
            "main.py": None
        },
        "frontend": {},
        "tools": {},
        "docs/prompts": {},
        "docs/metodologias": {},
        "docs/pdfs": {},
        "data/templates": {}
    }
}


# ---------------------------------------------------------------------
# Utilitários internos
# ---------------------------------------------------------------------

def ensure_dir(path: Path, log: list):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        log.append(f"[CREATE] Diretório criado: {path}")


def ensure_file(path: Path, log: list):
    if not path.exists():
        path.touch()
        log.append(f"[CREATE] Arquivo criado: {path}")


def validate_recursive(base: Path, structure: dict, log: list):
    """
    Caminha pela estrutura oficial e cria tudo que for necessário.
    """
    for name, content in structure.items():
        target = base / name

        # Caso seja arquivo (None ou lista)
        if isinstance(content, list) or content is None:
            if isinstance(content, list):
                # diretório contendo arquivos
                ensure_dir(target, log)
                for file_name in content:
                    ensure_file(target / file_name, log)
            else:
                # arquivo simples
                ensure_file(target, log)

        # Caso seja diretório com subestrutura
        elif isinstance(content, dict):
            ensure_dir(target, log)
            validate_recursive(target, content, log)


# ---------------------------------------------------------------------
# Relatório final
# ---------------------------------------------------------------------

def write_report(log: list, report_path: Path):
    report = {
        "task": "validate_structure",
        "timestamp": datetime.now().isoformat(),
        "actions_executed": log
    }
    with report_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)


# ---------------------------------------------------------------------
# Entry point da Task
# ---------------------------------------------------------------------

def run(context):
    """
    Ponto de entrada chamado pelo Automator.
    'context' contém:
        - project_root
        - logs_path
        - settings
    """

    project_root = Path(context["project_root"])
    logs_dir = Path(context["logs_path"])
    ensure_dir(logs_dir, [])

    log = []
    log.append("[INIT] Iniciando validate_structure")

    validate_recursive(project_root, REQUIRED_STRUCTURE, log)

    report_path = logs_dir / "validate_structure_report.json"
    write_report(log, report_path)

    return {
        "status": "success",
        "message": "Estrutura validada e corrigida.",
        "report": str(report_path)
    }


if __name__ == "__main__":
    # Execução direta (debug/manual)
    fake_context = {
        "project_root": str(Path(__file__).resolve().parents[2]),
        "logs_path": str(Path(__file__).resolve().parents[2] / "logs"),
        "settings": {}
    }
    print(run(fake_context))
