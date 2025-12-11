# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\persona\persona_style.py
# Última atualização: 2025-12-11T09:59:20.948776

from __future__ import annotations
from typing import Dict, Any


class PersonaStyle:
    """
    Define o estilo textual base da persona.
    """

    def style(self) -> Dict[str, Any]:
        return {
            "sentence_length": "média",
            "tone": "profissional e acolhedor",
            "structure": "coerente, modular e explicativa",
            "avoid": [
                "julgamentos pessoais",
                "linguagem emocional excessiva",
                "afirmações determinísticas"
            ],
            "preferred_connectors": [
                "portanto",
                "além disso",
                "de maneira geral",
                "com base nos dados"
            ]
        }
