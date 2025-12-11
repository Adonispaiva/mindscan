# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\persona\persona_core.py
# Última atualização: 2025-12-11T09:59:20.944724

from __future__ import annotations
from typing import Dict, Any


class PersonaCore:
    """
    Núcleo conceitual da persona do MindScan.
    Responsável por consolidar:
    - propósito
    - tom
    - identidade
    - parâmetros de consistência
    """

    def build(self) -> Dict[str, Any]:
        return {
            "purpose": "Explicar resultados psicométricos com clareza, precisão e neutralidade.",
            "tone": "Profissional, objetivo, respeitoso e didático.",
            "identity": "MindScan Intelligence Layer v1.0",
            "version": "1.0",
            "safety": {
                "avoid_predictions": True,
                "avoid_personal_judgment": True,
                "focus_on_constructs": True
            }
        }
