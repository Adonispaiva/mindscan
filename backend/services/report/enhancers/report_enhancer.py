# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\report\enhancers\report_enhancer.py
# Última atualização: 2025-12-11T09:59:21.292589

class ReportEnhancer:
    """
    Melhora relatórios com seções adicionais como:
    - Insights complementares
    - Tópicos de desenvolvimento
    - Recomendações práticas
    """

    @staticmethod
    def enhance(report: dict, results: dict) -> dict:

        improvements = []

        if results.get("global_score", 50) < 50:
            improvements.append("Reforçar gestão emocional e planejamento estratégico.")
        if results.get("global_score", 50) > 75:
            improvements.append("Aproveitar alto desempenho para assumir desafios estruturais.")

        report["enhancements"] = {
            "suggestions": improvements
        }

        return report
