"""
Consolidar Performance — Automação Total v1.0
Diretor: Leo Vinci — Inovexa Software

OBJETIVO:
- Criar core.py com a lógica atual de backend/algorithms/performance.py
- Transformar:
    - backend/algorithms/performance.py         (raiz)
    - backend/algorithms/performance/performance.py  (modular)
  em wrappers compatíveis
- Criar __init__.py expondo API unificada
- Preservar 100% da lógica original (Anti-Regressão Total)
"""

import shutil
from pathlib import Path
from datetime import datetime

# RAIZ DO PROJETO
ROOT = Path(__file__).resolve().parent.parent

# Diretório do algoritmo Performance
ALG_DIR = ROOT / "backend" / "algorithms" / "performance"

# Arquivos alvo
FILE_LEGACY  = ROOT / "backend" / "algorithms" / "performance.py"
FILE_MODULAR = ALG_DIR / "performance.py"
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


def consolidate_performance():
    print("\n=== CONSOLIDAÇÃO PERFORMANCE — INÍCIO ===")

    # 1. Verificar se o arquivo legacy existe
    if not FILE_LEGACY.exists():
        raise FileNotFoundError("Arquivo legacy performance.py não encontrado.")

    # 2. Backup dos arquivos envolvidos
    for f in [FILE_LEGACY, FILE_MODULAR]:
        if f.exists():
            backup(f)

    # 3. Ler lógica original — FONTE DA VERDADE
    legacy_code = read_file(FILE_LEGACY)

    # 4. Criar core.py com a lógica original
    write_file(FILE_CORE, legacy_code)

    # 5. Criar wrapper legado (performance.py raiz)
    wrapper_root = """# Wrapper legado — Performance
# Direciona para backend/algorithms/performance/core.py
from .performance.core import *
"""
    write_file(FILE_LEGACY, wrapper_root)

    # 6. Criar wrapper modular (pasta performance/)
    wrapper_modular = """# Wrapper modular — Performance
# Direciona para core consolidado
from .core import *
"""
    write_file(FILE_MODULAR, wrapper_modular)

    # 7. Criar __init__.py
    init_content = """# Pacote Performance — consolidado
from .core import *
"""
    write_file(FILE_INIT, init_content)

    print("=== CONSOLIDAÇÃO PERFORMANCE — FINALIZADA ===\n")


if __name__ == "__main__":
    consolidate_performance()
