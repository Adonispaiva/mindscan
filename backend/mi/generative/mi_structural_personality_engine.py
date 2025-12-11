# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_structural_personality_engine.py
# Última atualização: 2025-12-11T09:59:20.937724

class MIStructuralPersonalityEngine:
    """
    Descreve a estrutura geral da personalidade:
    - eixo emocional
    - eixo social
    - eixo cognitivo
    - eixo adaptativo
    """

    @staticmethod
    def map(results: dict) -> dict:
        big5 = results.get("big5", {})
        tei = results.get("teique", {})

        return {
            "emotional_axis": round((tei.get("autocontrole", 50) + tei.get("estresse", 50)) / 2, 2),
            "social_axis": round((big5.get("extroversao", 50) + big5.get("amabilidade", 50)) / 2, 2),
            "cognitive_axis": big5.get("abertura", 50),
            "adaptive_axis": results.get("performance_estimate", 50)
        }
