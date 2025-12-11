# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\services\mindscan_service.py
# Última atualização: 2025-12-11T09:59:20.761538

from backend.api.services.input_normalizer import InputNormalizer
from backend.api.services.diagnostic_orchestrator import DiagnosticOrchestrator
from backend.api.services.report_gateway import ReportGateway
from backend.api.services.output_formatter import OutputFormatter

class MindScanService:

    @staticmethod
    def run(user_id: str, form_data: dict, report_type: str):
        # 1. Normalização dos dados de entrada
        normalized = InputNormalizer.normalize(form_data)

        # 2. Execução do diagnóstico completo via Orchestrator
        results, test_id = DiagnosticOrchestrator.run(user_id, normalized)

        # 3. Geração do relatório conforme template
        pdf_path = ReportGateway.generate(test_id, results, report_type)

        # 4. Saída padronizada para API → frontend
        return OutputFormatter.build(
            test_id=test_id,
            pdf_path=pdf_path,
            results=results
        )
