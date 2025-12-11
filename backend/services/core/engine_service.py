# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\core\engine_service.py
# Última atualização: 2025-12-11T09:59:21.136630

# D:\mindscan\backend\services\core\engine_service.py
# -----------------------------------------------------
# EngineService — Coordenação estrutural do MindScan
# Autor: Leo Vinci — Inovexa Software
#
# Este módulo:
# - coordena execução de serviços
# - valida consistência do runtime
# - controla fallback e rotas internas
# - oferece interface única de alto nível
# - supervisiona erros e integrações do pipeline

from typing import Any, Dict

from .base_service import BaseService
from .runtime_interface import RuntimeInterface
from .data_service import DataService
from .export_service import ExportService
from .psych_core_service import PsychCoreService


class EngineService(BaseService):
    """
    Motor corporativo central do MindScan.
    Responsável por orquestrar serviços, validar sequências
    e oferecer um ponto único de acesso para sistemas internos.
    """

    def __init__(self):
        super().__init__("EngineService")
        self.runtime = RuntimeInterface()
        self.data = DataService()
        self.export = ExportService()
        self.psych = PsychCoreService()

    # ----------------------------------------------------------------------
    # VALIDAÇÕES
    # ----------------------------------------------------------------------

    def _validate_test_id(self, test_id: str):
        if not isinstance(test_id, str) or len(test_id) < 3:
            raise ValueError(f"test_id inválido: {test_id}")

    # ----------------------------------------------------------------------
    # EXECUÇÃO DO PIPELINE COMPLETO
    # ----------------------------------------------------------------------

    def run(self, test_id: str) -> Dict[str, Any]:
        """
        Roda o pipeline inteiro do MindScan com validação superior.
        """
        self._log(f"Iniciando EngineService.run para test_id={test_id}")
        self._validate_test_id(test_id)

        runtime_output = self.runtime.run_full_pipeline(test_id)

        return {
            "engine": "MindScan-Core",
            "test_id": test_id,
            "result": runtime_output,
            "status": "ok",
        }

    # ----------------------------------------------------------------------
    # CAMINHO ESPECÍFICO DE EXPORTAÇÃO
    # ----------------------------------------------------------------------

    def export_all(self, test_id: str) -> Dict[str, Any]:
        """
        Exporta todos os pacotes possíveis:
        - relatório pronto (PDF)
        - pacote HTML
        - JSON bruto
        """
        self._log(f"Executando export_all para test_id={test_id}")
        self._validate_test_id(test_id)

        pdf_pkg = self.export.export_pdf_package(test_id)
        html_pkg = self.export.export_html_package(test_id)
        raw_json = self.export.export_json(test_id)

        return {
            "pdf": pdf_pkg,
            "html": html_pkg,
            "json": raw_json,
            "meta": {"origin": "EngineService"},
        }

    # ----------------------------------------------------------------------
    # MÉTODO PADRÃO DE EXECUÇÃO
    # ----------------------------------------------------------------------

    def execute(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execução genérica prevista pela BaseService.
        """
        self._log("Executando pacote genérico via EngineService.")
        self._validate_input(data)
        return self._package_metadata(data)
