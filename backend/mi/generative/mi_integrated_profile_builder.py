# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_integrated_profile_builder.py
# Última atualização: 2025-12-11T09:59:20.903579

class MIIntegratedProfileBuilder:
    """
    Cria um perfil integrado combinando:
    - padrões
    - previsões
    - riscos
    - insights
    - liderança
    """

    @staticmethod
    def build(results: dict, generative_outputs: dict) -> dict:
        return {
            "profile": {
                "summary": generative_outputs.get("meta_insights"),
                "forecast": generative_outputs.get("forecast"),
                "leadership": generative_outputs.get("leadership"),
                "social": generative_outputs.get("social"),
                "conflicts": generative_outputs.get("conflicts")
            }
        }
