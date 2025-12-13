"""
Engine Context — MindScan

Contexto compartilhado entre engines.
"""

from typing import Dict, Any


class EngineContext:
    def __init__(self, initial: Dict[str, Any] | None = None):
        self.data: Dict[str, Any] = initial or {}

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def set(self, key: str, value: Any):
        self.data[key] = value
