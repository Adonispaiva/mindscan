# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\api\compat\external_api_compat_layer.py
# Última atualização: 2025-12-11T09:59:20.745854

class ExternalAPICompatLayer:
    """
    Transforma resultados internos do MindScan
    em formato neutro para serviços externos.
    """

    @staticmethod
    def convert(results: dict) -> dict:
        payload = {
            "score_global": results.get("global_score"),
            "risks": results.get("risks"),
            "competencias": results.get("semantic", {}).get("competency_alignment"),
            "cross_sections": results.get("cross"),
            "performance": results.get("performance_estimate")
        }
        return payload
