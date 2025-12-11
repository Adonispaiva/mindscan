# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\tools\consolidar_bussola_v1.py
# Última atualização: 2025-12-11T09:59:27.777220

"""
Consolidar Bússola — Automação Total v1.0
Diretor: Leo Vinci — Inovexa Software

OBJETIVO:
- Criar core.py com a lógica atual de backend/algorithms/bussola.py
- Transformar:
    - backend/algorithms/bussola.py               (raiz)
    - backend/algorithms/bussola/bussola.py       (modular)
  em wrappers compatíveis
- Criar __init__.py expondo API unificada
- Preservar 100% da lógica original (Anti-Regressão Total)
"""

import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent

ALG_DIR = ROOT / "backend" / "algorithms" / "bussola"

FILE_LEGACY  = ROOT / "backend" / "algorithms" / "bussola.py"
FILE_MODULAR = ALG_DIR / "bussola.py"
FILE_CORE    = ALG_DIR / "core.py"
FILE_INIT    = ALG_DIR / "__init__.py"

BACKUP_DIR = ROOT / "consolidation_backups"


def backup(path: Path):
    """Cria backup antes de qualquer alteração."""
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = BACKUP_DIR / f"{path.name}.backup_{timestamp}"

    if path.exists():
        if path.is_file():
            shutil.copy2(path, target)
        else:
            shutil.copytree(path, target)
        print(f"[BACKUP] {path} → {target}")


def read_file(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: Path, content: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[WRITE] {path}")


def consolidate_bussola():
    print("\n=== CONSOLIDAÇÃO BÚSSOLA — INÍCIO ===")

    # 1. Garantir existência do legacy
    if not FILE_LEGACY.exists():
        raise FileNotFoundError("Arquivo legacy bussola.py não encontrado.")

    # 2. Backups
    for f in [FILE_LEGACY, FILE_MODULAR]:
        if f.exists():
            backup(f)

    # 3. Carregar código original (fonte única da verdade)
    legacy_code = read_file(FILE_LEGACY)

    # 4. Criar core.py com lógica integral
    write_file(FILE_CORE, legacy_code)

    # 5. Criar wrapper raiz
    wrapper_root = """# Wrapper legado — Bússola
# Direciona para backend/algorithms/bussola/core.py
from .bussola.core import *
"""
    write_file(FILE_LEGACY, wrapper_root)

    # 6. Criar wrapper modular (subpasta)
    wrapper_modular = """# Wrapper modular — Bússola
# Direciona para core consolidado
from .core import *
"""
    write_file(FILE_MODULAR, wrapper_modular)

    # 7. Criar __init__.py padronizado
    init_content = """# Pacote Bússola — consolidado
from .core import *
"""
    write_file(FILE_INIT, init_content)

    print("=== CONSOLIDAÇÃO BÚSSOLA — FINALIZADA ===\n")


if __name__ == "__main__":
    consolidate_bussola()
