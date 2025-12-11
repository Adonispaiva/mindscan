# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\emotional_profile.py
# Última atualização: 2025-12-11T09:59:20.964461

"""
emotional_profile.py — MindScan ULTRA SUPERIOR
Perfil emocional avançado que sintetiza:

- Estabilidade emocional
- Reatividade
- Intensidade afetiva
- Controle e regulação
- Sensibilidade social
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class EmotionalProfile:
    axes: Dict[str, float]
    stability_index: float = 0.0
    regulation_index: float = 0.0

    def compute_stability(self) -> float:
        """Calcula o índice global de estabilidade emocional."""
        if not self.axes:
            return 0.0

        values = list(self.axes.values())
        avg = sum(values) / len(values)
        self.stability_index = max(0.0, min(100.0, 100 - abs(avg - 50)))
        return self.stability_index

    def compute_regulation(self) -> float:
        """Determina a capacidade de autocontrole emocional."""
        if "controle" not in self.axes:
            return 0.0

        controle = self.axes["controle"]
        self.regulation_index = max(0.0, min(100.0, controle * 1.25))
        return self.regulation_index
