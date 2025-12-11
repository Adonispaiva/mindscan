# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\generative\mi_relationship_stability_engine.py
# Última atualização: 2025-12-11T09:59:20.930427

class MIRelationshipStabilityEngine:
    """
    Avalia estabilidade de relacionamentos profissionais.
    """

    @staticmethod
    def evaluate(results: dict) -> dict:
        ami = results.get("big5", {}).get("amabilidade", 50)
        ext = results.get("big5", {}).get("extroversao", 50)

        return {
            "stability_index": round((ami * 0.6 + ext * 0.4), 2)
        }
