# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\diagnostic_matrix.py
# Última atualização: 2025-12-11T09:59:20.948776

"""
diagnostic_matrix.py — MindScan ULTRA SUPERIOR
Matriz de diagnóstico multidimensional que combina:

- Traços
- Riscos
- Indicadores emocionais
- Intensidade cognitiva
- Mapas de padrões comportamentais
"""

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class DiagnosticMatrix:
    traits: Dict[str, float]
    risks: Dict[str, float]
    emotional_signals: Dict[str, float]
    behavior_patterns: List[str]

    def compute_convergence(self) -> Dict[str, float]:
        """
        Gera métricas de convergência diagnóstica entre traços, riscos e sinais emocionais.
        """
        convergence = {}
        keys = set(self.traits) | set(self.risks) | set(self.emotional_signals)

        for k in keys:
            t = self.traits.get(k, 0)
            r = self.risks.get(k, 0)
            e = self.emotional_signals.get(k, 0)
            convergence[k] = (t + r + e) / 3

        return convergence
