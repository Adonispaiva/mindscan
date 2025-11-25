# ============================================================
# MindScan — Provider Manager
# ============================================================
# Gerencia e centraliza provedores externos e internos.
#
# Responsável por:
# - Carregar provedores registrados
# - Expor instâncias únicas (Singletons)
# - Facilitar substituições futuras (ex.: caching, emails, NLP)
# - Aumentar extensibilidade do ecossistema SynMind
#
# Versão: Final — SynMind 2025
# ============================================================

from typing import Any, Dict


class ProviderManager:
    """
    Centralizador de providers do sistema.
    """

    def __init__(self):
        self.providers: Dict[str, Any] = {}

    # ------------------------------------------------------------
    # Registrar um provider
    # ------------------------------------------------------------
    def register(self, name: str, instance: Any):
        if name in self.providers:
            raise ValueError(f"Provider '{name}' já está registrado.")
        self.providers[name] = instance

    # ------------------------------------------------------------
    # Obter provider
    # ------------------------------------------------------------
    def get(self, name: str) -> Any:
        provider = self.providers.get(name)
        if provider is None:
            raise ValueError(f"Provider '{name}' não encontrado.")
        return provider

    # ------------------------------------------------------------
    # Verificar provider
    # ------------------------------------------------------------
    def exists(self, name: str) -> bool:
        return name in self.providers

    # ------------------------------------------------------------
    # Listar providers
    # ------------------------------------------------------------
    def list(self):
        return list(self.providers.keys())


# Instância global
provider_manager = ProviderManager()
