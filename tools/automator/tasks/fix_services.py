"""
Task: fix_services
MindScan Automator — Inovexa Software
Autor: Leo Vinci (GPT Inovexa)
Data: 26/11/2025

Objetivo:
- Criar camada intermediária de SERVIÇOS do MindScan.
- Os serviços são responsáveis por:
    • Conectar módulos ao backend
    • Executar algoritmos
    • Preparar dados para o pipeline
    • Validações e saneamento de entrada
    • Orquestração de fluxo entre módulos

Estrutura criada:
mindscan/services/
    loader/
    dispatcher/
    validator/
    aggregator/
    report/
"""

from pathlib import Path
from datetime import datetime
import json
import os


# ---------------------------------------------------------------------
# TEMPLATES DE SERVIÇOS (robustos e padronizados)
# ---------------------------------------------------------------------

LOADER_TEMPLATE = """# loader.py — Carrega inputs do MindScan
class LoaderService:
    def load_payload(self, payload):
        # Futuro: conversão, normalização, validação inicial
        return payload
"""

VALIDATOR_TEMPLATE = """# validator.py — Validação de entrada
class ValidatorService:
    def validate(self, payload):
        # Futuro: regras específicas por módulo
        return True
"""

DISPATCHER_TEMPLATE = """# dispatcher.py — Encaminha para módulos corretos
class DispatcherService:
    def dispatch(self, modules, payload):
        results = {}
        for name, module in modules.items():
            module.load(payload)
            results[name] = module.compute()
        return results
"""

AGGREGATOR_TEMPLATE = """# aggregator.py — Agrega todos os resultados
class AggregatorService:
    def aggregate(self, data):
        # Futuro: cálculos combinados do MindScan
        return {"aggregated": data}
"""

REPORT_SERVICE_TEMPLATE = """# report_service.py — Consolida dados para relatório final
class ReportService:
    def prepare(self, aggregated):
        return {
            "final_report": aggregated,
            "status": "ready_for_pdf"
        }
"""


# ---------------------------------------------------------------------
# Estrutura de serviços a ser criada
# ---------------------------------------------------------------------

SERVICES_STRUCTURE = {
    "loader": {
        "__init__.py": "",
        "loader.py": "LOADER_TEMPLATE"
    },
    "dispatcher": {
        "__init__.py": "",
        "dispatcher.py": "DISPATCHER_TEMPLATE"
    },
    "validator": {
        "__init__.py": "",
        "validator.py": "VALIDATOR_TEMPLATE"
    },
    "aggregator": {
        "__init__.py": "",
        "aggregator.py": "AGGREGATOR_TEMPLATE"
    },
    "report": {
        "__init__.py": "",
        "report_service.py": "REPORT_SERVICE_TEMPLATE"
    }
}


# ---------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------

def ensure_dir(path: Path, log: list):
    if not path.exists():
        path.mkdir(parents=True)
        log.append(f"[CREATE] Diretório criado: {path}")


def ensure_file(path: Path, log: list, content: str):
    if not path.exists():
        with path.open("w", encoding="utf-8") as f:
            f.write(content)
        log.append(f"[CREATE] Arquivo criado: {path}")


# ---------------------------------------------------------------------
# Construção dos serviços
# ---------------------------------------------------------------------

def build_services(root: Path, log: list):
    services_root = root / "mindscan" / "services"
    ensure_dir(services_root, log)

    for service_name, files in SERVICES_STRUCTURE.items():
        folder = services_root / service_name
        ensure_dir(folder, log)

        for file_name, template_key in files.items():
            template = globals()[template_key] if template_key else ""
            ensure_file(folder / file_name, log, template)


# ---------------------------------------------------------------------
# Relatório
# ---------------------------------------------------------------------

def write_report(log: list, path: Path):
    report = {
        "task": "fix_services",
        "timestamp": datetime.now().isoformat(),
        "changes": log
    }
    with path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)


# ---------------------------------------------------------------------
# ENTRYPOINT
# ---------------------------------------------------------------------

def run(context):
    project_root = Path(context["project_root"])
    logs = Path(context["logs_path"])
    ensure_dir(logs, [])

    log = []
    log.append("[INIT] Executando fix_services")

    build_services(project_root, log)

    report_path = logs / "fix_services_report.json"
    write_report(log, report_path)

    return {
        "status": "success",
        "message": "Serviços centrais do MindScan criados com sucesso.",
        "report": str(report_path)
    }


if __name__ == "__main__":
    fake = {
        "project_root": str(Path(__file__).resolve().parents[2]),
        "logs_path": str(Path(__file__).resolve().parents[2] / "logs"),
        "settings": {}
    }
    print(run(fake))
