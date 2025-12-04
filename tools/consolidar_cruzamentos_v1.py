"""
Consolidar Cruzamentos — Automação Total v1.0
Diretor: Leo Vinci — Inovexa Software

OBJETIVO:
- Criar core.py com a lógica atual de backend/algorithms/cruzamentos.py
- Transformar:
    - backend/algorithms/cruzamentos.py                 (raiz real)
    - backend/algorithms/cruzamentos/cruzamentos.py     (modular placeholder)
  em wrappers compatíveis
- Criar __init__.py expondo API unificada
- Preservar 100% da lógica original (Anti-Regressão Total)
"""

import shutil
from pathlib import Path
from datetime import datetime

# Raiz do projeto MindScan
ROOT = Path(__file__).resolve().parent.parent

# Diretório do algoritmo
ALG_DIR = ROOT / "backend" / "algorithms" / "cruzamentos"

# Arquivos
FILE_LEGACY  = ROOT / "backend" / "algorithms" / "cruzamentos.py"
FILE_MODULAR = ALG_DIR / "cruzamentos.py"
FILE_CORE    = ALG_DIR / "core.py"
FILE_INIT    = ALG_DIR / "__init__.py"

# Backups
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


def consolidate_cruzamentos():
    print("\n=== CONSOLIDAÇÃO CRUZAMENTOS — INÍCIO ===")

    # 1. Verificar existência do arquivo raiz com lógica real
    if not FILE_LEGACY.exists():
        raise FileNotFoundError("Arquivo raiz cruzamentos.py não encontrado.")

    # 2. Backup total
    for f in [FILE_LEGACY, FILE_MODULAR]:
        if f.exists():
            backup(f)

    # 3. Ler lógica real (fonte única da verdade)
    legacy_code = read_file(FILE_LEGACY)

    # 4. Criar core.py com 100% do conteúdo original
    write_file(FILE_CORE, legacy_code)

    # 5. Criar wrapper raiz
    wrapper_root = """# Wrapper legado — Cruzamentos
# Direciona para backend/algorithms/cruzamentos/core.py
from .cruzamentos.core import *
"""
    write_file(FILE_LEGACY, wrapper_root)

    # 6. Criar wrapper modular (subpasta)
    wrapper_modular = """# Wrapper modular — Cruzamentos
# Direciona para core consolidado
from .core import *
"""
    write_file(FILE_MODULAR, wrapper_modular)

    # 7. Criar __init__.py
    init_content = """# Pacote Cruzamentos — consolidado
from .core import *
"""
    write_file(FILE_INIT, init_content)

    print("=== CONSOLIDAÇÃO CRUZAMENTOS — FINALIZADA ===\n")


if __name__ == "__main__":
    consolidate_cruzamentos()
