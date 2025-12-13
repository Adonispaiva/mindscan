"""
Contratos formais dos engines.
"""

from typing import Protocol, Dict, Any


class EngineContract(Protocol):
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        ...
