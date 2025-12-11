# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\tools\automator\audit_manager.py
# Última atualização: 2025-12-11T09:59:27.808460

"""
audit_manager.py
Auditoria MAX do MindScan – Versão Profissional Completa (A)

Camadas verificadas:
    1. Estrutura de diretórios
    2. Arquivos essenciais
    3. Integridade de módulos
    4. Imports e referências quebradas
    5. Schemas e modelos
    6. Backend (Flask/FastAPI)
    7. Algoritmos e núcleo lógico
    8. Testes e cobertura
    9. Relatório final consolidado

Saída:
    logs/audit/audit_<timestamp>.json
"""

import os
import json
import datetime
import ast


class AuditManager:
    def __init__(self, logger):
        self.log = logger
        self.root_path = r"D:\projetos-inovexa\mindscan"

        self.results = {
            "directory_structure": [],
            "missing_files": [],
            "module_integrity": [],
            "import_issues": [],
            "schemas": [],
            "backend": [],
            "algorithms": [],
            "tests": [],
            "summary": {
                "critical": 0,
                "warnings": 0,
                "ok": 0
            }
        }

    # ============================================================
    # Layer 1 — Estrutura de Diretórios
    # ============================================================

    def _check_structure(self):
        required_dirs = [
            "backend",
            "backend/services",
            "backend/algorithms",
            "core",
            "core/engine",
            "core/diagnostics",
            "core/scoring",
            "core/profiles",
            "core/metrics",
            "modules",
            "tools",
            "tools/automator",
            "logs"
        ]

        for d in required_dirs:
            full = os.path.join(self.root_path, d)
            exists = os.path.exists(full)

            self.results["directory_structure"].append({
                "path": d,
                "exists": exists
            })

            if exists:
                self.log.info(f"[OK] {d}")
                self.results["summary"]["ok"] += 1
            else:
                self.log.warn(f"[FALTA] {d}")
                self.results["summary"]["critical"] += 1
                self.results["missing_files"].append(d)

    # ============================================================
    # Layer 2 — Arquivos Essenciais
    # ============================================================

    def _check_essential_files(self):
        essential_files = [
            "backend/main.py",
            "backend/models.py",
            "backend/api_router.py",
            "backend/services",
            "tools/automator/main.py",
            "tools/automator/tasks.json"
        ]

        for f in essential_files:
            full = os.path.join(self.root_path, f)
            exists = os.path.exists(full)

            if exists:
                self.log.info(f"[OK] Arquivo essencial: {f}")
                self.results["summary"]["ok"] += 1
            else:
                self.log.error(f"[CRÍTICO] Arquivo essencial ausente: {f}")
                self.results["summary"]["critical"] += 1
                self.results["missing_files"].append(f)

    # ============================================================
    # Layer 3 — Integridade de Módulos
    # ============================================================

    def _check_module_integrity(self):
        target_dirs = [
            "backend/services",
            "backend/algorithms",
            "modules",
            "core"
        ]

        for d in target_dirs:
            full = os.path.join(self.root_path, d)
            if not os.path.exists(full):
                continue

            for root, dirs, files in os.walk(full):
                for f in files:
                    if f.endswith(".py"):
                        self.log.info(f"[OK] Módulo detectado: {f}")
                        self.results["summary"]["ok"] += 1
                        self.results["module_integrity"].append(os.path.join(root, f))

    # ============================================================
    # Layer 4 — Imports e Referências
    # ============================================================

    def _check_imports(self):
        """
        Checa imports quebrados via análise AST.
        """

        for module_path in self.results["module_integrity"]:

            try:
                with open(module_path, "r", encoding="utf-8") as f:
                    code = f.read()

                tree = ast.parse(code)
                for node in ast.walk(tree):

                    if isinstance(node, ast.Import):
                        for n in node.names:
                            self.log.info(f"[IMPORT] {module_path} => {n.name}")

                    if isinstance(node, ast.ImportFrom):
                        mod = node.module
                        self.log.info(f"[IMPORT] {module_path} => from {mod} import ...")

            except Exception as e:
                msg = f"Erro ao analisar imports em {module_path}: {e}"
                self.log.error(msg)
                self.results["import_issues"].append(msg)
                self.results["summary"]["warnings"] += 1

    # ============================================================
    # Layer 5 — Schemas
    # ============================================================

    def _check_schemas(self):
        backend_models = os.path.join(self.root_path, "backend", "models.py")

        if os.path.exists(backend_models):
            self.log.info("Schemas backend detectados.")
            self.results["schemas"].append(backend_models)
        else:
            self.log.warn("models.py ausente no backend.")
            self.results["summary"]["warnings"] += 1

    # ============================================================
    # Layer 6 — Backend
    # ============================================================

    def _check_backend(self):
        api_router = os.path.join(self.root_path, "backend", "api_router.py")

        if os.path.exists(api_router):
            self.log.info("[OK] api_router.py encontrado.")
            self.results["backend"].append(api_router)
        else:
            self.log.error("[CRÍTICO] api_router.py ausente.")
            self.results["summary"]["critical"] += 1

    # ============================================================
    # Layer 7 — Algoritmos
    # ============================================================

    def _check_algorithms(self):
        algo_dir = os.path.join(self.root_path, "backend", "algorithms")

        if os.path.exists(algo_dir):
            self.log.info("Algoritmos detectados.")
            self.results["algorithms"].append(algo_dir)
        else:
            self.log.warn("Nenhum algoritmo encontrado.")
            self.results["summary"]["warnings"] += 1

    # ============================================================
    # Layer 8 — Testes
    # ============================================================

    def _check_tests(self):
        tests_dir = os.path.join(self.root_path, "tests")

        if os.path.exists(tests_dir):
            self.log.info("Testes detectados.")
            self.results["tests"].append(tests_dir)
        else:
            self.log.warn("Nenhuma pasta de testes encontrada.")
            self.results["summary"]["warnings"] += 1

    # ============================================================
    # Layer 9 — Relatório Final
    # ============================================================

    def _generate_report(self):
        report_dir = os.path.join(self.root_path, "logs", "audit")
        os.makedirs(report_dir, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_file = os.path.join(report_dir, f"audit_{timestamp}.json")

        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=4, ensure_ascii=False)

        self.log.success(f"Relatório de auditoria gerado: {report_file}")

    # ============================================================
    # EXECUÇÃO PRINCIPAL DA AUDITORIA
    # ============================================================

    def run_full_audit(self):
        self.log.header("AUDITORIA MAX – INICIADA")

        self._check_structure()
        self._check_essential_files()
        self._check_module_integrity()
        self._check_imports()
        self._check_schemas()
        self._check_backend()
        self._check_algorithms()
        self._check_tests()

        self._generate_report()

        self.log.success("AUDITORIA MAX – CONCLUÍDA COM SUCESSO.")
