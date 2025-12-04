"""
OCAI Dimensions
Converte escores normalizados nas quatro dimensões fundamentais da cultura:
- Clã
- Adhocracia
- Mercado
- Hierarquia
"""

from typing import Dict


class OCAIDimensions:
    """
    Cálculo das quatro dimensões do OCAI a partir dos itens normalizados.
    """

    def __init__(self):
        self.version = "1.0"

        # Estrutura base: cada item pertence a uma das 4 culturas
        # (estrutura genérica para o template).
        self.mapping = {
            "clã": ["clã_1", "clã_2", "clã_3"],
            "adhocracia": ["adh_1", "adh_2", "adh_3"],
            "mercado": ["merc_1", "merc_2", "merc_3"],
            "hierarquia": ["hier_1", "hier_2", "hier_3"],
        }

    def compute(self, normalized: Dict[str, float]) -> Dict[str, float]:
        dims = {}

        for culture, items in self.mapping.items():
            values = [normalized.get(i, 0) for i in items]
            if values:
                dims[culture] = sum(values) / len(values)
            else:
                dims[culture] = 0.0

        return dims
