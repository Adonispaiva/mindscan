#!/usr/bin/env python3
"""
MindScan / Inovexa
Script estrutural definitivo para geração automática de __init__.py

Funções:
- Cria __init__.py em todas as pastas Python válidas
- Evita criação em diretórios irrelevantes
- Não sobrescreve arquivos existentes
- Possui modo dry-run
- Gera log auditável
- Retorna exit code adequado

Autor: Correção estrutural (Inovexa)
Data: 2025-12-12
"""

import os
import sys
import argparse
from datetime import datetime

# ============================================================
# CONFIGURAÇÃO
# ============================================================

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

IGNORE_DIRS = {
    "__pycache__",
    ".git",
    ".github",
    ".idea",
    ".vscode",
    "node_modules",
    "venv",
    ".venv",
    "dist",
    "build",
}

# Arquivos .py que NÃO caracterizam pacote Python por si só
NON_PACKAGE_FILES = {
    "manage.py",
    "wsgi.py",
    "asgi.py",
}

LOG_FILE = os.path.join(PROJECT_ROOT, "init_generation.log")

# ============================================================
# TEMPLATE DO __init__.py
# ============================================================

INIT_TEMPLATE = '''"""
Pacote Python inicializado automaticamente.

Projeto : MindScan / Inovexa
Gerado  : {timestamp}
Motivo  : Garantir resolução correta de imports absolutos e relativos
Aviso   : NÃO remover este arquivo.
"""
__all__ = []
'''

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def should_ignore(path: str) -> bool:
    parts = set(path.split(os.sep))
    return not parts.isdisjoint(IGNORE_DIRS)


def is_python_package_candidate(directory: str) -> bool:
    try:
        files = os.listdir(directory)
    except OSError:
        return False

    py_files = [
        f for f in files
        if f.endswith(".py")
        and f != "__init__.py"
        and f not in NON_PACKAGE_FILES
    ]

    return len(py_files) > 0


def ensure_init_file(directory: str, dry_run: bool) -> bool:
    init_path = os.path.join(directory, "__init__.py")

    if os.path.exists(init_path):
        return False

    if dry_run:
        log(f"[DRY-RUN] Criaria {init_path}")
        return True

    content = INIT_TEMPLATE.format(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    try:
        with open(init_path, "w", encoding="utf-8") as f:
            f.write(content)
        log(f"[CRIADO] {init_path}")
        return True
    except OSError as e:
        log(f"[ERRO] Falha ao criar {init_path}: {e}")
        raise


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Gera automaticamente __init__.py em pacotes Python válidos."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula a execução sem criar arquivos"
    )

    args = parser.parse_args()
    dry_run = args.dry_run

    log("=" * 70)
    log("MindScan / Inovexa — Geração automática de __init__.py")
    log(f"Raiz do projeto : {PROJECT_ROOT}")
    log(f"Modo dry-run    : {'SIM' if dry_run else 'NÃO'}")
    log("=" * 70)

    scanned_dirs = 0
    created_count = 0

    try:
        for root, dirs, files in os.walk(PROJECT_ROOT):
            if should_ignore(root):
                continue

            scanned_dirs += 1

            if is_python_package_candidate(root):
                if ensure_init_file(root, dry_run):
                    created_count += 1

        log("=" * 70)
        log(f"Pastas analisadas : {scanned_dirs}")
        log(f"__init__.py novos : {created_count}")
        log("Execução concluída com sucesso.")
        log("=" * 70)

        sys.exit(0)

    except Exception as e:
        log(f"[FATAL] Execução interrompida: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
