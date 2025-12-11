# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\tools\automator\core_manager.py
# Última atualização: 2025-12-11T09:59:27.808460

"""
core_manager.py
Reconstrutor Automático do CORE do MindScan
Versão Profissional Completa (A)

Responsabilidades:
    • Criar toda a arquitetura oficial do CORE
    • Validar se já existe estrutura
    • Realizar pré-análise dos arquivos do projeto
    • Indicar onde cada arquivo deveria ficar
    • Registrar relatório completo da reconstrução
    • NÃO mover arquivos ainda (isso é fase 2)
"""

import os
import json
import datetime

class CoreManager:

    # Estrutura oficial do CORE
    CORE_STRUCTURE = {
        "engine": [],
        "scoring": [],
        "diagnostics": [],
        "profiles": [],
        "metrics": [],
        "reporting": [],
        "algorithms": [],
        "utils": []
    }

    def __init__(self, logger):
        self.log = logger
        self.root_path = r"D:\projetos-inovexa\mindscan"
        self.core_path = os.path.join(self.root_path, "core")

        self.report = {
            "created_folders": [],
            "existing_folders": [],
            "files_detected": [],
            "mapping_suggestions": []
        }

    # ============================================================
    #        CRIA O CORE SE NÃO EXISTIR
    # ============================================================

    def _create_core_structure(self):
        """
        Cria toda a arquitetura CORE padrão.
        """

        if not os.path.exists(self.core_path):
            os.makedirs(self.core_path)
            self.report["created_folders"].append(self.core_path)
            self.log.info(f"CORE criado: {self.core_path}")
        else:
            self.report["existing_folders"].append(self.core_path)
            self.log.info("CORE já existe. Validando subpastas...")

        # Criar subpastas
        for sub in self.CORE_STRUCTURE.keys():
            sub_path = os.path.join(self.core_path, sub)

            if not os.path.exists(sub_path):
                os.makedirs(sub_path)
                self.report["created_folders"].append(sub_path)
                self.log.success(f"[CRIADO] {sub_path}")
            else:
                self.report["existing_folders"].append(sub_path)
                self.log.info(f"[OK] {sub_path} já existe")

    # ============================================================
    #       ANÁLISE INICIAL DO PROJETO
    # ============================================================

    def _scan_project(self):
        """
        Analisa pastas relevantes para futura reorganização:
        backend/, modules/, algorithms/, services/
        """

        SEARCH_DIRS = [
            "backend",
            "backend/services",
            "backend/algorithms",
            "modules",
            "modules/synmind_ai_engine",
            "algorithms",
        ]

        for folder in SEARCH_DIRS:
            full_path = os.path.join(self.root_path, folder)

            if not os.path.exists(full_path):
                continue

            for root, _, files in os.walk(full_path):
                for f in files:
                    if f.endswith(".py"):
                        file_path = os.path.join(root, f)
                        self.report["files_detected"].append(file_path)

    # ============================================================
    #      FASE 1 DO MAPEAMENTO (SEM MOVIMENTAÇÃO)
    # ============================================================

    def _suggest_file_mapping(self):
        """
        Gera sugestões de onde cada arquivo deveria ficar no novo CORE,
        com base em heurísticas internas.
        """

        for file_path in self.report["files_detected"]:
            file_lower = file_path.lower()

            # Determinação simples via heurísticas de nomes
            if "score" in file_lower or "metric" in file_lower:
                target = "scoring"
            elif "diagnos" in file_lower:
                target = "diagnostics"
            elif "profile" in file_lower:
                target = "profiles"
            elif "report" in file_lower:
                target = "reporting"
            elif "algo" in file_lower:
                target = "algorithms"
            elif "engine" in file_lower:
                target = "engine"
            else:
                target = "utils"

            suggestion = {
                "file": file_path,
                "suggested_target": target
            }

            self.report["mapping_suggestions"].append(suggestion)

    # ============================================================
    #      GERA RELATÓRIO DE ANÁLISE
    # ============================================================

    def _generate_report(self):
        """
        Salva relatório da reconstrução em JSON.
        """

        report_dir = os.path.join(self.root_path, "logs", "core_rebuilder")
        os.makedirs(report_dir, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_file = os.path.join(report_dir, f"rebuild_report_{timestamp}.json")

        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=4, ensure_ascii=False)

        self.log.success(f"Relatório gerado: {report_file}")

    # ============================================================
    #                 EXECUÇÃO PRINCIPAL
    # ============================================================

    def check_and_rebuild(self):
        self.log.header("CORE MANAGER – FASE 1")
        self.log.info("Reconstruindo estrutura oficial do CORE...")

        # 1. Criação da estrutura
        self._create_core_structure()

        # 2. Análise do projeto
        self.log.info("Analisando arquivos existentes...")
        self._scan_project()

        # 3. Sugestão de mapeamento
        self.log.info("Gerando sugestões de realocação...")
        self._suggest_file_mapping()

        # 4. Relatório final
        self._generate_report()

        self.log.success("FASE 1 DO CORE COMPLETA (sem mover nada).")
