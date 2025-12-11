# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_dynamic_performance_engine.py
# Última atualização: 2025-12-11T09:59:20.903579

class MIDynamicPerformanceEngine:
    """
    Calcula performance dinâmica:
    - consistência
    - adaptabilidade
    - resiliência produtiva
    """

    @staticmethod
    def compute(results: dict) -> dict:
        perf = results.get("performance_estimate", 50)
        tei = results.get("teique", {})

        consistency = round(perf * 0.8, 2)
        adaptability = round((tei.get("autocontrole", 50) + perf) / 2, 2)
        resilience = round(100 - tei.get("estresse", 50) * 0.6, 2)

        return {
            "consistency": consistency,
            "adaptability": adaptability,
            "resilience": resilience
        }
