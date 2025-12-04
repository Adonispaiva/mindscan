"""
Consolidar Big5 — Automação Total v1.0
Diretor: Leo Vinci — Inovexa

OBJETIVO:
- Criar core.py com a lógica de backend/algorithms/big5.py
- Transformar big5.py (raiz) e big5/big5.py (modular) em wrappers compatíveis
- Criar __init__.py expondo API unificada
- Preservar 100% da lógica original
- Anti-Regressão Total
"""

import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
ALG_DIR = ROOT / "backend" / "algorithms" / "big5"

FILE_LEGACY = ROOT / "backend" / "algorithms" / "big5.py"
FILE_MODULAR = ALG_DIR / "big5.py"
FILE_CORE = ALG_DIR / "core.py"
FILE_INIT = ALG_DIR / "__init__.py"
BACKUP_DIR = ROOT / "consolidation_backups"


def backup(path: Path):
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = BACKUP_DIR / f"{path.name}.backup_{timestamp}"

    if path.is_file():
        shutil.copy2(path, target)
    elif path.is_dir():
        shutil.copytree(path, target)

    print(f"[BACKUP] {path} → {target}")


def read_file(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: Path, content: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[WRITE] {path}")


def consolidate_big5():
    print("\n=== CONSOLIDAÇÃO BIG5 — INÍCIO ===")

    # 1. Validar existência dos arquivos
    if not FILE_LEGACY.exists():
        raise FileNotFoundError("Arquivo legacy big5.py não encontrado.")

    # 2. Backup de todos os arquivos envolvidos
    for f in [FILE_LEGACY, FILE_MODULAR]:
        if f.exists():
            backup(f)

    # 3. Ler lógica original do arquivo raiz (fonte da verdade)
    legacy_code = read_file(FILE_LEGACY)

    # 4. Criar core.py com lógica completa
    write_file(FILE_CORE, legacy_code)

    # 5. Criar wrapper para big5.py (raiz)
    wrapper_root = """# Wrapper legado — Big5
# Direciona para backend/algorithms/big5/core.py
from .big5.core import *
"""
    write_file(FILE_LEGACY, wrapper_root)

    # 6. Criar wrapper modular (subpasta big5/)
    wrapper_modular = """# Wrapper modular — Big5
# Direciona para core consolidado
from .core import *
"""
    write_file(FILE_MODULAR, wrapper_modular)

    # 7. Criar __init__.py
    init_content = """# Pacote Big5 — consolidado
from .core import *
"""
    write_file(FILE_INIT, init_content)

    print("=== CONSOLIDAÇÃO BIG5 — FINALIZADA ===\n")


if __name__ == "__main__":
    consolidate_big5()
