# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\coaching_v4\engine\coaching_contextual_engine.py
# Última atualização: 2025-12-11T09:59:27.542857

class CoachingContextualEngine:
    """
    Ajusta recomendações de coaching ao contexto organizacional.
    """

    @staticmethod
    def adapt(context: dict, base: dict):
        combined = base.copy()
        combined.update(context)
        return combined
