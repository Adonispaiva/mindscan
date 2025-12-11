# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\tools\automator\report_manager.py
# Última atualização: 2025-12-11T09:59:27.824087

"""
report_manager.py
Gerador Profissional de Relatórios do MindScan Automator
Versão Profissional Completa (A)

Funções:
    • Consolidar dados de execução do Automator
    • Criar relatórios JSON, TXT e SUMÁRIO
    • Registro de erros, avisos, módulos executados e desempenho
    • Preparar infra para PDF (fase futura)
"""

import os
import json
import datetime


class ReportManager:

    def __init__(self, logger):
        self.log = logger
        self.root_path = r"D:\projetos-inovexa\mindscan"
        self.reports_dir = os.path.join(self.root_path, "logs", "reports")

        os.makedirs(self.reports_dir, exist_ok=True)

    # ============================================================
    # Gera relatório em JSON
    # ============================================================

    def _generate_json_report(self, content, timestamp):
        json_file = os.path.join(self.reports_dir, f"automator_report_{timestamp}.json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=4, ensure_ascii=False)

        self.log.success(f"Relatório JSON criado: {json_file}")
        return json_file

    # ============================================================
    # Gera relatório em TXT
    # ============================================================

    def _generate_text_report(self, content, timestamp):
        txt_file = os.path.join(self.reports_dir, f"automator_report_{timestamp}.txt")

        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("============================================\n")
            f.write("       RELATÓRIO DO MINDSCAN AUTOMATOR      \n")
            f.write("============================================\n\n")

            f.write(f"Data/Hora: {content['timestamp']}\n")
            f.write(f"Módulos Executados: {', '.join(content['executed_modules'])}\n")
            f.write(f"Erros: {len(content['errors'])}\n")
            f.write(f"Avisos: {len(content['warnings'])}\n\n")

            f.write("---- Detalhes ----\n")
            for msg in content["details"]:
                f.write(f"- {msg}\n")

            f.write("\n---- Erros ----\n")
            for e in content["errors"]:
                f.write(f"- {e}\n")

            f.write("\n---- Avisos ----\n")
            for w in content["warnings"]:
                f.write(f"- {w}\n")

        self.log.success(f"Relatório TXT criado: {txt_file}")
        return txt_file

    # ============================================================
    # Gera sumário (mini-relatório)
    # ============================================================

    def _generate_summary(self, content, timestamp):
        summary_file = os.path.join(self.reports_dir, f"automator_summary_{timestamp}.txt")

        with open(summary_file, "w", encoding="utf-8") as f:
            f.write("======= SUMÁRIO DO AUTOMATOR =======\n")
            f.write(f"Execução: {content['timestamp']}\n")
            f.write(f"Módulos: {len(content['executed_modules'])}\n")
            f.write(f"Erros: {len(content['errors'])}\n")
            f.write(f"Avisos: {len(content['warnings'])}\n")
            f.write("====================================\n")

        self.log.success(f"Sumário criado: {summary_file}")
        return summary_file

    # ============================================================
    # Execução principal
    # ============================================================

    def generate_report(self):
        self.log.header("REPORT MANAGER – INICIADO")

        # Em uma versão mais avançada, estes dados viriam dos módulos executados.
        # Nesta versão, criamos dados de exemplo.
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        report_content = {
            "timestamp": timestamp,
            "executed_modules": [
                "core_manager",
                "audit_manager",
                "backend_manager",
                "cleanup_manager",
                "release_manager",
                "data_validator",
            ],
            "details": [
                "Execução padrão do automator concluída.",
                "Logs armazenados em logs/automator/.",
                "Relatórios separados gerados por módulo.",
            ],
            "errors": [],
            "warnings": []
        }

        # Criar relatórios reais
        json_path = self._generate_json_report(report_content, timestamp)
        txt_path = self._generate_text_report(report_content, timestamp)
        summary_path = self._generate_summary(report_content, timestamp)

        self.log.success("Relatórios criados com sucesso.")
        return {
            "json": json_path,
            "txt": txt_path,
            "summary": summary_path
        }
