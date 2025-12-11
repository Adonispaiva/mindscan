# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\tools\automator\tasks\__init__.py
# Última atualização: 2025-12-11T09:59:27.824087

"""
MindScan Automator — Registro de Tasks
Autor: Leo Vinci (GPT Inovexa)
Data: 26/11/2025

Função:
- Registrar todas as tasks do Automator.
- Mapear nomes → funções executáveis.
- Atender ao pipeline central.
- Garantir carregamento dinâmico e seguro.

Este arquivo consolida:
    • validate_structure
    • fix_backend
    • fix_modules
    • fix_services
    • run_audit
    • generate_report
"""

from .validate_structure import run as task_validate_structure
from .fix_backend import run as task_fix_backend
from .fix_modules import run as task_fix_modules
from .fix_services import run as task_fix_services
from .run_audit import run as task_run_audit
from .generate_report import run as task_generate_report


TASKS = {
    "validate_structure": task_validate_structure,
    "fix_backend": task_fix_backend,
    "fix_modules": task_fix_modules,
    "fix_services": task_fix_services,
    "run_audit": task_run_audit,
    "generate_report": task_generate_report,
}


def get_task(name):
    """
    Retorna a task registrada.
    """
    if name not in TASKS:
        return None
    return TASKS[name]


def list_tasks():
    """
    Lista todas as tasks disponíveis.
    """
    return list(TASKS.keys())
