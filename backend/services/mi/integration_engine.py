# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\mi\integration_engine.py
# Última atualização: 2025-12-11T09:59:21.162640

class IntegrationEngine:
    """
    Consolida narrativas múltiplas em um texto único e coerente.
    """

    def integrate(self, narratives: list[str]):
        # Filtra vazios
        narratives = [n for n in narratives if n and n.strip()]

        if not narratives:
            return ""

        # Junta com divisores suaves
        return "\n---\n".join(narratives)
