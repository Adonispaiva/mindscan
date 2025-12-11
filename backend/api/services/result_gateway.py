# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\services\result_gateway.py
# Última atualização: 2025-12-11T09:59:20.777102

from backend.core.diagnostic_engine import DiagnosticEngine

class ResultGateway:
    """
    Acessa, filtra e devolve resultados já existentes.
    Ideal para consultas via mindscan_web.
    """

    @staticmethod
    def load(test_id: str):
        return DiagnosticEngine.load_results(test_id)

    @staticmethod
    def summarize(results: dict) -> dict:
        return {
            "main_scores": results.get("global_scores"),
            "traits_summary": results.get("traits_summary"),
            "insights": results.get("insights"),
        }
