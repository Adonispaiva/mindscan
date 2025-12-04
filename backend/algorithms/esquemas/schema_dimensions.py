"""
Schema Dimensions
Constrói dimensões intermediárias de agrupamento por item,
diferentes da organização final em esquemas.
"""

from typing import Dict


class SchemaDimensions:
    """
    Cada item individual do inventário é reorganizado em blocos dimensionais
    que servem de base para análise psicodinâmica mais granular.
    """

    def __init__(self):
        self.version = "1.0"

        # Exemplo de agrupamento genérico de itens → dimensões.
        # No projeto real, cada item teria seu agrupamento correspondente.
        self.dim_groups = {
            "autorregulacao_emocional": ["inibicao_emocional", "hipercriticismo"],
            "vinculacao": ["abandono", "isolamento"],
            "autonomia": ["dependencia", "vulnerabilidade"],
            "autoimagem": ["defectividade", "fracasso"],
        }

    def compute(self, normalized: Dict[str, float]) -> Dict[str, float]:
        """
        Calcula a média dos itens pertencentes a cada dimensão intermediária.
        """

        results = {}

        for dim, items in self.dim_groups.items():
            values = [normalized.get(i, 0) for i in items]
            if values:
                results[dim] = sum(values) / len(values)
            else:
                results[dim] = 0.0

        return results
