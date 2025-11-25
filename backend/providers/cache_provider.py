# ============================================================
# MindScan — Cache Provider
# ============================================================
# Responsável por caching interno para:
# - algoritmos psicométricos
# - MI Engine
# - relatórios
# - dados temporários de sessão
#
# Objetivos:
# - Acelerar processamento
# - Evitar recomputação
# - Manter isolamento seguro
#
# Versão: Final — SynMind 2025
# ============================================================

import time
from typing import Any, Dict, Optional


class CacheProvider:
    """
    Cache de alta performance para o MindScan.
    """

    def __init__(self, default_expiration: int = 300):
        # Expiração padrão: 5 minutos
        self.default_expiration = default_expiration

        # Estrutura:
        # cache[key] = { "value": X, "expires_at": timestamp }
        self.cache: Dict[str, Dict[str, Any]] = {}

    # ------------------------------------------------------------
    # Criar entrada no cache
    # ------------------------------------------------------------
    def set(self, key: str, value: Any, expire: Optional[int] = None):
        ttl = expire if expire is not None else self.default_expiration
        self.cache[key] = {
            "value": value,
            "expires_at": time.time() + ttl
        }

    # ------------------------------------------------------------
    # Recuperar valor do cache
    # ------------------------------------------------------------
    def get(self, key: str) -> Optional[Any]:
        item = self.cache.get(key)

        if not item:
            return None

        if time.time() > item["expires_at"]:
            del self.cache[key]
            return None

        return item["value"]

    # ------------------------------------------------------------
    # Remover entrada
    # ------------------------------------------------------------
    def delete(self, key: str):
        if key in self.cache:
            del self.cache[key]

    # ------------------------------------------------------------
    # Limpar cache inteiro
    # ------------------------------------------------------------
    def clear(self):
        self.cache = {}

    # ------------------------------------------------------------
    # Limpar itens expirados
    # ------------------------------------------------------------
    def cleanup(self):
        now = time.time()
        expired = [k for k, v in self.cache.items() if v["expires_at"] < now]
        for k in expired:
            del self.cache[k]
