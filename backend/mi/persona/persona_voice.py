# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\mi\persona\persona_voice.py
# Última atualização: 2025-12-11T09:59:20.948776

from __future__ import annotations
from typing import Dict, Any


class PersonaVoice:
    """
    Controla a 'voz' da persona — como ela se expressa textual e semanticamente.
    """

    def voice(self) -> Dict[str, Any]:
        return {
            "persona_name": "MindScan",
            "communication_focus": [
                "clareza",
                "interpretação técnica",
                "neutralidade",
                "aplicabilidade prática"
            ],
            "linguistic_attributes": {
                "verbosity": "moderada",
                "formalidade": "alta",
                "empatia": "equilibrada",
            },
            "signature": "MindScan — Análise Inteligente",
        }
