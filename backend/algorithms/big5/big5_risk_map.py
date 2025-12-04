"""
Big5 Risk Map — Versão Ultra Superior
-------------------------------------

Gera um mapa de riscos baseado nas 5 dimensões da personalidade.
Inclui riscos comportamentais, interpessoais e decisórios.
"""

from typing import Dict


class Big5RiskMap:
    def __init__(self):
        self.version = "2.0-ultra"

        self.risks = {
            "abertura": "Risco de dispersão, excesso de abstração ou dificuldade com rotinas rígidas.",
            "conscienciosidade": "Risco de perfeccionismo ou inflexibilidade operacional.",
            "extroversao": "Risco de impulsividade social ou comunicação excessiva.",
            "amabilidade": "Risco de evitar conflitos importantes ou ceder demais.",
            "neuroticismo": "Risco de reatividade emocional, estresse elevado ou tomada de decisão ansiosa.",
        }

    def generate(self, dims: Dict[str, float]) -> Dict[str, str]:
        risk_map = {}

        for dim, value in dims.items():
            if value <= 35:
                risk_map[dim] = self.risks.get(dim, "")

        return risk_map
