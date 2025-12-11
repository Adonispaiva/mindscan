# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\graphql_live\engine\gql_live_context_engine.py
# Última atualização: 2025-12-11T09:59:27.683474

class GQLLiveContextEngine:
    """
    Integra contexto dinâmico ao fluxo de GraphQL Live.
    """

    @staticmethod
    def enrich(event: dict, context: dict):
        enriched = event.copy()
        enriched.update({"context": context})
        return enriched
