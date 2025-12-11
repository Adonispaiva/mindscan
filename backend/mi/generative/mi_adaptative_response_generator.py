# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_adaptative_response_generator.py
# Última atualização: 2025-12-11T09:59:20.887954

class MIAdaptiveResponseGenerator:
    """
    Gera respostas adaptativas para diferentes contextos:
    - conflitos
    - tomada de decisão
    - alta pressão
    """

    @staticmethod
    def generate(results: dict) -> dict:
        responses = []

        if results.get("risks", {}):
            responses.append("Respire profundamente antes de reagir a estímulos de estresse.")
        
        if results.get("performance_estimate", 50) > 65:
            responses.append("Assuma iniciativas estratégicas quando houver ambiguidade.")

        return {"adaptive_responses": responses}
