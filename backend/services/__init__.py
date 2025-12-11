# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\__init__.py
# Última atualização: 2025-12-11T09:59:21.120711

"""
MindScan Backend — Services Module
Diretor Técnico: Leo Vinci

Este módulo fornece a infraestrutura para carregamento
e registro de serviços internos do backend.

Cada serviço poderá implementar:
    - lógica psicométrica
    - análises internas
    - pré-processamento
    - pipelines independentes
"""

import importlib
from pathlib import Path
from datetime import datetime


# ----------------------------------------------------------------------
# Diretórios e Logs
# ----------------------------------------------------------------------
SERVICES_ROOT = Path(__file__).resolve().parent
RUNTIME_DIR = SERVICES_ROOT / "runtime"
RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

LOGFILE = RUNTIME_DIR / "services_runtime.log"


def slog(msg: str):
    """Log interno do módulo de serviços."""
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[Services {ts}] {msg}"
    print(line)

    with LOGFILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


# ----------------------------------------------------------------------
# Carregador Dinâmico de Serviços
# ----------------------------------------------------------------------
def load_services():
    """
    Carrega dinamicamente todos os serviços existentes
    em backend/services/ que contenham uma classe Service
    com método run().
    """
    slog("Carregando serviços...")

    services = []

    for file in SERVICES_ROOT.glob("*.py"):
        if file.name.startswith("_"):
            continue
        if file.name == "__init__.py":
            continue

        module_name = f"backend.services.{file.stem}"
        slog(f"Importando serviço: {module_name}")

        try:
            module = importlib.import_module(module_name)
        except Exception as e:
            slog(f"[ERRO] Falha ao importar {module_name}: {e}")
            continue

        # Buscar classes com run()
        for item in dir(module):
            obj = getattr(module, item)
            if hasattr(obj, "run") and callable(obj.run):
                services.append(obj)
                slog(f"Serviço detectado: {obj.__name__}")

    slog(f"Total de serviços carregados: {len(services)}")
    return services
