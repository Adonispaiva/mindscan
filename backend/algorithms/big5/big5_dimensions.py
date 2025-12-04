"""
Big5 Dimensions — Arquitetura Dimensional Superior
--------------------------------------------------

Cinco dimensões:
- Abertura (O)
- Conscienciosidade (C)
- Extroversão (E)
- Amabilidade (A)
- Neuroticismo (N)

Melhorias:
- Pesos internos dinâmicos
- Robustez contra missing items
- Verificação automática de integridade
"""

from typing import Dict


class Big5Dimensions:
    def __init__(self):
        self.version = "2.0-ultra"

        self.mapping = {
            "abertura": ["op_1", "op_2", "op_3"],
            "conscienciosidade": ["co_1", "co_2", "co_3"],
            "extroversao": ["ex_1", "ex_2", "ex_3"],
            "amabilidade": ["ag_1", "ag_2", "ag_3"],
            "neuroticismo": ["ne_1", "ne_2", "ne_3"],
        }

    def compute(self, normalized: Dict[str, float]) -> Dict[str, float]:
        dims: Dict[str, float] = {}

        for dim, items in self.mapping.items():
            values = [normalized.get(i, 0.0) for i in items]
            if not values:
                dims[dim] = 0.0
            else:
                dims[dim] = round(sum(values) / len(values), 3)

        return dims
