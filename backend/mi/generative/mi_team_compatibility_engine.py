# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_team_compatibility_engine.py
# Última atualização: 2025-12-11T09:59:20.938723

class MITeamCompatibilityEngine:
    """
    Define compatibilidade com diferentes tipos de equipes.
    """

    @staticmethod
    def evaluate(results: dict) -> dict:
        big5 = results.get("big5", {})

        return {
            "ideal_team_type": (
                "colaborativa" if big5.get("amabilidade", 50) > 60 else
                "visionária" if big5.get("abertura", 50) > 65 else
                "operacional"
            ),
            "collaboration_index": round((big5.get("amabilidade", 50) + big5.get("extroversao", 50)) / 2, 2)
        }
