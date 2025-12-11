# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\core\__init__.py
# Última atualização: 2025-12-11T09:59:27.558489

"""
MindScan CORE — Núcleo Cognitivo
Diretor Técnico: Leo Vinci

Este módulo inicializa o CORE, responsável por:
    - processamento cognitivo
    - algoritmos psicológicos
    - pontuação e perfis
    - métricas internas
    - motor cognitivo (engine)
    - integração com PsychCoreService

Nenhuma execução automática é feita aqui.
"""

from pathlib import Path
from datetime import datetime
import importlib


# ----------------------------------------------------------------------
# Diretórios e Logs do CORE
# ----------------------------------------------------------------------
CORE_ROOT = Path(__file__).resolve().parent
RUNTIME = CORE_ROOT / "runtime"
RUNTIME.mkdir(parents=True, exist_ok=True)

LOGFILE = RUNTIME / "core_runtime.log"


def corelog(msg: str):
    """Log central do CORE."""
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[CORE {ts}] {msg}"
    print(line)

    with LOGFILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


# ----------------------------------------------------------------------
# Carregador de Componentes
# ----------------------------------------------------------------------
def load_core_components():
    """
    Carrega dinamicamente os módulos essenciais do CORE:
        - engine
        - metrics
        - scoring
        - profiling
        - algorithms
        - diagnostics
        - reporting
        - utils
    """
    corelog("Carregando componentes principais do CORE...")

    components = [
        "engine",
        "metrics",
        "scoring",
        "profiles",
        "algorithms",
        "diagnostics",
        "reporting",
        "utils",
    ]

    loaded = []

    for comp in components:
        module_path = f"core.{comp}"
        try:
            importlib.import_module(module_path)
            loaded.append(module_path)
            corelog(f"Componente carregado: {module_path}")
        except Exception as e:
            corelog(f"[ERRO] Falha ao carregar {module_path}: {e}")

    corelog(f"Total carregado: {len(loaded)} componentes.")
    return loaded
