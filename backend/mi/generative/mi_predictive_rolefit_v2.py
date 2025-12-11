# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_predictive_rolefit_v2.py
# Última atualização: 2025-12-11T09:59:20.928429

class MIPredictiveRoleFitV2:
    """
    Versão 2 do sistema preditivo de compatibilidade com cargos.
    Mais robusto e baseado em múltiplos vetores comportamentais.
    """

    @staticmethod
    def evaluate(results: dict) -> dict:
        big5 = results.get("big5", {})
        perf = results.get("performance_estimate", 50)

        leadership = big5.get("extroversao", 50) * 0.4 + big5.get("consciencia", 50) * 0.4 + perf * 0.2
        analytics = big5.get("consciencia", 50) * 0.5 + big5.get("amabilidade", 50) * 0.2 + perf * 0.3
        creative = big5.get("abertura", 50) * 0.7 + perf * 0.3

        return {
            "leader_fit": round(leadership, 2),
            "analytic_fit": round(analytics, 2),
            "creative_fit": round(creative, 2)
        }
