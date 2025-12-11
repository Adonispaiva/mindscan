# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\culture_profile.py
# Última atualização: 2025-12-11T09:59:20.948776

"""
culture_profile.py — MindScan ULTRA SUPERIOR
Representa o perfil cultural organizacional de um indivíduo ou grupo,
utilizado em análises OCAI, Bússola Cultural e meta-avaliações.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class CultureProfile:
    """Modelo de perfil cultural com 6 eixos principais."""
    individual_values: Dict[str, float]
    team_values: Dict[str, float]
    organizational_alignment: float
    cultural_tensions: List[str] = field(default_factory=list)
    maturity_index: float = 0.0

    def compute_alignment(self) -> float:
        """Calcula o índice de alinhamento entre indivíduo, equipe e organização."""
        if not self.individual_values or not self.team_values:
            return 0.0

        keys = set(self.individual_values.keys()) & set(self.team_values.keys())
        if not keys:
            return 0.0

        diffs = []
        for k in keys:
            diffs.append(abs(self.individual_values[k] - self.team_values[k]))

        self.organizational_alignment = max(0.0, 100 - (sum(diffs) / len(diffs)))
        return self.organizational_alignment
