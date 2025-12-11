# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_confidence_projection_engine.py
# Última atualização: 2025-12-11T09:59:20.903579

class MIConfidenceProjectionEngine:
    """
    Estima projeção de confiança interna e social.
    """

    @staticmethod
    def project(results: dict) -> dict:
        big5 = results.get("big5", {})

        return {
            "internal_confidence": round(big5.get("consciencia", 50) * 1.1, 2),
            "social_confidence": round(big5.get("extroversao", 50) * 1.15, 2)
        }
