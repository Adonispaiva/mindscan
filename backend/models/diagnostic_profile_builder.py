# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\diagnostic_profile_builder.py
# Última atualização: 2025-12-11T09:59:20.948776

"""
diagnostic_profile_builder.py — MindScan ULTRA SUPERIOR
Responsável por montar o perfil diagnóstico final combinando:

- Matriz diagnóstica
- Flags
- Insights
- Riscos
- Análises cruzadas
- Narrativas cognitivas
"""

from dataclasses import dataclass
from typing import Dict, Any

from backend.models.diagnostic_matrix import DiagnosticMatrix
from backend.models.diagnostic_flags import DiagnosticFlags


@dataclass
class DiagnosticProfileBuilder:
    matrix: DiagnosticMatrix
    flags: DiagnosticFlags
    insights: Dict[str, Any]
    cross_analysis: Dict[str, Any]

    def build(self) -> Dict[str, Any]:
        """Constrói o perfil diagnóstico completo."""
        convergence = self.matrix.compute_convergence()
        has_risk = self.flags.has_risk()

        profile = {
            "convergence": convergence,
            "risks_detected": has_risk,
            "flags": self.flags.flags,
            "insights": self.insights,
            "cross_analysis": self.cross_analysis,
        }

        return profile
