"""
Big5 Needs Map — Versão Ultra Superior
--------------------------------------

Mapeia as necessidades psicológicas e emocionais associadas
a cada dimensão da personalidade.

É usado nos relatórios avançados e no motor de recomendações.
"""

from typing import Dict


class Big5NeedsMap:
    def __init__(self):
        self.version = "2.0-ultra"

        self.needs = {
            "abertura": "Necessidade de estímulos criativos, desafios intelectuais e liberdade cognitiva.",
            "conscienciosidade": "Necessidade de estrutura, metas claras, ordem e previsibilidade.",
            "extroversao": "Necessidade de interação social, expressividade e ambientes energéticos.",
            "amabilidade": "Necessidade de relações harmoniosas, cooperação e ambientes colaborativos.",
            "neuroticismo": "Necessidade de segurança emocional, suporte e mitigação de tensões.",
        }

    def map(self, dims: Dict[str, float]) -> Dict[str, str]:
        results = {}

        for dim, value in dims.items():
            # Todos recebem mapeamento, mas intensidade varia
            if value >= 70:
                results[dim] = f"Alta prioridade: {self.needs.get(dim)}"
            elif value >= 40:
                results[dim] = f"Prioridade moderada: {self.needs.get(dim)}"
            else:
                results[dim] = f"Prioridade discreta: {self.needs.get(dim)}"

        return results
