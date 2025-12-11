# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\mi_context_engine.py
# Última atualização: 2025-12-11T09:59:20.856706

class MIContextEngine:
    """
    Analisa contexto adicional do usuário ou da empresa
    para ajustar interpretações psicológicas e executivas.
    """

    @staticmethod
    def enrich(results: dict, context: dict) -> dict:
        enriched = {}

        if "cargo" in context:
            enriched["role_fit"] = {
                "cargo": context["cargo"],
                "ajuste": results.get("global_score", 50) >= 60
            }

        if "setor" in context:
            enriched["sector_impact"] = {
                "setor": context["setor"],
                "ajuste": "moderado"
            }

        return enriched
