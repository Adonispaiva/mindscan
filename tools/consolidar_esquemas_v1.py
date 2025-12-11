# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\tools\consolidar_esquemas_v1.py
# Última atualização: 2025-12-11T09:59:27.792836

"""
Consolidar Esquemas — Automação Total v1.0
Diretor: Leo Vinci — Inovexa Software

OBJETIVO:
- Criar core.py com a lógica atual de backend/algorithms/esquemas.py
- Transformar:
    - backend/algorithms/esquemas.py  (raiz)
    - backend/algorithms/esquemas/esquemas.py  (modular)
  em wrappers compatíveis
- Criar __init__.py expondo API unificada
- Preservar 100% da lógica original (Anti-Regressão Total)
"""

import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
ALG_DIR = ROOT / "backend" / "algorithms" / "esquemas"

FILE_LEGACY = ROOT / "backend" / "algorithms" / "esquemas.py"
FILE_MODULAR = ALG_DIR / "esquemas.py"
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


def consolidate_esquemas():
    print("\n=== CONSOLIDAÇÃO ESQUEMAS — INÍCIO ===")

    # 1. Validar existência do arquivo legacy (fonte oficial)
    if not FILE_LEGACY.exists():
        raise FileNotFoundError("Arquivo legacy esquemas.py não encontrado.")

    # 2. Backup dos arquivos envolvidos
    for f in [FILE_LEGACY, FILE_MODULAR]:
        if f.exists():
            backup(f)

    # 3. Ler conteúdo original (fonte da verdade)
    legacy_code = read_file(FILE_LEGACY)

    # 4. Criar core.py com a lógica consolidada
    write_file(FILE_CORE, legacy_code)

    # 5. Criar wrapper para esquemas.py (raiz)
    wrapper_root = """# Wrapper legado — Esquemas
# Direciona para backend/algorithms/esquemas/core.py
from .esquemas.core import *
"""
    write_file(FILE_LEGACY, wrapper_root)

    # 6. Criar wrapper da versão modular (subpasta)
    wrapper_modular = """# Wrapper modular — Esquemas
# Direciona para core consolidado
from .core import *
"""
    write_file(FILE_MODULAR, wrapper_modular)

    # 7. Criar __init__.py
    init_content = """# Pacote Esquemas — consolidado
from .core import *
"""
    write_file(FILE_INIT, init_content)

    print("=== CONSOLIDAÇÃO ESQUEMAS — FINALIZADA ===\n")


if __name__ == "__main__":
    consolidate_esquemas()
