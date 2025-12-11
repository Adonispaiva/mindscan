# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\mi_document.py
# Última atualização: 2025-12-11T09:59:20.964461

"""
mi_document.py — MindScan ULTRA SUPERIOR
Documento oficial das Inteligências Múltiplas (MI).
Representa o payload consolidado para a interpretação dos eixos MI.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class MIDocument:
    mi_scores: Dict[str, float]
    dominant_axes: Dict[str, float]
    synthetic_index: float = 0.0

    def compute_synthetic_index(self) -> float:
        """Calcula índice sintético global das Inteligências Múltiplas."""
        if not self.mi_scores:
            return 0.0

        total = sum(self.mi_scores.values())
        avg = total / len(self.mi_scores)

        self.synthetic_index = min(100.0, max(0.0, avg))
        return self.synthetic_index
