# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\algorithms\esquemas\esquemas_summary.py
# Última atualização: 2025-12-11T09:59:20.683445

"""
Esquemas Summary
Consolida:
- classificação dos esquemas
- fatores
- forças
- riscos
- necessidades
- top esquemas
"""

from typing import Dict, Any


class EsquemasSummary:
    """
    Gera bloco final usado por:
    - MindScanEngine
    - cruzamentos
    - narrativa psicodinâmica
    - relatórios
    """

    def __init__(self):
        self.version = "1.0"

    def build(
        self,
        classified: Dict[str, float],
        alerts: list,
        profile: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Monta o summary técnico.
        """

        # Top 3 esquemas em ordem decrescente
        top3 = sorted(
            classified.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]

        return {
            "module": "Esquemas",
            "version": self.version,
            "summary": {
                "top3": [x[0] for x in top3],
                "alerts": alerts,
                "factors": profile["factors"],
                "needs_map": profile["needs_map"],
                "predominant": profile["predominant_schemas"],
            },
            "details": {
                "classified": classified,
                "alerts_full": alerts,
                "profile_full": profile,
            }
        }
