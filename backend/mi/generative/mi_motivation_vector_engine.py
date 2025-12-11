# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_motivation_vector_engine.py
# Última atualização: 2025-12-11T09:59:20.922434

class MIMotivationVectorEngine:
    """
    Identifica vetores motivacionais principais.
    """

    @staticmethod
    def compute(results: dict) -> dict:
        openness = results.get("big5", {}).get("abertura", 50)
        conscientiousness = results.get("big5", {}).get("consciencia", 50)

        return {
            "innovation_drive": round(openness * 1.1, 2),
            "execution_drive": round(conscientiousness * 1.2, 2),
            "balance": round((openness + conscientiousness) / 2, 2)
        }
