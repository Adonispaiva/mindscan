# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_opportunity_scanner.py
# Última atualização: 2025-12-11T09:59:20.926431

class MIOpportunityScanner:
    """
    Detecta oportunidades de crescimento e potencial subaproveitado.
    """

    @staticmethod
    def scan(results: dict) -> dict:
        opps = []

        if results.get("performance_estimate", 50) > 60:
            opps.append("Alavancar alto desempenho para assumir novos projetos estratégicos.")

        if results.get("big5", {}).get("abertura", 50) > 70:
            opps.append("Potencial criativo acima da média — explorar inovação estruturada.")

        return {
            "opportunities": opps,
            "count": len(opps)
        }
