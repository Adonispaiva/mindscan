# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\core\export_service.py
# Última atualização: 2025-12-11T09:59:21.137689

# D:\mindscan\backend\services\core\export_service.py
# -----------------------------------------------------
# Serviço de exportação de dados MindScan
# Autor: Leo Vinci — Inovexa Software
# Arquivo definitivo, integrado e alinhado ao ecossistema MindScan.

import json
from typing import Any, Dict

from .base_service import BaseService
from .data_service import DataService


class ExportService(BaseService):
    """
    Serviço responsável por exportar dados consolidados do MindScan
    em múltiplos formatos:

    - JSON bruto
    - JSON compactado
    - Estruturas preparadas para HTML
    - Pacotes para renderização PDF

    Este serviço é utilizado pelo ReportService, pelo pipeline de testes
    e por integrações externas.
    """

    def __init__(self):
        super().__init__("ExportService")
        self.data_service = DataService()

    # ----------------------------------------------------------------------
    # EXPORTAÇÃO EM JSON
    # ----------------------------------------------------------------------

    def export_json(self, test_id: str, compact: bool = False) -> str:
        """
        Exporta o pacote completo de dados para JSON.
        """
        self._log(f"Exportando JSON para test_id={test_id}")
        data = self.data_service.get_report_ready_data(test_id)

        if compact:
            return json.dumps(data, separators=(",", ":"))

        return json.dumps(data, indent=2, ensure_ascii=False)

    # ----------------------------------------------------------------------
    # EXPORTAÇÃO PARA HTML SANITIZADO
    # ----------------------------------------------------------------------

    def export_html_package(self, test_id: str) -> Dict[str, Any]:
        """
        Exporta um pacote preparado para renderização HTML,
        usado pela pipeline de pré-PDF.
        """
        self._log(f"Gerando pacote HTML para test_id={test_id}")

        data = self.data_service.get_report_ready_data(test_id)

        return {
            "html_context": {
                "scores": data["scores"],
                "diagnostics": data["diagnostics"],
                "meta": {
                    "test_id": data["test_id"],
                    "timestamp": data["timestamp"],
                },
            }
        }

    # ----------------------------------------------------------------------
    # EXPORTAÇÃO PARA PDFs
    # ----------------------------------------------------------------------

    def export_pdf_package(self, test_id: str) -> Dict[str, Any]:
        """
        Pacote final usado diretamente pelos renderizadores PDF:
        technical, executive, psychodynamic e premium.
        """
        self._log(f"Gerando pacote PDF para test_id={test_id}")

        data = self.data_service.get_report_ready_data(test_id)

        return {
            "test_id": data["test_id"],
            "payload": {
                "scores": data["scores"],
                "diagnostics": data["diagnostics"],
                "normalized": data["normalized"],
            },
            "metadata": {
                "timestamp": data["timestamp"],
                "runtime": data["kernel_runtime"],
            },
        }

    # ----------------------------------------------------------------------
    # MÉTODO PADRÃO DE EXECUÇÃO
    # ----------------------------------------------------------------------

    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execução genérica.
        """
        self._log("Iniciando execução genérica.")
        self._validate_input(data)
        formatted = self._package_metadata(data)
        return formatted
