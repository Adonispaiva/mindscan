# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\persona\persona_metadata.py
# Última atualização: 2025-12-11T09:59:20.947726

from __future__ import annotations
from typing import Dict, Any


class PersonaMetadata:
    """
    Descreve metadados que definem como a persona opera internamente.
    """

    def describe(self) -> Dict[str, Any]:
        return {
            "language": "pt-BR",
            "domain": "psicometria aplicada",
            "compatibility": ["MI Engine", "Insight Layer", "Formatter"],
            "supports_crosslinks": True,
            "sensitivity": {
                "cultural": True,
                "contextual": True,
                "individual": True
            }
        }
