# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_cognitive_map_generator.py
# Última atualização: 2025-12-11T09:59:20.887954

class MICognitiveMapGenerator:
    """
    Constrói um mapa cognitivo baseado em:
    - abertura
    - padrões de pensamento
    - flexibilidade cognitiva
    """

    @staticmethod
    def generate(results: dict) -> dict:
        openness = results.get("big5", {}).get("abertura", 50)

        return {
            "conceptual_expansion": round(openness * 1.1, 2),
            "flexibility": round(100 - abs(50 - openness), 2),
            "creative_bandwidth": round(openness * 0.9, 2)
        }
