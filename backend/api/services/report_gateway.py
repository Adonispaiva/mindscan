# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\services\report_gateway.py
# Última atualização: 2025-12-11T09:59:20.761538

from backend.services.report.report_service import ReportService

class ReportGateway:

    @staticmethod
    def generate(test_id: str, results: dict, report_type: str):
        return ReportService.generate_pdf(
            test_id=test_id,
            results=results,
            report_type=report_type
        )
