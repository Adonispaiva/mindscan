"""
Big5 Traits Map — Versão Ultra Superior
---------------------------------------

Mapeia cada dimensão Big Five para TRAÇOS SUBJETIVOS,
que ajudam a construir descrições ricas para relatórios.

Conecta macro-dimensões a microtraços psicológicos.
"""

from typing import Dict, Any


class Big5TraitsMap:
    def __init__(self):
        self.version = "2.0-ultra"

        self.traits = {
            "abertura": [
                "imaginação ativa",
                "curiosidade intelectual",
                "flexibilidade cognitiva",
                "criatividade divergente",
            ],
            "conscienciosidade": [
                "responsabilidade",
                "disciplina pessoal",
                "organização",
                "atenção aos detalhes",
            ],
            "extroversao": [
                "assertividade social",
                "energia interpessoal",
                "expressividade",
                "espontaneidade",
            ],
            "amabilidade": [
                "cooperação",
                "empatia relacional",
                "gentileza",
                "tato social",
            ],
            "neuroticismo": [
                "sensibilidade afetiva",
                "reatividade emocional",
                "vulnerabilidade ao estresse",
                "autorregulação oscilante",
            ],
        }

    def map(self, dims: Dict[str, float]) -> Dict[str, Any]:
        mapped = {}

        for dim, value in dims.items():
            mapped[dim] = {
                "intensity": value,
                "traits": self.traits.get(dim, []),
            }

        return {
            "module": "Big5",
            "version": self.version,
            "traits_map": mapped,
        }
