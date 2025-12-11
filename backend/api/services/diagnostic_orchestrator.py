# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\services\diagnostic_orchestrator.py
# Última atualização: 2025-12-11T09:59:20.761538

from backend.core.diagnostic_engine import DiagnosticEngine

class DiagnosticOrchestrator:

    @staticmethod
    def run(user_id: str, normalized_input: dict):
        engine = DiagnosticEngine(user_id=user_id)
        results, test_id = engine.run(normalized_input)
        return results, test_id
