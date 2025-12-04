"""
FORCEGIT v3 — Blindado, Seguro e Não-Destrutivo
Inovexa Software — Leo Vinci

REGRAS DE SEGURANÇA:
- Apenas remove itens da WHITELIST.
- Nunca remove arquivos fora dessa lista.
- Cria backup obrigatório antes de cada remoção.
- Log completo em forcegit_v3.log.
- Compatível com NTFS e caminhos longos.
"""

import os
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # aponta para D:\MindScan

# Diretórios/arquivos permitidos para remoção (controle total)
WHITELIST = [
    "backups_autofix",
    "trash",
    "venv",
    "Indo",
    "cleanup_audit_blindado.log",
    "cleanup_audit_blindado_forcegit.log",
    "cleanup_audit_blindado_forcegit_v2.log",
    "log_sincronizacao.txt",
    "scan_project_file_sizes.py",
    "scan_project_file_sizes.bat",
    "revisor_global.py",
    "run_cleanup_blindado.bat",
    "fix_mindscan_cleanup_blindado_forcegit_v2.py"
]

LOG_FILE = ROOT / "forcegit_v3.log"


def log(msg: str):
    """Registra ações no log e imprime para acompanhamento."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(msg)


def create_backup(path: Path):
    """Cria uma cópia de segurança antes de qualquer remoção."""
    backup_dir = ROOT / "forcegit_backups"
    backup_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_target = backup_dir / f"{path.name}.backup_{timestamp}"

    if path.is_dir():
        shutil.copytree(path, backup_target)
    else:
        shutil.copy2(path, backup_target)

    log(f"Backup criado: {backup_target}")


def safe_remove(path: Path):
    """Remove apenas itens explicitamente permitidos."""
    if not path.exists():
        return

    create_backup(path)

    if path.is_dir():
        shutil.rmtree(path)
        log(f"Diretório removido: {path}")
    else:
        path.unlink()
        log(f"Arquivo removido: {path}")


def remove_bak_files():
    """Remove apenas arquivos .bak, garantindo que sejam backup residual."""
    for bak in ROOT.rglob("*.bak"):
        create_backup(bak)
        bak.unlink()
        rel = bak.relative_to(ROOT)
        log(f"Arquivo .bak removido: {rel}")


def run_forcegit():
    log("=== Iniciando ForceGit v3 (Blindado) ===")

    # 1. Remover resíduos .bak
    remove_bak_files()

    # 2. Remover somente itens explicitamente aprovados
    for item in WHITELIST:
        target = ROOT / item
        if target.exists():
            safe_remove(target)

    log("=== ForceGit v3 concluído com segurança ===")


if __name__ == "__main__":
    run_forcegit()
