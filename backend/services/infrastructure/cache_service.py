# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\infrastructure\cache_service.py
# Última atualização: 2025-12-11T09:59:21.158629

# -*- coding: utf-8 -*-
"""
cache_service.py
----------------

Serviço de cache interno do MindScan.
Permite armazenar resultados de pipelines pesados, evitando recomputação.
Implementação simples baseada em dicionário, mas compatível com Redis no futuro.
"""

from typing import Any, Dict


class CacheService:
    _cache: Dict[str, Any] = {}

    @classmethod
    def set(cls, key: str, value: Any) -> None:
        cls._cache[key] = value

    @classmethod
    def get(cls, key: str) -> Any:
        return cls._cache.get(key)

    @classmethod
    def exists(cls, key: str) -> bool:
        return key in cls._cache

    @classmethod
    def delete(cls, key: str) -> None:
        if key in cls._cache:
            del cls._cache[key]

    @classmethod
    def clear(cls) -> None:
        cls._cache.clear()
