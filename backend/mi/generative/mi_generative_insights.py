# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_generative_insights.py
# Última atualização: 2025-12-11T09:59:20.903579

class MIGenerativeInsights:
    """
    Gera insights interpretativos complexos com base em padrões
    extraídos e enriquecidos dos resultados psicométricos.
    """

    @staticmethod
    def generate(results: dict) -> dict:
        insights = []

        if results.get("global_score", 50) > 75:
            insights.append("O perfil demonstra elevado potencial estratégico e adaptativo.")
        if results.get("risks", {}):
            insights.append("Há riscos comportamentais que podem impactar relações e performance.")
        if results.get("performance_estimate", 50) > 70:
            insights.append("A performance preditiva indica forte consistência operacional.")

        return {
            "insights": insights,
            "count": len(insights)
        }
