"""
Big5 Factor Map — Versão Ultra Superior
---------------------------------------

Mapeia como cada dimensão do Big Five se desdobra em fatores
secundários e microcomponentes comportamentais.

Este módulo é usado para:
- Relatórios avançados
- Engines de matching
- Análises factor-level
- Expansão de traços para comportamentos observáveis
"""

from typing import Dict, Any


class Big5FactorMap:
    def __init__(self):
        self.version = "2.0-ultra"

        # Microfatores por dimensão — modelo ampliado da Inovexa
        self.factors = {
            "abertura": [
                "curiosidade intelectual",
                "imaginação",
                "criatividade aplicada",
                "flexibilidade cognitiva",
            ],
            "conscienciosidade": [
                "disciplina",
                "persistência",
                "planejamento",
                "orientação para metas",
            ],
            "extroversao": [
                "assertividade",
                "energia social",
                "expressividade",
                "busca por estímulo",
            ],
            "amabilidade": [
                "empatia",
                "cooperação",
                "tato social",
                "suavidade relacional",
            ],
            "neuroticismo": [
                "reatividade emocional",
                "vulnerabilidade ao estresse",
                "sensibilidade afetiva",
                "autorregulação",
            ],
        }

    def map(self, dims: Dict[str, float]) -> Dict[str, Any]:
        mapped = {}

        for dim, value in dims.items():
            if dim not in self.factors:
                continue

            mapped[dim] = {
                "intensity": value,
                "factors": self.factors[dim],
            }

        return {
            "module": "Big5",
            "version": self.version,
            "factor_map": mapped,
        }
