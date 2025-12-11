# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\services\output_formatter.py
# Última atualização: 2025-12-11T09:59:20.761538

class OutputFormatter:

    @staticmethod
    def build(test_id: str, pdf_path: str, results: dict):
        return {
            "status": "success",
            "message": "Diagnóstico concluído",
            "test_id": test_id,
            "report_url": str(pdf_path),
            "results": results
        }
