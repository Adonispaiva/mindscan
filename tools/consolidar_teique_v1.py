"""
Consolidar TEIQue — Automação Total v1.0
Diretor: Leo Vinci — Inovexa Software

OBJETIVO:
- Criar core.py com a lógica atual de backend/algorithms/teique.py
- Transformar:
    - backend/algorithms/teique.py         (raiz)
    - backend/algorithms/teique/teique.py  (modular)
  em wrappers compatíveis
- Criar __init__.py expondo API unificada
- Preservar 100% da lógica original (Anti-Regressão Total)
"""

import shutil
from pathlib import Path
from datetime import datetime

# RAIZ DO PROJETO (MindScan)
ROOT = Path(__file__).resolve().parent.parent

# Diretório do algoritmo
ALG_DIR = ROOT / "backend" / "algorithms" / "teique"

# Arquivos
FILE_LEGACY  = ROOT / "backend" / "algorithms" / "teique.py"
FILE_MODULAR = ALG_DIR / "teique.py"
FILE_CORE    = ALG_DIR / "core.py"
FILE_INIT    = ALG_DIR / "__init__.py"

# Diretório de backups
BACKUP_DIR = ROOT / "consolidation_backups"


def backup(path: Path):
    """Cria backup seguro antes de qualquer alteração."""
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


def consolidate_teique():
    print("\n=== CONSOLIDAÇÃO TEIQue — INÍCIO ===")

    # 1. Garantir que o arquivo legacy (raiz) existe
    if not FILE_LEGACY.exists():
        raise FileNotFoundError("Arquivo legacy teique.py não encontrado.")

    # 2. Backups antes de qualquer modificação
    for f in [FILE_LEGACY, FILE_MODULAR]:
        if f.exists():
            backup(f)

    # 3. Carregar a lógica original (fonte única da verdade)
    legacy_code = read_file(FILE_LEGACY)

    # 4. Criar core.py com 100% da lógica original
    write_file(FILE_CORE, legacy_code)

    # 5. Criar wrapper raiz para manter compatibilidade histórica
    wrapper_root = """# Wrapper legado — TEIQue
# Direciona para backend/algorithms/teique/core.py
from .teique.core import *
"""
    write_file(FILE_LEGACY, wrapper_root)

    # 6. Criar wrapper modular dentro da pasta teique/
    wrapper_modular = """# Wrapper modular — TEIQue
# Direciona para core consolidado
from .core import *
"""
    write_file(FILE_MODULAR, wrapper_modular)

    # 7. Criar __init__.py
    init_content = """# Pacote TEIQue — consolidado
from .core import *
"""
    write_file(FILE_INIT, init_content)

    print("=== CONSOLIDAÇÃO TEIQue — FINALIZADA ===\n")


if __name__ == "__main__":
    consolidate_teique()
