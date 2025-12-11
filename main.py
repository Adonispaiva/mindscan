# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\main.py
# Última atualização: 2025-12-11T09:59:20.421857

"""
MindScan - Sistema Principal (main.py)
Inovexa Software
Versão: 1.0 - Diretor Técnico (Leo Vinci)

Função:
    - Inicializar o ecossistema MindScan
    - Carregar pipelines, managers e automator
    - Validar estrutura do projeto
    - Ativar runtime e logs centrais
    - Gerenciar exceções de forma padronizada
"""

import sys
import time
import traceback
import importlib
from pathlib import Path
from datetime import datetime

# ----------------------------------------------------------------------
# Caminhos Base
# ----------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
TOOLS = ROOT / "tools"
MANAGERS = ROOT / "managers"
LOGS = ROOT / "logs" / "runtime"
LOGS.mkdir(parents=True, exist_ok=True)

RUNTIME_LOG = LOGS / f"runtime_{datetime.now().strftime('%Y-%m-%d_%Hh%Mmin%Ss')}.log"


# ----------------------------------------------------------------------
# Utilidades Internas
# ----------------------------------------------------------------------
def log(msg: str):
    """Escreve no log do runtime."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] {msg}"

    print(line)
    with RUNTIME_LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def safe_import(module_path: str):
    """Importa módulos dos managers com segurança."""
    try:
        return importlib.import_module(module_path)
    except Exception as e:
        log(f"[ERRO] Falha ao importar {module_path}: {e}")
        return None


# ----------------------------------------------------------------------
# Validação da Estrutura
# ----------------------------------------------------------------------
def validar_estrutura():
    """Confirma se pastas essenciais existem e não há colapsos estruturais."""
    obrigatorias = [
        "backend",
        "core",
        "frontend",
        "modules",
        "maintenance",
        "tasks",
        "releases",
        "automator",
        "tools",
        "logs"
    ]

    log("Validando estrutura do projeto...")

    faltantes = []
    for pasta in obrigatorias:
        if not (ROOT / pasta).exists():
            faltantes.append(pasta)

    if faltantes:
        log(f"[ERRO CRÍTICO] Pastas ausentes: {faltantes}")
        raise RuntimeError("Estrutura incompleta. Abortando.")

    log("Estrutura validada com sucesso.")


# ----------------------------------------------------------------------
# Carregamento dos MANAGERS
# ----------------------------------------------------------------------
def carregar_managers():
    """
    Carrega qualquer arquivo dentro de /managers que contenha
    uma classe Manager com método `run()`.
    """
    log("Carregando Managers...")

    managers_detectados = []

    for file in MANAGERS.glob("*.py"):
        if file.name.startswith("_"):
            continue

        module_name = f"managers.{file.stem}"
        module = safe_import(module_name)

        if not module:
            continue

        for item in dir(module):
            obj = getattr(module, item)
            if hasattr(obj, "run") and callable(obj.run):
                managers_detectados.append(obj)

    log(f"Managers detectados: {len(managers_detectados)}")

    return managers_detectados


# ----------------------------------------------------------------------
# Execução da Pipeline Principal
# ----------------------------------------------------------------------
def executar_pipeline(managers):
    """Executa os managers sequencialmente."""
    log("Executando pipeline principal...")

    for manager in managers:
        nome = manager.__name__
        log(f"[MANAGER] Iniciando {nome}...")

        try:
            manager.run()
            log(f"[MANAGER] {nome} concluído.")
        except Exception as e:
            log(f"[ERRO] Falha no manager {nome}: {e}")
            traceback.print_exc()


# ----------------------------------------------------------------------
# Hook para Automator
# ----------------------------------------------------------------------
def chamar_automator():
    """Chama o automator, se existir."""
    automator_main = TOOLS / "automator" / "main.py"

    if not automator_main.exists():
        log("Automator não encontrado. Pulando etapa.")
        return

    log("Iniciando Automator...")
    try:
        exec(automator_main.read_text(), {})
        log("Automator concluído.")
    except Exception as e:
        log(f"[ERRO] Automator: {e}")


# ----------------------------------------------------------------------
# MindScan Runtime
# ----------------------------------------------------------------------
def main():
    log("MindScan Runtime iniciado.")
    validar_estrutura()

    managers = carregar_managers()
    executar_pipeline(managers)

    chamar_automator()

    log("MindScan finalizado com sucesso.")


# ----------------------------------------------------------------------
# Execução Direta
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"[FATAL] MindScan encerrado com falha: {e}")
        traceback.print_exc()
        sys.exit(1)
