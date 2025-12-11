# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\leadership_profile.py
# Última atualização: 2025-12-11T09:59:20.964461

"""
leadership_profile.py — MindScan ULTRA SUPERIOR
Perfil de liderança que combina indicadores de:

- Influência
- Comunicação
- Tomada de decisão
- Visão estratégica
- Condução de equipes
- Estabilidade emocional sob pressão
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class LeadershipProfile:
    attributes: Dict[str, float]
    leadership_index: float = 0.0

    def compute_index(self) -> float:
        """Calcula índice global de liderança a partir dos atributos."""
        if not self.attributes:
            return 0.0

        weights = {
            "comunicacao": 1.2,
            "visao": 1.4,
            "influencia": 1.3,
            "decisao": 1.5,
            "estabilidade": 1.6,
        }

        score = 0.0
        for key, value in self.attributes.items():
            multiplier = weights.get(key, 1.0)
            score += value * multiplier

        self.leadership_index = min(100.0, max(0.0, score / len(self.attributes)))
        return self.leadership_index
