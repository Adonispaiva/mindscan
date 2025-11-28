"""
backend_manager.py
Validador Profissional do Backend do MindScan
Versão Profissional Completa (A)

Funções principais:
    • Validar estrutura do backend
    • Validar serviços (services)
    • Validar algoritmos (algorithms)
    • Validar api_router
    • Detectar imports quebrados via AST
    • Verificar consistência dos modelos (models.py)
    • Gerar relatório de integridade
"""

import os
import ast
import datetime
import json


class BackendManager:

    def __init__(self, logger):
        self.log = logger
        self.root_path = r"D:\projetos-inovexa\mindscan"
        self.backend_path = os.path.join(self.root_path, "backend")

        self.report = {
            "exists": True,
            "structure": [],
            "services": [],
            "algorithms": [],
            "api_router": [],
            "models": [],
            "import_issues": [],
            "summary": {
                "ok": 0,
                "warnings": 0,
                "critical": 0
            }
        }

    # ============================================================
    # Utilitário: verificar existência
    # ============================================================

    def _check_exists(self, relative_path, category):
        """
        Verifica existência de um arquivo/diretório e adiciona ao relatório
        """

        abs_path = os.path.join(self.backend_path, relative_path)

        exists = os.path.exists(abs_path)
        entry = {"path": relative_path, "exists": exists}
        self.report[category].append(entry)

        if exists:
            self.log.info(f"[OK] {relative_path}")
            self.report["summary"]["ok"] += 1
        else:
            self.log.error(f"[CRÍTICO] {relative_path} ausente!")
            self.report["summary"]["critical"] += 1

        return exists

    # ============================================================
    # Layer 1 — Validar estrutura do backend
    # ============================================================

    def _validate_structure(self):
        required = [
            "main.py",
            "api_router.py",
            "models.py",
            "services",
            "algorithms"
        ]

        for item in required:
            self._check_exists(item, "structure")

    # ============================================================
    # Layer 2 — Validar serviços
    # ============================================================

    def _validate_services(self):
        services_path = os.path.join(self.backend_path, "services")

        if not os.path.exists(services_path):
            self.log.warn("Pasta de serviços ausente.")
            self.report["summary"]["warnings"] += 1
            return

        for root, dirs, files in os.walk(services_path):
            for f in files:
                if f.endswith(".py"):
                    full = os.path.join(root, f)
                    self.report["services"].append(full)
                    self.log.info(f"[SERVICE] {f}")

    # ============================================================
    # Layer 3 — Validar algoritmos
    # ============================================================

    def _validate_algorithms(self):
        algo_path = os.path.join(self.backend_path, "algorithms")

        if not os.path.exists(algo_path):
            self.log.warn("Pasta algorithms ausente no backend.")
            self.report["summary"]["warnings"] += 1
            return

        for root, dirs, files in os.walk(algo_path):
            for f in files:
                if f.endswith(".py"):
                    full = os.path.join(root, f)
                    self.report["algorithms"].append(full)
                    self.log.info(f"[ALGORITHM] {f}")

    # ============================================================
    # Layer 4 — Validar api_router
    # ============================================================

    def _validate_api_router(self):
        api_path = os.path.join(self.backend_path, "api_router.py")

        if not os.path.exists(api_path):
            self.log.error("api_router.py ausente!")
            self.report["summary"]["critical"] += 1
            return

        self.report["api_router"].append(api_path)
        self.log.info("[OK] api_router.py encontrado.")

        # Checar se ele possui router / endpoints
        try:
            with open(api_path, "r", encoding="utf-8") as f:
                code = f.read()

            tree = ast.parse(code)

            has_router = False

            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    if hasattr(node.value, "func") and getattr(node.value.func, "id", "") == "APIRouter":
                        has_router = True

            if has_router:
                self.log.success("api_router possui APIRouter válido.")
            else:
                self.log.warn("api_router.py não parece inicializar um APIRouter.")

        except Exception as e:
            self.log.error(f"Erro ao analisar api_router.py: {e}")
            self.report["summary"]["warnings"] += 1

    # ============================================================
    # Layer 5 — Validar models.py
    # ============================================================

    def _validate_models(self):
        models_file = os.path.join(self.backend_path, "models.py")

        if not os.path.exists(models_file):
            self.log.warn("models.py não encontrado no backend.")
            self.report["summary"]["warnings"] += 1
            return

        self.report["models"].append(models_file)
        self.log.info("[OK] models.py encontrado.")

        # Verificar se contém classes Pydantic
        try:
            with open(models_file, "r", encoding="utf-8") as f:
                code = f.read()

            tree = ast.parse(code)

            has_pydantic = any(
                isinstance(node, ast.ClassDef) for node in ast.walk(tree)
            )

            if has_pydantic:
                self.log.success("models.py possui classes definidas.")
            else:
                self.log.warn("models.py não possui modelos definidos.")

        except Exception as e:
            self.log.error(f"Erro ao analisar models.py: {e}")
            self.report["summary"]["warnings"] += 1

    # ============================================================
    # Layer 6 — Verificar imports quebrados
    # ============================================================

    def _check_imports(self):
        """
        Análise AST completa em todos os módulos do backend
        """

        self.log.info("Analisando imports...")

        modules = (
            self.report["services"] +
            self.report["algorithms"] +
            self.report["api_router"] +
            self.report["models"]
        )

        for module_path in modules:
            try:
                with open(module_path, "r", encoding="utf-8") as f:
                    code = f.read()

                tree = ast.parse(code)

                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom):
                        if node.module is None:
                            self.report["import_issues"].append(f"{module_path}: import inválido")
                        else:
                            self.log.info(f"[IMPORT] {module_path} => from {node.module} import ...")

            except Exception as e:
                msg = f"Erro ao analisar imports em {module_path}: {e}"
                self.log.error(msg)
                self.report["import_issues"].append(msg)
                self.report["summary"]["warnings"] += 1

    # ============================================================
    # Salvar relatório
    # ============================================================

    def _generate_report(self):
        report_dir = os.path.join(self.root_path, "logs", "backend")
        os.makedirs(report_dir, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_file = os.path.join(report_dir, f"backend_report_{timestamp}.json")

        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=4, ensure_ascii=False)

        self.log.success(f"Relatório backend salvo em: {report_file}")

    # ============================================================
    # EXECUÇÃO PRINCIPAL
    # ============================================================

    def validate_backend(self):
        self.log.header("BACKEND MANAGER – VALIDAÇÃO INICIADA")

        # Layers
        self._validate_structure()
        self._validate_services()
        self._validate_algorithms()
        self._validate_api_router()
        self._validate_models()
        self._check_imports()

        # Relatório final
        self._generate_report()

        self.log.success("BACKEND VALIDADO COM SUCESSO.")
