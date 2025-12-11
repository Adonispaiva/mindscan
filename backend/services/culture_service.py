# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\services\culture_service.py
# Última atualização: 2025-12-11T09:59:21.089476

# -*- coding: utf-8 -*-
"""
culture_service.py
------------------

Interpreta o perfil cultural do indivíduo a partir dos
resultados coletados e mapeia a aderência com diferentes
modelos organizacionais.

Alimenta:
- Corporate Engines
- Renderers Executivos e Premium
- Seções de Cultura e Aderência
"""

from typing import Dict, Any

class CultureService:

    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload
        self.results = payload.get("results", {})
        self.traits = self.results.get("traits", {})
        self.context = payload.get("context", {})

    def compute_alignment(self) -> Dict[str, str]:
        openness = self.traits.get("openness", 50)
        agree = self.traits.get("agreeableness", 50)
        conscientious = self.traits.get("conscientiousness", 50)

        alignment = {}

        alignment["inovacao"] = (
            "Alta" if openness > 60 else
            "Moderada" if openness > 45 else
            "Baixa"
        )

        alignment["colaborativa"] = (
            "Alta" if agree > 60 else
            "Moderada" if agree > 45 else
            "Baixa"
        )

        alignment["alta_performance"] = (
            "Alta" if conscientious > 65 else
            "Moderada" if conscientious > 50 else
            "Baixa"
        )

        return alignment

    def build(self) -> Dict[str, Any]:
        return {
            "aderencia_cultural": self.compute_alignment(),
            "context": self.context,
        }
