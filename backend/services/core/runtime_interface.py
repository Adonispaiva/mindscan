# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\core\runtime_interface.py
# Última atualização: 2025-12-11T09:59:21.139688

# D:\mindscan\backend\services\core\runtime_interface.py
# --------------------------------------------------------
# Runtime Interface — MindScan Core
# Autor: Leo Vinci — Inovexa Software
#
# Este módulo funciona como a “ponte” operacional do MindScan:
# - faz coordenação entre serviços
# - padroniza chamadas internas
# - garante integridade de execução
# - fornece entrada unificada para ReportService e MI

from typing import Any, Dict

from .base_service import BaseService
from .data_service import DataService
from .export_service import ExportService
from .psych_core_service import PsychCoreService


class RuntimeInterface(BaseService):
    """
    Interface corporativa para orquestrar o fluxo MindScan:

    Pipeline geral:
        runtime.execute(test_id) →
            data_service → scoring → diagnostics →
            psych_core → export → pacote final
    """

    def __init__(self):
        super().__init__("RuntimeInterface")
        self.data_service = DataService()
        self.export_service = ExportService()
        self.psych_core = PsychCoreService()

    # ----------------------------------------------------------------------
    # PIPELINE PRINCIPAL
    # ----------------------------------------------------------------------

    def run_full_pipeline(self, test_id: str) -> Dict[str, Any]:
        """
        Executa todo o pipeline e retorna um pacote completo.
        Usado diretamente pelo ReportService.
        """
        self._log(f"Executando pipeline completo para test_id={test_id}")

        # 1. Dados brutos + normalização + scores + diagnostics
        data = self.data_service.get_report_ready_data(test_id)

        # 2. Perfil psicodinâmico
        psych = self.psych_core.build_psychodynamic_profile(test_id)

        # 3. Pacote para PDF e HTML
        export_pdf = self.export_service.export_pdf_package(test_id)
        export_html = self.export_service.export_html_package(test_id)

        # 4. Consolidação
        return {
            "test_id": test_id,
            "data": data,
            "psychodynamic": psych,
            "export_pdf": export_pdf,
            "export_html": export_html,
            "meta": {
                "runtime_interface": True,
                "diagnostics_ready": True,
            }
        }

    # ----------------------------------------------------------------------
    # MÉTODO PADRÃO DE EXECUÇÃO
    # ----------------------------------------------------------------------

    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execução genérica conforme BaseService.
        """
        self._log("Executando pacote runtime genérico.")
        self._validate_input(data)
        return self._package_metadata(data)
