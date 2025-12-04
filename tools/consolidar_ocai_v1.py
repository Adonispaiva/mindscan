"""
Consolidar OCAI — Automação Total v1.0
Diretor: Leo Vinci — Inovexa Software

OBJETIVO:
- Criar core.py com a lógica atual de backend/algorithms/ocai.py
- Transformar:
    - backend/algorithms/ocai.py  (raiz)
    - backend/algorithms/ocai/ocai.py  (modular)
  em wrappers compatíveis
- Criar __init__.py expondo API unificada
- Preservar 100% da lógica original (Anti-Regressão Total)
"""

import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
ALG_DIR = ROOT / "backend" / "algorithms" / "ocai"

FILE_LEGACY = ROOT / "backend" / "algorithms" / "ocai.py"
FILE_MODULAR = ALG_DIR / "ocai.py"
FILE_CORE = ALG_DIR / "core.py"
FILE_INIT = ALG_DIR / "__init__.py"
BACKUP_DIR = ROOT / "consolidation_backups"


def backup(path: Path):
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = BACKUP_DIR / f"{path.name}.backup_{timestamp}"

    if path.exists():
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


def consolidate_ocai():
    print("\n=== CONSOLIDAÇÃO OCAI — INÍCIO ===")

    # 1. Validar existência do arquivo legacy (fonte oficial)
    if not FILE_LEGACY.exists():
        raise FileNotFoundError("Arquivo legacy ocai.py não encontrado.")

    # 2. Backup dos arquivos envolvidos
    for f in [FILE_LEGACY, FILE_MODULAR]:
        if f.exists():
            backup(f)

    # 3. Ler conteúdo original (fonte da verdade)
    legacy_code = read_file(FILE_LEGACY)

    # 4. Criar core.py com a lógica consolidada
    write_file(FILE_CORE, legacy_code)

    # 5. Criar wrapper para ocai.py (raiz)
    wrapper_root = """# Wrapper legado — OCAI
# Direciona para backend/algorithms/ocai/core.py
from .ocai.core import *
"""
    write_file(FILE_LEGACY, wrapper_root)

    # 6. Criar wrapper modular (subpasta)
    wrapper_modular = """# Wrapper modular — OCAI
# Direciona para core consolidado
from .core import *
"""
    write_file(FILE_MODULAR, wrapper_modular)

    # 7. Criar __init__.py
    init_content = """# Pacote OCAI — consolidado
from .core import *
"""
    write_file(FILE_INIT, init_content)

    print("=== CONSOLIDAÇÃO OCAI — FINALIZADA ===\n")


if __name__ == "__main__":
    consolidate_ocai()
