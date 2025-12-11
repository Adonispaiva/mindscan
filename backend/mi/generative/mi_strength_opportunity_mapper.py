# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_strength_opportunity_mapper.py
# Última atualização: 2025-12-11T09:59:20.934724

class MIStrengthOpportunityMapper:
    """
    Mapeia como forças atuais se convertem em oportunidades estratégicas.
    """

    @staticmethod
    def map(results: dict) -> dict:
        big5 = results.get("big5", {})
        strengths = {k: v for k, v in big5.items() if v > 65}

        return {
            "strengths": strengths,
            "opportunities": [f"Explorar {s} em contextos de performance" for s in strengths]
        }
